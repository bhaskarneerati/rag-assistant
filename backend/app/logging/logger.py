"""
Structured logging module for the RAG Assistant.

This module provides a JSON-based structured logger that writes log events
to component-specific files in JSON Lines (.jsonl) format. This is useful
for both debugging and building analytics.
"""
import json
import os
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict


class StructuredLogger:
    """
    A thread-safe logger for writing structured JSON events to disk.

    Each instance of this logger is associated with a specific component and
    writes events to a corresponding .jsonl file in the 'backend/logs' directory.

    Attributes:
        component (str): The name of the component being logged.
        lock (threading.Lock): A lock to ensure thread-safe file writes.
        log_dir (str): The directory where log files are stored.
        log_file (str): The path to the specific log file for this component.
        tz (timezone): The timezone used for timestamps (default is UTC+5:30).
    """

    def __init__(self, component: str):
        """
        Initializes the StructuredLogger for a given component.

        Args:
            component (str): The name of the component (e.g., 'rag_engine', 'api').
        """
        self.component = component
        self.lock = threading.Lock()

        base_dir = os.path.abspath("backend")
        self.log_dir = os.path.join(base_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        self.log_file = os.path.join(
            self.log_dir,
            f"{component}.jsonl",
        )

        self.tz = timezone(timedelta(hours=5, minutes=30))

    def _timestamp(self) -> str:
        """
        Generates an ISO 8601 timestamp with millisecond precision in the local timezone.

        Returns:
            str: The formatted timestamp.
        """
        return datetime.now(self.tz).isoformat(timespec="milliseconds")

    def event(self, event: str, **data: Dict[str, Any]):
        """
        Logs a structured event with optional data.

        The event is formatted as a JSON object containing the timestamp,
        component name, event name, and any additional key-value pairs provided.

        Args:
            event (str): The name of the event being logged.
            **data: Additional key-value pairs to include in the log entry.
        """
        payload = {
            "timestamp": self._timestamp(),
            "component": self.component,
            "event": event,
            **data,
        }

        line = json.dumps(payload, ensure_ascii=False)

        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")