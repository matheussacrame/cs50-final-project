from flask import render_template

def apology(message, code):
    return render_template("apology.html", message=message, code=code), code

def calculate_expense(weight, gender, age, activity):
        matrix = [[14.818*weight+486.6, 15.057*weight+692.2],
                  [8.126*weight+845.6, 11.472*weight+873.1],
                  [9.082*weight+658.5, 11.711*weight+587.7]]

         # Multiply by matrix
        if gender == "Male":
            g = 1
        else:
            g = 0

        if age == "From 18 to 30":
            a = 0
        elif age == "From 30 to 60":
            a = 1
        else:
            a = 2

        basal = matrix[a][g]

        # Multiply metabolic per activity factor
        if activity == "No/light intensity":
            return basal*1.55
        elif activity == "Medium intensity":
            return basal*1.84
        else:
            return basal*2.2