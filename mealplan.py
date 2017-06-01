""" Helper functions for mealplan page."""

from model import *
from datetime import date
import datetime

def this_week_start_date():
    """Returns the start_date for the current user's week."""
    start_date = date.today() - datetime.timedelta(days=(date.today().weekday()+1))
    return start_date


def meal_plan_days(start_date):
    """Returns list of 7 consecutive days for a given datetime start_date."""
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

    for meal_date in week.plan_days():
        add_meal_entries(week_id, meal_date)


def add_meal_entries(week_id, meal_date):
    """Adding breakfast, lunch, dinner, snacks mealrecipes for a given date."""
    m01 = Meal(week_id=week_id, meal_type_id="br", meal_date=meal_date)
    m02 = Meal(week_id=week_id, meal_type_id="lu", meal_date=meal_date)
    m03 = Meal(week_id=week_id, meal_type_id="din", meal_date=meal_date)
    m04 = Meal(week_id=week_id, meal_type_id="snck", meal_date=meal_date)

    db.session.add_all([m01, m02, m03, m04])
    db.session.commit()


def create_meal_plan(week_id, all_days):
    """Creates mealplan dictionary to be sent to mealplan page."""
    meal_plan_list = []

    breakfast = create_meal_dict(week_id, "br")
    lunch = create_meal_dict(week_id, "lu")
    dinner = create_meal_dict(week_id, "din")
    snacks = create_meal_dict(week_id, "snck")

    meal_plan_list.append(breakfast)
    meal_plan_list.append(lunch)
    meal_plan_list.append(dinner)
    meal_plan_list.append(snacks)

    return meal_plan_list


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
            # print "Adding a meal recipe", meal_id, r_id
            new_meal_recipe = MealRecipe(recipe_id=r_id, meal_id=meal_id)
            db.session.add(new_meal_recipe)

    db.session.commit()


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


def meal_month_data(user_id):
    """Returns tuples of recipes based on past month."""

    weeks = User.query.get(user_id).weeks
    w_id_list = [w.week_id for w in weeks]

    today = date.today()
    today_month = today + datetime.timedelta(days=-30)

    q = db.session.query(Meal.meal_type_id, Recipe.recipe_name).\
        join(MealRecipe, Recipe).filter(Meal.meal_date >= today_month,\
            Meal.meal_date < today, Meal.week_id.in_(w_id_list)).all()

    return q


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
