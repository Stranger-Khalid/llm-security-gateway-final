import re

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"forget earlier rules",
    r"disregard previous directions",
]

SYSTEM_PROMPT_PATTERNS = [
    r"reveal system prompt",
    r"show hidden configuration",
    r"print hidden instructions",
]

JAILBREAK_PATTERNS = [
    r"pretend you are unrestricted",
    r"bypass safety",
    r"act as a hacker",
]

SECRET_EXTRACTION_PATTERNS = [
    r"print api keys",
    r"show passwords",
    r"reveal tokens",
]


def detect_rule_attacks(text: str):

    matched_categories = []

    score = 0.0

    categories = {
        "PROMPT_INJECTION": PROMPT_INJECTION_PATTERNS,
        "SYSTEM_PROMPT_EXTRACTION": SYSTEM_PROMPT_PATTERNS,
        "JAILBREAK": JAILBREAK_PATTERNS,
        "SECRET_EXTRACTION": SECRET_EXTRACTION_PATTERNS
    }

    for category, patterns in categories.items():

        for pattern in patterns:

            if re.search(pattern, text):

                matched_categories.append(category)

                score += 0.25

                break

    score = min(score, 1.0)

    return {
        "rule_score": score,
        "matched_categories": matched_categories
    }