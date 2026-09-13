from datetime import date, datetime, timedelta
from app.utils.timezone_utils import calculate_streaks

def test_empty_checkins():
    # Arrange:
    today = date(2026, 9, 6)
    check_ins = []

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 0
    assert longest_streak == 0

def test_today_checkin():

    # Arrange:
    today = date(2026, 9, 6)
    check_ins = [today]

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 1
    assert longest_streak == 1

def test_continuous_three_days_streak():

    # Arrange:
    today = date(2026, 9, 6)
    check_ins = [today - timedelta(days=i)for i in range(3)]

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 3
    assert longest_streak == 3

def test_last_checkin_yesterday():

    # Arrange:
    today = date(2026, 9, 6)
    yesterday = today - timedelta(days=1)
    check_ins = [yesterday, yesterday - timedelta(days=1)]

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 2
    assert longest_streak == 2

def test_last_checkedin_two_days_ago():

    # Arrange:
    today = date(2026, 9, 6)
    two_days_ago = today - timedelta(days=2)
    three_days_ago = today - timedelta(days=3)
    check_ins = [two_days_ago, three_days_ago]

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 0
    assert longest_streak == 2

def test_last_checkedin_two_days_ago_and_today():

    # Arrange:
    today = date(2026, 9, 6)
    two_days_ago = today - timedelta(days=2)
    three_days_ago = today - timedelta(days=3)
    check_ins = [two_days_ago, three_days_ago, today]

    # Act:
    current_streak, longest_streak = calculate_streaks(check_ins, today)

    # Assert:
    assert current_streak == 1
    assert longest_streak == 2
