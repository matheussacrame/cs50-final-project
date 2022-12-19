# NutriTrack application
#### Video Demo: https://youtu.be/XBkHDbD9p4E
#### Description:

This application intends to track an user's fitness parameters. Through the input of information such as weight, age and gender, it calculates the user's calorie expense. It also registers foods and meals, automating the calculation of calorie surplus or deficit, as well as macronutrient calculations.

## App.py file:

This is a python file that implements the backend (server) of the application using the Flask framework. It uses these dependencies:

```
from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request
from flask_session import Session
from helpers import apology, calculate_expense
from tempfile import mkdtemp
```

Helpers is also a file from this project (see below in the `Helpers.py` section). The other dependencies are external libraries.

The app.py file configures the flask application, connects the database `nutritrack.db` and implements each of the routes in the application.

The **INDEX** route only renders a template if the user's weight has been registered. Else, it redirects to the `/weight` route. The index route queries the user's meals and goals from the database. Then, it calculates how many calories, proteins, fats and carbs have been consumed and still should be consumed. It returns the `index.html` template, plugging in the calculated variables and a meal dictionary. The meal dictionary is used by `index.html` to show every meal consumed that day. It only accepts GET methods.

The **FOODS** route accepts POST and GET methods. The GET method simply queries all foods in the user's database and returns the `foods.html` template, plugging in a dictionary that will be used by the template to show all foods registered. This process also happens in the POST method.

The POST method gets food input submited by the user, validates and registers it in the database. It inserts the food name, calories, proteins, fats and carbs into the foods table in the database.

The **GOALS** route accepts POST and GET methods. The GET method simply renders the template `goals.html`.

The POST method gets user input on preferences (manual or automatic), age, gender, physical activity intensity, manual calorie expense, surplus/deficit goal, surplus/deficit value and macronutrient goals (proteins, fats and carbs). Besides validating all inputs, it also queries the user's weight and calls the function `calculate_expense()` to automatically calculate the calorie expense. It then updates the goals table in the `nutritrack.db`, already multiplying the macronutrients by the user's weight. Lastly, it redirects the user to the `/` (or index) route.

The **MEALS** route accepts POST and GET methods. The GET method simply renders the `meals.html` template, which also happens on the POST method.

The POST method gets input on food name, quantity and whether the user is adding or removing from the database. It validates the inputs and registers or updates the food information on `nutritrack.db`.

The **WEIGHT** route accepts POST and GET methods. The GET method simply renders the `weight.html` template.

The POST method gets user input on weight, validates it and registers or updates it into the database, redirecting the user to the `/goals` route and flashing a success message.

## Flask Session folder:

The Flask Session folder holds information on the user's session.

## Helpers.py file:

This is a python file that holds helper functions used in the `app.py` file. `Helpers.py` depends on `Flask` function `render_template()`.

Helpers has two functions: `apology()`, which takes a message and a code as input and returns an `apology.html` template with an error code; and `calculate_expense()`, which takes four arguments (weight, gender, age, physical activity level) and returns the calculated caloric expense.

## Nutritrack.db file:

The nutritrack.db file is a database. It has four tables: `goals`, `weights`, `meals` and `foods`.

The `goals` table has the columns date (TEXT), calories (INTEGER), proteins (INTEGER), fats (INTEGER) and carbs (INTEGER). It registers the user's daily goals.

The `weights` table has the columns date (TEXT) and weight (NUMERIC). It registers the user's daily weight.

The `meals` table has the columns date (TEXT), food (TEXT) and quantity (FOOD). The `meals.food` column is a foreign key to `foods.name`. It register the user's meals.

The `foods` table has the columns name (TEXT), calories (INTEGER), proteins (INTEGER), fats (INTEGER) and carbs (INTEGER). It register the user's foods.

## Requirements.txt file:

The requirements.txt file specifies the dependencies of the application.

## Static folder:

### icon.png

The small icon used in the browser tab.

### bigicon.png

The larger icon used in the templates.

### events.js

A javascript file that is linked in the templates. It listens to the click of a button in `foods.html` and toggles the visibility of a table with all foods registered in the database.

### styles.css

A css file that sets some styles in the templates. It mostly changes background colors, font and display property.

## Templates folder:

### apology.html

Extends `layout.html`. Uses Jinja syntax to report an error code and message.

### foods.html

Extends `layout.html`. Explains where to find nutritional information on foods. Uses a form to get input on new foods to register in the database. Has a button that can be clicked, toggling the view of a table with all registered foods.

Uses Jinja syntax to generate table data from a dictionary passed by `render_template()` in `app.py`.

### goals.html

Extends `layout.html`. Explains how to set your goals and how to gain or lose weight. Uses a form to get input on the user's goals.

### index.html

Extends `layout.html`. Explains some sections of the application. Shows three tables: the user's caloric goals versus calories consumed; the user's macro goals and macros consumed; all foods eaten by the user that day.

Uses Jinja syntax to generate table data from dictionaries passed by `render_template()` in `app.py`.

### layout.html

Structures the head, navigation bar, flashed messages and footer of all pages.

Uses Jinja syntax to allow extension in other pages, as well as `if` logic to show flashed messages.

### meals.html

Extends `layout.html`. Explains how to register meals and gets input on what meal has been eaten by the user.

### weight.html

Extends `layout.html`. Explains why weight is a valuable measurement and gets input on the user's weight.

## Future implementations

### Login and Registration
This application is implemented to work for a single user. It can be made multi-user by implementing login, logout and registration templates in `static/templates` and routes in `app.py`. It would need security measures for passwords, cookies and a new table in the database, as well as implementing new columns for "user_id" in the existing tables. It would also demand adaptations in the `SQL` queries in `app.py`.

### Analytics
When there is enough information registerd in the databases, it would be interesting to show visual graphs - such as the ones outputed by python libraries like `matplotlib` - giving the user analytics about his habits. How did his weight fluctuate over time? And his goals? Which days of the week does he perform better?

