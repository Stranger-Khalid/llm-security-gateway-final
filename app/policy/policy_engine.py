def make_decision(
        rule_score: float,
        semantic_score: float,
        pii_entities: list
):

    risk_score = max(
        rule_score,
        semantic_score
    )

    # Dangerous attack
    if risk_score >= 0.5:
        return "BLOCK"

    # Safe but contains PII
    if len(pii_entities) > 0:
        return "MASK"

    return "ALLOW"