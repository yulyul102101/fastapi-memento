import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.models.day import Day


class TodoBase(SQLModel):
    content: str
    is_done: bool = False


class TodoCreate(TodoBase):
    date: date


class TodoUpdate(SQLModel):
    content: str | None
    is_done: bool | None


class Todo(TodoBase, table=True):
    __tablename__ = "todo"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    day_id: uuid.UUID = Field(foreign_key="day.id", ondelete="CASCADE")

    day: "Day" = Relationship(back_populates="todos")


class TodoPublic(TodoBase):
    id: uuid.UUID
    day_id: uuid.UUID

    class Config:
        from_attributes = True


class TodosPublic(SQLModel):
    data: list[TodoPublic]
    count: int