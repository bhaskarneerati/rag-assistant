"""
Offline ingestion script.

Usage:
python scripts/ingest.py
"""

from app.core.rag_engine import RAGEngine

def main():
    rag = RAGEngine()
    stats = rag.ingest()

    print("Ingestion complete")
    print(f"Documents processed: {stats['documents']}")
    print(f"Chunks created: {stats['chunks']}")

if __name__ == "__main__":
    main()