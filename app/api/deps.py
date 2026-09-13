from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import db_session
from app.models.db_models import User
from app.core.security import decode_token
from typing import Annotated

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
tokendep = Annotated[str, Depends(oauth2_schema)]

def get_current_user(token: tokendep, db: db_session) -> User:
    creadential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate Creadentials",
        headers={
            "WWW-Authenticate":"Bearer"
        }
    )

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Get the sub string from the payload
    str_user_id = payload.get('sub')
    if str_user_id is None:
        raise creadential_exception

    # Convert it to int:
    try:
        user_id = int(str_user_id)
    except (ValueError, TypeError):
        raise creadential_exception

    # Query the database for the user existence
    user = db.query(
        User
    ).filter(User.id == user_id).first()
    if user is None:
        raise creadential_exception

    return user

# We will use this in the endpoints:
current_user = Annotated[User, Depends(get_current_user)]