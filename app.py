from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            num_ac = int(request.form["num_ac"])
            hours_on = float(request.form["hours_on"])
            ac_type = int(request.form["ac_type"])
            current_temp = int(request.form["current_temp"])
            target_temp = int(request.form["target_temp"])
            cost_per_kwh = float(request.form["cost_per_kwh"])

            if target_temp <= current_temp:
                raise ValueError("Target temperature must be higher than current temperature.")

            temp_diff = target_temp - current_temp

            if ac_type == 1:
                saving_per_degree = 0.06
            elif ac_type == 2:
                saving_per_degree = 0.12
            else:
                raise ValueError("Invalid AC type selected.")

            # kWh saved per unit per hour
            kwh_saved = temp_diff * saving_per_degree * hours_on * num_ac
            money_saved = kwh_saved * cost_per_kwh
            carbon_reduced = kwh_saved * 0.69  # Rough estimate of kg CO2 per kWh

            results = {
                'num_ac': num_ac,
                'hours_on': hours_on,
                'ac_type': ac_type,
                'current_temp': current_temp,
                'target_temp': target_temp,
                'cost_per_kwh': cost_per_kwh,
                'kwh_day': kwh_saved,
                'money_day': money_saved,
                'carbon_day': carbon_reduced,
                'money_week': money_saved * 7,
                'carbon_week': carbon_reduced * 7,
                'money_month': money_saved * 30,
                'carbon_month': carbon_reduced * 30,
                'money_year': money_saved * 365,
                'carbon_year': carbon_reduced * 365,
            }

            return render_template("index.html", results=results)
        except ValueError as ve:
            return render_template("index.html", error=str(ve))
        except Exception as e:
            return render_template("index.html", error="An unexpected error occurred.")
    
    return render_template("index.html")
