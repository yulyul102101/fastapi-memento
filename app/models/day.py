import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.models.enums import EmotionEnum
from app.models.todo import TodoPublic


if TYPE_CHECKING:
    from app.models.diary import Diary
    from app.models.todo import Todo, TodoPublic
    from app.models.user import User


class DayBase(SQLModel):
    date: date
    wrote_diary: bool = False
    mark_diary_written: bool = False
    emotion: EmotionEnum | None = None
    total_todo: int = 0
    completed_todo: int = 0


class DayCreate(DayBase):
    date: date


class DayUpdate(SQLModel):  # id는 따로 받음
    emotion: EmotionEnum | None
    mark_diary_written: bool | None


class Day(DayBase, table=True):
    __tablename__ = "day"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")

    user: "User" = Relationship(back_populates="days")
    todos: list["Todo"] | None = Relationship(back_populates="day")
    diary: Optional["Diary"] = Relationship(back_populates="day")


class DayPublic(DayBase):
    id: uuid.UUID
    todos: list[TodoPublic]


class DaysPublic(SQLModel):
    data: list[DayPublic]
    count: int


class DayEmotionPublic(SQLModel):
    date: date
    emotion: EmotionEnum | None


class DayEmotionsPublic(SQLModel):  # 트래커용
    data: list[DayEmotionPublic]
    count: int