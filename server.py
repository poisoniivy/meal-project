from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import *

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
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_user():
    """Handles registering user route."""

    return render_template("register_form.html")


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
    del session["user_id"]

    return redirect("/")


@app.route('/user/<user_name>')
def user_info(user_name):
    """Users page when logged in."""

    user = User.query.filter(User.user_name==user_name).one()

    return render_template("user.html", user=user)


#Python says to place function before where I call it. Need to move it out later
def this_week_start_date():
    """Returns the start_date for the current user's week."""
    start_date = date.today() - datetime.timedelta(days=(date.today().weekday()+1))
    return start_date


@app.route('/mealplan')
def show_meal_plan(start_date=this_week_start_date()):
    """Shows user's mealplan."""

    # Checking if user is logged in
    if 'user_name' in session:
        user = User.query.filter(User.user_name==session['user_name']).one()
        all_recipes = user.recipes

        weeks = Week.query.filter(Week.user_id==user.user_id).all()
        week_list = [(w.start_date, w.week_id) for w in weeks]
        print "week_list: ", week_list

        if get_week_id(user.user_id, start_date) == False:
            print "Hardcoding week ID to be 2."
            week_id = 2
        else:
            week_id = get_week_id(user.user_id, start_date)

        all_days = meal_plan_days(start_date)

        meal_plan = create_meal_plan(week_id, all_days)
        return render_template("mealplan.html",
                                all_days=all_days,
                                meal_plan=meal_plan,
                                all_recipes=all_recipes,
                                week_list=week_list)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/meal-plan-week')
def show_meal_plan_week_id():
    """Given a week_id, show the meal plan for that week."""
    if 'user_name' in session:

        week_id = request.args.get("select-week-id")
        # import pdb; pdb.set_trace()
        print "week_id", week_id
        user = User.query.filter(User.user_name==session['user_name']).one()
        all_recipes = user.recipes

        weeks = Week.query.filter(Week.user_id==user.user_id).all()
        week_list = [(w.start_date, w.week_id) for w in weeks]

        start_date = Week.query.filter(Week.week_id==week_id).one().start_date

        all_days = meal_plan_days(start_date)

        meal_plan = create_meal_plan(week_id, all_days)

        return render_template("mealplan.html",
                                all_days=all_days,
                                meal_plan=meal_plan,
                                all_recipes=all_recipes,
                                week_list=week_list)
    else:
        flash("You need to log in to access this page.")
        return redirect("/")


@app.route('/edit-plan', methods=["POST"])
def edit_meal_plan(start_date=this_week_start_date()):
    """Edits Meal plan, modifies DB with new meals, returns user to mealpage."""
    if 'user_name' in session:

        user = User.query.filter(User.user_name==session['user_name']).one()

        if get_week_id(user.user_id, start_date) == False:
            print "Hardcoding week ID to be 2."
            week_id = 2
        else:
            week_id = get_week_id(user.user_id, start_date)

        all_days = meal_plan_days(start_date)

        i = 1
        while i <= 7:
            day = request.json["day"+str(i)]
            meal_date = all_days[i-1]

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
        all_recipes = user.recipes

        flash("Your meal has been saved.")

        return redirect("/mealplan")

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
        print "start_date_string: ", start_date_string
        start_date = datetime.datetime.strptime(start_date_string, "%m/%d/%Y").date()
        print "date object: ", start_date

        # If the week already exists
        if Week.query.filter(Week.user_id==user.user_id,
                             Week.start_date==start_date).all() != []:
            flash("Week already exists.")
            show_meal_plan(start_date)
        # Week does not exist, need to create it
        else:
            create_new_week(start_date)
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
    rec = Recipe.query.filter(Recipe.recipe_id==recipe_id).one()
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

    print rec_dict
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
    # recipes = {"recipes": recipe_list}

    print recipes
    return jsonify(recipes)


@app.route('/shoppinglist')
def show_shopping_list():
    """shows users shopping list."""
    pass


def meal_plan_days(start_date):
    """Returns a list of 7 days for mealplan for a given datetime start_date."""
    all_days = [start_date,
                    start_date + datetime.timedelta(days=1),
                    start_date + datetime.timedelta(days=2),
                    start_date + datetime.timedelta(days=3),
                    start_date + datetime.timedelta(days=4),
                    start_date + datetime.timedelta(days=5),
                    start_date + datetime.timedelta(days=6)]
    return all_days


def get_week_id(user_id, start_date):
    """Returns the week_id given a user_id and a start_date."""
    if Week.query.filter(Week.user_id==user_id,
                            Week.start_date==start_date).all() == []:
        return False
    else:
        return Week.query.filter(Week.user_id==user_id,
                            Week.start_date==start_date).one().week_id


def create_new_week(start_date):
    """Creates a new week and also all the meals that are associated with week."""

    # user = User.query.filter(User.user_name==session['user_name']).one()
    user = User.query.filter(User.user_id == 1).one()

    week = Week(user_id=user.user_id, start_date=start_date)
    all_days = meal_plan_days(start_date)

    db.session.add(week)
    db.session.commit()
    week_id = week.week_id

    m01 = Meal(week_id=week_id, meal_type_id="br", meal_date=start_date)
    m02 = Meal(week_id=week_id, meal_type_id="lu", meal_date=start_date)
    m03 = Meal(week_id=week_id, meal_type_id="din", meal_date=start_date)
    m04 = Meal(week_id=week_id, meal_type_id="snck", meal_date=start_date)

    m05 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[1])
    m06 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[1])
    m07 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[1])
    m08 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[1])

    m09 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[2])
    m10 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[2])
    m11 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[2])
    m12 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[2])

    m13 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[3])
    m14 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[3])
    m15 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[3])
    m16 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[3])

    m17 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[4])
    m18 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[4])
    m19 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[4])
    m20 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[4])

    m21 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[5])
    m22 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[5])
    m23 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[5])
    m24 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[5])

    m25 = Meal(week_id=week_id, meal_type_id="br", meal_date=all_days[6])
    m26 = Meal(week_id=week_id, meal_type_id="lu", meal_date=all_days[6])
    m27 = Meal(week_id=week_id, meal_type_id="din", meal_date=all_days[6])
    m28 = Meal(week_id=week_id, meal_type_id="snck", meal_date=all_days[6])

    # db.session.add_all([meal1, meal2, meal3, meal4])
    db.session.add_all([m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11,
        m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25,
        m26, m27, m28])
    db.session.commit()


def create_meal_plan(week_id, all_days):
    meal_plan_list = []

    # Creating a meal-plan-dictionary based on meals -> easier to display

    breakfast = create_meal_dict(week_id, "br")
    lunch = create_meal_dict(week_id, "lu")
    dinner = create_meal_dict(week_id, "din")
    snacks = create_meal_dict(week_id, "snck")

    meal_plan_list.append(breakfast)
    meal_plan_list.append(lunch)
    meal_plan_list.append(dinner)
    meal_plan_list.append(snacks)

    return meal_plan_list

# Things to check/To do Later: make sure week_id exists
def create_meal_dict(week_id, meal_type_id):
    """Returns a dictionary of meals and recipes for mealplan page."""
    meals_list = Meal.query.filter(Meal.week_id==week_id,
            Meal.meal_type_id==meal_type_id).order_by(Meal.meal_date).all()
    meals_dict = {}
    meals_dict["meal_type"] = MealType.query.filter(
                        MealType.meal_type_id==meal_type_id).one().type_name

    i = 1
    for meal in meals_list:
        recipe_list = meal.recipes
        while len(recipe_list) < 4:
            recipe_list = recipe_list + ['']
        meals_dict["day" + str(i)] = recipe_list
        i += 1

    return meals_dict


def edit_meals(meal_type_id, recipe_list, week_id, meal_date):
    """ Adds meal_recipes to database for meal plan."""
    meal_id = Meal.query.filter(Meal.week_id==week_id,
                                Meal.meal_type_id==meal_type_id,
                                Meal.meal_date==meal_date).one().meal_id
    for r_id in recipe_list:
        # Need to check with the meal_recipe_id does not already exist:
        if MealRecipe.query.filter(MealRecipe.meal_id==meal_id,
                                    MealRecipe.recipe_id==r_id).all() == []:
            print "Adding a meal recipe", meal_id, r_id
            new_meal_recipe = MealRecipe(recipe_id=r_id, meal_id=meal_id)
            db.session.add(new_meal_recipe)

    db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
