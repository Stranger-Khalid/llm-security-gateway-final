import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from app.utils.preprocessing import preprocess_text
from app.detectors.rule_detector import detect_rule_attacks
from app.detectors.semantic_detector import detect_semantic_attack
from app.pii.presido_engine import detect_pii
from app.policy.policy_engine import make_decision


# --------------------------------
# Load Dataset
# --------------------------------

df = pd.read_csv(
    "data/final_eval.csv"
)


# --------------------------------
# Store Results
# --------------------------------

predictions = []

ground_truth = []

results = []


# --------------------------------
# Run Evaluation
# --------------------------------

for _, row in df.iterrows():

    prompt = row["prompt"]

    expected = row["expected_policy"]

    processed_text = preprocess_text(
        prompt
    )

    # Rule Detection
    rule_result = detect_rule_attacks(
        processed_text
    )

    # Semantic Detection
    semantic_result = detect_semantic_attack(
        processed_text
    )

    # PII Detection
    pii_entities = detect_pii(
        prompt
    )

    # Final Decision
    decision = make_decision(
        rule_result["rule_score"],
        semantic_result["semantic_score"],
        pii_entities
    )

    predictions.append(decision)

    ground_truth.append(expected)

    results.append({

        "prompt": prompt,

        "expected": expected,

        "predicted": decision,

        "rule_score":
            rule_result["rule_score"],

        "semantic_score":
            semantic_result["semantic_score"]
    })


# --------------------------------
# Metrics
# --------------------------------

accuracy = accuracy_score(
    ground_truth,
    predictions
)

precision = precision_score(
    ground_truth,
    predictions,
    average="weighted"
)

recall = recall_score(
    ground_truth,
    predictions,
    average="weighted"
)

f1 = f1_score(
    ground_truth,
    predictions,
    average="weighted"
)


# --------------------------------
# Print Metrics
# --------------------------------

print("\n========== EVALUATION ==========\n")

print(f"Accuracy : {accuracy:.2f}")

print(f"Precision: {precision:.2f}")

print(f"Recall   : {recall:.2f}")

print(f"F1-Score : {f1:.2f}")

print("\nClassification Report:\n")

print(
    classification_report(
        ground_truth,
        predictions
    )
)


# --------------------------------
# Save Results CSV
# --------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/evaluation_results.csv",
    index=False
)

print(
    "\nResults saved to:"
)

print(
    "results/evaluation_results.csv"
)