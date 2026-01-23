"""
Core RAG (Retrieval-Augmented Generation) engine for the AI Assistant.

This module encapsulates the main logic for document ingestion, vector search,
and LLM-based answer generation. It acts as the bridge between the retrieval
system (VectorDB) and the generation system (LLM).
"""
import os
import re
from typing import Dict, List

from app.core.llm import get_llm
from app.core.prompts import SYSTEM_PROMPT
from app.retrieval.vectordb import VectorDB
from app.logging.logger import StructuredLogger


def format_for_chat(answer: str) -> str:
    """
    Cleans and formats markdown LLM output for a better user experience in chat UI.

    This function removes excessive markdown headers, converts headers to plain text,
    strips out bold/italic styling, and normalizes bullet points.

    Args:
        answer (str): The raw output from the LLM.

    Returns:
        str: The cleaned and formatted chat message.
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
    Orchestrates the Retrieval-Augmented Generation process.

    This class handles:
    1. Ingesting raw documents into the vector database.
    2. Querying the vector database for relevant context.
    3. Constructing prompts and generating answers using an LLM.
    4. Logging events for monitoring and debugging.
    """

    def __init__(self):
        """
        Initializes the RAGEngine with an LLM instance, a VectorDB instance,
        and a structured logger.
        """
        self.llm = get_llm()
        self.vector_db = VectorDB()
        self.logger = StructuredLogger(component="rag_engine")

    def ingest(self) -> Dict[str, int]:
        """
        Loads local documents and indexes them in the vector database.

        Scans the 'knowledge_base/raw' directory for .txt files, reads their content,
        and adds them to ChromaDB.

        Returns:
            Dict[str, int]: A dictionary with counts of 'documents' and 'chunks' processed.
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
        Processes a user question and returns an AI-generated answer based on retrieved context.

        This method performs the following steps:
        1. Logs the query event.
        2. Searches the vector database for context relevant to the question.
        3. If no context is found, returns a standard "not found" message.
        4. If context is found, formats a prompt and invokes the LLM.
        5. Formats the LLM output and extracts source information.
        6. Logs the completion event and returns the result.

        Args:
            question (str): The user's question.
            session_id (str): The ID of the current session for logging.

        Returns:
            Dict[str, List[str]]: A dictionary containing the 'answer' and a list of 'sources'.
        """
        self.logger.event(
            "query_received",
            session_id=session_id,
            question=question,
        )

        results = self.vector_db.search(question)
        if not results["documents"]:
            return {
                "answer": "I'm sorry, I couldn't find any information regarding that in the provided documents. Feel free to ask something else!",
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