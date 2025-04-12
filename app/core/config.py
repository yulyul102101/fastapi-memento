import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')

    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY:         str = os.getenv('SECRET_KEY')

    SMTP_HOST:          int = os.getenv('SMTP_HOST')
    SMTP_PORT:          int = os.getenv('SMTP_PORT')
    SMTP_USER:          int = os.getenv('SMTP_USER')
    SMTP_PASSWORD:      int = os.getenv('SMTP_PASSWORD')

    UPLOAD_DIR:         str = os.getenv('UPLOAD_DIR')


settings = Settings()  # type: ignore