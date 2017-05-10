"""Models and database functions for my Meal Planner Project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of meal plan app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    # age = db.Column(db.Integer, nullable=True)
    # zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id={} email={}>".format(self.user_id,
                                                   self.email)


class Week(db.Model):
    """The plan for the week."""

    __tablename__ = "weeks"

    week_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.user_id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False) #A day Mon - Sun
    # end_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User",
        backref=db.backref("weeks", order_by=week_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<week_id=%s start_date=%s>" % (self.week_id,
                                                 self.start_date)


class MealType(db.Model):
    """Type for each meal."""

    __tablename__ = "meal_types"

    meal_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<meal_id=%s type_name=%s>" % (self.meal_type_id,
                                                self.type_name)


class Meal(db.Model):
    """Each meal in the plan."""

    __tablename__ = "meals"

    meal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.week_id'), nullable=False)
    meal_type_id = db.Column(db.Integer, db.ForeignKey('meal_types.meal_type_id'),
        nullable=False)
    meal_date = db.Column(db.DateTime, nullable=False)

    week = db.relationship("Week",
        backref=db.backref("meals", order_by=meal_id))

    meal_type = db.relationship("MealType",
        backref=db.backref("meals", order_by=meal_id))

    recipes = db.relationship("Recipe",
                             secondary="meal_recipes",
                             backref="meals")

    def __repr__(self):
        """Provide helpful representation when printed."""
        s = "<Meal meal_id=%s meal_type=%s date=%s>"
        return s % (self.meal_id, self.meal_type, self.meal_date)


class MealRecipe(db.Model):
    """Association Table to connect meals and recipes."""

    __tablename__ = "meal_recipes"

    meal_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'),
        nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.meal_id'),
        nullable=False)

    meal = db.relationship("Meal",
        backref=db.backref("meal_recipes", order_by=meal_recipe_id))

    recipe = db.relationship("Recipe",
        backref=db.backref("meal_recipes", order_by=meal_recipe_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        s = "<meal_recipe_id=%s recipe_id=%s meal_id=%s>"
        return s % (self.meal_recipe_id, self.recipe_id, self.meal_id)


class Recipe(db.Model):
    """Each recipe."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String(150), nullable=True)
    directions = db.Column(db.String(10000), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<recipe_id=%s recipe_name=%s>" % (self.recipe_id,
                                                self.recipe_name)


class Unit(db.Model):
    """List of all types of units of a recipe."""

    __tablename__ = "units"

    unit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<unit_id=%s unit_name=%s>" % (self.unit_id,
                                                self.unit_name)


class Category(db.Model):
    """All possible categories for an ingredient."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<category_id=%s category_name=%s>" % (self.category_id,
            self.category_name)


class Ingredient(db.Model):
    """All possible ingredients."""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'),
        nullable=True)
    has_nuts = db.Column(db.Boolean, nullable=True)
    has_dairy = db.Column(db.Boolean, nullable=True)
    has_gluten = db.Column(db.Boolean, nullable=True)
    need_whole_number = db.Column(db.Boolean, nullable=True)

    category = db.relationship("Category",
        backref=db.backref("ingredients", order_by=ingredient_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<ingredient_id=%s ingredient_name=%s>" % (self.ingredient_id,
                                                self.ingredient_name)


class RecipeIngredient(db.Model):
    """Middle Table connecting Ingredients to Recipes."""

    __tablename__ = "recipe_ingredients"

    recipe_ing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
        db.ForeignKey('recipes.recipe_id'), nullable=False)
    ingredient_id = db.Column(db.Integer,
        db.ForeignKey('ingredients.ingredient_id'), nullable=False)
    unit_id = db.Column(db.Integer,
        db.ForeignKey('units.unit_id'), nullable=True)
    qty = db.Column(db.Float, nullable=True)

    recipes = db.relationship("Recipe",
        backref=db.backref("recipe_ingredients", order_by=recipe_ing_id))

    ingredient = db.relationship("Ingredient",
        backref=db.backref("recipe_ingredients", order_by=recipe_ing_id))

    unit = db.relationship("Unit",
        backref=db.backref("recipe_ingredients", order_by=recipe_ing_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return ("<recipe_ing_id=%s recipe_id=%s ingredient_id=%s>" %
            (self.recipe_ing_id, self.recipe_id, self.ingredient_id))


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
