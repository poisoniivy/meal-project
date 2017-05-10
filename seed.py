from model import *
from model import db, connect_to_db
from datetime import date
from server import app

""" Loading Test Data into Database."""


def load_users():
    """Loading test uesrs."""
    user1 = User(email="ivychen@gmail.com", password="hello")
    user2 = User(email="mel@ubermelong.com", password="melon")

    db.session.add_all([user1, user2])
    db.session.commit()


def load_weeks():
    """Loading test weeks."""
    week1 = Week(user_id=1, start_date=date(2017, 5, 7))
    week2 = Week(user_id=1, start_date=date(2017, 5, 14))

    db.session.add_all([week1, week2])
    db.session.commit()


def load_meal_types():
    """Loading test meal types."""
    type1 = MealType(type_name="breakfast")
    type2 = MealType(type_name="lunch")
    type3 = MealType(type_name="dinner")
    type4 = MealType(type_name="snack")

    db.session.add_all([type1, type2, type3, type4])
    db.session.commit()


def load_meals():
    """Loading test meals."""
    meal1 = Meal(week_id=1, meal_type_id=3, meal_date=date(2017, 5, 7))
    meal2 = Meal(week_id=1, meal_type_id=3, meal_date=date(2017, 5, 8))
    meal3 = Meal(week_id=1, meal_type_id=3, meal_date=date(2017, 5, 9))
    meal4 = Meal(week_id=1, meal_type_id=1, meal_date=date(2017, 5, 7))

    db.session.add_all([meal1, meal2, meal3, meal4])
    db.session.commit()


def load_recipes():
    """Loaindg test recipes."""
    r1 = Recipe(recipe_name="pulled pork",
        img_url="http://www.fifteenspatulas.com/wp-content/uploads/2013/09/SlowCookerPulledPorkFifteenSpatulas.jpg",
        directions="cook it")
    r2 = Recipe(recipe_name="chicken")
    r3 = Recipe(recipe_name="yogurt")
    r4 = Recipe(recipe_name="banana")

    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()


def load_meal_recipes():
    """Loading meal_recipes."""
    mr1 = MealRecipe(recipe_id=1, meal_id=1)
    mr2 = MealRecipe(recipe_id=2, meal_id=2)
    mr3 = MealRecipe(recipe_id=2, meal_id=3)
    mr4 = MealRecipe(recipe_id=3, meal_id=4)
    mr5 = MealRecipe(recipe_id=4, meal_id=4)

    db.session.add_all([mr1, mr2, mr3, mr4, mr5])
    db.session.commit()


def load_units():
    """Loading units."""
    tablespoon = Unit(unit_name="tablespoon")
    teaspoon = Unit(unit_name="teaspoon")
    cup = Unit(unit_name="cup")
    whole = Unit(unit_name="whole")

    db.session.add_all([tablespoon, teaspoon, cup, whole])
    db.session.commit()


def load_categories():
    c1 = Category(category_name="poultry")
    c2 = Category(category_name="meat")
    c3 = Category(category_name="dairy")
    c4 = Category(category_name="produce")
    c5 = Category(category_name="seasonings")

    db.session.add_all([c1, c2, c3, c4, c5])
    db.session.commit()


def load_ingredients():
    ing1 = Ingredient(ingredient_name="chicken", category_id=1)
    ing2 = Ingredient(ingredient_name="salt", category_id=5)
    ing3 = Ingredient(ingredient_name="pepper", category_id=5)
    ing4 = Ingredient(ingredient_name="pork shoulder", category_id=2)
    ing5 = Ingredient(ingredient_name="yogurt", category_id=3)
    ing6 = Ingredient(ingredient_name="banana", category_id=5)

    db.session.add_all([ing1, ing2, ing3, ing4, ing5, ing6])
    db.session.commit()


def load_recipe_ingredients():
    rec1 = RecipeIngredient(recipe_id=2, ingredient_id=1, unit_id=4, qty=1)
    rec2 = RecipeIngredient(recipe_id=2, ingredient_id=2, unit_id=1, qty=1)
    rec3 = RecipeIngredient(recipe_id=2, ingredient_id=3, unit_id=1, qty=0.5)

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
