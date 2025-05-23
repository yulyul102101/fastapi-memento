import os
from pathlib import Path

from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')

    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES:    int = 60 * 24 * 7
    # 60 minutes * 24 hours * 30 days = 30 days
    REFRESH_TOKEN_EXPIRE_DAYS:      int = 60 * 24 * 30

    OPENAI_API_KEY:     str = os.getenv('OPENAI_API_KEY')

    SECRET_KEY:         str = os.getenv('SECRET_KEY')

    SMTP_HOST:          str = os.getenv('SMTP_HOST')
    SMTP_PORT:          str = os.getenv('SMTP_PORT')
    SMTP_USER:          str = os.getenv('SMTP_USER')
    SMTP_PASSWORD:      str = os.getenv('SMTP_PASSWORD')

    TOKEN_URL:          str = "/api/auth/login/access-token"

    BASE_DIR:           str = str(Path(__file__).resolve().parent.parent.parent)
    UPLOAD_DIR:         str = os.getenv('UPLOAD_DIR')


settings = Settings()  # type: ignore