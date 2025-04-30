import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import GenderEnum, AgeGroupEnum


if TYPE_CHECKING:
    from app.models.day import Day


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, max_length=255, unique=True)
    nickname: str = Field(max_length=100)
    gender: GenderEnum
    age_group: AgeGroupEnum


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    nickname: str = Field(max_length=100)
    gender: GenderEnum
    age_group: AgeGroupEnum


class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    nickname: str | None = Field(default=None, max_length=100)
    gender: GenderEnum | None = None
    age_group: AgeGroupEnum | None = None


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    refresh_token: str | None = None

    days: list["Day"] | None = Relationship(back_populates="user", cascade_delete=True)


class UserPublic(UserBase):
    id: uuid.UUID
