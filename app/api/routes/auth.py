from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.core.security import verify_refresh_token
from app.crud import user as user_crud
from app.api.deps import SessionDep, ExpiredUser
from app.models.common import Token

router = APIRouter(prefix="/auth", tags=["auth"])


# 로그인(JWT 생성)
@router.post("/login/access-token")
def login_access_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token()

    user_crud.update_refresh_token(
        session=session,
        db_user=user,
        refresh_token=refresh_token
    )

    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return token


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    session: SessionDep,
    refresh_token: Annotated[str, Form()],
    expired_user: ExpiredUser,
):
    """
    access_token 및 refresh_token 갱신
    """
    if not verify_refresh_token(refresh_token) or expired_user.refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        expired_user.id, expires_delta=access_token_expires
    )
    new_refresh_token = security.create_refresh_token()

    user_crud.update_refresh_token(
        session=session,
        db_user=expired_user,
        refresh_token=new_refresh_token
    )

    token = Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )
    return token