import uuid
from datetime import date

from sqlmodel import Session, select

from app.models.todo import TodoCreate, Todo, TodoUpdate


def get_todo_by_id(session: Session, todo_id: uuid.UUID) -> Todo | None:
    """
    주어진 todo_id로 Todo 객체를 조회합니다.
    """
    return session.get(Todo, todo_id)


def create_todo(*,
    session: Session, todo_create: TodoCreate, day_id: uuid.UUID,
) -> Todo:
    db_obj = Todo.model_validate(
        todo_create, update={"day_id": day_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_todo(*,
    session: Session, db_todo: Todo, todo_in: TodoUpdate
) -> Todo:
    todo_data = todo_in.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_todos_by_user_and_date(*,
    session: Session, day_date: date, user_id: uuid.UUID,
) -> list[Todo]:
    from app.models.day import Day
    day_statement = select(Day).where(Day.user_id == user_id, Day.date == day_date)
    day = session.exec(day_statement).first()

    if not day:
        return []

    todo_statement = select(Todo).where(Todo.day_id == day.id)
    todos = session.exec(todo_statement).all()

    return todos