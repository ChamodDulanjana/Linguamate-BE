from fastapi import FastAPI
from app.services.grammar_corrector import GrammarCorrector
from app.models.grammar_request import GrammarRequest
from app.services.grammar_explanator import GrammarExplanator
from app.models.learning_concept_request import LearningConceptRequest
from app.models.activity_request import ActivityRequest
from app.services.activity_generator import ActivityGenerator

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

grammar_corrector = GrammarCorrector()
grammar_explanator = GrammarExplanator()
activity_generator = ActivityGenerator()


@app.get("/")
def root():
    return {"message": "LinguaMate backend is running 🚀"}


@app.post("/grammar-correct")
def grammar_correct(request: GrammarRequest):
    return grammar_corrector.respond(request.text)


@app.post("/grammar-explain")
def grammar_explain(request: LearningConceptRequest):
    return grammar_explanator.respond(request.learningConcepts, request.language)


@app.post("/generate-activity")
def generate_activity(request: ActivityRequest):
    return activity_generator.generate(request.learningConcepts, request.activityType, request.language)
