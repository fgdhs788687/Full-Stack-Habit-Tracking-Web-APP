from fastapi import APIRouter, HTTPException, Request, status
from app.schemas.pydantic_schemas import ChatMessage, ChatResponse, HabitResponse
from app.api.deps import current_user
from app.agent.llm_model import llm
from app.api.rate_limiting_setting import limiter
from app.core.database import db_session
from app.models.db_models import Habit, Checkins, ChatHistory
from sqlalchemy.orm import selectinload
from app.utils.timezone_utils import get_user_local_date, calculate_streaks
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from langchain.messages import HumanMessage, AIMessage, SystemMessage

router = APIRouter()


@router.post('/', status_code=200, response_model=ChatResponse)
@limiter.limit('2/minute')
def chatting(request: Request,chat: ChatMessage, user:current_user, db: db_session) -> ChatResponse:
    # Let's extract all the habits with their respective checkins:
    user_habits = db.query(Habit).options(selectinload(Habit.check_ins)).filter(Habit.user_id == user.id).all() 
    # .all() returns a list, it can be empty or list of user's habits.

    habits_with_streak = []
    today_date = get_user_local_date(datetime.now(timezone.utc), user.timezone)
    current_day_name = datetime.now(timezone.utc).astimezone(ZoneInfo(user.timezone)).strftime("%A")
    
    for habit in user_habits:

        dates = [date.local_date for date in habit.check_ins]
        current_streak, longest_streak = calculate_streaks(dates, today_date)

        habits_with_streak.append(
            HabitResponse(
                id=habit.id,
                user_id=habit.user_id,
                name=habit.name,
                description=habit.description,
                current_streak=current_streak,
                longest_streak=longest_streak,
                created_at=habit.created_at
        )
    )

    # Now we will concatinate the complete habit list (with streaks each) to the summary:
    if not user_habits:
        habit_summary = "The user doesn't have any habits set up currently."
    else:
        habit_summary = "Here are the users active habits and thier streaks(current_streaks & longest_streaks):\n"
        habit_summary += "\n".join(
            [f" -{h.name}: {h.description or 'No description'} | Current_streak: {h.current_streak} days and Longest_streak: {h.longest_streak} days\n" for h in habits_with_streak]
    )

    # Past messeges (History of the current user):
    past_messeges = db.query(
        ChatHistory
    ).filter(ChatHistory.user_id == user.id).order_by(ChatHistory.created_at.desc()).limit(12).all()
    past_messeges.reverse()

    langchain_history = []
    for msg in past_messeges:
        if msg.role == ChatHistory.Role.HUMAN:
            langchain_history.append(HumanMessage(content=msg.content))
        else:
            langchain_history.append(AIMessage(content=msg.content))

    system_prompt = SystemMessage(content=(
        f"You are an empathetic, motivating AI habit-tracking coach. You are talking to user ID {user.id} ({user.email}).\n"
        f"Their current local timezone is {user.timezone} and today date is {current_day_name}, and todays date is {today_date}.\n\n"
        f"{habit_summary}\n\n"
        "Provide constructive feedback, hold them accountable for their streaks, and help them stay consistent."
    ))

    messages = [system_prompt] + langchain_history + [HumanMessage(content=chat.message)]

    try:
        response = llm.invoke(messages)
        ai_response_text = response.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="OpenRouter free tier is busy or rate-limited. Please try again in a few seconds."
        )

    db_user_msg = ChatHistory(
        user_id=user.id,
        role=ChatHistory.Role.HUMAN,
        content=chat.message
    )
    db_ai_msg = ChatHistory(
        user_id=user.id,
        role=ChatHistory.Role.AI,
        content=ai_response_text
    )
    db.add_all([db_user_msg, db_ai_msg])
    db.commit()
    
    return {'response': ai_response_text}

    


    


    
