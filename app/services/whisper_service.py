from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry
from fastapi import UploadFile


class WhisperService:
    def transcribe(self, audio: UploadFile):

        audio.file.seek(0)

        transcription = call_openai_with_retry(
            lambda: client.audio.transcriptions.create(
                model="whisper-1",
                file=(audio.filename, audio.file, audio.content_type),
                response_format="verbose_json"
            )
        )

        return transcription
