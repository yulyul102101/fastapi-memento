import os
from typing import Annotated
from datetime import date

from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from starlette.responses import FileResponse

from app.api.deps import SessionDep, CurrentUser
from app.core.config import settings
from app.crud import day as day_crud
from app.crud import diary as diary_crud
from app.models.day import DayCreate
from app.models.diary import (
    DiaryCreate,
    DiaryPublic,
    DiariesPublic
)
from app.services import diary as diary_service


router = APIRouter(prefix="/diary", tags=["diary"])


@router.post("/", response_model=DiaryPublic)
def create_or_update_diary(
    *,
    session:        SessionDep,
    current_user:   CurrentUser,
    diary_date:     Annotated[date, Form()],
    content:        Annotated[str | None, Form()] = None,
    audio_file:     Annotated[UploadFile | None, File()] = None
) -> DiaryPublic:
    """
    Create or update a diary draft.
    diary_in의 content, audio_path 는 None으로 고정
    """
    diary = diary_service.save_diary_draft(
                session=session,
                user_id=current_user.id,
                diary_day=DayCreate(
                    date=diary_date,
                ),
                content=content,
                audio_file=audio_file,
            )
    return diary


@router.get("/", response_model=DiariesPublic)
def read_user_diaries(
    *,
    session:        SessionDep,
    current_user:   CurrentUser,
) -> DiariesPublic:
    """
    Get all diaries written by the user.
    """
    diaries = diary_crud.get_diaries_by_user(session=session, user_id=current_user.id)
    return DiariesPublic(data=diaries, count=len(diaries))


@router.get("/{day_date}", response_model=DiaryPublic)
def read_diary_by_day(
    *,
    session:        SessionDep,
    current_user:   CurrentUser,
    day_date:       date,
) -> DiaryPublic:
    """
    Get a diary by its day ID.
    """
    day = day_crud.get_or_create_day(
        session=session,
        day_create=DayCreate(date=day_date),
        user_id=current_user.id
    )
    diary = diary_crud.get_diary_by_day_id(session=session, day_id=day.id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.post("/finalize", response_model=DiaryPublic)
def finalize_diary(
    *,
    session:        SessionDep,
    current_user:   CurrentUser,
    diary_date:     Annotated[date, Form()],
    content:        Annotated[str | None, Form()] = None,
    audio_file:     Annotated[UploadFile | None, File()] = None
) -> DiaryPublic:
    """
    Finalize a diary:
    - Perform speech-to-text if audio only.
    - Analyze emotion.
    - Generate a comment.
    - Mark day as completed.
    """
    diary = diary_service.save_diary_draft(
        session=session,
        user_id=current_user.id,
        diary_day=DayCreate(
            date=diary_date,
        ),
        content=content,
        audio_file=audio_file,
    )
    diary = diary_service.finalize_diary_and_analyze_emotion(
        session=session,
        user_id=current_user.id,
        diary_day=DayCreate(
            date=diary_date,
        ),
    )
    return diary


@router.get("/file/{diary_id}")
def get_audio_by_diary_id(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    diary_id: str
):
    """
    diary_id에 해당하는 Diary의 오디오 파일 반환.
    """
    diary = diary_crud.get_diary_by_id(session=session, diary_id=diary_id)

    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if not diary.audio_path:
        raise HTTPException(status_code=404, detail="No audio file associated with this diary")

    full_path = os.path.join(settings.BASE_DIR, diary.audio_path)

    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        path=full_path,
        media_type="audio/wav",
        filename=os.path.basename(full_path)
    )