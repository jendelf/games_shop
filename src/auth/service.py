from datetime import datetime, timedelta, timezone
import jwt
from .constants import ACCESS_TOKEN_EXPIRE_MINUTES
from settings import settings
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):  # Verifies that the provided plain password matches the hashed password from the database
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password): # generating hashed version of the given password
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None): # create json web token with the given payload(data) and expiration time
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt