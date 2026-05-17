from presidio_analyzer import AnalyzerEngine
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern

from presidio_anonymizer import AnonymizerEngine


# -----------------------------
# Analyzer & Anonymizer
# -----------------------------

analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()


# -----------------------------
# Custom CNIC Recognizer
# -----------------------------

cnic_pattern = Pattern(
    name="cnic_pattern",
    regex=r"\b\d{5}-\d{7}-\d\b",
    score=0.85
)

cnic_recognizer = PatternRecognizer(
    supported_entity="CNIC",
    patterns=[cnic_pattern]
)

analyzer.registry.add_recognizer(
    cnic_recognizer
)


# -----------------------------
# Student ID Recognizer
# -----------------------------

student_pattern = Pattern(
    name="student_pattern",
    regex=r"\bFA\d{2}-[A-Z]{3}-\d{3}\b",
    score=0.80
)

student_recognizer = PatternRecognizer(
    supported_entity="STUDENT_ID",
    patterns=[student_pattern]
)

analyzer.registry.add_recognizer(
    student_recognizer
)


# -----------------------------
# Analyze PII
# -----------------------------

def detect_pii(text: str):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    entities = []

    for result in results:

        # Ignore weak detections
        if result.score < 0.5:
            continue

        entities.append({

            "type": result.entity_type,

            "text": text[result.start:result.end],

            "score": round(result.score, 2)
        })

    return entities

# -----------------------------
# Mask PII
# -----------------------------

def anonymize_pii(text: str):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return anonymized_result.text