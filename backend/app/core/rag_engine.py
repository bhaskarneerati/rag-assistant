import os
import re
from typing import Dict, List

from app.core.llm import get_llm
from app.core.prompts import SYSTEM_PROMPT
from app.retrieval.vectordb import VectorDB
from app.logging.logger import StructuredLogger


def format_for_chat(answer: str) -> str:
    """
    Convert markdown-style LLM output into
    clean chat-friendly text.
    """

    if not answer:
        return ""

    lines = answer.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        # Skip empty markdown headers
        if re.match(r"^#+\s*$", line):
            continue

        # Convert headers to sentence case
        line = re.sub(r"^#{1,6}\s*", "", line)

        # Remove bold / italics
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"\*(.*?)\*", r"\1", line)

        # Bullet points
        if line.startswith("- ") or line.startswith("* "):
            cleaned.append(f"• {line[2:].strip()}")
        else:
            cleaned.append(line)

    # Remove excessive empty lines
    final_lines = []
    for line in cleaned:
        if line or (final_lines and final_lines[-1]):
            final_lines.append(line)

    return "\n".join(final_lines).strip()


class RAGEngine:
    """
    Core RAG logic.
    - No FastAPI imports
    - No session logic
    - Pure retrieval + generation
    """

    def __init__(self):
        self.llm = get_llm()
        self.vector_db = VectorDB()
        self.logger = StructuredLogger(component="rag_engine")

    def ingest(self) -> Dict[str, int]:
        """
        Load documents from knowledge_base/raw and index them.
        """
        base_path = "knowledge_base/raw"
        documents = []

        for filename in os.listdir(base_path):
            if filename.endswith(".txt"):
                path = os.path.join(base_path, filename)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        documents.append(
                            {
                                "id": filename,
                                "text": text,
                                "metadata": {"source": filename},
                            }
                        )

        chunks = self.vector_db.add_documents(documents)
        documents_count = len(documents),

        self.logger.event(
            "ingestion_complete",
            documents=len(documents),
            chunks=chunks,
        )

        return {"documents": len(documents), "chunks": chunks}

    def query(self, question: str, session_id: str) -> Dict[str, List[str]]:
        """
        Query vector DB + LLM.
        """
        self.logger.event(
            "query_received",
            session_id=session_id,
            question=question,
        )

        results = self.vector_db.search(question)

        if not results["documents"]:
            return {
                "answer": "I'm sorry, that information is not in this document.",
                "sources": [],
            }

        context = "\n\n".join(results["documents"])

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )

        response = self.llm.invoke(prompt)

        raw_answer = response.content.strip()
        answer = format_for_chat(raw_answer)
        sources = list(
            {meta["source"] for meta in results["metadatas"]}
        )

        self.logger.event(
            "query_answered",
            session_id=session_id,
            sources=sources,
        )

        return {"answer": answer, "sources": sources}