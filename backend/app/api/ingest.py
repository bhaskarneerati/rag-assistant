from fastapi import APIRouter, HTTPException

from app.core.rag_engine import RAGEngine

router = APIRouter()
rag_engine = RAGEngine()


@router.post("/")
def ingest_documents():
    """
    Ingest documents from knowledge_base/raw into the vector database.
    Intended to be triggered manually or during setup.
    """
    try:
        stats = rag_engine.ingest()
        return {
            "status": "success",
            "documents_processed": stats["documents"],
            "chunks_created": stats["chunks"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))