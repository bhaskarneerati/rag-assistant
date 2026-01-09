from typing import TypedDict, Optional, List


class LogEvent(TypedDict):
    timestamp: str
    component: str
    event: str


class QueryEvent(LogEvent):
    session_id: str
    question: str


class AnswerEvent(LogEvent):
    session_id: str
    sources: List[str]


class IngestionEvent(LogEvent):
    documents: int
    chunks: int