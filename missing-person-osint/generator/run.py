"""
Main CLI orchestrator for synthetic digital evidence generation.
Usage: python -m generator.run --seed 42 --days 45
"""
from __future__ import annotations
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

from generator.persona import load_case_bible
from generator.accounts import generate_profiles
from generator.photos import generate_photo_catalog
from generator.posts import generate_posts
from generator.connections import generate_connections
from generator.phones import generate_telephony_data
from generator.checkins import generate_checkins

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def generate_all(
    seed: int = 42,
    days: int = 45,
    case_path: Path | None = None,
    output_dir: Path | None = None
) -> Dict[str, Any]:
    project_root = Path(__file__).resolve().parent.parent
    if case_path is None:
        case_path = project_root / "case" / "case_bible.yaml"
    if output_dir is None:
        output_dir = project_root / "data"

    output_dir.mkdir(parents=True, exist_ok=True)
    photos_dir = output_dir / "photos"
    photos_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading case bible from {case_path}...")
    case_data = load_case_bible(case_path)

    logger.info(f"Generating profiles with seed {seed}...")
    profiles = generate_profiles(case_data, seed=seed)
    with open(output_dir / "profiles.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)

    logger.info("Generating photo catalog and injecting EXIF metadata...")
    photo_catalog = generate_photo_catalog(case_data, photos_dir, seed=seed)
    with open(output_dir / "photos_metadata.json", "w", encoding="utf-8") as f:
        json.dump(photo_catalog, f, indent=2)

    logger.info(f"Generating posts over {days} days...")
    posts_df = generate_posts(case_data, photo_catalog, seed=seed, days=days)
    posts_df.to_csv(output_dir / "posts.csv", index=False)

    logger.info("Generating social connections graph...")
    connections_df = generate_connections(profiles, posts_df, seed=seed)
    connections_df.to_csv(output_dir / "connections.csv", index=False)

    logger.info("Generating cellular phones and call records (CDR)...")
    phones_df, cdr_df = generate_telephony_data(case_data, seed=seed, days=days)
    phones_df.to_csv(output_dir / "phones.csv", index=False)
    cdr_df.to_csv(output_dir / "call_records.csv", index=False)

    logger.info("Generating venue check-ins...")
    checkins_df = generate_checkins(case_data, seed=seed, days=days)
    checkins_df.to_csv(output_dir / "checkins.csv", index=False)

    # Generate archive_snapshot.json (containing deleted posts and old cached profile states)
    logger.info("Generating web archive snapshot (including pre-deletion forensic state)...")
    archive_snapshot = {
        "snapshot_id": "WAYBACK-ARCHIVE-2026-03-12",
        "timestamp_utc": "2026-03-12T12:00:00Z",
        "crawler": "FictionalWaybackBot/3.1",
        "cached_deleted_posts": posts_df[posts_df["deleted"] == True].to_dict(orient="records"),
        "historical_handles_detected": ["mayalin_art", "pixel_maya", "m_lin99"]
    }
    with open(output_dir / "archive_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(archive_snapshot, f, indent=2)

    logger.info(f"Successfully generated all synthetic evidence in {output_dir}!")
    return {
        "profiles_count": len(profiles),
        "posts_count": len(posts_df),
        "photos_count": len(photo_catalog),
        "connections_count": len(connections_df),
        "cdrs_count": len(cdr_df),
        "checkins_count": len(checkins_df)
    }

def main():
    parser = argparse.ArgumentParser(description="Deterministic Synthetic OSINT Evidence Generator")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--days", type=int, default=45, help="Number of timeline days to simulate")
    parser.add_argument("--case", type=str, default=None, help="Path to custom case bible yaml")
    parser.add_argument("--output", type=str, default=None, help="Output directory path")

    args = parser.parse_args()
    case_path = Path(args.case) if args.case else None
    output_dir = Path(args.output) if args.output else None

    summary = generate_all(seed=args.seed, days=args.days, case_path=case_path, output_dir=output_dir)
    print("\n--- GENERATION SUMMARY ---")
    for k, v in summary.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
