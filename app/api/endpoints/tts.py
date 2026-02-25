from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.tts_service import tts_service

router = APIRouter()

@router.get("/tts/stream")
async def stream_tts(text: str, language: str):

    audio_stream = tts_service.stream_speech(
        text,
        language
    )

    return StreamingResponse(
        audio_stream.iter_bytes(),
        media_type="audio/mpeg"
    )