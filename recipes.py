""" Helper functions for recipe page."""

from model import *
from datetime import date
import datetime

def get_ingredients_list(recipe_id):
    """Returns list of tuples of ingredient information given a recipe_id."""

    # Perhaps refactor later and create an extensive SQLAlchemy query
    recipe = Recipe.query.get(recipe_id)

    recipe_ingredients_list = recipe.recipe_ingredients

    ingredient_list = []

    for ril in recipe_ingredients_list:
        ing = ril.ingredient
        ing_name = ing.ingredient_name
        ing_id = ing.ingredient_id
        cat_name = ing.category.category_name
        unit = ril.unit.unit_long
        amount = ril.amt

        ingredient_list.append((ing_id, ing_name, cat_name, amount, unit))

    print ingredient_list
    return ingredient_list


def get_all_recipes_from_week(week_id):
    """Returns a list of all recipes (undeduplicated) given a week_id."""
    week = Week.query.get(week_id)

    meals = week.meals
    recipe_list = []
    for meal in meals:
        recipes = meal.recipes
        recipe_list.extend(recipes)

    return recipe_list


def get_shopping_list(recipe_list):
    """Returns shopping list info for given recipe object list."""

    shopping_list = {}

    for recipe in recipe_list:
        print recipe
        ingredient_info = get_ingredients_list(recipe.recipe_id)

        for ing_id, ing_name, cat_name, amount, unit in ingredient_info:

            # if category already exists or ingredient already in category list
            category_list = cat_name.split(";")
            category_name = category_list[0]
            other_categories = category_list[1:]

            if category_name in shopping_list:
                if ing_id in shopping_list[cat_name]:
                    shopping_list[category_name][ing_id]["amount"] += amount
                else:
                    ing_obj = {}
                    ing_obj["name"] = ing_name
                    ing_obj["amount"] = amount
                    ing_obj["unit"] = unit
                    shopping_list[category_name][ing_id] = ing_obj
            else:
                ing_obj = {}
                ing_obj["name"] = ing_name
                ing_obj["amount"] = amount
                ing_obj["unit"] = unit
                ing_obj["other"] = other_categories

                category_obj = {ing_id: ing_obj}
                shopping_list[category_name] = category_obj

    print shopping_list
    return shopping_list


def add_ingredient_to_recipe(ingredient_id, recipe_id, unit_id, amount):
    """Connects an ingredient to a recipe in RecipeIngredient table."""
    recipe_ing = RecipeIngredient(recipe_id=recipe_id,
                                ingredient_id=ingredient_id,
                                unit_id=unit_id,
                                amt=amount)
    db.session.add(recipe_ing)
    db.session.commit()
    # return recipe_ing.recipe_ing_id


def add_ingredient(ingredient_name, category_id=None, ingredient_url=None):
    """Adds an ingredient to the ingredient table and returns the ing_id"""
    new_ing = Ingredient(ingredient_name=ingredient_name,
                            category_id=category_id,
                            ingredient_url=ingredient_url)
    db.session.add(new_ing)
    db.session.commit()
    return new_ing.ingredient_id


def add_new_recipe(recipe_name, directions=None, recipe_url=None,
    has_dairy=None, has_gluten=None, vegetarian=None):
    """Creates a new recipe and returns the recipe_id."""
    new_rec = Recipe(recipe_name=recipe_name,
                    directions=directions,
                    recipe_url=recipe_url,
                    has_dairy=has_dairy,
                    has_gluten=has_gluten,
                    vegetarian=vegetarian)
    db.session.add(new_rec)
    db.session.commit()
    return new_rec.recipe_id


def add_recipe_to_user(recipe_id, user_id):
    """Connects a recipe to a user's recipebox."""
    user_rec = UserRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(user_rec)
    db.session.commit()


def remove_recipe_from_user(recipe_id, user_id):
    """Removes the connection between a recipe and a user."""
    ur = UserRecipe.query.filter(UserRecipe.recipe_id==recipe_id,
                                UserRecipe.user_id==user_id).one()
    db.session.delete(ur)
    db.session.commit()

def remove_recipe_from_meal(recipe_id):
    """Removies all the meals that a recipe is connected to."""
    mr_list = MealRecipe.query.filter(MealRecipe.recipe_id==recipe_id).all()

    for mr in mr_list:
        db.session.delete_all(mr)

    db.session.commit


def remove_ingredients_from_recipe(recipe_id):
    """Removes the connection of a recipe to all its ingredients."""
    rec_ing_list = RecipeIngredient.query.filter(
                    RecipeIngredient.recipe_id==recipe_id).all()

    for rec_ing in rec_ing_list:
        db.session.delete(rec_ing)

    db.session.commit()


def remove_recipe(recipe_id):
    """Deletes recipe from DB."""

    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()


def ingredient_in_recipe(ingredient_id, recipe_id):
    """Checks to see if ingredient already in the recipe. Returns boolean."""

    check = RecipeIngredient.query.filter(RecipeIngredient.recipe_id==recipe_id,
                        RecipeIngredient.ingredient_id==ingredient_id).first()
    return check


def edit_recipe_ingredient(recipe_id, ingredient_id, unit, amount):
    """Edits ingredient info for a specfic recipe."""
    data = {    "unit_id": unit,
                "amt": amount
            }
    db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id==recipe_id,
        RecipeIngredient.ingredient_id==ingredient_id).update(data)
    db.session.commit()


def edit_recipe_information(recipe_id, recipe_name, directions=None,
        recipe_url=None, has_dairy=None, has_gluten=None, vegetarian=None):
    data = {    "recipe_name": recipe_name,
                "recipe_url": recipe_url,
                "directions": directions,
                "has_dairy": has_dairy,
                "has_gluten": has_gluten,
                "vegetarian": vegetarian
            }
    db.session.query(Recipe).filter(Recipe.recipe_id==recipe_id).update(data)
    db.session.commit()

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
