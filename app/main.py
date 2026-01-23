from fastapi import FastAPI
from app.services.language_detector import LanguageDetector
from app.models.text_request import TextRequest

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

language_detector = LanguageDetector()


@app.get("/")
def root():
    return {"message": "LinguaMate backend is running 🚀"}


@app.post("/detect-language")
def detect_language(request: TextRequest):
    return language_detector.detect_language(request.text)
