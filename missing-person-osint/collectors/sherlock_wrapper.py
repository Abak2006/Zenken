"""
Sherlock OSINT Username Enumeration Wrapper.
ETHICAL SAFEGUARD:
Real-platform username searches on live sites are disabled by default.
Fictional usernames queried against real platforms risk false positives matching real people.
Provides a mock mode generating realistic enumeration records from the synthetic case universe.
"""
from __future__ import annotations
import argparse
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from collectors.chain_of_custody import ChainOfCustody

logger = logging.getLogger(__name__)

ETHICAL_WARNING = """
================================================================================
[!] ETHICAL AND LEGAL OSINT SAFEGUARD WARNING:
Querying public social networks for fictional usernames is STRICTLY DISABLED
by default. Any matching accounts on live production platforms belong to real,
unrelated human individuals.
Mock mode is enabled by default to evaluate synthetic identity correlation safely.
================================================================================
"""

# Synthetic platform lookup directory simulating Sherlock outputs
SYNTHETIC_PLATFORMS = [
    "InstaPhoto", "ChirpNet", "PortfolioHub", "WhisperWire", "DevCode",
    "SoundPulse", "ArtStationSynth", "GitRepoSim", "MetroChat"
]

def run_sherlock(
    username: str,
    mock_mode: bool = True,
    output_path: Optional[Path] = None,
    custody_ledger: Optional[ChainOfCustody] = None
) -> Dict[str, Any]:
    """
    Executes username lookup. In mock mode, maps handles to simulated platform hits.
    """
    if not mock_mode:
        print(ETHICAL_WARNING)
        logger.warning("Live Sherlock invocation requested! Ensure you have explicit authorization.")
        # Attempt running real sherlock if installed
        try:
            cmd = ["sherlock", username, "--timeout", "5", "--print-found"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            results = {"username": username, "mode": "live", "raw_output": res.stdout}
        except Exception as e:
            logger.error(f"Live Sherlock execution failed: {e}. Falling back to mock mode.")
            mock_mode = True

    if mock_mode:
        # Load local profiles to determine synthetic presence
        profiles_file = Path(__file__).resolve().parent.parent / "data" / "profiles.json"
        known_handles = {}
        if profiles_file.exists():
            with open(profiles_file, "r", encoding="utf-8") as f:
                profs = json.load(f)
                for p in profs:
                    known_handles[p["handle"].lower()] = p

        matched_platforms = []
        u_lower = username.lower()

        if u_lower in known_handles:
            primary_plat = known_handles[u_lower].get("platform", "InstaPhoto")
            matched_platforms.append({
                "platform": primary_plat,
                "url": f"http://127.0.0.1:5005/u/{username}",
                "status": "CLAIMED",
                "http_status": 200,
                "response_time_ms": 42
            })
            # Add secondary hits for aliases
            if u_lower in ["mayalin_art", "m_lin99"]:
                matched_platforms.append({
                    "platform": "PortfolioHub",
                    "url": f"http://127.0.0.1:5005/u/pixel_maya",
                    "status": "CROSS_REFERENCED",
                    "http_status": 200,
                    "response_time_ms": 55
                })
        else:
            # Handle not in case bible
            matched_platforms.append({
                "platform": "UnknownPlatform",
                "url": f"http://127.0.0.1:5005/u/{username}",
                "status": "AVAILABLE",
                "http_status": 404,
                "response_time_ms": 30
            })

        results = {
            "username": username,
            "mode": "mock_synthetic",
            "total_sites_checked": len(SYNTHETIC_PLATFORMS),
            "found_count": len([m for m in matched_platforms if m["status"] in ["CLAIMED", "CROSS_REFERENCED"]]),
            "claims": matched_platforms
        }

    # Record chain of custody
    custody = custody_ledger or ChainOfCustody()
    content_str = json.dumps(results, indent=2)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content_str)

    custody.record_artifact(
        artifact_id=f"ART-SHERLOCK-{username}",
        source=f"sherlock://local_mock/{username}",
        content_type="application/json",
        raw_data=content_str,
        collector_name="SherlockWrapper/2.0",
        metadata={"username": username, "mode": results["mode"]}
    )

    return results

def main():
    parser = argparse.ArgumentParser(description="Sherlock OSINT Wrapper with Ethics Safeguard")
    parser.add_argument("username", type=str, help="Username handle to investigate")
    parser.add_argument("--live", action="store_true", help="Opt-in to live querying (CAUTION: Real people warning)")
    parser.add_argument("--output", type=str, default=None, help="Output JSON path")
    args = parser.parse_args()

    out_path = Path(args.output) if args.output else Path(__file__).resolve().parent.parent / "data" / f"sherlock_{args.username}.json"
    res = run_sherlock(args.username, mock_mode=not args.live, output_path=out_path)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
