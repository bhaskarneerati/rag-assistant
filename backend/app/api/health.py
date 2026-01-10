"""
Health check module for the RAG Assistant API.

This module provides a simple endpoint to verify that the API service is running
and responsive.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary containing the status and service name.
    """
    return {
        "status": "ok",
        "service": "rag-assistant"
    }