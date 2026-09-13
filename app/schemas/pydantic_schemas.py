from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from zoneinfo import ZoneInfoNotFoundError, ZoneInfo
from datetime import datetime, date


# User's schemas:
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    timezone: str = "Asia/Kolkata"

    @field_validator('timezone')
    @classmethod
    def check_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
            return value
        except (ZoneInfoNotFoundError, Exception):
            return ValueError(f"Invalid timezone name: {value}")

class UserOut(BaseModel):
    id: int
    email: EmailStr
    timezone: str

    model_config = ConfigDict(from_attributes=True)


# Habit schemas:
class HabitCreate(BaseModel):
    name: str
    description: str | None = None

class HabitResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    current_streak: int
    longest_streak: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# CheckinIn schemas:
class CheckInResponse(BaseModel):
    id: int
    habit_id: int
    local_date: date
    utc_timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# Token Schemas:
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None


# LLM Chat Schema:
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str