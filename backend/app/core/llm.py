import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    """
    LLM factory.
    Selects provider based on available environment variables.
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