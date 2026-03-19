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

@router.get("/tts/sentence")
async def tts_sentence(text: str, language: str):

    async def audio_stream():
        response = tts_service.stream_speech(
            text,
            language
        )

        for chunk in response.iter_bytes(chunk_size=1024):
            if chunk:
                yield chunk

    return StreamingResponse(
        audio_stream(),
        media_type="audio/mpeg"
    )