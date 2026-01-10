"""
Utility functions for the RAG Assistant.

This module provides helper functions for common tasks, such as identifying
and responding to greetings, which helps reduce unnecessary LLM calls.
"""

def is_greeting(text: str) -> bool:
    """
    Checks if the provided text is a common greeting or short polite phrase.

    Args:
        text (str): The input text to check.

    Returns:
        bool: True if the text is a greeting, False otherwise.
    """
    if not text:
        return False

    normalized = text.strip().lower()

    greetings = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "ok",
        "okay"
    }

    return normalized in greetings

def greeting_response() -> str:
    """
    Returns a standard greeting response.

    Returns:
        str: A friendly greeting string.
    """
    return "Hello! How can I help you?"