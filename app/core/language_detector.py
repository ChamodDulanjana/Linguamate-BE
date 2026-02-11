import fasttext
from pathlib import Path


class LanguageDetector:
    def __init__(self):
        model_path = Path(__file__).parent.parent / "models" / "lid.176.bin"
        self.model = fasttext.load_model(str(model_path))

    def detect_language(self, text: str) -> dict:
        if not text.strip():
            return {
                "language": "unknown",
                "confidence": 0.0
            }

        prediction = self.model.predict(text, k=1)

        language = prediction[0][0].replace("__label__", "")
        confidence = float(prediction[1][0])

        return {
            "language": language,
            "confidence": round(confidence, 3)
        }

# SINGLETON INSTANCE
language_detector = LanguageDetector()