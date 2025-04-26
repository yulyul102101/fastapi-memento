from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.crud.diary import get_diaries_by_user, get_diary_by_day_id
from app.models.diary import (
    DiaryCreate,
    DiaryPublic,
    DiariesPublic
)
from app.services.diary import save_diary_draft, finalize_diary_and_analyze_emotion


router = APIRouter(prefix="/diary", tags=["diary"])


@router.post("/", response_model=DiaryPublic)
def create_or_update_diary(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    diary_in: DiaryCreate,
) -> DiaryPublic:
    """
    Create or update a diary draft.
    """
    diary = save_diary_draft(session=session, user_id=current_user.id, diary_in=diary_in)
    return diary


@router.get("/", response_model=DiariesPublic)
def read_user_diaries(
    *,
    session: SessionDep,
    current_user: CurrentUser,
) -> DiariesPublic:
    """
    Get all diaries written by the user.
    """
    diaries = get_diaries_by_user(session=session, user_id=current_user.id)
    return DiariesPublic(data=diaries, count=len(diaries))


@router.get("/{day_id}", response_model=DiaryPublic)
def read_diary_by_day(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    day_id: UUID,
) -> DiaryPublic:
    """
    Get a diary by its day ID.
    """
    diary = get_diary_by_day_id(session=session, day_id=day_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.post("/finalize", response_model=DiaryPublic)
def finalize_diary(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    diary_in: DiaryCreate,
) -> DiaryPublic:
    """
    Finalize a diary:
    - Perform speech-to-text if audio only.
    - Analyze emotion.
    - Generate a comment.
    - Mark day as completed.
    """
    diary = save_diary_draft(session=session, user_id=current_user.id, diary_in=diary_in)
    diary = finalize_diary_and_analyze_emotion(
        session=session,
        user_id=current_user.id,
        diary_date=diary_in.date,
    )
    return diary