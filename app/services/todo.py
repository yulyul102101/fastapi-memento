import uuid
from typing import Any

from sqlmodel import Session

from app.crud.day import get_or_create_day, get_day
from app.crud.todo import create_todo, update_todo
from app.models.todo import TodoCreate, Todo, TodoUpdate


def create_todo_with_day_update(*,
        session: Session, todo_in: TodoCreate, user_id: uuid.UUID,
) -> Todo:
    day = get_or_create_day(session=session, day_create=todo_in.date, user_id=user_id)

    todo = create_todo(session=session, todo_create=todo_in, day_id=day.id)

    # Day의 상태 반영
    day.total_todo += 1
    session.add(day)
    session.commit()
    return todo


def update_todo_with_day_update(*,
        session: Session, db_todo: Todo, todo_in: TodoUpdate, user_id: uuid.UUID,
) -> Todo:
    day = get_day(session=session, day_date=db_todo.date, user_id=user_id)

    previous_done = db_todo.is_done

    todo = update_todo(session=session, db_todo=db_todo, todo_in=todo_in)

    if "is_done" in todo_in:
        # 완료 → 미완료
        if previous_done is True and todo.is_done is False:
            day.completed_todo = max(0, day.completed_todo - 1)
        # 미완료 → 완료
        elif previous_done is False and todo.is_done is True:
            day.completed_todo += 1

        session.add(day)

    session.commit()
    return todo


def delete_todo_with_day_update(*,
        session: Session, db_todo: Todo, user_id: uuid.UUID,
) -> Any:
    day = get_day(session=session, day_date=db_todo.date, user_id=user_id)

    session.delete(db_todo)

    # Day의 상태 반영
    day.total_todo = max(0, day.completed_todo - 1)
    session.add(day)
    session.commit()
    return None