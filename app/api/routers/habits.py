from fastapi import APIRouter, HTTPException, Request
from app.schemas.pydantic_schemas import HabitCreate, HabitResponse, CheckInResponse
from app.core.database import db_session
from app.api.deps import current_user
from app.models.db_models import Habit, Checkins
from app.utils.timezone_utils import get_user_local_date, calculate_streaks
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
from app.api.rate_limiting_setting import limiter

router = APIRouter()

@router.post('', status_code=201)
@limiter.limit('5/minute')
def post_habit(request: Request, habit: HabitCreate, db: db_session, currentuser: current_user) -> HabitResponse:

    new_habit = Habit(
        user_id = currentuser.id,
        name = habit.name,
        description = habit.description
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return HabitResponse(
        id = new_habit.id,
        user_id = new_habit.user_id,
        name = new_habit.name,
        description = new_habit.description,
        current_streak = 0, # new habit dont have current_streak
        longest_streak = 0, # new habit dont have longest_streak
        created_at = new_habit.created_at
    )

@router.get('', response_model=list[HabitResponse])
@limiter.limit('5/minute')
def get_habits(request: Request,db: db_session, user: current_user) -> list[HabitResponse]:

    # Fetching all the habits with all thier checkins from the database:
    habits = (
        db.query(Habit)
        .options(selectinload(Habit.check_ins))
        .filter(Habit.user_id == user.id)
        .all()
    )

    # Getting the current local date:
    today_local_date = get_user_local_date(datetime.now(timezone.utc), user.timezone)

    response = [] # Will apend all the users habits with thier streaks and display

    for habit in habits:
        # from all the check_ins get the dates and make a list:
        dates = [c.local_date for c in habit.check_ins]

        current_streak, longest_streak = calculate_streaks(dates, today_local_date)

        response.append(
            HabitResponse(
                id = habit.id,
                user_id = habit.user_id,
                name = habit.name,
                description = habit.description,
                current_streak = current_streak,
                longest_streak = longest_streak,
                created_at = habit.created_at
            )
        )

    return response

@router.delete('/{habit_id}')
@limiter.limit('5/minute')
def delete_habit(request: Request, habit_id: int, db: db_session, currentuser: current_user) -> dict:
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == currentuser.id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail=f"Habit with id:{habit_id} not found")

    db.delete(habit)
    db.commit()

    return {"detail":f"Habit with id:{habit_id} has been deleted from the database."}

@router.post('/{habit_id}/checkin')
@limiter.limit('5/minute')
def do_checkin(request: Request, habit_id: int, db: db_session, user: current_user) -> CheckInResponse:
    habit = db.query(
        Habit
    ).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail=f"Habit with id:{habit_id} not found")

    today = get_user_local_date(datetime.now(timezone.utc), user.timezone)

    existing_checkins = db.query(Checkins).filter(Checkins.habit_id == habit.id, Checkins.local_date == today).first()
    if existing_checkins:
        raise HTTPException(status_code=400, detail=f"You already checked in today for this habit")
    
    new_checkin = Checkins(
        habit_id = habit.id,
        utc_timestamp = datetime.now(timezone.utc),
        local_date = today
    )
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)

    return new_checkin
    