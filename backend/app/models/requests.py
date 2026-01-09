from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question to the RAG assistant",
        examples=["What is this document about?"],
    )