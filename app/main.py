from fastapi import FastAPI
from app.services.language_detector import LanguageDetector
from app.models.text_request import TextRequest
from app.services.grammar_corrector import GrammarCorrector
from app.models.grammar_request import GrammarRequest
from app.services.grammar_explanator import GrammarExplanator
from app.models.learning_concept_request import LearningConceptRequest

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

language_detector = LanguageDetector()
grammar_corrector = GrammarCorrector()
grammar_explanator = GrammarExplanator()


@app.get("/")
def root():
    return {"message": "LinguaMate backend is running 🚀"}


@app.post("/detect-language")
def detect_language(request: TextRequest):
    return language_detector.detect_language(request.text)


@app.post("/grammar-correct")
def grammar_correct(request: GrammarRequest):
    return grammar_corrector.respond(request.text)


@app.post("/grammar-explain")
def grammar_explain(request: LearningConceptRequest):
    return grammar_explanator.respond(request.learningConcept, request.category)
