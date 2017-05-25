""" Helper functions for recipe page."""

from model import *
from datetime import date
import datetime

def get_ingredients_list(recipe_id):
    """Returns list of tuples of ingredient information given a recipe_id."""

    recipe = Recipe.query.filter(Recipe.recipe_id==recipe_id)

    recipe_ingredients_list = recipe.recipe_ingredients_list

    ingredient_list = []

    for ril in recipe_ingredients_list:
        ing = ril.ingredient
        ing_name = ing.ingredient_name
        ing_id = ing.ingredient_id
        cat_name = ing.category.category_name
        unit = ril.unit.unit_long 
        amount = ril.amt
