# AC Energy Saving Calculator 🌿

This simple Flask web app helps users estimate their potential energy cost savings and carbon emission reductions when raising the temperature of their air conditioners (ACs).

## 💡 Features
- Supports 1 HP and 2 HP AC types
- Calculates savings based on:
  - Number of AC units
  - Duration of use (hours/day)
  - Current and target temperature
  - Electricity cost (user-defined)
- Displays savings per day, week, month, and year
- Estimates carbon emissions reduced (based on Malaysia’s grid average)

## 🚀 Live Demo
Deployed on [Render](https://render.com/) (URL will be shown after deployment).

---

## 🖥️ Local Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ac-saving-app.git
cd ac-saving-app

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

python app.py

http://127.0.0.1:5000

ac-saving-app/
│
├── app.py                # Flask app
├── requirements.txt      # Dependencies
├── Procfile              # For deployment on Render
└── templates/
    └── index.html        # HTML frontend

Carbon reduction calculation uses Malaysia’s grid average: 0.584 kg CO₂ per kWh.

Adjust cost per kWh based on local rates (default: RM 0.435).
