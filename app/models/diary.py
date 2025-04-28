from __future__ import annotations
import uuid
from datetime import date

from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Relationship


class DiaryBase(SQLModel):
    content: str | None = None
    audio_path: str | None = Field(default=None)


class DiaryCreate(DiaryBase):
    date: date
    audio_file: UploadFile | None = Field(default=None)


class DiaryUpdate(DiaryBase):
    audio_file: UploadFile | None = Field(default=None)


class Diary(DiaryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    day_id: uuid.UUID = Field(foreign_key="day.id", unique=True, ondelete="CASCADE")

    day: day.Day = Relationship(back_populates="diary")
    comment: comment.Comment | None = Relationship(back_populates="diary")


class DiaryPublic(DiaryBase):
    id: uuid.UUID
    day_id: uuid.UUID

    class Config:
        from_attributes = True


class DiariesPublic(SQLModel):
    data: list[DiaryPublic]
    count: int