"""
Unit tests for pipeline evaluation against isolated ground_truth.json.
"""
import pytest
from evaluation.evaluate import evaluate_pipeline

def test_pipeline_evaluation_metrics():
    eval_res = evaluate_pipeline()
    assert "metrics" in eval_res
    metrics = eval_res["metrics"]

    # Check Entity resolution metrics
    er = metrics["entity_resolution"]
    assert er["precision"] >= 0.70
    assert er["recall"] >= 0.80
    assert er["f1_score"] >= 0.75
    assert er["target_persona_cluster_accuracy"] == 1.0

    # Check LKL distance error (Whispering Pines sector hit)
    lkl = metrics["last_known_location"]
    assert lkl["distance_error_meters"] < 2000.0  # Within 2km sector

    # Check Red Herring traps avoided
    rh = metrics["red_herring_audit"]
    assert rh["traps_followed_count"] == 0
