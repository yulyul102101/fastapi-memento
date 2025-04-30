import uuid
from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep, CurrentUser
from app.models.todo import (
    TodoCreate,
    TodoUpdate,
    TodoPublic,
    TodosPublic
)
from app.crud import todo as todo_crud
from app.services import todo as todo_service

router = APIRouter(prefix="/todo", tags=["todo"])


@router.post("/", response_model=TodoPublic)
def create_todo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    todo_in: TodoCreate,
) -> Any:
    """
    Create a new todo and update Day's total_todo.
    """
    todo = todo_service.create_todo_with_day_update(session=session, todo_in=todo_in, user_id=current_user.id)
    return todo


@router.get("/", response_model=TodosPublic)
def read_todos_by_date(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    date: date = Query(),
) -> Any:
    """
    Read todos for a specific date.
    """
    todos = todo_crud.get_todos_by_user_and_date(session=session, day_date=date, user_id=current_user.id)
    return TodosPublic(data=todos, count=len(todos))


@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    todo_id: uuid.UUID,
    todo_in: TodoUpdate,
) -> Any:
    """
    Update a todo and adjust Day's completed_todo if needed.
    """
    db_todo = todo_crud.get_todo_by_id(session=session, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = todo_service.update_todo_with_day_update(
        session=session,
        db_todo=db_todo,
        todo_in=todo_in,
        user_id=current_user.id
    )
    return updated_todo


@router.delete("/{todo_id}")
def delete_todo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    todo_id: uuid.UUID,
) -> Any:
    """
    Delete a todo and update Day's total_todo.
    """
    db_todo = todo_crud.get_todo_by_id(session=session, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_service.delete_todo_with_day_update(session=session, db_todo=db_todo, user_id=current_user.id)
    return {"message": "Todo deleted successfully"}