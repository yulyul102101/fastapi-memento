from uuid import UUID

from fastapi import UploadFile
from sqlmodel import Session

from app.crud.comment import create_comment
from app.models.day import DayCreate
from app.models.diary import Diary, DiaryCreate, DiaryUpdate
from app.crud import diary as diary_crud
from app.crud import day as day_crud
from app.utils.file import save_audio_file


def save_diary_draft(   # 임시 저장
    *,
    session: Session,
    user_id: UUID,
    diary_day: DayCreate,
    content: str | None = None,
    audio_file: UploadFile | None = None
) -> Diary:
    day = day_crud.get_or_create_day(
        session=session,
        day_create=diary_day,
        user_id=user_id,
    )

    diary_in = DiaryCreate(
        date=diary_day.date,
    )

    existing_diary = diary_crud.get_diary_by_day_id(session=session, day_id=day.id)

    # 오디오 저장 처리
    if audio_file:
        diary_in.audio_path = save_audio_file(audio_file, user_id, diary_in.date)
    else:
        diary_in.content = content

    day.wrote_diary = True

    if existing_diary:
        return diary_crud.update_diary(session=session, diary=existing_diary, diary_in=diary_in)
    else:
        return diary_crud.create_diary(session=session, day_id=day.id, diary_in=diary_in)


def finalize_diary_and_analyze_emotion(
    *,
    session: Session,
    user_id: UUID,
    diary_day: DayCreate,
) -> Diary:
    day = day_crud.get_or_create_day(session=session, day_create=diary_day, user_id=user_id)
    diary = diary_crud.get_diary_by_day_id(session=session, day_id=day.id)
    # 임시저장된 diary가 없는 경우도 있으니 라우터에서 save_diary_draft 를 먼저 수행할것

    if not diary:
        raise ValueError("Diary not found")

    # 음성 일기일시 → STT 수행
    if not diary.content and diary.audio_path:
        # stt 수행
        from app.services.ai.speech_to_text import stt
        content = stt.transcribe_audio(diary.audio_path)
        diary.content = content
        session.add(diary)

    if not diary.content:
        raise ValueError("No content available for emotion analysis")

    # 감정 분석
    from app.services.ai.emotion_detection import sa
    emotion, _ = sa.analyze_emotion(diary.content)
    day.emotion = emotion
    day.wrote_diary = True

    from app.services.ai.comment_generator import comment_generator
    content = comment_generator.requestAdvice(str(emotion), diary.content)
    comment = create_comment(session=session, diary_id=diary.id, content=content)

    diary.comment = comment

    session.add(day)
    session.commit()
    session.refresh(diary)

    return diary
