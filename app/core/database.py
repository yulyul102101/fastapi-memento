from sqlalchemy import create_engine

from app.core.config import settings

# MySQL(배포시)
# engine = create_engine(
#     settings.SQLALCHEMY_DATABASE_URL,
#     pool_pre_ping=True,  # 연결이 유효한지 사전 확인
#     pool_recycle=3600    # 1시간마다 연결 재활용
# )

# SQLite(개발시)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()