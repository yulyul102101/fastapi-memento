from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router


app = FastAPI()
app.include_router(api_router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{file_path:path}")
def get_diary_audio_file(file_path: str):
    """
    주어진 파일 경로로 오디오 파일 반환
    예: /api/audio/uploads/audio/abc123/sound.wav
    """
    import os
    from app.core.config import settings
    full_path = os.path.join(settings.BASE_DIR, file_path)

    from fastapi import HTTPException
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    from starlette.responses import FileResponse
    return FileResponse(
        path=full_path,
        media_type="audio/wav",
        filename=os.path.basename(full_path)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        reload=True,
        host="0.0.0.0",
        port=7777   # 임시 TODO 수정하기
    )