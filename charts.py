""" Functions to help query db for analysis page."""

from model import *
from datetime import date
import datetime


def meal_week_data(user_id):
    """Returns tuples of number of recipes based on past week."""

    # User's list of week ids to look in
    weeks = User.query.get(user_id).weeks
    w_id_list = [w.week_id for w in weeks]

    today = date.today()
    # date that was a week ago
    today_week = today + datetime.timedelta(days=-7)

    q = db.session.query(Meal.meal_type_id, Recipe.recipe_name).\
        join(MealRecipe, Recipe).filter(Meal.meal_date >= today_week,\
            Meal.meal_date < today, Meal.week_id.in_(w_id_list)).all()

    return q


def prepare_meal_data(user_id, lookback_date):
    """Returns tuples of recipes based on past month."""

    weeks = User.query.get(user_id).weeks
    w_id_list = [w.week_id for w in weeks]

    today = date.today()
    today_month = today + datetime.timedelta(days=-30)

    q = db.session.query(Meal.meal_type_id, Recipe.recipe_name).\
        join(MealRecipe, Recipe).filter(Meal.meal_date >= lookback_date,\
            Meal.meal_date < today, Meal.week_id.in_(w_id_list)).all()

    chart_dict = {}
    recipe_count = {}
    labels = []
    data = []
    colors = ['#4ABDAC', '#FC4A1A', '#B0FFF3', '#64FFE8', '#587F7A',\
    '#50CCBA', '#FF8767', '#FF4B1A', '#7F4433', '#CC3C15',\
    '#F7B733', '#ffd681']

    for meal_type, recipe in q:
        recipe_count[recipe] = recipe_count.get(recipe, 0) + 1

    for r in recipe_count.keys():
        labels.append(r)
        data.append(recipe_count[r])

    chart_dict = {
        "labels": labels[:12],
        "datasets": [
            {   "label": "# of Recipes",
                "backgroundColor": colors,
                "data": data[:12],
            }
        ]
    }

    return chart_dict


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealplan'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
