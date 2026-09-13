from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, UniqueConstraint, Index, Text, Enum as SQLEnum
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum

# This class is for 'users' table:
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    timezone = Column(String, nullable=False,default="Asia/Kolkata")

    # User can have many habits:
    habits = relationship("Habit", back_populates="owner")
    history = relationship("ChatHistory", back_populates="user")

# This class is for 'habits' table:
class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default= lambda: datetime.now(timezone.utc))

    # Habit can have only one User
    owner = relationship("User", back_populates="habits") 
    # Habit can have many Checkins:
    check_ins = relationship("Checkins", back_populates="habit")

# This class is for 'check_ins' table:
class Checkins(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    utc_timestamp = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    local_date = Column(Date, nullable=False)

    # Checkins can have only one Habit
    habit = relationship("Habit", back_populates="check_ins")

    # We need this for the unique constraint (a user cannot do checkins for a same habit twice on a day)
    __table_args__ = (
        UniqueConstraint(
            "habit_id",
            "local_date",
            name = "unique_habit_local_date"
        ),
    )

# This class is for chat history between user and ai assistant:
class ChatHistory(Base):
    __tablename__ = 'chat_history'

    class Role(str, Enum):
        HUMAN = 'human'
        AI = 'ai'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(SQLEnum(Role), default=Role.HUMAN, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    # A user can have only one ChatHistory:
    user = relationship(
        "User",
        back_populates='history'
    )

    # Speeds up user history queries and keeps records ordered:
    __table_args__ = (
        Index(
            'idx_user_chat_timeline',
            'user_id',
            'created_at'
        ),
    )