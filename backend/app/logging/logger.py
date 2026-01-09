import json
import os
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict


class StructuredLogger:
    """
    JSON structured logger.
    One file per component, append-only.
    """

    def __init__(self, component: str):
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
        return datetime.now(self.tz).isoformat(timespec="milliseconds")

    def event(self, event: str, **data: Dict[str, Any]):
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