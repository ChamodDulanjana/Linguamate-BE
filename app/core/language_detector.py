import fasttext
from pathlib import Path
from app.models.language_detection import LanguageDetectionResult
import os
import urllib.request

MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
MODEL_PATH = "app/models/lid.176.bin"

class LanguageDetector:
    def __init__(self):
        # model_path = Path(__file__).parent.parent / "models" / "lid.176.bin"    
        # self.model = fasttext.load_model(str(model_path))

        if not os.path.exists(MODEL_PATH):
            print("Downloading FastText model...")
            os.makedirs("app/models", exist_ok=True)
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

        self.model = fasttext.load_model(MODEL_PATH)
        print("FastText model loaded successfully")

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