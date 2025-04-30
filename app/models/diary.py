import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Relationship

# if TYPE_CHECKING:
from app.models.day import Day, DayPublic
from app.models.comment import Comment, CommentPublic


class DiaryBase(SQLModel):
    date: date
    content: str | None = None
    audio_path: str | None = Field(default=None)


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(DiaryBase):
    pass


class Diary(DiaryBase, table=True):
    __tablename__ = "diary"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    day_id: uuid.UUID = Field(foreign_key="day.id", unique=True, ondelete="CASCADE")

    day: "Day" = Relationship(back_populates="diary")
    comment: Optional["Comment"] = Relationship(back_populates="diary")


class DiaryPublic(DiaryBase):
    id: uuid.UUID
    day_id: uuid.UUID
    day: "DayPublic"
    comment: Optional["CommentPublic"] = None

    class Config:
        from_attributes = True


class DiariesPublic(SQLModel):
    data: list[DiaryPublic]
    count: int


DiaryPublic.model_rebuild()
DiariesPublic.model_rebuild()