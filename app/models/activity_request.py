from typing import Literal
from pydantic import BaseModel


class ActivityRequest(BaseModel):
    learningConcepts: list[str]
    activityType: Literal["QUIZ", "FILL_IN_THE_BLANKS", "SPEAKING_PRACTICE"]