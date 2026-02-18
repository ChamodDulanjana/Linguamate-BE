import fasttext
from pathlib import Path
from app.models.language_detection import LanguageDetectionResult


class LanguageDetector:
    def __init__(self):
        model_path = Path(__file__).parent.parent / "models" / "lid.176.bin"
        self.model = fasttext.load_model(str(model_path))

    def detect_language(self, text: str) -> LanguageDetectionResult:
        cleaned = text.strip().lower()

        if not cleaned:
            return LanguageDetectionResult(
                language="unknown",
                confidence=0.0
            )

        # Greeting fallback
        COMMON_GREETINGS = {"hi", "hello", "hey", "yo", "sup"}
        
        if cleaned in COMMON_GREETINGS:
            return LanguageDetectionResult(
                language="en",
                confidence=1.0
            )

        # Short text fallback
        if len(cleaned) <= 3:
            return LanguageDetectionResult(
                language="en",
                confidence=0.0
            )

        prediction = self.model.predict(cleaned, k=1)

        language = prediction[0][0].replace("__label__", "")
        confidence = float(prediction[1][0])

        return LanguageDetectionResult(
            language=language,
            confidence=round(confidence, 3)
        )

# SINGLETON INSTANCE
language_detector = LanguageDetector()