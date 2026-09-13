from datetime import date
from .timezone_utils import calculate_streaks
import zoneinfo

today = date(2026, 9, 6)

check_ins = [date(2026, 9, 2), date(2026, 9, 1), date(2026, 8, 31), date(2026, 9, 5)]

curr, longest = calculate_streaks(check_ins, today)
# print(curr, longest) # output -> 1 , 3
# print(zoneinfo.available_timezones())

