"""
Logging schemas for the RAG Assistant.

This module defines the TypedDict structures used by the structured logger
to ensure consistent event formatting across different components.
"""
from typing import TypedDict, Optional, List


class LogEvent(TypedDict):
    """
    Base structure for all logged events.

    Attributes:
        timestamp (str): ISO 8601 formatted timestamp.
        component (str): The name of the component that generated the log.
        event (str): The name or type of the event.
    """
    timestamp: str
    component: str
    event: str


class QueryEvent(LogEvent):
    """
    Structure for user query events.

    Attributes:
        session_id (str): The ID of the session where the query occurred.
        question (str): The user's input question.
    """
    session_id: str
    question: str


class AnswerEvent(LogEvent):
    """
    Structure for AI answer response events.

    Attributes:
        session_id (str): The ID of the session where the answer was generated.
        sources (List[str]): The document sources cited in the answer.
    """
    session_id: str
    sources: List[str]


class IngestionEvent(LogEvent):
    """
    Structure for document ingestion events.

    Attributes:
        documents (int): The number of documents processed.
        chunks (int): The number of vector chunks created.
    """
    documents: int
    chunks: int