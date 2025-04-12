from uuid import UUID
from sqlmodel import Session, select

from app.models.comment import Comment


def get_comment_by_diary_id(session: Session, diary_id: UUID) -> Comment | None:
    """
    특정 일기에 연결된 코멘트를 가져옵니다.
    """
    statement = select(Comment).where(Comment.diary_id == diary_id)
    return session.exec(statement).first()


def create_comment(session: Session, diary_id: UUID, content: str) -> Comment:
    """
    새로운 코멘트를 생성합니다.
    """
    comment = Comment(diary_id=diary_id, content=content)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment