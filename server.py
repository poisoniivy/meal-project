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


@app.route('/mealplan')
def show_meal_plan():
    """Shows user's mealplan."""

    # Checking if user is logged in
    if 'user_name' in session:
        user = User.query.filter(User.user_name==session['user_name']).one()
        all_recipes = user.recipes

        today = date.today()
        display_week = Meal.query.filter(Meal.meal_date==today).all()[0].week_id

        # Currently the week starts on a Sunday
        start_date = date.today() - datetime.timedelta(days=(date.today().weekday()+1))
        # Listing out days of the week to display in one week's mealplan
        all_days = [start_date,
                    start_date + datetime.timedelta(days=1),
                    start_date + datetime.timedelta(days=2),
                    start_date + datetime.timedelta(days=3),
                    start_date + datetime.timedelta(days=4),
                    start_date + datetime.timedelta(days=5),
                    start_date + datetime.timedelta(days=6)]

        meal_plan = create_meal_plan(display_week, all_days)
        return render_template("mealplan.html",
                                all_days=all_days,
                                meal_plan=meal_plan,
                                all_recipes=all_recipes)
    else:
        flash("You need to log in to access this page.")
        redirect("/")



def create_meal_plan(week_id, all_days):
    meal_plan_list = []

    # Creating a meal-plan-list based on days
    # i = 1
    # for day in all_days:
    #     meal_dict = {}
    #     meal_dict["day"] = i

    #     br_list = Meal.query.filter(Meal.week_id==week_id,
    #                     Meal.meal_date==day,
    #                     Meal.meal_type_id=="br").one().recipes
    #     meal_dict["breakfast"] = br_list

    #     lu_list = Meal.query.filter(Meal.week_id==week_id,
    #                     Meal.meal_date==day,
    #                     Meal.meal_type_id=="lu").one().recipes
    #     meal_dict["lunch"] = lu_list

    #     din_list = Meal.query.filter(Meal.week_id==week_id,
    #                     Meal.meal_date==day,
    #                     Meal.meal_type_id=="din").one().recipes
    #     meal_dict["dinner"] = din_list

    #     snack_list = Meal.query.filter(Meal.week_id==week_id,
    #                     Meal.meal_date==day,
    #                     Meal.meal_type_id=="snck").one().recipes
    #     meal_dict["snack"] = snack_list

    #     i += 1
    #     meal_plan_list.append(meal_dict)

    # Creating a meal-plan-dictionary based on meals -> easier to display
    breakfast_meals = Meal.query.filter(Meal.week_id==2,
            Meal.meal_type_id=="br").order_by(Meal.meal_date).all()
    br_dict = {}
    br_dict["meal_type"] = "breakfast"
    i = 1
    for meal in breakfast_meals:
        meal_list = meal.recipes
        while len(meal_list) < 4:
            meal_list = meal_list + ['']
        br_dict["day" + str(i)] = meal_list
        i += 1
    meal_plan_list.append(br_dict)

    lunch_meals = Meal.query.filter(Meal.week_id==2,
            Meal.meal_type_id=="lu").order_by(Meal.meal_date).all()
    lu_dict = {}
    lu_dict["meal_type"] = "lunch"
    i = 1
    for meal in lunch_meals:
        meal_list = meal.recipes
        while len(meal_list) < 4:
            meal_list = meal_list + ['']
        lu_dict["day" + str(i)] = meal_list
        i += 1
    meal_plan_list.append(lu_dict)

    dinner_meals = Meal.query.filter(Meal.week_id==2,
            Meal.meal_type_id=="din").order_by(Meal.meal_date).all()
    din_dict = {}
    din_dict["meal_type"] = "dinner"
    i = 1
    for meal in dinner_meals:
        meal_list = meal.recipes
        while len(meal_list) < 4:
            meal_list = meal_list + ['']
        din_dict["day" + str(i)] = meal_list
        i += 1
    meal_plan_list.append(din_dict)

    snack_meals = Meal.query.filter(Meal.week_id==2,
            Meal.meal_type_id=="snck").order_by(Meal.meal_date).all()
    snack_dict = {}
    snack_dict["meal_type"] = "snack"
    i = 1
    for meal in snack_meals:
        meal_list = meal.recipes
        while len(meal_list) < 4:
            meal_list = meal_list + ['']
        snack_dict["day" + str(i)] = meal_list
        i += 1
    meal_plan_list.append(snack_dict)

    return meal_plan_list


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
        redirect("/")


@app.route('/recipes/<recipe_id>')
def show_recipe_info():
    pass


@app.route('/shoppinglist')
def show_shopping_list():
    """shows users shopping list."""
    pass


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
