from datetime import datetime, date, time, timedelta
from app import db
from app.models import Habits

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
    today = date.today()
    habits_to_reset = Habits.query.filter(Habits.last_reset_date < today).all()
    
    for habit in habits_to_reset:
        habit.completata = False
        habit.last_reset_date = today
    
    db.session.commit()