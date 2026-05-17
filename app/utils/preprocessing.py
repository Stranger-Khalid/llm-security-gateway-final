import re


LEETSPEAK_MAP = {
    "@": "a",
    "$": "s",
    "!": "i"
}


def normalize_leetspeak(text: str):

    for key, value in LEETSPEAK_MAP.items():
        text = text.replace(key, value)

    return text


def preprocess_text(text: str):

    # lowercase
    text = text.lower()

    # normalize light obfuscation
    text = normalize_leetspeak(text)

    # remove special punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text