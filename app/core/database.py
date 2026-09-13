from app.core.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from typing import Annotated
from fastapi import Depends

engine = create_engine(
    setting.DATABASE_URL
)

SessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This is a dependency for the database session:
db_session = Annotated[Session, Depends(get_db)]