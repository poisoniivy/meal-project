from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import *


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
        return render_template("mealplan.html", user=user)
    else:
        flash("You need to log in to access this page.")
        redirect("/")


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
