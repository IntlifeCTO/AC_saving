from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get user input values from the form
            num_ac = int(request.form["num_ac"])
            hours_on = float(request.form["hours_on"])
            ac_type = int(request.form["ac_type"])
            current_temp = int(request.form["current_temp"])
            target_temp = int(request.form["target_temp"])
            cost_per_kwh = float(request.form["cost_per_kwh"])
            mode = request.form["mode"]  # New mode input

            # Input validation
            if target_temp <= current_temp:
                raise ValueError("Target temperature must be higher than current temperature.")

            # Calculate temperature difference
            temp_diff = target_temp - current_temp

            # Calculate energy savings per degree of temperature change
            saving_per_degree = 0.06 if ac_type == 1 else 0.12
            base_kwh = 0.85 if ac_type == 1 else 1.7  # Base kWh consumption for 1 HP or 2 HP

            # Calculate energy savings and adjusted values
            kwh_saved = temp_diff * saving_per_degree * hours_on * num_ac
            kwh_with_adjustment = base_kwh * hours_on * num_ac - kwh_saved
            money_saved = kwh_saved * cost_per_kwh
            carbon_reduced = kwh_saved * 0.69  # Assuming 0.69 kg CO2 per kWh saved

            # Daily savings (no adjustment)
            kwh_no_adjustment = base_kwh * hours_on * num_ac
            money_no_adjustment = kwh_no_adjustment * cost_per_kwh

            # Mode logic (weekdays only for office mode, all days for resident mode)
            days_per_week = 5 if mode == "office" else 7
            days_per_month = 21 if mode == "office" else 30
            days_per_year = 260 if mode == "office" else 365

            # Calculate monthly savings
            kwh_saved_month = kwh_saved * days_per_month
            money_saved_month = money_saved * days_per_month
            kwh_no_adjustment_month = kwh_no_adjustment * days_per_month  # Corrected here
            money_no_adjustment_month = money_no_adjustment * days_per_month

            # Pass all the results to the template
            results = {
                'num_ac': num_ac,
                'hours_on': hours_on,
                'ac_type': ac_type,
                'current_temp': current_temp,
                'target_temp': target_temp,
                'cost_per_kwh': cost_per_kwh,
                'mode': mode,
                'kwh_day': kwh_saved,
                'money_day': money_saved,
                'carbon_day': carbon_reduced,
                'money_week': money_saved * days_per_week,
                'carbon_week': carbon_reduced * days_per_week,
                'money_month': money_saved_month,
                'carbon_month': carbon_reduced * days_per_month,
                'money_year': money_saved * days_per_year,
                'carbon_year': carbon_reduced * days_per_year,
                'chart': {
                    'adjusted_kwh': round(kwh_with_adjustment, 2),
                    'adjusted_cost': round(kwh_with_adjustment * cost_per_kwh, 2),
                    'original_kwh': round(kwh_no_adjustment, 2),
                    'original_cost': round(money_no_adjustment, 2),
                    'adjusted_kwh_month': round(kwh_with_adjustment * days_per_month, 2),
                    'adjusted_cost_month': round(kwh_with_adjustment * days_per_month * cost_per_kwh, 2),
                    'original_kwh_month': round(kwh_no_adjustment_month, 2),
                    'original_cost_month': round(money_no_adjustment_month, 2)
                }
            }

            return render_template("index.html", results=results)
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

