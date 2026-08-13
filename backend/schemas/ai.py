from pydantic import BaseModel


class AIChatRequest(BaseModel):

    # User ka question
    question: str


class AIChatResponse(BaseModel):

    success: bool

    intent: str

    response: dict