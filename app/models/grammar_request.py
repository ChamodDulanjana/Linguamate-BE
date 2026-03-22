from pydantic import BaseModel
from typing import Literal


class GrammarRequest(BaseModel):
    text: str
    input_type: Literal["text", "speech"]
