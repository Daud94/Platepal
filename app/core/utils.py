from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from app.config.env_config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify password function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire, "jti": uuid4().hex})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def generate_unique_number(length: int) -> str:
    """
    Generate a unique number string of specified length.

    Args:
        length: The desired length of the number string

    Returns:
        A string of random numbers with the specified length
    """
    import random
    return ''.join(str(random.randint(0, 9)) for _ in range(length))
