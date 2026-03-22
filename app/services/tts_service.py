from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry


class TTSService:
    def stream_speech(self, text: str, language: str):

        # Language → Voice mapping
        VOICE_MAP = {
            "en": "alloy",
            "es": "verse",
            "fr": "verse",
            "de": "alloy"
        }

        voice = VOICE_MAP.get(language, "alloy")

        audio_stream = call_openai_with_retry(
            lambda: client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
            )
        )

        return audio_stream 

tts_service = TTSService()
