"""
Unit tests for confidence scoring and entity resolution.
"""
import pytest
from correlation.confidence import compute_combined_confidence
from correlation.entity_resolution import resolve_entities

def test_confidence_combination():
    evidence = [
        {"type": "EXACT_EMAIL", "detail": "Match", "weight": 0.95},
        {"type": "BIO_MATCH", "detail": "Match", "weight": 0.50}
    ]
    conf, rationale = compute_combined_confidence(evidence)
    # Probabilistic noisy-OR: 1 - (1 - 0.95) * (1 - 0.50) = 1 - 0.05 * 0.5 = 1 - 0.025 = 0.975
    assert conf > 0.97
    assert "EXACT_EMAIL" in rationale
    assert "BIO_MATCH" in rationale

def test_entity_resolution_clusters():
    res = resolve_entities()
    assert res["resolved_clusters_count"] > 0
    assert res["confirmed_links_count"] >= 4

    # Verify Maya Lin's cluster
    maya_cluster = next((c for c in res["clusters"] if "mayalin_art" in c["accounts"]), None)
    assert maya_cluster is not None
    assert "m_lin99" in maya_cluster["accounts"]
    assert "pixel_maya" in maya_cluster["accounts"]
    assert "m.shadow_7" in maya_cluster["accounts"]
    assert len(maya_cluster["accounts"]) == 4
