from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from .config import setting
import jwt

# Password Hashing and Verification Context Setup:
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Creates a hashed password from plain-password:
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify the password with the hashed password:
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generates a signed token for the user:
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        setting.SECRET_KEY,
        algorithm=setting.ALGORITHM
    )

    return encoded_jwt

# decodes the token and gives the payload( dict ):
def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None # token expire, token invalid, or corrupted token then we will return None