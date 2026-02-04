from pydantic import BaseModel


class LearningConceptRequest(BaseModel):
    learningConcepts: list[str]