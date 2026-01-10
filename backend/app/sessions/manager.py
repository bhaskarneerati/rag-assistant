"""
Session management module for the RAG Assistant.

This module provides a SessionManager class to handle the creation and
retrieval of chat session identifiers.
"""
import uuid
from typing import Optional

from app.logging.logger import StructuredLogger


class SessionManager:
    """
    A service class for managing chat sessions.

    Currently, this manager is stateless and focuses on generating or
    validating session IDs. In the future, it can be extended to store
    session data in a database or cache.

    Attributes:
        logger (StructuredLogger): Logger for tracking session life cycles.
    """

    def __init__(self):
        """
        Initializes the SessionManager with a structured logger.
        """
        self.logger = StructuredLogger(component="session_manager")

    def get_session_id(
        self,
        provided_session_id: Optional[str],
        force_new: bool = False,
    ) -> str:
        """
        Retrieves an existing session ID or generates a new one.

        This method follows these rules:
        1. If 'force_new' is True, a new UUID is generated.
        2. If 'provided_session_id' is None or empty, a new UUID is generated.
        3. Otherwise, the 'provided_session_id' is returned.

        Args:
            provided_session_id (Optional[str]): The session ID provided in the request.
            force_new (bool): Whether to ignore the provided ID and create a new session.

        Returns:
            str: A valid session ID.
        """
        if force_new or not provided_session_id:
            session_id = str(uuid.uuid4())
            self.logger.event(
                "new_session",
                session_id=session_id,
            )
            return session_id

        return provided_session_id