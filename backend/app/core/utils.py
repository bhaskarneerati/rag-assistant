def is_greeting(text: str) -> bool:
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
    return "Hello! How can I help you?"