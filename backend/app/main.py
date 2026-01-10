"""
Main entry point for the RAG Assistant FastAPI application.

This module initializes the FastAPI app, configures CORS middleware for local development,
and includes the API routers for health checks, chat functionality, and document ingestion.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router

app = FastAPI(
    title="RAG Assistant",
    version="1.0.0",
)

# Local development CORS (widget, demo pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])