from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime


class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    started_at: datetime
    ended_at: Optional[datetime] = None