# Eat.Plan.Love.

Eat.Plan.Love. is a meal planner app that allows users to plan meals for the week, add family recipes to use in meal planning, and also create a shopping list that aggregates all the ingredients to take to a grocery store. It reduces stress and saves time so you don't need to think about what to eat every night and not need to run to the store if you don't have an ingredient.

## Technology
<b>Backend:</b> Python, Flask, PostgreSQL, SQLAlchemy</br>
<b>Frontend:</b> JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br>
<b>APIs:</b> Spoonacular<br>

## Setup

To Run Eat.Plan.Love, you will need:

- PostgreSQL
- Python 2.7

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/poisoniivy/meal-project.git
```

Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install needed libraries:
```
$ pip install -r requirements.txt
```

Create database 'mealplan'.
```
$ createdb mealplan
```
Create your database tables and seed example data.
```
$ python model.py
$ python seed.py
```
Run the app from the command line.
```
$ python server.py
