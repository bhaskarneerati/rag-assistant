"""
Document ingestion module for the RAG Assistant API.

This module provides endpoints to trigger the ingestion process, which reads
raw documents from the knowledge base and indexes them into the vector database.
"""
from fastapi import APIRouter, HTTPException

from app.core.rag_engine import RAGEngine

router = APIRouter()
rag_engine = RAGEngine()


@router.post("/")
def ingest_documents():
    """
    Ingest documents from the raw knowledge base into the vector database.

    This endpoint triggers the RAG engine to scan the 'knowledge_base/raw' directory,
    process any new or existing text files, chunk them, and store their embeddings
    in the ChromaDB vector database.

    Returns:
        dict: A summary of the ingestion process, including the number of documents
              processed and chunks created.

    Raises:
        HTTPException: If any error occurs during the ingestion process.
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