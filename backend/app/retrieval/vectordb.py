"""
Vector database management module for the RAG Assistant.

This module provides a wrapper around ChromaDB for storing and retrieving
document embeddings. It handles model initialization, document chunking,
idempotent ingestion, and semantic search.
"""
import os
from typing import List, Dict, Any

import chromadb
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.logging.logger import StructuredLogger


class VectorDB:
    """
    A class to interact with a persistent ChromaDB instance.

    This class encapsulates all vector database operations, including:
    - Initializing the local embedding model (sentence-transformers).
    - Managing a persistent collection of document chunks.
    - Handling document ingestion with duplicate prevention.
    - Performing semantic searches to find relevant context for user queries.

    Attributes:
        collection_name (str): The name of the ChromaDB collection.
        persist_path (str): The file path where ChromaDB persists data.
        embedding_model_name (str): The name of the HuggingFace model used for embeddings.
        embeddings (HuggingFaceEmbeddings): The initialized embedding model instance.
        client (chromadb.PersistentClient): The ChromaDB client.
        collection (chromadb.Collection): The active collection object.
        splitter (RecursiveCharacterTextSplitter): Utility for chunking text before indexing.
        logger (StructuredLogger): Logger for tracking DB operations.
    """

    def __init__(self):
        """
        Initializes the VectorDB with configuration from environment variables.

        Sets up the embedding model (using CPU, CUDA, or MPS), initializes the
        persistent ChromaDB client, and prepares the document splitter.
        """
        self.logger = StructuredLogger(component="vectordb")

        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "rag_docs")
        self.persist_path = os.getenv("CHROMA_PATH", "./backend/chroma_db")

        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        self.embedding_model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={"device": device},
        )

        self.client = chromadb.PersistentClient(path=self.persist_path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        self.logger.event(
            "vectordb_initialized",
            collection=self.collection_name,
            device=device,
        )

    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Chunks and inserts multiple documents into the vector database.

        This method is idempotent: it checks for existing chunk IDs before inserting
        to avoid duplicates. It only generates embeddings for new chunks.

        Args:
            documents (List[Dict[str, Any]]): A list of dictionaries, where each dict
                contains 'id' (filename), 'text' (content), and 'metadata'.

        Returns:
            int: The total number of new chunks added to the collection.
        """

        total_chunks_added = 0

        # 1️⃣ Fetch existing IDs once
        existing_ids = set()
        try:
            existing = self.collection.get(include=[])
            existing_ids = set(existing.get("ids", []))
        except Exception:
            # Collection may be empty
            existing_ids = set()

        for doc in documents:
            chunks = self.splitter.split_text(doc["text"])

            ids = [f"{doc['id']}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [doc.get("metadata", {}) for _ in chunks]

            # 2️⃣ Filter only NEW chunks
            new_chunks = []
            new_ids = []
            new_metas = []

            for i, chunk_id in enumerate(ids):
                if chunk_id not in existing_ids:
                    new_chunks.append(chunks[i])
                    new_ids.append(chunk_id)
                    new_metas.append(metadatas[i])

            if not new_chunks:
                continue

            # 3️⃣ Embed only NEW chunks
            embeddings = self.embeddings.embed_documents(new_chunks)

            # 4️⃣ Add to Chroma
            self.collection.add(
                documents=new_chunks,
                embeddings=embeddings,
                metadatas=new_metas,
                ids=new_ids,
            )

            total_chunks_added += len(new_chunks)
            existing_ids.update(new_ids)

        self.logger.event(
            "documents_indexed",
            documents=len(documents),
            chunks_added=total_chunks_added,
        )

        return total_chunks_added

    def search(self, query: str, n_results: int = 3, session_id: str | None = None) -> Dict[str, Any]:
        """
        Performs a semantic search to find the most relevant document chunks.

        Args:
            query (str): The search query (user's question).
            n_results (int): The number of top results to return.
            session_id (str, optional): The session ID for logging.

        Returns:
            Dict[str, Any]: A dictionary containing lists of 'documents',
                            'metadatas', and 'distances' for the top matches.
        """
        self.logger.event(
            "search_initiated",
            session_id=session_id,
            query=query[:100] + ("..." if len(query) > 100 else ""),
        )

        query_embedding = self.embeddings.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        if not results or not results.get("documents"):
            self.logger.event(
                "search_completed",
                session_id=session_id,
                results_count=0,
            )
            return {"documents": [], "metadatas": [], "distances": []}

        self.logger.event(
            "search_completed",
            session_id=session_id,
            results_count=len(results["documents"][0]),
        )

        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0],
        }