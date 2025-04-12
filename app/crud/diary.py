import uuid

from sqlmodel import Session, select
from app.models.diary import Diary, DiaryCreate, DiaryUpdate


def get_diary_by_day_id(*, session: Session, day_id: uuid.UUID) -> Diary | None:
    statement = select(Diary).where(Diary.day_id == day_id)
    session_day = session.exec(statement).first()
    return session_day


def create_diary(*, session: Session, day_id: uuid.UUID, diary_in: DiaryCreate) -> Diary:
    diary = Diary.model_validate(diary_in, update={"day_id": day_id})
    session.add(diary)
    session.commit()
    session.refresh(diary)
    return diary


def update_diary(*, session: Session, diary: Diary, diary_in: DiaryUpdate) -> Diary:
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
        .where(Day.user_id == user_id)
        .order_by(Day.date.desc())  # 최신순 정렬 (선택)
    )
    diaries = session.exec(statement).all()
    return diaries
