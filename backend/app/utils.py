from datetime import datetime, date, time, timedelta
from app import db
from app.models import Habits
import threading

last_check_date = date.today()

def get_end_of_day():
    now = datetime.now()
    return datetime.combine(now.date(), time(23, 59, 59))

def get_today_range():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)
    return start_of_day, end_of_day

def calculate_xp(difficolta_xp):
    if difficolta_xp == 10:  # Easy
        return 10, 5
    elif difficolta_xp == 20:  # Medium
        return 20, 10
    elif difficolta_xp == 30:  # Hard
        return 40, 20
    else:
        return 0, 0  # Default case, no XP

def check_and_reset_habits():
    global last_check_date
    current_date = date.today()
    
    if current_date > last_check_date:
        with db.session.begin():
            habits = Habits.query.filter_by(completata=True).all()
            for habit in habits:
                habit.completata = False
            last_check_date = current_date
        print(f"Habits reset on {current_date}")

def run_periodic_check():
    while True:
        check_and_reset_habits()
        # Dormi fino all'inizio della prossima ora
        now = datetime.now()
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
        sleep_seconds = (next_hour - now).total_seconds()
        threading.Event().wait(sleep_seconds)

def start_habit_reset_thread():
    thread = threading.Thread(target=run_periodic_check)
    thread.daemon = True
    thread.start()
