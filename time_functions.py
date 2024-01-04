import os
from dotenv import load_dotenv

load_dotenv("space-odyssey.env")


def calculate_current_time_left() -> int:
    import time, datetime, pytz

    event_end_time_ist = (
        int(os.getenv("EVENT_END_TIME")) if os.getenv("EVENT_END_TIME") else 1677054600
    )
    current_time_ist_float = time.mktime(
        datetime.datetime.now(pytz.timezone("Asia/Kolkata")).timetuple()
    )
    time_left = event_end_time_ist - current_time_ist_float
    if time_left > 1:
        return int(time_left)
    return 1


def get_base_value(time_left: int = 0):
    # returns base_value and time_diff past that base value
    base_value = 900
    if time_left >= 3600:
        base_value = 3600
    elif time_left >= 2700:
        base_value = 2700
    elif time_left >= 1800:
        base_value = 1800
    elif time_left >= 900:
        base_value = 900
    elif time_left >= 600:
        base_value = 600
    elif time_left >= 300:
        base_value = 300
    elif time_left >= 100:
        base_value = 100
    elif 60 >= time_left >= 0:
        base_value = 60
    return base_value


def get_time_differentiator(time_left: int = 0) -> int:
    # returns time_diff past that base value
    time_differentiator = 60
    if time_left > 3600:
        time_differentiator = 200
    elif time_left > 2700:
        time_differentiator = 120
    elif time_left > 1800:
        time_differentiator = 90
    elif time_left > 900:
        time_differentiator = 60
    elif time_left > 600:
        time_differentiator = 50
    elif time_left > 300:
        time_differentiator = 40
    elif time_left > 100:
        time_differentiator = 30
    elif 100 > time_left >= 0:
        time_differentiator = 3
    return time_differentiator


def calculate_points_for_answering(
    question_level: str, hints_used: bool, time_left: int = 0
):
    if not time_left:
        time_left = calculate_current_time_left()
    base_value = get_base_value(time_left)
    time_differentiator = get_time_differentiator(time_left)
    if question_level in ("easy", "start"):
        multiplier = 50
    elif question_level in ("medium", "ctfe"):
        multiplier = 75
    elif question_level in ("hard", "ctfm"):
        multiplier = 120
    else:
        multiplier = 0
    divider = 1
    if hints_used:
        divider = 1.5
    ratio = multiplier / divider
    points_without_time = int(ratio + 1)
    points_with_time = int(
        abs(((((ratio * (time_left % base_value)) / time_differentiator))) + 1)
    )

    return points_without_time, points_with_time
