from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    password: str | None = None


class ChatResponse(BaseModel):
    answer: str
    requires_password: bool = False