from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request
from flask_session import Session
from helpers import apology, calculate_expense

from tempfile import mkdtemp

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///nutritrack.db")

# Index route
@app.route("/")
def index():

    # Get date
    day = date.today().strftime("%d/%m/%Y")

    # Query daily meals and goals
    list_dict_meals = db.execute("SELECT food, calories, proteins, fats, carbs, quantity FROM foods JOIN (SELECT * FROM meals WHERE date=?) AS meals ON foods.name = meals.food", day)
    list_dict_goals = db.execute("SELECT calories, proteins, fats, carbs FROM goals WHERE date=?", day)

    # Calculate consumed calories and macros
    cal_consumed = 0
    pro_consumed = 0
    fat_consumed = 0
    car_consumed = 0

    for meal in list_dict_meals:
        cal_consumed += meal["calories"] / 100 * meal["quantity"]
        pro_consumed += meal["proteins"] / 100 * meal["quantity"]
        fat_consumed += meal["fats"] / 100 * meal["quantity"]
        car_consumed += meal["carbs"] / 100 * meal["quantity"]

    # If daily goals aren't set
    if list_dict_goals == []:
        return redirect("/weight")

    # Calculate remaining calories and macros
    cal_left = list_dict_goals[0]["calories"] - cal_consumed
    pro_left = list_dict_goals[0]["proteins"] - pro_consumed
    fat_left = list_dict_goals[0]["fats"] - fat_consumed
    car_left = list_dict_goals[0]["carbs"] - car_consumed

    #Render template
    return render_template("index.html", cal_consumed=cal_consumed, cal_left=cal_left, pro_consumed=pro_consumed, pro_left=pro_left, fat_consumed=fat_consumed, fat_left=fat_left, car_consumed=car_consumed, car_left=car_left, list_dict_meals=list_dict_meals)

# Foods route
@app.route("/foods", methods=["GET", "POST"])
def foods():

    # If method is post
    if request.method == "POST":

        # Get user input
        food = request.form.get("food").strip().capitalize()
        calories = request.form.get("calories", type=int)
        proteins = request.form.get("proteins", type=float)
        fats = request.form.get("fats", type=float)
        carbs = request.form.get("carbs", type=float)

        # Validate user input
        if None in [food, calories, proteins, fats, carbs] or food == "" or any(i < 0 for i in [calories, proteins, fats, carbs]):
            return apology("Invalid input", 400)

        # Register food in database
        # If food does not exist in database
        food_list_dict = db.execute("SELECT name FROM foods WHERE name=?", food)
        if food_list_dict == []:
            db.execute("INSERT INTO foods VALUES (?, ?, ?, ?, ?)", food, calories, proteins, fats, carbs)
            flash(f"Succesfully registered {food.lower()}!")

        # If food does exist
        else:
            db.execute("UPDATE foods SET calories=?, proteins=?, fats=?, carbs=? WHERE name=?", calories, proteins, fats, carbs, food)
            flash(f"Succesfully updated {food.lower()}!")

    # Query all foods in database
    list_dict_all_foods = db.execute("SELECT * FROM foods")

    # Return template
    return render_template("foods.html", list_dict_all_foods=list_dict_all_foods)

# Goals route
@app.route("/goals", methods=["GET", "POST"])
def goals():

    if request.method == "POST":

        # Get current date
        day = date.today().strftime("%d/%m/%Y")

        # Query user's weight
        weight_dict_list = db.execute("SELECT weight FROM weights WHERE date = ?", day)
        if weight_dict_list == []:
            return apology("No weight registered today - please set daily weight before calculating goals", 400)
        weight = weight_dict_list[0]["weight"]

        # If auto expense calculation
        if request.form.get("auto_or_manual") == "auto":

            # Get user automatic expense input
            gender = request.form.get("gender")
            age = request.form.get("age")
            activity = request.form.get("activity")

            # Validate input
            if gender not in ["Male", "Female"] or age not in ["From 18 to 30", "From 30 to 60", "Over 60"] or activity not in ["No/light intensity", "Medium intensity", "High intensity"]:
                return apology("Invalid input", 400)

            # Calculate expense
            expense = calculate_expense(weight, gender, age, activity)

        # Else if manual expense input
        elif request.form.get("auto_or_manual") == "manual":

            # Get manual caloric expense input
            expense = request.form.get("manual_intake", type=int)

            # Validate input
            if expense == None or expense < 0:
                return apology("Invalid input", 400)

        # Invalid input
        else:
            return apology("Select manual or automatic expense", 400)

        # Get deficit/surplus goal input:
        sd = request.form.get("sd")
        sd_value = request.form.get("sd_value", type=int)

        # Validate input
        if sd not in ["Surplus", "Deficit"] or sd_value == None or sd_value < 0 or sd_value > expense:
            return apology("Invalid input", 400)

        # Add/subtract the surplus/deficit:
        if sd == "Surplus":
            calories = expense + sd_value
        else:
            calories = expense - sd_value

        # Get macros input:
        proteins = request.form.get("proteins", type=float)
        fats = request.form.get("fats", type=float)
        carbs = request.form.get("carbs", type=float)


        # Validate input:
        if None in [proteins, fats, carbs] or any(i<0 for i in [proteins, fats, carbs]):
            return apology("Invalid input", 400)

        # Update calories and macros goals in the database
        # If there is no input for the day
        if db.execute("SELECT * FROM goals WHERE date=?", day) == []:
            db.execute("INSERT INTO goals VALUES (?, ?, ?, ?, ?)", day, calories, proteins * weight, fats * weight, carbs * weight)
            flash("Succesfully registered today's goals!")

        # If there already is a calorie goal
        else:
            db.execute("UPDATE goals SET calories=?, proteins=?, fats=?, carbs=? WHERE date=?", calories, proteins * weight, fats * weight, carbs * weight, day)
            flash("Succesfully updated today's goals!")

        return redirect("/")

    #Render template:
    return render_template("goals.html")

# Meals route
@app.route("/meals", methods=["GET", "POST"])
def meals():

    # If method is post
    if request.method == "POST":

        # Get current date
        day = date.today().strftime("%d/%m/%Y")

        # Get user input
        food = request.form.get("food").strip().capitalize()
        quantity = request.form.get("quantity", type=int)
        option = request.form.get("option")

        # Validate user input
        if quantity == None or quantity < 0 or food == "" or option not in ["Add meal", "Remove meal"]:
            return apology("Invalid input", 400)

        # Check if food is in the database
        food_list_dict = db.execute("SELECT name FROM foods WHERE name=?", food)
        if food_list_dict == []:
            return apology("Food not found", 400)

        # Add meal
        if option == "Add meal":

            # Store meal in database
            db.execute("INSERT INTO meals VALUES (?, ?, ?)", day, food, quantity)
            flash(f"Succesfully registered {food.lower()} meal!")

        else:
            db.execute("DELETE FROM meals WHERE date=? AND food=? AND quantity=? LIMIT 1", day, food, quantity)
            flash(f"Succesfully removed {food.lower()} meal!")

    # Render template
    return render_template("meals.html")

# Weight route
@app.route("/weight", methods=["GET", "POST"])
def weight():

    # If POST
    if request.method == "POST":

        # Get user input
        kg = request.form.get("weight", type=float)

        # Validate the input
        if kg == None or kg < 0:
            return apology("Invalid weight", 400)

        # Add weight to database if first time today
        day = date.today().strftime("%d/%m/%Y")
        if db.execute("SELECT * FROM weights WHERE date = ?", day) == []:
            db.execute("INSERT INTO weights VALUES (?, ?)", day, kg)

            # Flash feedback (added)
            flash("Succesfully regsitered today's weight!")

        # Overwrite weight to database if already there
        else:
            db.execute("UPDATE weights SET weight=? WHERE date=?", kg, day)

            # Flash feedback (overwrite)
            flash("Succesfully updated today's weight!")

        return redirect("/goals")

    # Render template
    return render_template("weight.html")


