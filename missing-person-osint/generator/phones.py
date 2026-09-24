"""
Generates synthetic telecommunications evidence:
- phones.csv: Handset and subscriber registration records.
- call_records.csv: Call Detail Records (CDR) with duration and cell tower sector coordinates.
"""
from __future__ import annotations
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
import pandas as pd

def generate_telephony_data(
    case_data: Dict[str, Any],
    seed: int = 42,
    days: int = 45
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    random.seed(seed)
    base_date = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)

    # 1. Phone Registry (phones.csv)
    phones = [
        {
            "phone_number": "+1-555-0144",
            "registered_owner": "Maya Lin",
            "account_link_hint": "mayalin_art, m_lin99",
            "carrier": "Pacific Cellular Synthetic",
            "plan_type": "Postpaid Unlimited",
            "status": "Inactive - Ceased Traffic 2026-03-10",
            "first_seen": "2023-09-01",
            "last_seen": "2026-03-10T08:14:00Z"
        },
        {
            "phone_number": "+1-555-0199",
            "registered_owner": "Prepaid Cash Customer (Anonymous)",
            "account_link_hint": "m.shadow_7",
            "carrier": "Metro Synthetic Prepaid",
            "plan_type": "Prepaid 30-Day SIM",
            "status": "Active until 2026-03-14T21:45:00Z (Handset Off)",
            "first_seen": "2026-03-10T11:00:00Z",
            "last_seen": "2026-03-14T21:45:00Z"
        },
        {
            "phone_number": "+1-555-0188",
            "registered_owner": "Kaelen Vance",
            "account_link_hint": "kaelen_v",
            "carrier": "Pacific Cellular Synthetic",
            "plan_type": "Business Fleet",
            "status": "Active",
            "first_seen": "2024-02-15",
            "last_seen": "2026-03-15T00:00:00Z"
        },
        {
            "phone_number": "+1-555-0121",
            "registered_owner": "Chloe Simmons",
            "account_link_hint": "chloe_creative",
            "carrier": "Pacific Cellular Synthetic",
            "plan_type": "Postpaid Family",
            "status": "Active",
            "first_seen": "2023-01-10",
            "last_seen": "2026-03-15T00:00:00Z"
        },
        {
            "phone_number": "+1-555-0133",
            "registered_owner": "David Lin",
            "account_link_hint": "david_lin_tech",
            "carrier": "BayArea Telecom Synthetic",
            "plan_type": "Postpaid Individual",
            "status": "Active",
            "first_seen": "2022-06-12",
            "last_seen": "2026-03-15T00:00:00Z"
        },
        {
            "phone_number": "+1-555-0155",
            "registered_owner": "Lucas Reed",
            "account_link_hint": "lucas_r_sound",
            "carrier": "Pacific Cellular Synthetic",
            "plan_type": "Postpaid Individual",
            "status": "Active",
            "first_seen": "2023-03-20",
            "last_seen": "2026-03-15T00:00:00Z"
        }
    ]
    phones_df = pd.DataFrame(phones)

    # 2. Call Detail Records (call_records.csv)
    # Cell Tower database
    towers = {
        "TOWER-BAY-01": {"name": "Marina Arts Sector", "lat": 37.8020, "lon": -122.4220},
        "TOWER-BAY-02": {"name": "Harbor Wharf Sector", "lat": 37.8060, "lon": -122.4350},
        "TOWER-RWD-04": {"name": "Redwood Crest Sector", "lat": 37.8720, "lon": -122.4900},
        "TOWER-SAUS-07": {"name": "Shoreline Sausalito Sector", "lat": 37.8550, "lon": -122.4800},
        "TOWER-PAC-09": {"name": "Whispering Pines Ridge Sector", "lat": 37.8930, "lon": -122.5730},
        "TOWER-SFO-12": {"name": "Airport Gateway Sector", "lat": 37.6010, "lon": -122.3820}
    }

    cdr_list: List[Dict[str, Any]] = []
    call_idx = 1001

    # Routine calls on primary phone (+1-555-0144)
    for day in range(2, 38):
        if random.random() < 0.45:
            call_dt = base_date + timedelta(days=day, hours=random.randint(10, 20), minutes=random.randint(0, 59))
            recipient = random.choice(["+1-555-0121", "+1-555-0133"])
            tower_id = "TOWER-BAY-01" if random.random() < 0.6 else "TOWER-BAY-02"
            cdr_list.append({
                "call_id": f"CDR-{call_idx}",
                "caller_number": "+1-555-0144",
                "receiver_number": recipient,
                "timestamp_utc": call_dt.isoformat(),
                "duration_sec": random.randint(45, 920),
                "call_type": "VOICE",
                "cell_tower_id": tower_id,
                "cell_tower_sector": towers[tower_id]["name"],
                "tower_latitude": towers[tower_id]["lat"],
                "tower_longitude": towers[tower_id]["lon"]
            })
            call_idx += 1

    # Inbound solicitation call from Kaelen Vance to primary phone (Day 32)
    c_dt1 = base_date + timedelta(days=32, hours=15, minutes=20)
    cdr_list.append({
        "call_id": f"CDR-{call_idx}",
        "caller_number": "+1-555-0188",
        "receiver_number": "+1-555-0144",
        "timestamp_utc": c_dt1.isoformat(),
        "duration_sec": 412,
        "call_type": "VOICE",
        "cell_tower_id": "TOWER-BAY-01",
        "cell_tower_sector": towers["TOWER-BAY-01"]["name"],
        "tower_latitude": towers["TOWER-BAY-01"]["lat"],
        "tower_longitude": towers["TOWER-BAY-01"]["lon"]
    })
    call_idx += 1

    # Burner phone (+1-555-0199) calls to Kaelen Vance (+1-555-0188)
    burner_calls = [
        (40, 14, 10, 185, "TOWER-BAY-01"), # Day 40 in city
        (42, 11, 45, 310, "TOWER-SAUS-07"), # Day 42 near Sausalito Shoreline
        (43, 19, 30, 95, "TOWER-SAUS-07"), # Day 43 evening
        (44, 16, 50, 240, "TOWER-SAUS-07"), # Day 44 pre-meeting
        (44, 21, 45, 0, "TOWER-PAC-09")     # Day 44 final cell tower ping / SMS delivery attempt
    ]

    for day_off, hr, mn, dur, tower_id in burner_calls:
        b_dt = base_date + timedelta(days=day_off, hours=hr, minutes=mn)
        cdr_list.append({
            "call_id": f"CDR-{call_idx}",
            "caller_number": "+1-555-0199",
            "receiver_number": "+1-555-0188",
            "timestamp_utc": b_dt.isoformat(),
            "duration_sec": dur,
            "call_type": "VOICE" if dur > 0 else "SMS_ROUTING_PING",
            "cell_tower_id": tower_id,
            "cell_tower_sector": towers[tower_id]["name"],
            "tower_latitude": towers[tower_id]["lat"],
            "tower_longitude": towers[tower_id]["lon"]
        })
        call_idx += 1

    # Red Herring: Lucas Reed at Airport (Day 44 evening)
    lucas_airport_dt = base_date + timedelta(days=44, hours=19, minutes=10)
    cdr_list.append({
        "call_id": f"CDR-{call_idx}",
        "caller_number": "+1-555-0155",
        "receiver_number": "+1-555-0129", # Julian Gomez
        "timestamp_utc": lucas_airport_dt.isoformat(),
        "duration_sec": 340,
        "call_type": "VOICE",
        "cell_tower_id": "TOWER-SFO-12",
        "cell_tower_sector": towers["TOWER-SFO-12"]["name"],
        "tower_latitude": towers["TOWER-SFO-12"]["lat"],
        "tower_longitude": towers["TOWER-SFO-12"]["lon"]
    })

    cdr_df = pd.DataFrame(cdr_list).sort_values(by="timestamp_utc").reset_index(drop=True)
    return phones_df, cdr_df
