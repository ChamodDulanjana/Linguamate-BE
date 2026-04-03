from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.tts_service import tts_service
from app.models.voice_type import VoiceType

router = APIRouter()

@router.get("/tts/stream")
async def stream_tts(text: str, language: str, voice_type: VoiceType):

    audio_stream = tts_service.stream_speech(
        text,
        language,
        voice_type.value
    )

    return StreamingResponse(
        audio_stream.iter_bytes(),
        media_type="audio/mpeg"
    )

@router.get("/tts/sentence")
async def tts_sentence(text: str, language: str, voice_type: VoiceType):

    async def audio_stream():
        response = tts_service.stream_speech(
            text,
            language,
            voice_type.value
        )

        for chunk in response.iter_bytes(chunk_size=1024):
            if chunk:
                yield chunk

    return StreamingResponse(
        audio_stream(),
        media_type="audio/mpeg"
    )