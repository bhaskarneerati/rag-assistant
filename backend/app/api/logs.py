"""
Logs API module for the RAG Assistant.

This module provides endpoints to retrieve chat session history and detailed
debugging logs by reading structured log files from disk.
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException

router = APIRouter()

LOGS_DIR = os.path.abspath("backend/logs")

def get_all_logs() -> List[Dict[str, Any]]:
    """Reads all .jsonl files in the logs directory and returns a sorted list of entries."""
    all_entries = []
    if not os.path.exists(LOGS_DIR):
        return []
    
    for filename in os.listdir(LOGS_DIR):
        if filename.endswith(".jsonl"):
            path = os.path.join(LOGS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        all_entries.append(entry)
                    except json.JSONDecodeError:
                        continue
    
    # Sort by timestamp
    all_entries.sort(key=lambda x: x.get("timestamp", ""))
    return all_entries

@router.get("/sessions")
def list_sessions():
    """
    Returns a list of unique session IDs with their start time and last activity.
    """
    logs = get_all_logs()
    sessions = {}
    
    for entry in logs:
        sid = entry.get("session_id")
        if not sid:
            continue
            
        ts = entry.get("timestamp")
        if sid not in sessions:
            sessions[sid] = {
                "session_id": sid,
                "start_time": ts,
                "last_activity": ts,
                "event_count": 1
            }
        else:
            sessions[sid]["last_activity"] = ts
            sessions[sid]["event_count"] += 1
            
    # Convert to list and sort by last activity (newest first)
    result = list(sessions.values())
    result.sort(key=lambda x: x["last_activity"], reverse=True)
    return result

@router.get("/sessions/{session_id}")
def get_session_details(session_id: str):
    """
    Returns all log entries associated with a specific session ID.
    This includes both chat history and internal debugging events.
    """
    logs = get_all_logs()
    session_logs = [e for e in logs if e.get("session_id") == session_id]
    
    if not session_logs:
        # Check if it was a "new_session" event which might have session_id in a different field
        # or if we should just return empty
        pass

    return {
        "session_id": session_id,
        "logs": session_logs
    }
