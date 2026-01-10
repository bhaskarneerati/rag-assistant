"""
Text chunking utilities for the RAG Assistant.

This module provides functions to split large text documents into smaller,
overlapping chunks, which is necessary for efficient vector database indexing
and retrieval.
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Splits a long string into smaller chunks using a recursive character strategy.

    This utility uses LangChain's RecursiveCharacterTextSplitter to create chunks
    that maintain semantic continuity by overlapping and splitting at logical
    boundaries like paragraphs or sentences.

    Args:
        text (str): The raw text to be chunked.
        chunk_size (int): The maximum number of characters per chunk.
        chunk_overlap (int): The number of characters that consecutive chunks share.

    Returns:
        List[str]: A list of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)