from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import EmailStr

from app.api.deps import SessionDep, CurrentUser
from app.core.security import verify_password, get_password_hash
from app.crud import user as user_crud
from app.services import user as user_service
from app.models.common import Message
from app.models.user import (
    UserPublic,
    UserRegister,
    UserCreate,
    UserUpdate,
    UpdatePassword
)
from app.services import verification as verification_service
from app.utils.email import send_verification_email

router = APIRouter(prefix="/user", tags=["user"])


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdate, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = user_crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    user_service.delete_user_with_dependencies(session=session, user=current_user)
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = user_crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = user_crud.create_user(session=session, user_create=user_create)
    return user


@router.post("/send-code")
async def send_email_code(email: EmailStr):
    """
    email로 인증코드를 전송합니다.
    """
    code = verification_service.generate_code()
    await verification_service.store_code(email, code)
    await send_verification_email(email, code)
    return {"message": "Verification code sent"}


@router.post("/verify-code")
async def verify_email_code(email: EmailStr, code: str):
    """
    입력한 인증코드가 유효한지 확인합니다.
    """
    is_valid = await verification_service.validate_code(email, code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"verified": True}