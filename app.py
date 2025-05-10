from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get form inputs
            num_ac = int(request.form["num_ac"])
            hours_on = float(request.form["hours_on"])
            ac_hp = float(request.form["ac_type"])  # Now allows 1.0–3.0 in 0.5 steps
            current_temp = int(request.form["current_temp"])
            target_temp = int(request.form["target_temp"])
            cost_per_kwh = float(request.form["cost_per_kwh"])
            mode = request.form["mode"]

            if target_temp <= current_temp:
                raise ValueError("Target temperature must be higher than current temperature.")

            # Calculate temperature difference
            temp_diff = target_temp - current_temp

            # Energy consumption and saving per degree per HP
            kwh_per_hp = 0.85  # 1.0 HP = 0.85 kWh, so scale it
            saving_per_degree_per_hp = 0.06  # base for 1 HP

            base_kwh = kwh_per_hp * ac_hp
            saving_per_degree = saving_per_degree_per_hp * ac_hp

            kwh_saved = temp_diff * saving_per_degree * hours_on * num_ac
            kwh_with_adjustment = base_kwh * hours_on * num_ac - kwh_saved
            money_saved = kwh_saved * cost_per_kwh
            carbon_reduced = kwh_saved * 0.69

            # No adjustment baseline
            kwh_no_adjustment = base_kwh * hours_on * num_ac
            money_no_adjustment = kwh_no_adjustment * cost_per_kwh

            # Mode logic
            days_per_week = 5 if mode == "office" else 7
            days_per_month = 21 if mode == "office" else 30
            days_per_year = 260 if mode == "office" else 365

            kwh_saved_month = kwh_saved * days_per_month
            money_saved_month = money_saved * days_per_month
            kwh_no_adjustment_month = kwh_no_adjustment * days_per_month
            money_no_adjustment_month = money_no_adjustment * days_per_month

            results = {
                'num_ac': num_ac,
                'hours_on': hours_on,
                'ac_type': ac_hp,
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
