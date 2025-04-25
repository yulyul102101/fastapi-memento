from uuid import UUID
from datetime import date

from sqlmodel import Session

from app.models.diary import Diary, DiaryCreate, DiaryUpdate
from app.crud import diary as crud_diary
from app.crud.day import get_or_create_day
from app.models.enums import EmotionEnum
from app.utils.file import save_audio_file


def save_diary_draft(   # 임시 저장
    *,
    session: Session,
    user_id: UUID,
    diary_in: DiaryCreate
) -> Diary:
    day = get_or_create_day(session=session, day_create=diary_in.date, user_id=user_id)

    existing_diary = crud_diary.get_diary_by_day_id(session=session, day_id=day.id)

    # 오디오 저장 처리
    if diary_in.audio_file:
        diary_in.audio_path = save_audio_file(diary_in.audio_file, user_id, diary_in.date)

    day.wrote_diary = True

    if existing_diary:
        return crud_diary.update_diary(session=session, diary=existing_diary, diary_in=diary_in)
    else:
        return crud_diary.create_diary(session=session, day_id=day.id, diary_in=diary_in)


def finalize_diary_and_analyze_emotion(
    *,
    session: Session,
    user_id: UUID,
    diary_date: date
) -> Diary:
    day = get_or_create_day(session=session, day_create=diary_date, user_id=user_id)
    diary = crud_diary.get_diary_by_day_id(session=session, day_id=day.id)
    # 임시저장된 diary가 없는 경우도 있으니 라우터에서 save_diary_draft 를 먼저 수행할것

    if not diary:
        raise ValueError("Diary not found")

    # 음성 일기일시 → STT 수행
    if not diary.content and diary.audio_path:
        # TODO STT 수행
        diary.content = "temp"
        session.add(diary)

    # 감정 분석
    if not diary.content:
        raise ValueError("No content available for emotion analysis")

    # TODO 감정 분석 수행
    day.emotion = EmotionEnum.neutral
    day.wrote_diary = True

    session.add(day)
    session.commit()
    session.refresh(diary)

    return diary
