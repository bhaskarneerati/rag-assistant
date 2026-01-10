"""
LLM provider module for the RAG Assistant.

This module provides a factory function to initialize and return a LangChain
Chat model based on the available environment variables. It supports OpenAI,
Groq, and Google Generative AI (Gemini) as providers.
"""
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    """
    Factory function to create and return an LLM instance.

    The function checks for environment variables in the following order of priority:
    1. OpenAI (OPENAI_API_KEY)
    2. Groq (GROQ_API_KEY)
    3. Google Gemini (GOOGLE_API_KEY)

    It uses the model specified in the corresponding environment variable (e.g., OPENAI_MODEL)
     or a default model if not specified. Temperature is set to 0.0 for consistent results.

    Returns:
        BaseChatModel: A LangChain-compatible chat model instance.

    Raises:
        RuntimeError: If no supported LLM API keys are found in the environment.
    """

    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=model,
            temperature=0.0,
        )

    if os.getenv("GROQ_API_KEY"):
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        return ChatGroq(
            model=model,
            temperature=0.0,
        )

    if os.getenv("GOOGLE_API_KEY"):
        model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        return ChatGoogleGenerativeAI(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            model=model,
            temperature=0.0,
        )


    raise RuntimeError(
        "No LLM API key found. Set OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY."
    )