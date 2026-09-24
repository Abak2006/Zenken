"""
Tests for Synthetic Generator determinism and data schema validation.
"""
import pytest
from pathlib import Path
from generator.persona import load_case_bible
from generator.accounts import generate_profiles
from generator.posts import generate_posts
from generator.run import generate_all

def test_case_bible_loads():
    case_data = load_case_bible()
    assert "missing_person" in case_data
    assert case_data["missing_person"]["full_name"] == "Maya Lin"
    assert len(case_data["digital_identities"]) >= 4
    assert len(case_data["associates"]) >= 12
    assert len(case_data["venues"]) >= 8

def test_generator_determinism():
    case_data = load_case_bible()
    # Profiles determinism
    p1 = generate_profiles(case_data, seed=42)
    p2 = generate_profiles(case_data, seed=42)
    p3 = generate_profiles(case_data, seed=99)

    assert p1 == p2, "Generator with same seed must produce identical profiles"
    assert p1 != p3, "Generator with different seeds should produce variations"

def test_photos_generation(tmp_path):
    from generator.photos import generate_photo_catalog
    case_data = load_case_bible()
    photos_dir = tmp_path / "photos"
    catalog = generate_photo_catalog(case_data, photos_dir, seed=42)
    
    assert len(catalog) >= 10
    # Verify image files exist on disk
    for ph in catalog:
        img_file = photos_dir / ph["filename"]
        assert img_file.exists()
        assert img_file.stat().st_size > 0
        assert "phash" in ph
