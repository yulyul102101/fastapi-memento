import os
import uuid

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from app.models.diary import Diary, DiaryCreate, DiaryUpdate, DiaryBase


def get_diary_by_day_id(*, session: Session, day_id: uuid.UUID) -> Diary | None:
    statement = (
        select(Diary)
        .options(
            selectinload(Diary.day),
            selectinload(Diary.comment)
        )
        .where(Diary.day_id == day_id)
    )
    diary = session.exec(statement).first()
    return diary


def create_diary(
        *,
        session: Session,
        day_id: uuid.UUID,
        diary_in: DiaryBase
) -> Diary:
    diary = Diary.model_validate(diary_in, update={"day_id": day_id})
    session.add(diary)
    session.commit()
    session.refresh(diary)
    return diary


def update_diary(
        *,
        session: Session,
        diary: Diary,
        diary_in: DiaryBase
) -> Diary:
    # TODO 새 audio_file이 있으면 기존 diary의 audio_file 삭재
    update_data = diary_in.model_dump(exclude_unset=True)
    diary.sqlmodel_update(update_data)
    session.add(diary)
    session.commit()
    session.refresh(diary)
    return diary


def delete_diary(*, session: Session, diary: Diary) -> None:    # 안씀
    session.delete(diary)
    session.commit()


def get_diaries_by_user(*, session: Session, user_id: uuid.UUID) -> list[Diary]:
    from app.models.day import Day

    statement = (
        select(Diary)
        .join(Day)
        .options(
            selectinload(Diary.day),
            selectinload(Diary.comment)
        )
        .where(Day.user_id == user_id)
        .order_by(Day.date.desc())
    )
    diaries = session.exec(statement).all()
    return diaries
