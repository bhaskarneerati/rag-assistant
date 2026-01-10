"""
Chat API module for the RAG Assistant.

This module defines the main chat endpoint that handles user questions,
manages session state, and interacts with the RAG engine to generate answers.
"""
from fastapi import APIRouter, Header, HTTPException

from app.core import utils
from app.core.rag_engine import RAGEngine
from app.sessions.manager import SessionManager
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse

router = APIRouter()

rag_engine = RAGEngine()
session_manager = SessionManager()


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    x_session_id: str | None = Header(default=None),
    x_new_session: bool = Header(default=False),
):
    """
    Main chat endpoint that processes user questions and returns AI-generated responses.

    This function performs the following steps:
    1. Validates the input question.
    2. Manages the user session (either reusing an existing one or creating a new one).
    3. Checks if the question is a simple greeting and provides a predefined response if so.
    4. Delegates the retrieval and generation logic to the RAG engine.
    5. Returns the generated answer along with session information and source citations.

    Args:
        request (ChatRequest): The request body containing the user's question.
        x_session_id (str, optional): The session ID provided in the request headers.
        x_new_session (bool, optional): A flag to force the creation of a new session.

    Returns:
        ChatResponse: The response containing the generated answer, session ID, and sources.

    Raises:
        HTTPException: If the question is empty or if an error occurs during processing.
    """

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    session_id = session_manager.get_session_id(
        provided_session_id=x_session_id,
        force_new=x_new_session,
    )

    if utils.is_greeting(request.question,):
        return {"answer": utils.greeting_response(),"session_id": session_id}

    result = rag_engine.query(
        question=request.question,
        session_id=session_id,
    )

    return ChatResponse(
        session_id=session_id,
        answer=result["answer"],
        sources=result["sources"],
    )   