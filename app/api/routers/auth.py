from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import db_session
from app.models.db_models import User
from app.api.deps import current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.pydantic_schemas import UserCreate, UserOut, TokenData, Token
from typing import Annotated
from app.api.rate_limiting_setting import limiter

router = APIRouter()

@router.post('/register', status_code=201)
@limiter.limit('5/minute')
def register(request: Request, user: UserCreate, db: db_session) -> UserOut:
    check_for_user = db.query(
        User
    ).filter(User.email == user.email).first()

    if check_for_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email = user.email,
        hashed_password = hash_password(user.password),
        timezone = user.timezone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_session) -> Token:
    credential_exception = HTTPException(
        status_code=401,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None:
        raise credential_exception

    if verify_password(form_data.password, user.hashed_password):
        token = create_access_token(data = {"sub": str(user.id)})
        return Token(access_token=token, token_type="bearer")
    else:
        raise credential_exception

# To check if the current_user dependency working correctly or not:    
@router.get('/me')
@limiter.limit('5/minute')
def get_me(request: Request, user: current_user) -> UserOut:
    return user