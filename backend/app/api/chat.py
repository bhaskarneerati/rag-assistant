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
    Main chat endpoint for the RAG assistant.
    - x-session-id: existing session id (optional)
    - x-new-session: true => force new session (on refresh)
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