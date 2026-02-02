from pydantic import BaseModel


class LearningConceptRequest(BaseModel):
    learningConcept: str
    category: str