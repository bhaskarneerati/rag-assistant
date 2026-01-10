"""
Standalone CLI script for document ingestion.

This script allows you to manually trigger the RAG engine to process documents
from the 'knowledge_base/raw' directory and index them into ChromaDB without
running the FastAPI server.

Usage:
    python scripts/ingest.py
"""
from app.core.rag_engine import RAGEngine

def main():
    """
    Initializes the RAG engine, performs document ingestion, and prints the results.
    """
    rag = RAGEngine()
    stats = rag.ingest()

    print("Ingestion complete")
    print(f"Documents processed: {stats['documents']}")
    print(f"Chunks created: {stats['chunks']}")

if __name__ == "__main__":
    main()