from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# In-memory storage (resets when app restarts)
user_data = {}#为什么在这里

def sleep_feedback(hours: float) -> str:
    if hours < 5:
        return "⚠️ Very low sleep (<5h). Try to prioritize rest tonight."
    elif hours < 7:  # 5–6.99
        return "😴 A bit low (5–6h). Aim for 7–9 hours if possible."
    elif hours <= 9:
        return "✅ Great! 7–9 hours is an ideal range."
    else:
        return "🛌 You slept >9h. If this is unusual, check your routine/energy."


def water_feedback(water_glasses: float, weekly_exercise_hours: float) -> str:
    if weekly_exercise_hours > 5:
        good = water_glasses >= 11
        reason = "you exercise a lot and need extra hydration"
    elif weekly_exercise_hours >= 2:
        good = water_glasses >= 9
        reason = "moderate exercise increases hydration needs"
    else:
        good = water_glasses >= 8
        reason = "steady daily hydration supports overall health"

    if good:
        return f"✅ Good hydration — {reason}."
    else:
        return f"💧 Not enough water — {reason}."



@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_num = datetime.now().weekday()
    days_to_weekend = 5-day_num if day_num<5 else 0
    return render_template(
        'index.html',
        time=current_time,
        days_to_weekend = days_to_weekend,
        user_data = user_data
    )

@app.route('/results')
def results():
    return render_template('results.html', user_data=user_data)


@app.route('/submit', methods=['POST'])
def submit():
    # Get form data (strings from the form)
    name = request.form.get('name', '').strip()
    sleep_hours_str = request.form.get('sleep_hours', '')
    water_glasses_str = request.form.get('water_glasses', '')
    weekly_exercise_hours_str = request.form.get('weekly_exercise_hours', '')

    # Convert to numbers safely
    try:
        sleep_hours = float(sleep_hours_str)
    except ValueError:
        sleep_hours = 0.0

    try:
        water_glasses = float(water_glasses_str)
    except ValueError:
        water_glasses = 0.0

    try:
        weekly_exercise_hours = float(weekly_exercise_hours_str)
    except ValueError:
        weekly_exercise_hours = 0.0

    # Store it (store numeric values so templates display cleanly)
    user_data['name'] = name
    user_data['sleep_hours'] = sleep_hours
    user_data['water_glasses'] = water_glasses
    user_data['weekly_exercise_hours'] = weekly_exercise_hours

    # Generate feedback (separate messages)
    user_data['sleep_feedback'] = sleep_feedback(sleep_hours)
    user_data['water_feedback'] = water_feedback(water_glasses, weekly_exercise_hours)

    print("DEBUG - Data stored:", user_data) # <-- Show your collected variable in terminal.
    # ... it's being stored as an in-memory Python dict... it's not going to an API or database yet! We'll work on that in a future lecture.

    # Redirect back to a new page called results
    return redirect(url_for('results'))


if __name__ == '__main__':
    app.run(debug=True)
