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
            mode = request.form["mode"]  # New

            if target_temp <= current_temp:
                raise ValueError("Target temperature must be higher than current temperature.")

            temp_diff = target_temp - current_temp
            saving_per_degree = 0.06 if ac_type == 1 else 0.12
            base_kwh = 0.85 if ac_type == 1 else 1.7

            # Adjusted
            kwh_saved = temp_diff * saving_per_degree * hours_on * num_ac
            kwh_with_adjustment = base_kwh * hours_on * num_ac - kwh_saved
            money_saved = kwh_saved * cost_per_kwh
            carbon_reduced = kwh_saved * 0.69

            # Daily base (no adjustment)
            kwh_no_adjustment = base_kwh * hours_on * num_ac
            money_no_adjustment = kwh_no_adjustment * cost_per_kwh

            # Mode logic
            days_per_week = 5 if mode == "office" else 7
            days_per_month = 21 if mode == "office" else 30
            days_per_year = 260 if mode == "office" else 365

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
                'money_month': money_saved * days_per_month,
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

