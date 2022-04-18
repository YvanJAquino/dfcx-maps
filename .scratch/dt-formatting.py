from datetime import datetime

sample = {
    "year": 2021,
    "month": 9,
    "day": 21,
    "hours": 16,
    "minutes": 0,
    "seconds": 0,
    "nanos": 0
}

def format_datetime(pt: dict):
    year = pt['year']
    month = pt['month']
    day = pt['day']
    hour = pt['hours']
    minute = pt['minutes']
    dt_object = datetime(
        year, month, day,
        hour=hour, minute=minute
    )
    date = dt_object.strftime("%Y-%m-%d")
    time = dt_object.strftime('%I:%M %p')
    return date, time

dt, tm = format_datetime(sample)
print(dt, tm)