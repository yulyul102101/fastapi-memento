from datetime import date

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.models.day import DaysPublic, DayPublic, DayUpdate, Day, DayCreate
from app.crud import day as day_crud

router = APIRouter(prefix="/day", tags=["day"])


@router.get("/", response_model=DaysPublic)
def read_days(
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    해당 사용자의 모든 Day를 최신순으로 가져옵니다.
    """
    days = day_crud.get_days_by_user(session, user_id=current_user.id)
    return DaysPublic(data=days, count=len(days))


@router.get("/{day_date}", response_model=DayPublic)
def read_day(
    day_date: date,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    해당 사용자의 특정 날짜의 Day를 가져옵니다. (Todo list 포함)
    """
    db_day = day_crud.get_day(session=session, day_date=day_date, user_id=current_user.id)
    if not db_day:
        raise HTTPException(status_code=404, detail="Day not found")
    return db_day


@router.patch("/{day_date}", response_model=DayPublic)
def update_day(
    day_date: date,
    day_update: DayUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    """
    해당 사용자의 특정 Day를 수정합니다.
    - 해당 Day의 감정
    - 해당 Day에 일기를 썼다고 표시할건지
    """
    db_day = day_crud.get_or_create_day(
        session=session,
        day_create=DayCreate(
            date=day_date,
        ),
        user_id=current_user.id)
    if not db_day or db_day.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Day not found or not authorized")

    updated_day = day_crud.update_day_by_id(session=session, day_id=db_day.id, update_data=day_update)
    return updated_day