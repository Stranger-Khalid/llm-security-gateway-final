import time

from fastapi import FastAPI
from pydantic import BaseModel

from app.utils.preprocessing import preprocess_text
from app.utils.language import detect_language
from app.utils.logging_utils import save_audit_log

from app.detectors.rule_detector import detect_rule_attacks
from app.detectors.semantic_detector import detect_semantic_attack

from app.pii.presido_engine import (
    detect_pii,
    anonymize_pii
)

from app.policy.policy_engine import make_decision


app = FastAPI(
    title="LLM Security Gateway",
    version="1.0"
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def home():

    return {
        "message": "LLM Security Gateway Running"
    }


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):

    start_time = time.time()

    original_text = request.prompt

    # -----------------------------
    # Preprocessing
    # -----------------------------

    processed_text = preprocess_text(
        original_text
    )

    # -----------------------------
    # Language Detection
    # -----------------------------

    language = detect_language(
        original_text
    )

    # -----------------------------
    # Rule-Based Detection
    # -----------------------------

    rule_result = detect_rule_attacks(
        processed_text
    )

    # -----------------------------
    # Semantic Detection
    # -----------------------------

    semantic_result = detect_semantic_attack(
        processed_text
    )

    # -----------------------------
    # PII Detection
    # -----------------------------

    pii_entities = detect_pii(
        original_text
    )

    safe_text = anonymize_pii(
        original_text
    )

    # -----------------------------
    # Policy Decision
    # -----------------------------

    decision = make_decision(
        rule_result["rule_score"],
        semantic_result["semantic_score"],
        pii_entities
    )

    # -----------------------------
    # Reason Codes
    # -----------------------------

    reason_codes = []

    if rule_result["rule_score"] >= 0.5:
        reason_codes.append(
            "RULE_BASED_ATTACK"
        )

    if semantic_result["semantic_score"] >= 0.5:
        reason_codes.append(
            "SEMANTIC_ATTACK"
        )

    if len(pii_entities) > 0:
        reason_codes.append(
            "PII_DETECTED"
        )

    # -----------------------------
    # Latency
    # -----------------------------

    latency_ms = round(
        (time.time() - start_time) * 1000,
        2
    )

    # -----------------------------
    # Audit Logging
    # -----------------------------

    save_audit_log({

        "original_text": original_text,

        "processed_text": processed_text,

        "language": language,

        "rule_score": rule_result["rule_score"],

        "semantic_score": semantic_result["semantic_score"],

        "decision": decision,

        "reason_codes": reason_codes,

        "latency_ms": latency_ms
    })

    # -----------------------------
    # Final JSON Response
    # -----------------------------

    return {

        "original_text": original_text,

        "processed_text": processed_text,

        "language": language,

        "rule_score": rule_result["rule_score"],

        "semantic_score": semantic_result["semantic_score"],

        "closest_attack": semantic_result["closest_attack"],

        "matched_categories": rule_result["matched_categories"],

        "pii_entities": pii_entities,

        "safe_text": safe_text,

        "decision": decision,

        "reason_codes": reason_codes,

        "latency_ms": latency_ms
    }