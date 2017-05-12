from model import *
from model import db, connect_to_db
from datetime import date
from server import app

""" Loading Test Data into Database."""


def load_users():
    """Loading test uesrs."""

    User.query.delete()

    user1 = User(email="ivychen@gmail.com", password="hello")
    user2 = User(email="mel@ubermelong.com", password="melon")

    db.session.add_all([user1, user2])
    db.session.commit()


def load_weeks():
    """Loading test weeks."""

    Week.query.delete()

    week1 = Week(user_id=1, start_date=date(2017, 5, 7))
    week2 = Week(user_id=1, start_date=date(2017, 5, 14))

    db.session.add_all([week1, week2])
    db.session.commit()


def load_meal_types():
    """Loading test meal types."""

    MealType.query.delete()

    type1 = MealType(meal_type_id="br", type_name="breakfast")
    type2 = MealType(meal_type_id="lu", type_name="lunch")
    type3 = MealType(meal_type_id="din", type_name="dinner")
    type4 = MealType(meal_type_id="snck", type_name="snack")

    db.session.add_all([type1, type2, type3, type4])
    db.session.commit()


def load_meals():
    """Loading test meals."""

    Meal.query.delete()

    meal1 = Meal(week_id=1, meal_type_id="din", meal_date=date(2017, 5, 7))
    meal2 = Meal(week_id=1, meal_type_id="din", meal_date=date(2017, 5, 8))
    meal3 = Meal(week_id=1, meal_type_id="din", meal_date=date(2017, 5, 9))
    meal4 = Meal(week_id=1, meal_type_id="br", meal_date=date(2017, 5, 7))

    db.session.add_all([meal1, meal2, meal3, meal4])
    db.session.commit()


def load_recipes():
    """Loaindg test recipes."""

    Recipe.query.delete()

    r1 = Recipe(recipe_name="pulled pork",
        recipe_url="http://www.fifteenspatulas.com/wp-content/uploads/2013/09/SlowCookerPulledPorkFifteenSpatulas.jpg",
        directions="cook it", vegetarian=False, has_dairy=False, has_gluten=False)
    r2 = Recipe(recipe_name="chicken", vegetarian=False, has_dairy=False)
    r3 = Recipe(recipe_name="yogurt", vegetarian=True, has_dairy=True)
    r4 = Recipe(recipe_name="banana", vegetarian=True, has_dairy=True)

    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()


def load_meal_recipes():
    """Loading meal_recipes."""

    MealRecipe.query.delete()

    mr1 = MealRecipe(recipe_id=1, meal_id=1)
    mr2 = MealRecipe(recipe_id=2, meal_id=2)
    mr3 = MealRecipe(recipe_id=2, meal_id=3)
    mr4 = MealRecipe(recipe_id=3, meal_id=4)
    mr5 = MealRecipe(recipe_id=4, meal_id=4)

    db.session.add_all([mr1, mr2, mr3, mr4, mr5])
    db.session.commit()


def load_units():
    """Loading units."""

    Unit.query.delete()

    for row in open("data/units.txt"):
        name, short_name, long_name = row.rstrip().split("|")

        unit_item = Unit(unit_id=name,
                         unit_short=short_name,
                         unit_long=long_name)

        db.session.add(unit_item)

    db.session.commit()


def load_categories():

    Category.query.delete()

    # Read categories.txt file and insert data
    for row in open("data/categories.txt"):
        row = row.rstrip()

        c = Category(category_name=row)

        # We need to add to the session or it won't ever be stored
        db.session.add(c)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ingredients():

    # Ingredient.query.delete()

    for row in open("data/ing-cat.txt"):
        ingredient, cat, url = row.rstrip().split("|")

        new_ing = Ingredient(ingredient_name=ingredient,
                             category_id=cat,
                             ingredient_url=url)

        db.session.add(new_ing)

    db.session.commit()


def load_recipe_ingredients():

    RecipeIngredient.query.delete()
    rec1 = RecipeIngredient(recipe_id=2, ingredient_id=1, unit_id="lb", amt=1)
    rec2 = RecipeIngredient(recipe_id=2, ingredient_id=2, unit_id="Tbsp", amt=1)
    rec3 = RecipeIngredient(recipe_id=2, ingredient_id=3, unit_id="Tbsp", amt=0.5)

    db.session.add_all([rec1, rec2, rec3])
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_users()
    print "users"
    load_weeks()
    print "weeks"
    load_meal_types()
    print "meal types"
    load_meals()
    print "meals"
    load_recipes()
    print "recipes"
    load_meal_recipes()
    print "meal recipes"
    load_units()
    print "units"
    load_categories()
    print "categories"
    load_ingredients()
    print "ingredients"
    load_recipe_ingredients()
    print "recipe_ingredients"
