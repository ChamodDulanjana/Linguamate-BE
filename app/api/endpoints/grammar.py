from fastapi import APIRouter
from app.models.grammar_request import GrammarRequest
from app.models.learning_concept_request import LearningConceptRequest
from app.services.grammar_corrector import GrammarCorrector
from app.services.grammar_explanator import GrammarExplanator

router = APIRouter()
grammar_corrector = GrammarCorrector()
grammar_explanator = GrammarExplanator()

@router.post("/grammar-correct")
def grammar_correct(request: GrammarRequest):
    return grammar_corrector.respond(request.text, request.input_type)

@router.post("/learning-concept-explain")
def grammar_explain(request: LearningConceptRequest):
    return grammar_explanator.respond(request.learningConcepts, request.language)
