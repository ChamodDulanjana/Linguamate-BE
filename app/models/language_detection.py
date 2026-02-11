from pydantic import BaseModel

class LanguageDetectionResult(BaseModel):
    language: str
    confidence: float
