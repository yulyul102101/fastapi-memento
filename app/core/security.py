from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import Boolean

from app.core.config import settings
from app.models.common import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
        expires_delta: timedelta = timedelta(settings.REFRESH_TOKEN_EXPIRE_DAYS)
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(refresh_token: str) -> bool:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        TokenPayload(**payload)  # exp 유효성 확인
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValidationError):
        return False
    return True


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)