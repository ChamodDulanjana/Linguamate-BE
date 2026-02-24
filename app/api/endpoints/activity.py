from fastapi import APIRouter
from app.models.activity_request import ActivityRequest
from app.services.activity_generator import ActivityGenerator

router = APIRouter()
activity_generator = ActivityGenerator()

@router.post("/generate-activity")
def generate_activity(request: ActivityRequest):
    return activity_generator.generate(request.learningConcepts, request.activityType, request.language)
