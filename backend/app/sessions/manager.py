import uuid
from typing import Optional

from app.logging.logger import StructuredLogger


class SessionManager:
    """
    Stateless session manager.
    Session ID is generated client-side or via header.
    """

    def __init__(self):
        self.logger = StructuredLogger(component="session_manager")

    def get_session_id(
        self,
        provided_session_id: Optional[str],
        force_new: bool = False,
    ) -> str:
        if force_new or not provided_session_id:
            session_id = str(uuid.uuid4())
            self.logger.event(
                "new_session",
                session_id=session_id,
            )
            return session_id

        return provided_session_id