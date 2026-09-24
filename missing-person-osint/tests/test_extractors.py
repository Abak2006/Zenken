"""
Unit tests for EXIF extraction, Time Normalization, and NLP Entity/Sentiment extraction.
"""
from pathlib import Path
import pytest
from extractors.time_normalizer import normalize_timestamp
from extractors.exif_extractor import extract_image_forensics
from extractors.nlp_extractor import extract_entities_and_topics, analyze_sentiment

def test_time_normalizer_pst():
    res = normalize_timestamp("2026-03-01 14:00:00 PST")
    assert res["valid"] is True
    # 14:00 PST is 22:00 UTC
    assert res["iso_utc"] == "2026-03-01T22:00:00Z"
    assert res["detected_tz"] == "PST"

def test_time_normalizer_epoch():
    res = normalize_timestamp("1772402400") # Sample epoch
    assert res["valid"] is True
    assert res["iso_utc"] is not None
    assert res["epoch_sec"] == 1772402400

def test_nlp_extraction():
    sample_text = "Urgent meeting with @kaelen_v at Pacific Horizon Diner on Friday to finalize secret contract."
    res = extract_entities_and_topics(sample_text)
    assert "kaelen_v" in res["mentions"]
    assert "rendezvous_plans" in res["matched_topics"]
    assert "geographic_clues" in res["matched_topics"]

def test_sentiment_scoring():
    score_pos, label_pos = analyze_sentiment("Stunning photography and pure serenity at the sunset ridge!")
    assert score_pos > 0.0
    assert label_pos == "positive"

    score_fear, label_fear = analyze_sentiment("I feel strangely watched and my anxiety is through the roof.")
    assert score_fear < 0.0
    assert "fear" in label_fear.lower() or "anxiety" in label_fear.lower()

def test_exif_extraction(tmp_path):
    # Test on generated sample photo
    data_dir = Path(__file__).resolve().parent.parent / "data"
    photo_file = data_dir / "photos" / "PH-001.jpg"
    if photo_file.exists():
        forensics = extract_image_forensics(photo_file)
        assert forensics["valid"] is True
        assert forensics["has_exif"] is True
        assert forensics["camera_make"] == "Sony"
        assert forensics["camera_model"] == "ILCE-7M4"
        assert forensics["latitude"] is not None
        assert forensics["longitude"] is not None
