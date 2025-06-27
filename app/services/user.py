from sqlmodel import Session, select
from app.models.user import User
from app.models.day import Day
from app.models.todo import Todo


def delete_user_with_dependencies(session: Session, user: User):
    # 1. 사용자에 연결된 Day 객체 모두 조회
    days = session.exec(select(Day).where(Day.user_id == user.id)).all()

    for day in days:
        # 2. Diary 삭제
        if day.diary:
            # Comment 삭제
            if day.diary.comment:
                session.delete(day.diary.comment)
            session.delete(day.diary)

        # 3. Todo 삭제
        todos = session.exec(select(Todo).where(Todo.day_id == day.id)).all()
        for todo in todos:
            session.delete(todo)

        # 4. Day 삭제
        session.delete(day)

    # 5. User 삭제
    session.delete(user)
    session.commit()
