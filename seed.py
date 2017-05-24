from model import *
from model import db, connect_to_db
from datetime import date
from server import app

""" Loading Test Data into Database."""


def load_users():
    """Loading test uesrs."""

    User.query.delete()

    user1 = User(email="ivychen@gmail.com", password="hello", user_name="ivy")
    user2 = User(email="mel@ubermelong.com", password="melon", user_name="mel")

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

    m01 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 14))
    m02 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 14))
    m03 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 14))
    m04 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 14))

    m05 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 15))
    m06 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 15))
    m07 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 15))
    m08 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 15))

    m09 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 16))
    m10 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 16))
    m11 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 16))
    m12 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 16))

    m13 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 17))
    m14 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 17))
    m15 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 17))
    m16 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 17))

    m17 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 18))
    m18 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 18))
    m19 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 18))
    m20 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 18))

    m21 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 19))
    m22 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 19))
    m23 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 19))
    m24 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 19))

    m25 = Meal(week_id=2, meal_type_id="br", meal_date=date(2017, 5, 20))
    m26 = Meal(week_id=2, meal_type_id="lu", meal_date=date(2017, 5, 20))
    m27 = Meal(week_id=2, meal_type_id="din", meal_date=date(2017, 5, 20))
    m28 = Meal(week_id=2, meal_type_id="snck", meal_date=date(2017, 5, 20))

    # db.session.add_all([meal1, meal2, meal3, meal4])
    db.session.add_all([m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11,
        m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25,
        m26, m27, m28])
    db.session.commit()


def load_recipes():
    """Loaindg test recipes."""

    Recipe.query.delete()

    # r1 = Recipe(recipe_name="pulled pork",
    #     recipe_url="http://www.fifteenspatulas.com/wp-content/uploads/2013/09/SlowCookerPulledPorkFifteenSpatulas.jpg",
    #     directions="cook it", vegetarian=False, has_dairy=False, has_gluten=False)
    # r2 = Recipe(recipe_name="chicken", vegetarian=False, has_dairy=False)
    # r3 = Recipe(recipe_name="yogurt", vegetarian=True, has_dairy=True)
    # r4 = Recipe(recipe_name="banana", vegetarian=True, has_dairy=True)

    br1 = Recipe(recipe_name="yogurt", vegetarian=True, has_dairy=True)
    br2 = Recipe(recipe_name="bananas", vegetarian=True, has_dairy=False)
    br3 = Recipe(recipe_name="milk", vegetarian=True, has_dairy=True)
    br4 = Recipe(recipe_name="fried eggs", vegetarian=False, has_dairy=False)
    br5 = Recipe(recipe_name="toast", vegetarian=True, has_dairy=False)
    br6 = Recipe(recipe_name="egg sandwich", vegetarian=False, has_dairy=False)
    br7 = Recipe(recipe_name="granola with milk", vegetarian=True, has_dairy=False)

    lu1 = Recipe(recipe_name="leftover chicken", vegetarian=False, has_dairy=False)
    lu2 = Recipe(recipe_name="leftover pulled pork", vegetarian=False, has_dairy=False)
    lu3 = Recipe(recipe_name="carrots", vegetarian=True, has_dairy=False)

    din1 = Recipe(recipe_name="pulled pork")
    din2 = Recipe(recipe_name="roast chicken")
    din3 = Recipe(recipe_name="pork chops")
    din4 = Recipe(recipe_name="steak")
    din5 = Recipe(recipe_name="bok choy")
    din6 = Recipe(recipe_name="noodles")

    s1 = Recipe(recipe_name="grapes")
    s2 = Recipe(recipe_name="crackers")
    s3 = Recipe(recipe_name="cookies")
    s4 = Recipe(recipe_name="strawberries")

    # db.session.add_all([r1, r2, r3, r4])

    db.session.add_all([br1, br2, br3, br4, br5, br6, br7])
    db.session.add_all([lu1, lu2, lu3])
    db.session.add_all([din1, din2, din3, din4, din5, din6])
    db.session.add_all([s1, s2, s3, s4])
    db.session.commit()


def load_meal_recipes():
    """Loading meal_recipes."""

    MealRecipe.query.delete()

    mr1 = MealRecipe(recipe_id=1, meal_id=5)
    mr2 = MealRecipe(recipe_id=2, meal_id=5)
    mr3 = MealRecipe(recipe_id=3, meal_id=5)
    mr4 = MealRecipe(recipe_id=5, meal_id=5)
    mr5 = MealRecipe(recipe_id=9, meal_id=6)
    mr6 = MealRecipe(recipe_id=10, meal_id=6)
    mr7 = MealRecipe(recipe_id=20, meal_id=6)
    mr8 = MealRecipe(recipe_id=11, meal_id=7)
    mr9 = MealRecipe(recipe_id=15, meal_id=7)

    db.session.add_all([mr1, mr2, mr3, mr4, mr5, mr6, mr7, mr8, mr9])
    db.session.commit()


def load_user_recipes():
    """Preloading user_recipes."""

    UserRecipe.query.delete()

    u1 = UserRecipe(user_id=1, recipe_id=1)
    u2 = UserRecipe(user_id=1, recipe_id=2)
    u3 = UserRecipe(user_id=1, recipe_id=3)
    u4 = UserRecipe(user_id=1, recipe_id=4)
    u5 = UserRecipe(user_id=1, recipe_id=5)
    u6 = UserRecipe(user_id=1, recipe_id=6)
    u7 = UserRecipe(user_id=1, recipe_id=7)
    u8 = UserRecipe(user_id=1, recipe_id=8)
    u9 = UserRecipe(user_id=1, recipe_id=9)
    u10 = UserRecipe(user_id=1, recipe_id=10)
    u11 = UserRecipe(user_id=1, recipe_id=11)
    u12 = UserRecipe(user_id=1, recipe_id=12)
    u13 = UserRecipe(user_id=1, recipe_id=13)
    u14 = UserRecipe(user_id=1, recipe_id=14)
    u15 = UserRecipe(user_id=1, recipe_id=15)
    u16 = UserRecipe(user_id=1, recipe_id=16)
    u17 = UserRecipe(user_id=1, recipe_id=17)
    u18 = UserRecipe(user_id=1, recipe_id=18)
    u19 = UserRecipe(user_id=1, recipe_id=19)
    u20 = UserRecipe(user_id=1, recipe_id=20)

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10,
        u11, u12, u13, u14, u15, u16, u17, u18, u19, u20])
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
    r1 = RecipeIngredient(recipe_id=1, ingredient_id=1258, unit_id="c", amt=1)
    r2 = RecipeIngredient(recipe_id=2, ingredient_id=113, unit_id="p", amt=1)
    r3 = RecipeIngredient(recipe_id=3, ingredient_id=1991, unit_id="c", amt=2)
    r4 = RecipeIngredient(recipe_id=4, ingredient_id=74, unit_id="w", amt=2)
    r5 = RecipeIngredient(recipe_id=5, ingredient_id=2050, unit_id="p", amt=2)
    r6 = RecipeIngredient(recipe_id=5, ingredient_id=74, unit_id="w", amt=1)
    r7 = RecipeIngredient(recipe_id=6, ingredient_id=605, unit_id="c", amt=2)
    r13 = RecipeIngredient(recipe_id=6, ingredient_id=1991, unit_id="c", amt=2)
    r8 = RecipeIngredient(recipe_id=10, ingredient_id=211, unit_id="lb", amt=1)
    r9 = RecipeIngredient(recipe_id=11, ingredient_id=854, unit_id="lb", amt=6)
    r10 = RecipeIngredient(recipe_id=12, ingredient_id=2017, unit_id="lb", amt=5)
    r11 = RecipeIngredient(recipe_id=13, ingredient_id=848, unit_id="lb", amt=2)
    r12 = RecipeIngredient(recipe_id=14, ingredient_id=1582, unit_id="lb", amt=2)
    r14 = RecipeIngredient(recipe_id=15, ingredient_id=126, unit_id="lb", amt=2)
    r15 = RecipeIngredient(recipe_id=16, ingredient_id=521, unit_id="lb", amt=0.5)
    r16 = RecipeIngredient(recipe_id=17, ingredient_id=596, unit_id="c", amt=1)
    r17 = RecipeIngredient(recipe_id=18, ingredient_id=2066, unit_id="c", amt=2)
    r18 = RecipeIngredient(recipe_id=19, ingredient_id=219, unit_id="c", amt=2)
    r19 = RecipeIngredient(recipe_id=20, ingredient_id=1753, unit_id="c", amt=1)

    db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12,
        r13, r14, r15, r16, r17, r18, r19])
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
    load_user_recipes()
    print "user recipes"
    load_units()
    print "units"
    load_categories()
    print "categories"
    load_ingredients()
    print "ingredients"
    load_recipe_ingredients()
    print "recipe_ingredients"
