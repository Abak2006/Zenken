"""
Confidence score computation and evidential rationale builder.
Combines multiple independent pieces of OSINT evidence using probabilistic belief combination.
"""
from __future__ import annotations
from typing import List, Dict, Any, Tuple

def compute_combined_confidence(evidence_pieces: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    Combines independent evidence scores using probabilistic noisy-OR:
    Confidence = 1 - PRODUCT(1 - w_i)
    Returns normalized confidence [0.0, 1.0] and an evidentiary audit explanation.
    """
    if not evidence_pieces:
        return 0.0, "No corroborating evidence detected."

    unbelief = 1.0
    explanations = []

    for item in evidence_pieces:
        weight = float(item.get("weight", 0.0))
        weight = max(0.0, min(1.0, weight))
        unbelief *= (1.0 - weight)
        explanations.append(f"{item.get('type')}: {item.get('detail')} (w={weight:.2f})")

    combined_score = round(1.0 - unbelief, 4)
    explanation_str = " | ".join(explanations)
    return combined_score, explanation_str
