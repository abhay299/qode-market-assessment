import re

URL_PATTERN = re.compile(r"http\S+|www\.\S+")


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove URLs
    text = URL_PATTERN.sub("", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Lowercase (keep Unicode/emojis intact)
    text = text.lower().strip()

    return text
