
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_ac = int(request.form["num_ac"])
        hours_on = float(request.form["hours_on"])
        ac_type = int(request.form["ac_type"])
        current_temp = int(request.form["current_temp"])
        target_temp = int(request.form["target_temp"])
        cost_per_kwh = float(request.form["cost_per_kwh"])

        if ac_type == 1:
            saving_per_degree = 0.06
        elif ac_type == 2:
            saving_per_degree = 0.12
        else:
            return render_template("index.html", error="Invalid AC type.")

        degrees_saved = target_temp - current_temp
        if degrees_saved <= 0:
            return render_template("index.html", error="Target temperature must be higher than current.")

        total_kwh_saved_per_day = num_ac * hours_on * saving_per_degree * degrees_saved
        money_saved_per_day = total_kwh_saved_per_day * cost_per_kwh
        carbon_saved_per_day = total_kwh_saved_per_day * 0.584  # Malaysia average CO₂ grid factor

        results = {
            "kwh_day": total_kwh_saved_per_day,
            "money_day": money_saved_per_day,
            "carbon_day": carbon_saved_per_day,
            "money_week": money_saved_per_day * 7,
            "money_month": money_saved_per_day * 30,
            "money_year": money_saved_per_day * 365,
            "carbon_week": carbon_saved_per_day * 7,
            "carbon_month": carbon_saved_per_day * 30,
            "carbon_year": carbon_saved_per_day * 365
        }

        return render_template("index.html", results=results)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
