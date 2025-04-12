import os
import uuid
from fastapi import UploadFile
from pathlib import Path
from datetime import date

from app.core.config import settings


def save_audio_file(file: UploadFile, user_id: uuid.UUID, diary_date: date) -> str:
    """
    오디오 파일을 저장하고 경로를 반환합니다.
    """
    upload_dir = Path(settings.UPLOAD_DIR) / "audio" / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{diary_date.isoformat()}_{uuid.uuid4().hex}.wav"
    file_path = upload_dir / filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return str(file_path)  # 이 경로를 audio_path로 저장
