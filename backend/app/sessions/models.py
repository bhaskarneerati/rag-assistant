"""
Session-related data models for the RAG Assistant.

This module defines the Pydantic models used to track chat history and
manage session metadata.
"""
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class ChatMessage(BaseModel):
    """
    Data model for a single message in a chat session.

    Attributes:
        role (str): The role of the message author ("user" or "assistant").
        content (str): The text content of the message.
        timestamp (datetime): The time when the message was sent.
    """
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime


class ChatSession(BaseModel):
    """
    Data model for a complete chat session.

    Attributes:
        session_id (str): The unique identifier for the session.
        messages (List[ChatMessage]): The sequence of messages in the session.
        started_at (datetime): The time when the session was created.
        ended_at (Optional[datetime]): The time when the session was closed (if applicable).
    """
    session_id: str
    messages: List[ChatMessage]
    started_at: datetime
    ended_at: Optional[datetime] = None