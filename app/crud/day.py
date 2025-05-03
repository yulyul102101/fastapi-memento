import uuid
from datetime import date

from sqlmodel import Session, select

from app.models.day import Day, DayCreate, DayUpdate, DayEmotionPublic


def get_or_create_day(*, session: Session, day_create: DayCreate, user_id: uuid.UUID) -> Day:
    statement = select(Day).where(Day.user_id == user_id, Day.date == day_create.date)
    session_day = session.exec(statement).first()
    if session_day:
        return session_day
    else:
        return create_day(
            session=session,
            day_create=day_create,
            user_id=user_id
            )


def get_day(*, session: Session, day_date: date, user_id: uuid.UUID) -> Day:
    statement = select(Day).where(Day.user_id == user_id, Day.date == day_date)
    session_day = session.exec(statement).first()
    return session_day


def create_day(*, session: Session, day_create: DayCreate, user_id: uuid.UUID) -> Day:
    db_obj = Day.model_validate(
        day_create, update={"user_id": user_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_days_by_user(session: Session, user_id: uuid.UUID) -> list[Day]:
    """
    해당 사용자의 모든 Day를 최신순으로 가져옵니다.
    """
    statement = select(Day).where(Day.user_id == user_id).order_by(Day.date.desc())
    return session.exec(statement).all()


def update_day_by_id(session: Session, day_id: uuid.UUID, update_data: DayUpdate) -> Day:
    """
    day_id로 Day를 찾아 업데이트합니다.
    """
    db_day = session.get(Day, day_id)
    if not db_day:
        raise ValueError("Day not found")

    update_fields = update_data.model_dump(exclude_unset=True)
    db_day.sqlmodel_update(update_fields)

    session.add(db_day)
    session.commit()
    session.refresh(db_day)
    return db_day


def get_day_emotions_by_user(session: Session, user_id: uuid.UUID) -> list[DayEmotionPublic]:
    """
    해당 유저의 모든 Day에 대해 date-emotion 매핑 목록 반환 (트래커용).
    """
    statement = (
        select(Day.date, Day.emotion)
        .where(Day.user_id == user_id)
        .order_by(Day.date.asc())
    )
    results = session.exec(statement).all()

    # 결과를 DayEmotionPublic로 변환
    return [DayEmotionPublic(date=row[0], emotion=row[1]) for row in results]