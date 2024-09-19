from datetime import datetime, time

def get_end_of_day():
    now = datetime.now()
    return datetime.combine(now.date(), time(23, 59, 59))

def get_today_range():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)
    return start_of_day, end_of_day