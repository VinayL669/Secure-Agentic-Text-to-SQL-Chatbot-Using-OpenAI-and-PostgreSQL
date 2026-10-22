import uuid

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=500)


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sql: str | None = None
    facts: dict


def new_conversation_id() -> str:
    return str(uuid.uuid4())