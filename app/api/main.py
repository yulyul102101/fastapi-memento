from fastapi import APIRouter

from app.api.routes import auth, comment, day, diary, todo, user

api_router = APIRouter(prefix='/api')
api_router.include_router(auth.router)
api_router.include_router(comment.router)
api_router.include_router(day.router)
api_router.include_router(diary.router)
api_router.include_router(todo.router)
api_router.include_router(user.router)