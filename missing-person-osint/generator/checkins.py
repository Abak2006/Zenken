"""
Generates synthetic geo-location check-in events across social media platforms.
"""
from __future__ import annotations
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
import pandas as pd

def generate_checkins(
    case_data: Dict[str, Any],
    seed: int = 42,
    days: int = 45
) -> pd.DataFrame:
    random.seed(seed)
    base_date = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)
    venues = {v["id"]: v for v in case_data.get("venues", [])}

    checkins: List[Dict[str, Any]] = []
    chk_idx = 501

    # Routine Checkins for Maya (Days 1 to 30)
    routine_venues = ["venue_01", "venue_02", "venue_03", "venue_04"]
    for day in range(1, 31):
        if random.random() < 0.7:
            v_id = random.choice(routine_venues)
            v = venues[v_id]
            dt = base_date + timedelta(days=day, hours=random.randint(8, 19), minutes=random.randint(0, 50))
            # Slightly jitter coordinates within 30 meters for realism
            lat_jitter = v["latitude"] + random.uniform(-0.0002, 0.0002)
            lon_jitter = v["longitude"] + random.uniform(-0.0002, 0.0002)
            checkins.append({
                "checkin_id": f"CHK-{chk_idx:04d}",
                "account": "mayalin_art" if random.random() < 0.75 else "m_lin99",
                "venue_id": v_id,
                "venue_name": v["name"],
                "timestamp_utc": dt.isoformat(),
                "latitude": round(lat_jitter, 6),
                "longitude": round(lon_jitter, 6),
                "platform": "InstaPhoto"
            })
            chk_idx += 1

    # Final Days Checkins:
    # Day 42 - Pacific Horizon Diner
    v_diner = venues["venue_06"]
    dt_diner = base_date + timedelta(days=42, hours=16, minutes=30)
    checkins.append({
        "checkin_id": f"CHK-{chk_idx:04d}",
        "account": "mayalin_art",
        "venue_id": "venue_06",
        "venue_name": v_diner["name"],
        "timestamp_utc": dt_diner.isoformat(),
        "latitude": v_diner["latitude"],
        "longitude": v_diner["longitude"],
        "platform": "InstaPhoto"
    })
    chk_idx += 1

    # Day 44 - Pacific Horizon Diner afternoon meeting
    dt_diner2 = base_date + timedelta(days=44, hours=17, minutes=15)
    checkins.append({
        "checkin_id": f"CHK-{chk_idx:04d}",
        "account": "m.shadow_7",
        "venue_id": "venue_06",
        "venue_name": v_diner["name"],
        "timestamp_utc": dt_diner2.isoformat(),
        "latitude": v_diner["latitude"],
        "longitude": v_diner["longitude"],
        "platform": "WhisperWire"
    })
    chk_idx += 1

    # Day 44 - Final check-in at Whispering Pines Overlook
    v_pines = venues["venue_05"]
    dt_pines = base_date + timedelta(days=44, hours=21, minutes=5)
    checkins.append({
        "checkin_id": f"CHK-{chk_idx:04d}",
        "account": "m.shadow_7",
        "venue_id": "venue_05",
        "venue_name": v_pines["name"],
        "timestamp_utc": dt_pines.isoformat(),
        "latitude": v_pines["latitude"],
        "longitude": v_pines["longitude"],
        "platform": "WhisperWire"
    })
    chk_idx += 1

    # Red Herring: Lucas Reed check-in at SFO Marriott
    v_sfo = venues["venue_09"]
    dt_sfo = base_date + timedelta(days=44, hours=18, minutes=50)
    checkins.append({
        "checkin_id": f"CHK-{chk_idx:04d}",
        "account": "lucas_r_sound",
        "venue_id": "venue_09",
        "venue_name": v_sfo["name"],
        "timestamp_utc": dt_sfo.isoformat(),
        "latitude": v_sfo["latitude"],
        "longitude": v_sfo["longitude"],
        "platform": "ChirpNet"
    })

    df = pd.DataFrame(checkins).sort_values(by="timestamp_utc").reset_index(drop=True)
    return df
