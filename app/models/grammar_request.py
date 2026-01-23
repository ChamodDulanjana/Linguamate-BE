from pydantic import BaseModel


class GrammarRequest(BaseModel):
    text: str
