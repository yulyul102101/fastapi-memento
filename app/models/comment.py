import uuid
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.models.diary import Diary


# CommentCreate 시 dait_id path 로 받음
class Comment(SQLModel, table=True):
    __tablename__ = "comment"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    diary_id: uuid.UUID = Field(foreign_key="diary.id", unique=True, ondelete="CASCADE")
    content: str = Field()

    diary: "Diary" = Relationship(back_populates="comment")


class CommentPublic(SQLModel):
    id: uuid.UUID
    diary_id: uuid.UUID
    content: str

    class Config:
        from_attributes = True


class CommentsPublic(SQLModel):
    data: list[CommentPublic]
    count: int