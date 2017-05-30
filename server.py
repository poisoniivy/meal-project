from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import *

from mealplan import *

from recipes import *

from datetime import date

import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Mealplan App Homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_user():
    """Handles registering user route."""

    return render_template("register-form.html")


@app.route('/register', methods=["POST"])
def register_complete():
    """Completes the registration sign-up."""
    email = request.form.get("email")
    password = request.form.get("password")
    user_name = request.form.get("username")

    # import pdb; pdb.set_trace()

    # If user email does not currently exist in database:
    if not User.query.filter(User.email==email).all():
        # If user name does not currently exist in database:
        if not User.query.filter(User.user_name==user_name).all():
            # Create new user if email and username both do not exist
            new_user = User(email=email, password=password, user_name=user_name)

            db.session.add(new_user)
            db.session.commit()
            flash("Your account has been created. Please sign in.")
            return redirect("/")
        else:
            flash("Username already exists.")
            return redirect("/register")
    else:
        flash("User email already exists.")
        return redirect("/register")


@app.route('/login', methods=["POST"])
def login():
    """Handles Login route, checks username/password, directs to user page."""

    email = request.form.get("email")
    password = request.form.get("password")

    print email, password

    # If the user email is not in the database
    if not User.query.filter(User.email==email).all():
        flash("User does not exist")
        return redirect("/")
    else:
        user = User.query.filter(User.email==email).one()
        if password==user.password:
            session['user_name'] = user.user_name
            flash("You are logged in")
            return redirect("/user/" + user.user_name)
        else:
            flash("Password is incorrect, please try again")
            return redirect("/login")


@app.route('/logout')
def logout():
    """Logs out user."""
    flash("You are logged out.")
    del session["user_name"]

    return redirect("/")


@app.route('/user/<user_name>')
def user_info(user_name):
    """Users main page when logged in."""

    user = User.query.filter(User.user_name==user_name).one()

    return render_template("user.html", user=user)


@app.route('/mealplan')
def show_meal_plan(start_date=this_week_start_date()):
    """Shows user's mealplan page."""

    # Checking if user is logged in
    if 'user_name' in session:
        user = User.query.filter(User.user_name==session['user_name']).one()
        all_recipes = user.recipes

        # Grabbing all the week objects that belong to a user
        weeks = user.weeks
        week_list = [(w.start_date, w.week_id) for w in weeks]

        # If the user does not have that week created, then mealplan
        # page shows the last created mealplan
        if get_week_id(user.user_id, start_date) == False:
            flash("You do not have a meal plan for this week.")
            # sets week ID to the most recent week that was created
            week_id = Week.query.filter(Week.user_id==user.user_id).order_by(
                Week.start_date.desc()).all()[0].week_id
        else:
            # week-id is the current week's start_date
            week_id = get_week_id(user.user_id, start_date)

        # Grabbing the list of all the days that belong to the week_id
        w = Week.query.get(week_id)
        all_days = w.plan_days()

        meal_plan = create_meal_plan(week_id, all_days)
        return render_template("mealplan.html",
                                all_days=all_days,
                                meal_plan=meal_plan,
                                all_recipes=all_recipes,
                                week_list=week_list,
                                week_id=week_id)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/meal-plan-week')
def show_meal_plan_week_id():
    """Given a week_id, show the meal plan for that week."""
    if 'user_name' in session:

        week_id = request.args.get("select-week-id")
        week = Week.query.get(week_id)

        return show_meal_plan(week.start_date)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/edit-plan', methods=["POST"])
def edit_meal_plan():
    """Edits Meal plan, modifies DB with new meals, returns user to mealpage."""
    if 'user_name' in session:

        user = User.query.filter(User.user_name==session['user_name']).one()
        week_id = request.json["week_id"]

        week = Week.query.get(week_id)
        start_date = week.start_date
        all_days = week.plan_days()

        i = 1
        while i <= 7:
            day = request.json["day"+str(i)]
            meal_date = all_days[i-1]
            print "meal_date", meal_date

            # import pdb; pdb.set_trace()
            if day["breakfast"] != []:
                edit_meals("br", day["breakfast"], week_id, meal_date)
            if day["lunch"] != []:
                edit_meals("lu", day["lunch"], week_id, meal_date)
            if day["dinner"] != []:
                edit_meals("din", day["dinner"], week_id, meal_date)
            if day["snacks"] != []:
                edit_meals("snck", day["snacks"], week_id, meal_date)
            i += 1

        meal_plan = create_meal_plan(week_id, all_days)

        flash("Your meal has been saved.")
        return jsonify("/mealplan")

    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/create-new-meal-plan')
def create_new_meal_plan_pick_week():
    """Goes to calendar to pick a week."""
    return render_template("/pick-calendar-week.html")


@app.route('/create-new-meal-plan', methods=["POST"])
def create_new_meal_plan():
    """Checks if week already exists, if not, creates it."""
    if 'user_name' in session:
        user_name = session['user_name']
        user = User.query.filter(User.user_name==user_name).one()

        date_string = request.form.get("picked-week")
        start_date_string = date_string[:10]
        # print "start_date_string: ", start_date_string
        start_date = datetime.datetime.strptime(start_date_string, "%m/%d/%Y").date()
        # print "date object: ", start_date

        # If the week already exists
        if Week.query.filter(Week.user_id==user.user_id,
                             Week.start_date==start_date).all() != []:
            flash("Week already exists.")
            return show_meal_plan(start_date)
        # Week does not exist, need to create it
        else:
            create_new_week(start_date)
            flash("Please fill in your meals.")
            return show_meal_plan(start_date)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/recipes')
def show_recipes():
    """Shows list of all user's recipes."""
    # Checking if user is logged in
    if 'user_name' in session:
        user_name = session['user_name']
        user = User.query.filter(User.user_name==user_name).one()
        recipes = user.recipes
        return render_template("recipes.html", user=user, recipes=recipes)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/recipe-info.json')
def show_recipe_info():
    recipe_id = request.args.get("recipe_id")
    rec = Recipe.query.get(recipe_id)
    rec_dict = {}
    rec_dict["recipe_name"] = rec.recipe_name
    if "directions" in rec_dict:
        rec_dict["directions"] = rec.directions
    if "has_dairy" in rec_dict:
        rec_dict["has_dairy"] = rec.has_dairy
    if "has_gluten" in rec_dict:
        rec_dict["has_gluten"] = rec.has_gluten
    if "vegetarian" in rec_dict:
        rec_dict["vegetarian"] = rec.vegetarian

    return jsonify(rec_dict)


@app.route('/show-filter-recipes.json', methods=["GET"])
def filter_recipes():
    """Returns a list of recipes from filter."""
    meal_type = request.args.get("meal_type")
    print "meal_type: ", meal_type
    meal_list = Meal.query.filter(Meal.meal_type_id==meal_type).all()

    recipe_list = []
    for m in meal_list:
        print m.recipes
        if m.recipes != None:
            recipe_list = recipe_list + m.recipes

    recipe_list = list(set(recipe_list))
    recipes = [{'id':rec.recipe_id, 'name':rec.recipe_name} for rec in recipe_list]

    print recipes
    return jsonify(recipes)


@app.route('/edit-recipe', methods=["GET"])
def show_edit_recipe_page():
    """Directs user to edit recipe page with pre-filled info to edit."""
    recipe_id = request.args.get("recipe-id")
    r = Recipe.query.get(recipe_id)

    return render_template("edit-recipe.html", recipe=r)


@app.route('/edit-recipe', methods=["POST"])
def edit_recipe():
    """Takes changes from user and edits recipe info."""
    return redirect("/recipes")


@app.route('/add-recipe')
def show_add_recipe_page():
    units = Unit.query.all()
    ingredients = Ingredient.query.all()
    return render_template("add-recipe.html",
                            units=units,
                            ingredients=ingredients)


@app.route('/add-recipe', methods=["POST"])
def add_recipe():

    if 'user_name' in session:
        user_name = session['user_name']
        user = User.query.filter(User.user_name==user_name).one()

        # import pdb; pdb.set_trace()

        recipe_name = request.json["name"]
        directions = request.json["directions"]
        ingredient_dict = request.json["ingredients"]

        # import pdb; pdb.set_trace()
        print recipe_name, directions, ingredient_dict

        # Adding recipe to database
        # Future: add in booleans
        recipe_id = add_new_recipe(recipe_name=recipe_name,
                                directions=directions)

        # connect the user to recipe
        add_recipe_to_user(recipe_id, user.user_id)

        # Adding the ingredients to the database
        for item in ingredient_dict.keys():
            ing_name, amount, unit = ingredient_dict[item]

            ing_query = Ingredient.query.filter(
                Ingredient.ingredient_name==str(ing_name))
            # if ingredient already exists in db:
            if ing_query.all():
                ing = ing_query.one()
                add_ingredient_to_recipe(ing.ingredient_id, recipe_id,
                    str(unit), float(amount))
            # ingredient does not exist in db
            else:
                ing_id = add_ingredient(str(ing_name))
                add_ingredient_to_recipe(ing_id, recipe_id,
                    str(unit), float(amount))
        print "finished adding ingredients"
        return jsonify("/recipes")

    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/shoppinglist')
def show_shopping_list():
    """shows users shopping list."""
    week_id = request.args.get("week_id")

    week = Week.query.get(week_id)
    recipe_list = get_all_recipes_from_week(week_id)

    shopping_list = get_shopping_list(recipe_list)

    return render_template("shoppinglist.html", shopping_list=shopping_list,
                                                week_start_date=week.start_date)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
