from fastapi import APIRouter, UploadFile, File, Form
from app.models.activity_request import ActivityRequest
from app.services.activity_generator import ActivityGenerator
from app.services.whisper_service import WhisperService
from app.services.speaking_evaluator import SpeakingEvaluator
from app.services.pronunciation_heatmap import PronunciationHeatmap

router = APIRouter()
activity_generator = ActivityGenerator()
whisper_service = WhisperService()
speaking_evaluator = SpeakingEvaluator()
heatmap_engine = PronunciationHeatmap()

@router.post("/generate-activity")
def generate_activity(request: ActivityRequest):
    return activity_generator.generate(request.learningConcepts, request.activityType, request.language)

@router.post("/speaking/evaluate")
async def evaluate_speaking(
    audio: UploadFile = File(...),
    targetSentence: str = Form(...),
    language: str = Form(...)
):
    # 🔹 Step 1 — Whisper transcription
    transcription = whisper_service.transcribe(audio)
    spoken_text = transcription.text

    # 🔹 Step 2 — Generate heatmap
    heatmap = heatmap_engine.generate(
        targetSentence,
        spoken_text
    )

    # 🔹 Step 3 — Evaluate speaking
    result = speaking_evaluator.evaluate(
        targetSentence,
        spoken_text,
        language
    )

    return {
        "transcript": spoken_text,
        "score": result["score"],
        "isCorrect": result["isCorrect"],
        "feedback": result["feedback"],
        "heatmap": heatmap
    }