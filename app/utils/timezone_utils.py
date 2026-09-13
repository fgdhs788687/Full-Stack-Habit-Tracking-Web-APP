from datetime import datetime, timezone, date, timedelta
from zoneinfo import ZoneInfo, available_timezones

def get_user_local_date(utc_dt: datetime, tz_name: str) -> date:
    if tz_name not in available_timezones():
        raise ValueError(f"Invalid timezone name: {tz_name}")

    # if tzinfo( timzone info ) is None then we need to set it as 'UTC' first:
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)

    # Then we need to convert it to the local timezone of the user:
    local_date = utc_dt.astimezone(ZoneInfo(tz_name))
    return local_date.date()

# This function calculates current_streak and longest_streak and returns it in the form of tuple:
def calculate_streaks(check_in_date: list[date], user_today: date) -> tuple[int, int]:
    # if the list is empty then we return 0 for current_streak and longest_streak:
    if len(check_in_date) == 0:
        return 0,0

    # lets sort the dates first:
    unique_dates = sorted(set(check_in_date))
    dates_set = set(unique_dates)

    # initializing the current_run and longest_streak:
    longest_streak = 1
    current_run = 1

    # For longest streak:
    for i in range(1, len(unique_dates)):
        if (unique_dates[i] - unique_dates[i-1]).days == 1:
            current_run += 1
        else:
            current_run = 1 # streak broke and we need to reset it to 1

        longest_streak = max(longest_streak, current_run)

    # For current streak:
    yesterday = user_today - timedelta(days=1)

    if user_today in dates_set:
        anchor_date = user_today
    elif yesterday in dates_set:
        anchor_date = yesterday # yesterday = user_today - timedelta(days=1)
    else:
        return 0, longest_streak

    current_streak = 0
    while anchor_date in dates_set:
        current_streak += 1
        anchor_date -= timedelta(days=1)
    return current_streak, longest_streak
        