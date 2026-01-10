"""
Request models for the RAG Assistant API.

This module defines the Pydantic models used to validate the structure of
incoming requests to the chat and ingestion endpoints.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Data model for a user's chat request.

    Attributes:
        question (str): The question asked by the user, which must be at least
                        one character long.
    """
    question: str = Field(
        ...,
        min_length=1,
        description="User question to the RAG assistant",
        examples=["What is this document about?"],
    )