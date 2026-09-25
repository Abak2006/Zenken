"""
Synthetic Data Generator for Case MP-2026-0527: Ananya Nair (Bengaluru, India).
Generates an advanced, high-tech industrial cyber-espionage and autonomous UAV firmware exfiltration dataset:
- Case Bible (JSON) with 14 distinct Bengaluru / NH-44 corridor venues
- Profiles (JSON) - 10 developer, POI & academic profiles
- Posts (CSV) - 9 developer & covert social posts (POST-AN-001 .. POST-AN-009)
- Call Detail Records (CSV) - 18 telecom VoLTE & burner CDR records (CDR-AN-001 .. CDR-AN-018)
- Physical Check-ins (CSV) - 7 physical check-ins (CHK-AN-001 .. CHK-AN-007)
- Photo EXIF Metadata (JSON) - 17 forensic photo records (IMG-AN-001 .. IMG-AN-017)
- Device Artifacts (JSON) - 6 device forensics records (DEV-AN-001 .. DEV-AN-006)
- GitHub / Code Telemetry (JSON) - 4 cryptographic commits (GH-AN-001 .. GH-AN-004)
- OSINT Correlations (JSON) - 5 cross-platform correlation links (OSINT-AN-001 .. OSINT-AN-005)
- Phones (CSV) & Connections (CSV)
- Structured Timeline Events (JSON) - Exactly 76 forensic events (EV-AN-001 .. EV-AN-076)
- Resolved Identities (JSON) - ~38 entities
- Movement Analysis & DBSCAN (JSON)
- Hypotheses Evaluation (JSON) & Ground Truth Evaluation (JSON)
- Real NetworkX Investigation Graph -> Stationary Vis.js HTML files
- Interactive Folium Tactical Map & Overview Corridor Map
- Interactive Plotly 5-Lane Timeline
"""
from __future__ import annotations
import sys
import json
import os
import math
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
import networkx as nx
import folium
from folium.plugins import HeatMap
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta

def generate_ananya_dataset(target_dir: Path | None = None) -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    if target_dir is None:
        target_dir = base_dir / "data" / "cases" / "MP-2026-0527"
    target_dir.mkdir(parents=True, exist_ok=True)

    # ============================================================
    # 1. CASE BIBLE & 14 DISTINCT VENUES
    # ============================================================
    venues = [
        {"id": "blr_v01", "name": "Koramangala 4th Block Housing", "category": "Residence", "latitude": 12.9345, "longitude": 77.6258, "address": "Koramangala 4th Block, Bengaluru"},
        {"id": "blr_v02", "name": "Electronic City BIT Robotics Lab", "category": "Academic", "latitude": 12.8452, "longitude": 77.6602, "address": "Electronics City Phase 1, Hosur Road, Bengaluru"},
        {"id": "blr_v03", "name": "Third Wave Coffee Koramangala", "category": "Cafe", "latitude": 12.9352, "longitude": 77.6245, "address": "80 Feet Road, 4th Block, Koramangala"},
        {"id": "blr_v04", "name": "WeWork Galaxy Residency Road", "category": "Coworking", "latitude": 12.9715, "longitude": 77.6074, "address": "43 Residency Road, Shanthala Nagar, Bengaluru"},
        {"id": "blr_v05", "name": "Indiranagar Roastery", "category": "Cafe/Meeting", "latitude": 12.9719, "longitude": 77.6412, "address": "100 Feet Road, Indiranagar, Bengaluru"},
        {"id": "blr_v06", "name": "Cubbon Park Bamboo Grove", "category": "Park", "latitude": 12.9763, "longitude": 77.5929, "address": "Kasturba Road, Bengaluru"},
        {"id": "blr_v07", "name": "Hebbal Lake Transit Hub", "category": "Transit/Observation", "latitude": 13.0410, "longitude": 77.5910, "address": "Bellary Road, Hebbal, Bengaluru"},
        {"id": "blr_v08", "name": "Devanahalli Logistics Corridor", "category": "Industrial/Transit", "latitude": 13.2483, "longitude": 77.7126, "address": "NH-44 Airport Bypass, Devanahalli, Bengaluru"},
        {"id": "blr_v09", "name": "Nandi Hills Ridge Overlook", "category": "Scenic/Terminal Radar", "latitude": 13.3702, "longitude": 77.6835, "address": "Nandi Hills Ridge Radar Base, Chikkaballapur District"},
        {"id": "blr_v10", "name": "Whitefield ITPL Tech Corridor", "category": "Industrial/Tech", "latitude": 12.9860, "longitude": 77.7310, "address": "International Tech Park, Whitefield, Bengaluru"},
        {"id": "blr_v11", "name": "Yelahanka Airbase Sector", "category": "Aviation Perimeter", "latitude": 13.1350, "longitude": 77.6050, "address": "Air Force Station Yelahanka Perimeter, Bengaluru"},
        {"id": "blr_v12", "name": "Manyata Tech Park North", "category": "Commercial/R&D", "latitude": 13.0480, "longitude": 77.6200, "address": "Nagavara Outer Ring Road, Bengaluru"},
        {"id": "blr_v13", "name": "Bellary Road Tollway Sector", "category": "Highway/FASTAG", "latitude": 13.1800, "longitude": 77.6350, "address": "NH-44 Expressway Toll Plaza, Bengaluru North"},
        {"id": "blr_v14", "name": "Chikkaballapur Foothills Checkpoint", "category": "Rural Checkpoint", "latitude": 13.3900, "longitude": 77.7200, "address": "SH-104 Foothills Junction, Chikkaballapur"}
    ]

    case_bible = {
        "case_metadata": {
            "case_id": "MP-2026-0527",
            "investigation_title": "Disappearance of Ananya Nair — Autonomous Systems Security Incident",
            "status": "OPEN",
            "date_reported": "2026-04-18T09:00:00Z",
            "assigned_team": "Central Cyber Forensics & Special OSINT Squad",
            "jurisdiction": "Bengaluru Central / Electronic City Cyber Crime Division"
        },
        "missing_person": {
            "full_name": "Ananya Nair",
            "age": 22,
            "pronouns": "she/her",
            "occupation": "Distributed Systems & Autonomous Drone Firmware Researcher",
            "institution": "Bengaluru Institute of Technology (BIT)",
            "last_seen_date": "2026-04-16T21:15:00Z",
            "last_seen_location_name": "Nandi Hills Ridge Overlook",
            "last_seen_coordinates": {
                "latitude": 13.3702,
                "longitude": 77.6835
            },
            "routine_description": (
                "Final-year B.Tech CS researcher leading the HyperMesh-K9 peer-to-peer telemetry swarm project. "
                "Maintained daily routines between Koramangala student quarters and Electronic City campus robotics labs. "
                "Disappeared following a secret contract NDA meeting at Indiranagar Roastery. Digital audit reveals repository force-pushes, "
                "JTAG testbench flash dumps, and a burner handset trace heading north on the NH-44 highway corridor."
            )
        },
        "digital_identities": [
            {
                "platform": "ChirpNet",
                "handle": "ananya_dev",
                "display_name": "Ananya Nair | Systems & Kernel",
                "account_type": "primary",
                "status": "active",
                "bio": "CS Senior @ BIT. Distributed consensus, drone mesh firmware, eBPF, Rust. Mail: ananya.nair.sys@fictional-mail.in",
                "email": "ananya.nair.sys@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "InstaPhoto",
                "handle": "ananya.n",
                "display_name": "Ananya N.",
                "account_type": "variant_alias",
                "status": "active",
                "bio": "filter coffee, terminal logs & Western Ghats ridge treks",
                "email": "ananya_personal@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "CodeHub",
                "handle": "ananyan-dev",
                "display_name": "Ananya Nair",
                "account_type": "dormant_developer",
                "status": "active",
                "bio": "Maintainer: bit-lab/hypermesh-core. PGP: 0x9E4B2F81A07C",
                "email": "ananya.nair.sys@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "ShadowNet",
                "handle": "void_null07",
                "display_name": "null_ptr",
                "account_type": "covert_burner",
                "status": "active",
                "bio": "ephemeral telemetry nodes & cold hardware corridors",
                "email": "anon_blr07@proton-synthetic.me",
                "phone_reference": "+91-98801-0199"
            }
        ],
        "venues": venues
    }
    with open(target_dir / "case_bible.json", "w", encoding="utf-8") as f:
        json.dump(case_bible, f, indent=2)

    # ============================================================
    # 2. PROFILES (10 Forensic Entity Accounts)
    # ============================================================
    profiles = [
        {
            "account_id": "acc_target_an_01",
            "handle": "ananya_dev",
            "display_name": "Ananya Nair | Systems & Kernel",
            "platform": "ChirpNet",
            "account_type": "primary",
            "bio": "CS Senior @ BIT. Distributed consensus, drone mesh firmware, eBPF, Rust.",
            "email": "ananya.nair.sys@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 3420,
            "following_count": 280,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_02",
            "handle": "ananya.n",
            "display_name": "Ananya N.",
            "platform": "InstaPhoto",
            "account_type": "personal",
            "bio": "filter coffee, terminal logs & Western Ghats ridge treks",
            "email": "ananya_personal@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 1150,
            "following_count": 390,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_03",
            "handle": "ananyan-dev",
            "display_name": "Ananya Nair",
            "platform": "CodeHub",
            "account_type": "developer",
            "bio": "Maintainer: bit-lab/hypermesh-core. PGP: 0x9E4B2F81A07C",
            "email": "ananya.nair.sys@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 890,
            "following_count": 94,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_04",
            "handle": "void_null07",
            "display_name": "null_ptr",
            "platform": "ShadowNet",
            "account_type": "covert_burner",
            "bio": "ephemeral telemetry nodes & cold hardware corridors",
            "email": "anon_blr07@proton-synthetic.me",
            "phone": "+91-98801-0199",
            "is_private": True,
            "followers_count": 19,
            "following_count": 4,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_cont_01",
            "handle": "vector_zero",
            "display_name": "Vector Zero / CipherCore",
            "platform": "ChirpNet",
            "account_type": "poi",
            "bio": "Autonomous swarm intelligence architect. Confidential defense telemetry recruiter.",
            "email": "ops@ciphercore-vector.io",
            "phone": "+91-98801-0900",
            "is_private": False,
            "followers_count": 5120,
            "following_count": 140,
            "real_name_reference": "Vector Zero",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_02",
            "handle": "priya_k",
            "display_name": "Priya Krishnamurthy",
            "platform": "InstaPhoto",
            "account_type": "roommate",
            "bio": "Computational Biology @ IISc · Ananya's flatmate at Koramangala",
            "email": "priya.k@biotech-blr.in",
            "phone": "+91-98801-0222",
            "is_private": True,
            "followers_count": 740,
            "following_count": 480,
            "real_name_reference": "Priya Krishnamurthy",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_03",
            "handle": "rohan_sys",
            "display_name": "Rohan Sharma",
            "platform": "ChirpNet",
            "account_type": "colleague",
            "bio": "Systems Engineer & Co-Researcher on HyperMesh @ BIT Robotics Lab",
            "email": "rohan.sharma@fictional-bit.in",
            "phone": "+91-98801-0333",
            "is_private": False,
            "followers_count": 680,
            "following_count": 310,
            "real_name_reference": "Rohan Sharma",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_04",
            "handle": "prof_menon_sys",
            "display_name": "Dr. Vikram S. Menon",
            "platform": "ChirpNet",
            "account_type": "faculty",
            "bio": "Dean of Computer Science & Autonomous Systems Lab Director @ BIT",
            "email": "vsmenon@bit-dept.ac.in",
            "phone": "+91-98801-0444",
            "is_private": False,
            "followers_count": 2150,
            "following_count": 110,
            "real_name_reference": "Dr. Vikram S. Menon",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_05",
            "handle": "kavya_drone_ai",
            "display_name": "Kavya Patel",
            "platform": "ChirpNet",
            "account_type": "expert",
            "bio": "Aerospace guidance systems researcher. UAV spectrum analyst Bengaluru.",
            "email": "kavya.patel@aero-blr.in",
            "phone": "+91-98801-0555",
            "is_private": False,
            "followers_count": 1840,
            "following_count": 220,
            "real_name_reference": "Kavya Patel",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_06",
            "handle": "deepak_kernel",
            "display_name": "Deepak Rao",
            "platform": "ChirpNet",
            "account_type": "hardware_engineer",
            "bio": "Hardware security & JTAG reverse engineering. Embedded systems architect.",
            "email": "d_rao@kernel-embed.in",
            "phone": "+91-98801-0777",
            "is_private": False,
            "followers_count": 920,
            "following_count": 180,
            "real_name_reference": "Deepak Rao",
            "is_target_identity": False
        }
    ]
    with open(target_dir / "profiles.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)

    # ============================================================
    # 3. POSTS (9 Focused Technical & Covert Social Records)
    # Target profile: ~9 Social items (POST-AN-001 .. POST-AN-009)
    # ============================================================
    posts = [
        {"post_id": "POST-AN-001", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-03-28 10:15:00 UTC", "timestamp_utc_iso": "2026-03-28T10:15:00Z", "text": "Pushed HyperMesh-K9 v0.4 release tag. Sub-4ms consensus round latency across 128 simulated UAV swarm nodes in Rust.", "hashtags": "#rust #uav #distributed", "mentions": "@rohan_sys", "location_tag": "Electronic City BIT Robotics Lab", "likes": 142, "photo_id": "IMG-AN-001", "deleted": False, "sentiment_label": "POSITIVE"},
        {"post_id": "POST-AN-002", "account": "vector_zero", "platform": "ChirpNet", "timestamp_raw": "2026-03-30 17:10:00 UTC", "timestamp_utc_iso": "2026-03-30T17:10:00Z", "text": "@ananya_dev Your K9 consensus model bypasses conventional telemetry jamming. CipherCore is deploying autonomous edge clusters in Karnataka. Check encrypted dispatch.", "hashtags": "#stealth #defense #recruiting", "mentions": "@ananya_dev", "location_tag": "Indiranagar", "likes": 34, "photo_id": None, "deleted": False, "sentiment_label": "NEUTRAL"},
        {"post_id": "POST-AN-003", "account": "kavya_drone_ai", "platform": "ChirpNet", "timestamp_raw": "2026-04-02 11:20:00 UTC", "timestamp_utc_iso": "2026-04-02T11:20:00Z", "text": "Advisory notice to Bengaluru aerospace labs: Several unregistered entities are soliciting student researchers for drone transponder telemetry under shell defense names.", "hashtags": "#security #advisory", "mentions": None, "location_tag": "Bengaluru Central", "likes": 210, "photo_id": None, "deleted": False, "sentiment_label": "WARNING"},
        {"post_id": "POST-AN-004", "account": "ananya.n", "platform": "InstaPhoto", "timestamp_raw": "2026-04-05 16:45:00 UTC", "timestamp_utc_iso": "2026-04-05T16:45:00Z", "text": "Brief respite from terminal logs in the bamboo groves before a high-stakes deployment week.", "hashtags": "#cubbonpark #bengaluru", "mentions": "@priya_k", "location_tag": "Cubbon Park Bamboo Grove", "likes": 184, "photo_id": "IMG-AN-004", "deleted": False, "sentiment_label": "POSITIVE"},
        {"post_id": "POST-AN-005", "account": "void_null07", "platform": "ShadowNet", "timestamp_raw": "2026-04-09 23:15:00 UTC", "timestamp_utc_iso": "2026-04-09T23:15:00Z", "text": "PGP key 0x9E4B2F81A07C validated. Secondary encrypted cellular uplink active. Terminal bridge configured.", "hashtags": "#pgp #stealth", "mentions": None, "location_tag": "Hebbal Lake Transit Hub", "likes": 5, "photo_id": None, "deleted": False, "sentiment_label": "COVERT"},
        {"post_id": "POST-AN-006", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-12 16:15:00 UTC", "timestamp_utc_iso": "2026-04-12T16:15:00Z", "text": "Meeting CipherCore vector team tonight at Indiranagar Roastery at 20:00 to execute the autonomous IP contract agreement.", "hashtags": "#contract #ciphercore", "mentions": "@vector_zero", "location_tag": "Indiranagar Roastery", "likes": 22, "photo_id": "IMG-AN-008", "deleted": True, "sentiment_label": "CRITICAL_DELETED"},
        {"post_id": "POST-AN-007", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-12 19:40:00 UTC", "timestamp_utc_iso": "2026-04-12T19:40:00Z", "text": "Contract terms dictate immediate repository wipe. Transitioning all local test NVMe drives into cold storage enclosures.", "hashtags": "#stealth #wipe", "mentions": None, "location_tag": "Indiranagar Roastery", "likes": 11, "photo_id": None, "deleted": True, "sentiment_label": "CRITICAL_DELETED"},
        {"post_id": "POST-AN-008", "account": "deepak_kernel", "platform": "ChirpNet", "timestamp_raw": "2026-04-14 14:00:00 UTC", "timestamp_utc_iso": "2026-04-14T14:00:00Z", "text": "Someone performed a raw JTAG flash dump on the FPGA drone telemetry board in Lab 4 yesterday evening. Serial barcodes scraped clean.", "hashtags": "#hardware #breach", "mentions": "@rohan_sys;@prof_menon_sys", "location_tag": "Electronic City BIT Robotics Lab", "likes": 56, "photo_id": "IMG-AN-010", "deleted": False, "sentiment_label": "ALARM"},
        {"post_id": "POST-AN-009", "account": "void_null07", "platform": "ShadowNet", "timestamp_raw": "2026-04-16 19:10:00 UTC", "timestamp_utc_iso": "2026-04-16T19:10:00Z", "text": "Uplink lock established. Transit initiated north toward Devanahalli gateway. Handset powering down upon radar approach.", "hashtags": "#transit #stealth", "mentions": None, "location_tag": "Devanahalli Logistics Corridor", "likes": 2, "photo_id": "IMG-AN-014", "deleted": False, "sentiment_label": "COVERT"}
    ]
    pd.DataFrame(posts).to_csv(target_dir / "posts.csv", index=False)

    # ============================================================
    # 4. CALL DETAIL RECORDS (18 Telecom CDRs)
    # Target profile: ~18 Telecom CDR items (CDR-AN-001 .. CDR-AN-018)
    # ============================================================
    calls = [
        {"call_id": "CDR-AN-001", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0222", "call_type": "Voice", "timestamp_utc": "2026-03-30 08:30:00", "duration_sec": 140, "cell_tower_id": "BLR-TWR-401", "cell_tower_sector": "Koramangala 4th Block", "tower_latitude": 12.9345, "tower_longitude": 77.6258},
        {"call_id": "CDR-AN-002", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0333", "call_type": "Voice", "timestamp_utc": "2026-04-01 10:15:00", "duration_sec": 210, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-AN-003", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0444", "call_type": "Voice", "timestamp_utc": "2026-04-03 14:20:00", "duration_sec": 380, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-AN-004", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0222", "call_type": "Voice", "timestamp_utc": "2026-04-05 19:10:00", "duration_sec": 65, "cell_tower_id": "BLR-TWR-401", "cell_tower_sector": "Koramangala 4th Block", "tower_latitude": 12.9345, "tower_longitude": 77.6258},
        {"call_id": "CDR-AN-005", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0777", "call_type": "Voice", "timestamp_utc": "2026-04-07 11:45:00", "duration_sec": 95, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-AN-006", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0900", "call_type": "Encrypted VoIP", "timestamp_utc": "2026-04-09 17:35:00", "duration_sec": 420, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar 100ft Road", "tower_latitude": 12.9719, "tower_longitude": 77.6412},
        {"call_id": "CDR-AN-007", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0222", "call_type": "Voice", "timestamp_utc": "2026-04-10 18:15:00", "duration_sec": 195, "cell_tower_id": "BLR-TWR-401", "cell_tower_sector": "Koramangala 4th Block", "tower_latitude": 12.9345, "tower_longitude": 77.6258},
        {"call_id": "CDR-AN-008", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0333", "call_type": "Voice", "timestamp_utc": "2026-04-11 11:20:00", "duration_sec": 84, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-AN-009", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0444", "call_type": "Voice", "timestamp_utc": "2026-04-11 15:40:00", "duration_sec": 310, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-AN-010", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0900", "call_type": "Encrypted VoIP", "timestamp_utc": "2026-04-12 17:35:00", "duration_sec": 360, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar 100ft Road", "tower_latitude": 12.9719, "tower_longitude": 77.6412},
        {"call_id": "CDR-AN-011", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0222", "call_type": "Voice", "timestamp_utc": "2026-04-12 19:15:00", "duration_sec": 45, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar 100ft Road", "tower_latitude": 12.9719, "tower_longitude": 77.6412},
        {"call_id": "CDR-AN-012", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-14 20:10:00", "duration_sec": 50, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar Metro Sector", "tower_latitude": 12.9784, "tower_longitude": 77.6385},
        {"call_id": "CDR-AN-013", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0777", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-15 11:30:00", "duration_sec": 24, "cell_tower_id": "BLR-TWR-615", "cell_tower_sector": "Cubbon Park / High Court", "tower_latitude": 12.9763, "tower_longitude": 77.5929},
        {"call_id": "CDR-AN-014", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-15 16:45:00", "duration_sec": 65, "cell_tower_id": "BLR-TWR-712", "cell_tower_sector": "Hebbal Flyover North", "tower_latitude": 13.0358, "tower_longitude": 77.5970},
        {"call_id": "CDR-AN-015", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 18:20:00", "duration_sec": 30, "cell_tower_id": "BLR-TWR-780", "cell_tower_sector": "Yelahanka Airbase Sector", "tower_latitude": 13.1007, "tower_longitude": 77.5963},
        {"call_id": "CDR-AN-016", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 19:40:00", "duration_sec": 48, "cell_tower_id": "BLR-TWR-810", "cell_tower_sector": "Devanahalli Highway Corridor", "tower_latitude": 13.2483, "tower_longitude": 77.7126},
        {"call_id": "CDR-AN-017", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 20:50:00", "duration_sec": 32, "cell_tower_id": "BLR-TWR-8840", "cell_tower_sector": "Nandi Foot Base Station", "tower_latitude": 13.3412, "tower_longitude": 77.6890},
        {"call_id": "CDR-AN-018", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 21:15:00", "duration_sec": 19, "cell_tower_id": "BLR-TWR-8841", "cell_tower_sector": "Nandi Hills Ridge Radar Sector", "tower_latitude": 13.3702, "tower_longitude": 77.6835}
    ]
    pd.DataFrame(calls).to_csv(target_dir / "call_records.csv", index=False)

    # ============================================================
    # 5. PHYSICAL CHECK-INS (7 Check-ins)
    # Target profile: ~7 Check-in items (CHK-AN-001 .. CHK-AN-007)
    # ============================================================
    checkins = [
        {"checkin_id": "CHK-AN-001", "account": "ananya_dev", "venue_id": "blr_v02", "venue_name": "Electronic City BIT Robotics Lab", "timestamp_utc": "2026-04-08 09:00:00", "latitude": 12.8452, "longitude": 77.6602, "platform": "ChirpNet"},
        {"checkin_id": "CHK-AN-002", "account": "ananya_dev", "venue_id": "blr_v03", "venue_name": "Third Wave Coffee Koramangala", "timestamp_utc": "2026-04-09 14:30:00", "latitude": 12.9352, "longitude": 77.6245, "platform": "ChirpNet"},
        {"checkin_id": "CHK-AN-003", "account": "ananya.n", "venue_id": "blr_v04", "venue_name": "WeWork Galaxy Residency Road", "timestamp_utc": "2026-04-11 11:00:00", "latitude": 12.9715, "longitude": 77.6074, "platform": "InstaPhoto"},
        {"checkin_id": "CHK-AN-004", "account": "ananya.n", "venue_id": "blr_v05", "venue_name": "Indiranagar Roastery", "timestamp_utc": "2026-04-12 18:00:00", "latitude": 12.9719, "longitude": 77.6412, "platform": "InstaPhoto"},
        {"checkin_id": "CHK-AN-005", "account": "ananya.n", "venue_id": "blr_v06", "venue_name": "Cubbon Park Bamboo Grove", "timestamp_utc": "2026-04-13 16:30:00", "latitude": 12.9763, "longitude": 77.5929, "platform": "InstaPhoto"},
        {"checkin_id": "CHK-AN-006", "account": "void_null07", "venue_id": "blr_v07", "venue_name": "Hebbal Lake Transit Hub", "timestamp_utc": "2026-04-15 15:10:00", "latitude": 13.0410, "longitude": 77.5910, "platform": "ShadowNet"},
        {"checkin_id": "CHK-AN-007", "account": "void_null07", "venue_id": "blr_v09", "venue_name": "Nandi Hills Ridge Overlook", "timestamp_utc": "2026-04-16 20:45:00", "latitude": 13.3702, "longitude": 77.6835, "platform": "ShadowNet"}
    ]
    pd.DataFrame(checkins).to_csv(target_dir / "checkins.csv", index=False)

    # ============================================================
    # 6. PHOTO EXIF METADATA (17 Forensic Photo Records)
    # Target profile: ~17 Photo EXIF items (IMG-AN-001 .. IMG-AN-017)
    # ============================================================
    photos = [
        {"photo_id": "IMG-AN-001", "account": "ananya.n", "timestamp_utc": "2026-03-28 10:20:00", "filename": "oscilloscope_capture_spi.jpg", "camera_make": "Sony", "camera_model": "ILCE-7M4", "latitude": 12.8452, "longitude": 77.6602, "caption": "Digital oscilloscope logic trace capturing 4-channel SPI bus packet bursts at BIT Lab", "is_red_herring": False},
        {"photo_id": "IMG-AN-002", "account": "rohan_sys", "timestamp_utc": "2026-03-29 14:10:00", "filename": "bench_test_drone_rig.jpg", "camera_make": "OnePlus", "camera_model": "OnePlus 12", "latitude": 12.8452, "longitude": 77.6602, "caption": "UAV quadrotor carbon frame mounted on gimbal testbench", "is_red_herring": False},
        {"photo_id": "IMG-AN-003", "account": "ananya.n", "timestamp_utc": "2026-04-01 11:35:00", "filename": "third_wave_pour_over.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9352, "longitude": 77.6245, "caption": "Manual pour-over coffee notes with printed consensus paper", "is_red_herring": False},
        {"photo_id": "IMG-AN-004", "account": "ananya.n", "timestamp_utc": "2026-04-05 16:50:00", "filename": "cubbon_park_canopy.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9763, "longitude": 77.5929, "caption": "Bamboo trees in afternoon light near high court perimeter", "is_red_herring": False},
        {"photo_id": "IMG-AN-005", "account": "ananya.n", "timestamp_utc": "2026-04-07 09:15:00", "filename": "bit_robotics_whiteboard.jpg", "camera_make": "Sony", "camera_model": "ILCE-7M4", "latitude": 12.8452, "longitude": 77.6602, "caption": "Cryptographic nonce rotation equations on lab whiteboard", "is_red_herring": False},
        {"photo_id": "IMG-AN-006", "account": "priya_k", "timestamp_utc": "2026-04-08 20:30:00", "filename": "koramangala_balcony_sunset.jpg", "camera_make": "Samsung", "camera_model": "Galaxy S23", "latitude": 12.9345, "longitude": 77.6258, "caption": "Evening skyline view from Koramangala 4th block terrace", "is_red_herring": False},
        {"photo_id": "IMG-AN-007", "account": "ananya.n", "timestamp_utc": "2026-04-10 15:40:00", "filename": "wework_hotdesk_terminal.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9715, "longitude": 77.6074, "caption": "Dual monitor setup running Rust cargo build benchmarks", "is_red_herring": False},
        {"photo_id": "IMG-AN-008", "account": "ananya.n", "timestamp_utc": "2026-04-12 18:10:00", "filename": "indiranagar_roastery_patio.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9719, "longitude": 77.6412, "caption": "Evening coffee table setup before the CipherCore NDA discussion", "is_red_herring": False},
        {"photo_id": "IMG-AN-009", "account": "ananya.n", "timestamp_utc": "2026-04-12 21:05:00", "filename": "contract_document_fold.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9719, "longitude": 77.6412, "caption": "Signed NDA agreement watermark in low ambient light", "is_red_herring": False},
        {"photo_id": "IMG-AN-010", "account": "deepak_kernel", "timestamp_utc": "2026-04-14 13:45:00", "filename": "scraped_pcb_board.jpg", "camera_make": "Samsung", "camera_model": "Galaxy S23", "latitude": 12.8452, "longitude": 77.6602, "caption": "Laboratory bench macro photo showing desoldered EEPROM pins and shaved serial hashes", "is_red_herring": False},
        {"photo_id": "IMG-AN-011", "account": "void_null07", "timestamp_utc": "2026-04-15 15:20:00", "filename": "hebbal_flyover_pylon.jpg", "camera_make": "Nokia", "camera_model": "Nokia 105", "latitude": 13.0410, "longitude": 77.5910, "caption": "Low-resolution 640x480 snapshot of transit pillar north", "is_red_herring": False},
        {"photo_id": "IMG-AN-012", "account": "surveillance_node", "timestamp_utc": "2026-04-16 17:30:00", "filename": "manyata_ring_road_cam.jpg", "camera_make": "Hikvision", "camera_model": "DS-2CD2043G2", "latitude": 13.0480, "longitude": 77.6200, "caption": "Traffic camera capture of dark SUV moving north toward NH-44", "is_red_herring": False},
        {"photo_id": "IMG-AN-013", "account": "highway_cctv", "timestamp_utc": "2026-04-16 19:42:00", "filename": "devanahalli_toll_lane3.jpg", "camera_make": "Dahua", "camera_model": "ITC237-PW1B-IRZ", "latitude": 13.2483, "longitude": 77.7126, "caption": "FASTAG ANPR snapshot of transit vehicle passing through Devanahalli plaza", "is_red_herring": False},
        {"photo_id": "IMG-AN-014", "account": "void_null07", "timestamp_utc": "2026-04-16 20:55:00", "filename": "nandi_ridge_fog.jpg", "camera_make": "Sony", "camera_model": "ILCE-7M4", "latitude": 13.3702, "longitude": 77.6835, "caption": "Dense valley mist over radar dome facility at 1,400m elevation", "is_red_herring": False},
        {"photo_id": "IMG-AN-015", "account": "radar_telemetry_station", "timestamp_utc": "2026-04-16 21:14:00", "filename": "flir_drone_thermal_track.jpg", "camera_make": "Teledyne FLIR", "camera_model": "Boson 640", "latitude": 13.3702, "longitude": 77.6835, "caption": "Long-wave thermal signature showing small UAV autonomous rotor spool-up", "is_red_herring": False},
        {"photo_id": "IMG-AN-016", "account": "tourist_bot_decoy", "timestamp_utc": "2026-04-17 12:00:00", "filename": "old_manali_cafe_decoy.jpg", "camera_make": "Apple", "camera_model": "iPhone 13", "latitude": 32.2568, "longitude": 77.1734, "caption": "Distracting tourist snapshot claiming researcher sighting in Himachal Pradesh", "is_red_herring": True},
        {"photo_id": "IMG-AN-017", "account": "goa_decoy_account", "timestamp_utc": "2026-04-17 15:30:00", "filename": "anjuna_beach_shack_decoy.jpg", "camera_make": "Google", "camera_model": "Pixel 7", "latitude": 15.5800, "longitude": 73.7400, "caption": "Scraped travel photo posted with spoofed EXIF timestamp to confuse search radius", "is_red_herring": True}
    ]
    with open(target_dir / "photos_metadata.json", "w", encoding="utf-8") as f:
        json.dump(photos, f, indent=2)

    # ============================================================
    # 7. DEVICE ARTIFACTS (6 Device Forensics Records)
    # Target profile: ~6 Device Artifact items (DEV-AN-001 .. DEV-AN-006)
    # ============================================================
    devices = [
        {
            "device_id": "DEV-AN-001",
            "device_name": "ThinkPad P1 Gen 6 (Workstation)",
            "device_type": "Laptop / Workstation",
            "platform": "Arch Linux (Kernel 6.8.4-zen)",
            "imei_or_mac": "48:2a:e3:10:9c:51",
            "associated_account": "ananyan-dev",
            "owner_entity": "Ananya Nair",
            "timestamp_utc": "2026-04-12 23:45:00",
            "event": "LUKS key wipe command executed over SSH from remote bridge",
            "status": "Cryptographically Sanitized",
            "confidence": 1.0
        },
        {
            "device_id": "DEV-AN-002",
            "device_name": "OnePlus 12 (Primary Smartphone)",
            "device_type": "Smartphone",
            "platform": "OxygenOS 14 (Android 14)",
            "imei_or_mac": "864920184029112",
            "associated_account": "ananya_dev",
            "owner_entity": "Ananya Nair",
            "timestamp_utc": "2026-04-13 08:15:00",
            "event": "Airtel postpaid SIM removed; left powered on at Koramangala room",
            "status": "Abandoned in Room",
            "confidence": 0.99
        },
        {
            "device_id": "DEV-AN-003",
            "device_name": "Nokia 105 (Prepaid Burner Handset)",
            "device_type": "Feature Phone / Burner",
            "platform": "Series 30+",
            "imei_or_mac": "863920194829104",
            "associated_account": "void_null07",
            "owner_entity": "Ananya Nair",
            "timestamp_utc": "2026-04-16 21:15:00",
            "event": "Battery abruptly removed following final Nandi Hills radar ping",
            "status": "Terminated LKL",
            "confidence": 0.98
        },
        {
            "device_id": "DEV-AN-004",
            "device_name": "Xilinx Zynq UltraScale+ FPGA Board",
            "device_type": "Embedded Hardware",
            "platform": "FreeRTOS / Bare-Metal",
            "imei_or_mac": "MAC: 00:0A:35:FE:81:42",
            "associated_account": "ananyan-dev",
            "owner_entity": "BIT Robotics Lab",
            "timestamp_utc": "2026-04-14 02:10:00",
            "event": "JTAG programmer flash dump of flight control firmware",
            "status": "Hardware Desoldered & Scraped",
            "confidence": 0.95
        },
        {
            "device_id": "DEV-AN-005",
            "device_name": "Sabrent Tool-Free NVMe Enclosure",
            "device_type": "Cold Storage SSD",
            "platform": "Hardware Encrypted",
            "imei_or_mac": "SN: NVME-EXT-9941",
            "associated_account": "void_null07",
            "owner_entity": "Ananya Nair",
            "timestamp_utc": "2026-04-12 21:30:00",
            "event": "Full repository clone and encrypted firmware dump archived",
            "status": "Exfiltrated with Subject",
            "confidence": 0.94
        },
        {
            "device_id": "DEV-AN-006",
            "device_name": "DJI Matrice 300 RTK Radio Transceiver",
            "device_type": "RF Drone Telemetry Transponder",
            "platform": "OcuSync Enterprise (2.4/5.8 GHz)",
            "imei_or_mac": "RF-TX: 2488-K9-9182",
            "associated_account": "void_null07",
            "owner_entity": "CipherCore Vector Systems",
            "timestamp_utc": "2026-04-16 21:14:00",
            "event": "Autonomous drone swarm telemetry uplink burst at 2.412 GHz",
            "status": "Airborne RF Terminal Ping",
            "confidence": 0.96
        }
    ]
    with open(target_dir / "devices.json", "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)

    # ============================================================
    # 8. GITHUB / CODE ACTIVITY (4 VCS Commits)
    # Target profile: ~4 GitHub / Code items (GH-AN-001 .. GH-AN-004)
    # ============================================================
    github_commits = [
        {
            "commit_id": "GH-AN-001",
            "commit_sha": "a8f3c91e42b08d7",
            "repo": "bit-lab/hypermesh-core",
            "branch": "main",
            "author": "Ananya Nair",
            "author_account": "ananyan-dev",
            "timestamp_utc": "2026-03-28 09:15:00",
            "message": "release: tag v0.4 swarm consensus protocol with sub-4ms broadcast",
            "type": "Code Commit",
            "ip_or_terminal": "BIT Campus Lab LAN",
            "pgp_signature_valid": True,
            "pgp_key_id": "0x9E4B2F81A07C"
        },
        {
            "commit_id": "GH-AN-002",
            "commit_sha": "c41e08db91a45f2",
            "repo": "bit-lab/hypermesh-core",
            "branch": "feature/spi-fastpath",
            "author": "Ananya Nair",
            "author_account": "ananyan-dev",
            "timestamp_utc": "2026-04-04 18:30:00",
            "message": "driver: optimize DMA burst buffers for UltraScale FPGA transceiver",
            "type": "Code Commit",
            "ip_or_terminal": "BIT Campus Lab LAN",
            "pgp_signature_valid": True,
            "pgp_key_id": "0x9E4B2F81A07C"
        },
        {
            "commit_id": "GH-AN-003",
            "commit_sha": "f92a10b40e729a1",
            "repo": "bit-lab/hypermesh-core",
            "branch": "feature/spi-fastpath",
            "author": "Ananya Nair",
            "author_account": "ananyan-dev",
            "timestamp_utc": "2026-04-12 22:45:00",
            "message": "refactor: force-scrub embedded telemetry keys and proprietary headers",
            "type": "Force-Push Scrub",
            "ip_or_terminal": "ProtonVPN Netherlands Exit Node",
            "pgp_signature_valid": True,
            "pgp_key_id": "0x9E4B2F81A07C"
        },
        {
            "commit_id": "GH-AN-004",
            "commit_sha": "e77b02c819fa003",
            "repo": "bit-lab/hypermesh-core",
            "branch": "main",
            "author": "null_ptr",
            "author_account": "void_null07",
            "timestamp_utc": "2026-04-14 23:10:00",
            "message": "purge: repository branch force-deleted via upstream administrator token",
            "type": "Branch Force-Deletion",
            "ip_or_terminal": "Tor Onion Gateway Node",
            "pgp_signature_valid": True,
            "pgp_key_id": "0x9E4B2F81A07C"
        }
    ]
    with open(target_dir / "github_commits.json", "w", encoding="utf-8") as f:
        json.dump(github_commits, f, indent=2)
    with open(target_dir / "git_commits.json", "w", encoding="utf-8") as f:
        json.dump(github_commits, f, indent=2)

    # ============================================================
    # 9. OSINT ACCOUNT CORRELATIONS (5 Correlation Links)
    # Target profile: ~5 OSINT Correlation items (OSINT-AN-001 .. OSINT-AN-005)
    # ============================================================
    osint_links = [
        {
            "link_id": "OSINT-AN-001",
            "source_account": "@ananyan-dev",
            "target_account": "@void_null07",
            "platform": "PGP Web of Trust",
            "basis": "Identical GPG Master Key ID (0x9E4B2F81A07C) and subkey fingerprints",
            "confidence": 0.99,
            "first_observed": "2026-04-09 23:15:00",
            "status": "CONFIRMED_SAME_PERSON"
        },
        {
            "link_id": "OSINT-AN-002",
            "source_account": "@ananya_dev",
            "target_account": "@ananya.n",
            "platform": "ChirpNet / InstaPhoto",
            "basis": "Shared recovery phone +91-98801-0144 and bio bio-metric facial match on campus",
            "confidence": 0.98,
            "first_observed": "2024-08-01 12:00:00",
            "status": "CONFIRMED_SAME_PERSON"
        },
        {
            "link_id": "OSINT-AN-003",
            "source_account": "@void_null07",
            "target_account": "@vector_zero",
            "platform": "ShadowNet",
            "basis": "Mutual PGP encrypted session handshake exchanging recruit code SYS-K9-BLR",
            "confidence": 0.94,
            "first_observed": "2026-04-10 01:20:00",
            "status": "VERIFIED_POI_CONTACT"
        },
        {
            "link_id": "OSINT-AN-004",
            "source_account": "+91-98801-0199",
            "target_account": "@void_null07",
            "platform": "Cellular CDR / ShadowNet",
            "basis": "Handset IMEI 863920194829104 cellular data pings precisely match ShadowNet session logins",
            "confidence": 0.97,
            "first_observed": "2026-04-14 20:10:00",
            "status": "CONFIRMED_BURNER_HARDWARE"
        },
        {
            "link_id": "OSINT-AN-005",
            "source_account": "@vector_zero",
            "target_account": "CipherCore Vector Systems",
            "platform": "Corporate Registry & Darknet",
            "basis": "Domain WHOIS registration and SIP PBX gateway (+91-98801-0900) corporate routing",
            "confidence": 0.95,
            "first_observed": "2025-11-15 09:00:00",
            "status": "IDENTIFIED_EMPLOYER_ENTITY"
        }
    ]
    with open(target_dir / "osint_links.json", "w", encoding="utf-8") as f:
        json.dump(osint_links, f, indent=2)

    # ============================================================
    # 10. PHONES & CONNECTIONS
    # ============================================================
    phones = [
        {"phone_number": "+91-98801-0144", "registered_owner": "Ananya Nair", "account_link_hint": "ananya_dev", "carrier": "Airtel Karnataka 5G", "plan_type": "Postpaid", "status": "Abandoned in Room (SIM Removed)", "first_seen": "2024-08-01", "last_seen": "2026-04-12"},
        {"phone_number": "+91-98801-0199", "registered_owner": "Anonymous Cash SIM (IMEI 863920194829104)", "account_link_hint": "void_null07", "carrier": "Jio Karnataka Prepaid", "plan_type": "Prepaid Burner Handset", "status": "Terminated at Nandi Ridge 21:15 UTC", "first_seen": "2026-04-14", "last_seen": "2026-04-16"},
        {"phone_number": "+91-98801-0900", "registered_owner": "CipherCore Vector Systems Ltd", "account_link_hint": "vector_zero", "carrier": "Vodafone Business Secure SIP", "plan_type": "Encrypted VoIP Trunk", "status": "Active / Uncooperative", "first_seen": "2025-11-15", "last_seen": "2026-04-18"},
        {"phone_number": "+91-98801-0222", "registered_owner": "Priya Krishnamurthy", "account_link_hint": "priya_k", "carrier": "Airtel Karnataka", "plan_type": "Postpaid", "status": "Active", "first_seen": "2024-06-10", "last_seen": "2026-04-18"},
        {"phone_number": "+91-98801-0333", "registered_owner": "Rohan Sharma", "account_link_hint": "rohan_sys", "carrier": "Jio Karnataka", "plan_type": "Prepaid", "status": "Active", "first_seen": "2024-08-20", "last_seen": "2026-04-18"},
        {"phone_number": "+91-98801-0777", "registered_owner": "Deepak Rao", "account_link_hint": "deepak_kernel", "carrier": "Airtel Karnataka", "plan_type": "Postpaid", "status": "Active", "first_seen": "2024-09-01", "last_seen": "2026-04-18"}
    ]
    pd.DataFrame(phones).to_csv(target_dir / "phones.csv", index=False)

    connections = [
        {"source": "ananya_dev", "target": "vector_zero", "relationship_type": "CONTACTED", "weight": 1.0, "context": "Inbound recruiting pitch regarding autonomous drone swarm telemetry"},
        {"source": "vector_zero", "target": "ananya_dev", "relationship_type": "MENTIONS", "weight": 0.95, "context": "Public commendation of HyperMesh-K9 benchmarks"},
        {"source": "ananya_dev", "target": "rohan_sys", "relationship_type": "CO_RESEARCHER", "weight": 1.0, "context": "Co-author on distributed consensus and drone swarm protocols"},
        {"source": "ananya_dev", "target": "prof_menon_sys", "relationship_type": "ADVISOR", "weight": 0.85, "context": "Faculty supervisor and lab director at BIT"},
        {"source": "ananya_dev", "target": "priya_k", "relationship_type": "ROOMMATE", "weight": 1.0, "context": "Flatmate connection at Koramangala quarters"},
        {"source": "ananya_dev", "target": "deepak_kernel", "relationship_type": "COLLABORATOR", "weight": 0.8, "context": "Hardware JTAG flashing on testboards"},
        {"source": "kavya_drone_ai", "target": "ananya_dev", "relationship_type": "WARNED", "weight": 0.9, "context": "Advisory warning regarding unregistered aerospace defense recruiters"}
    ]
    pd.DataFrame(connections).to_csv(target_dir / "connections.csv", index=False)

    # ============================================================
    # 11. STRUCTURED FORENSIC TIMELINE EVENTS (Exactly 76 Events)
    # Target profile: ~76 Events (EV-AN-001 .. EV-AN-076)
    # Spanning March 28, 2026 to April 17, 2026
    # ============================================================
    timeline_events = [
        # Phase 1: Baseline Research & Swarm Benchmarks (Mar 28 – Apr 03)
        {"event_id": "EV-AN-001", "timestamp": "2026-03-28 09:15:00", "case_id": "MP-2026-0527", "source_type": "GitHub / Code", "event_type": "Repository Release", "severity": "NORMAL", "description": "Release v0.4 of HyperMesh-K9 swarm consensus tagged on bit-lab/hypermesh-core", "entity_ids": ["ananya_nair", "ananyan-dev"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["GH-AN-001"], "confidence": 1.0, "phase": "Baseline Research"},
        {"event_id": "EV-AN-002", "timestamp": "2026-03-28 10:15:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Public Post", "severity": "NORMAL", "description": "@ananya_dev announced sub-4ms consensus round benchmarks across 128 UAV nodes", "entity_ids": ["ananya_nair", "ananya_dev"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["POST-AN-001"], "confidence": 1.0, "phase": "Baseline Research"},
        {"event_id": "EV-AN-003", "timestamp": "2026-03-28 10:20:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "Sony ILCE-7M4 photo capture of 4-channel SPI bus logic trace in robotics lab", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["IMG-AN-001"], "confidence": 0.98, "phase": "Baseline Research"},
        {"event_id": "EV-AN-004", "timestamp": "2026-03-29 14:10:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "Gimbal testbench setup photograph with quadrotor carbon frame", "entity_ids": ["rohan_sys"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["IMG-AN-002"], "confidence": 0.95, "phase": "Baseline Research"},
        {"event_id": "EV-AN-005", "timestamp": "2026-03-30 08:30:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Voice call between Ananya and roommate Priya (140s) from Koramangala quarters", "entity_ids": ["ananya_nair", "priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block", "evidence_ids": ["CDR-AN-001"], "confidence": 1.0, "phase": "Baseline Research"},
        {"event_id": "EV-AN-006", "timestamp": "2026-03-30 17:10:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "POI Outreach", "severity": "NOTABLE", "description": "@vector_zero public pitch regarding CipherCore autonomous edge clusters", "entity_ids": ["vector_zero", "ananya_dev"], "location_id": "blr_v05", "location_name": "Indiranagar", "evidence_ids": ["POST-AN-002"], "confidence": 0.95, "phase": "Baseline Research"},
        {"event_id": "EV-AN-007", "timestamp": "2026-04-01 10:15:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Call with colleague Rohan Sharma regarding testbench SPI throughput (210s)", "entity_ids": ["ananya_nair", "rohan_sys"], "location_id": "blr_v02", "location_name": "Electronic City Phase 1", "evidence_ids": ["CDR-AN-002"], "confidence": 1.0, "phase": "Baseline Research"},
        {"event_id": "EV-AN-008", "timestamp": "2026-04-01 11:35:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "iPhone 15 Pro photo of pour-over coffee and research paper draft", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v03", "location_name": "Third Wave Coffee Koramangala", "evidence_ids": ["IMG-AN-003"], "confidence": 0.98, "phase": "Baseline Research"},
        {"event_id": "EV-AN-009", "timestamp": "2026-04-02 11:20:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Security Advisory", "severity": "SUSPICIOUS", "description": "Dr. Kavya Patel issues public advisory warning regarding shell aerospace recruiters", "entity_ids": ["kavya_drone_ai"], "location_id": "blr_v04", "location_name": "Bengaluru Central", "evidence_ids": ["POST-AN-003"], "confidence": 0.90, "phase": "Baseline Research"},
        {"event_id": "EV-AN-010", "timestamp": "2026-04-03 14:20:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Voice consultation with faculty director Dr. Menon on capstone evaluation (380s)", "entity_ids": ["ananya_nair", "prof_menon_sys"], "location_id": "blr_v02", "location_name": "Electronic City Phase 1", "evidence_ids": ["CDR-AN-003"], "confidence": 1.0, "phase": "Baseline Research"},

        # Phase 2: Inbound Recruiting & CipherCore Pitch (Apr 04 – Apr 11)
        {"event_id": "EV-AN-011", "timestamp": "2026-04-04 18:30:00", "case_id": "MP-2026-0527", "source_type": "GitHub / Code", "event_type": "Code Commit", "severity": "NORMAL", "description": "Git commit c41e08d optimizing DMA burst buffers for UltraScale FPGA transceiver", "entity_ids": ["ananya_nair", "ananyan-dev"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["GH-AN-002"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-012", "timestamp": "2026-04-05 16:45:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Personal Post", "severity": "NORMAL", "description": "@ananya.n photo post relaxing in bamboo grove before deployment sprint", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v06", "location_name": "Cubbon Park Bamboo Grove", "evidence_ids": ["POST-AN-004"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-013", "timestamp": "2026-04-05 16:50:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "iPhone 15 Pro photo of bamboo trees near high court perimeter", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v06", "location_name": "Cubbon Park Bamboo Grove", "evidence_ids": ["IMG-AN-004"], "confidence": 0.98, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-014", "timestamp": "2026-04-05 19:10:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Routine evening check-in call with roommate Priya (65s)", "entity_ids": ["ananya_nair", "priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block", "evidence_ids": ["CDR-AN-004"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-015", "timestamp": "2026-04-07 09:15:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "Sony A7M4 photo of nonce rotation equations on lab whiteboard", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["IMG-AN-005"], "confidence": 0.98, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-016", "timestamp": "2026-04-07 11:45:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Call with hardware engineer Deepak Rao regarding JTAG flasher availability (95s)", "entity_ids": ["ananya_nair", "deepak_kernel"], "location_id": "blr_v02", "location_name": "Electronic City Phase 1", "evidence_ids": ["CDR-AN-005"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-017", "timestamp": "2026-04-08 09:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Venue Check-in", "severity": "NORMAL", "description": "ChirpNet geo check-in at BIT Robotics Lab for morning firmware test session", "entity_ids": ["ananya_nair", "ananya_dev"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["CHK-AN-001"], "confidence": 0.95, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-018", "timestamp": "2026-04-08 20:30:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "Galaxy S23 photo of evening skyline view from Koramangala flat", "entity_ids": ["priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["IMG-AN-006"], "confidence": 0.95, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-019", "timestamp": "2026-04-09 14:30:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Venue Check-in", "severity": "NORMAL", "description": "Check-in at Third Wave Coffee Koramangala during code review break", "entity_ids": ["ananya_nair", "ananya_dev"], "location_id": "blr_v03", "location_name": "Third Wave Coffee Koramangala", "evidence_ids": ["CHK-AN-002"], "confidence": 0.95, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-020", "timestamp": "2026-04-09 17:35:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Encrypted VoIP", "severity": "SUSPICIOUS", "description": "Inbound encrypted SIP call from CipherCore trunk (+91-98801-0900) lasting 420s", "entity_ids": ["ananya_nair", "vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar 100ft Road", "evidence_ids": ["CDR-AN-006"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-021", "timestamp": "2026-04-09 23:15:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Covert Handshake", "severity": "CRITICAL", "description": "@void_null07 posted PGP key 0x9E4B2F81A07C activation dispatch on ShadowNet", "entity_ids": ["ananya_nair", "void_null07"], "location_id": "blr_v07", "location_name": "Hebbal Lake Transit Hub", "evidence_ids": ["POST-AN-005"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-022", "timestamp": "2026-04-09 23:15:00", "case_id": "MP-2026-0527", "source_type": "OSINT Correlation", "event_type": "Key Correlation", "severity": "CRITICAL", "description": "PGP key 0x9E4B2F81A07C on ShadowNet directly matches CodeHub key of @ananyan-dev", "entity_ids": ["ananyan-dev", "void_null07"], "location_id": "blr_v07", "location_name": "Hebbal Lake Transit Hub", "evidence_ids": ["OSINT-AN-001"], "confidence": 0.99, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-023", "timestamp": "2026-04-10 01:20:00", "case_id": "MP-2026-0527", "source_type": "OSINT Correlation", "event_type": "Covert Messaging", "severity": "SUSPICIOUS", "description": "ShadowNet handshake between @void_null07 and @vector_zero exchanging code SYS-K9-BLR", "entity_ids": ["void_null07", "vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar", "evidence_ids": ["OSINT-AN-003"], "confidence": 0.94, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-024", "timestamp": "2026-04-10 15:40:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NORMAL", "description": "Dual monitor terminal benchmark setup photo at WeWork Galaxy", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v04", "location_name": "WeWork Galaxy Residency Road", "evidence_ids": ["IMG-AN-007"], "confidence": 0.98, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-025", "timestamp": "2026-04-10 18:15:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Call with roommate Priya confirming dinner plans at Koramangala quarters (195s)", "entity_ids": ["ananya_nair", "priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block", "evidence_ids": ["CDR-AN-007"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-026", "timestamp": "2026-04-11 11:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Venue Check-in", "severity": "NORMAL", "description": "InstaPhoto location check-in at WeWork Galaxy Residency Road", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v04", "location_name": "WeWork Galaxy Residency Road", "evidence_ids": ["CHK-AN-003"], "confidence": 0.95, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-027", "timestamp": "2026-04-11 11:20:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Call with colleague Rohan discussing upcoming capstone thesis deadline (84s)", "entity_ids": ["ananya_nair", "rohan_sys"], "location_id": "blr_v02", "location_name": "Electronic City Phase 1", "evidence_ids": ["CDR-AN-008"], "confidence": 1.0, "phase": "Inbound Outreach"},
        {"event_id": "EV-AN-028", "timestamp": "2026-04-11 15:40:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Lengthy academic review call with Dr. Menon regarding lab equipment signoff (310s)", "entity_ids": ["ananya_nair", "prof_menon_sys"], "location_id": "blr_v02", "location_name": "Electronic City Phase 1", "evidence_ids": ["CDR-AN-009"], "confidence": 1.0, "phase": "Inbound Outreach"},

        # Phase 3: Digital Sanitization & Hardware Wipe (Apr 12 – Apr 15)
        {"event_id": "EV-AN-029", "timestamp": "2026-04-12 16:15:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Deleted Post", "severity": "CRITICAL", "description": "DELETED POST: @ananya_dev confirmed 20:00 meeting at Indiranagar Roastery with @vector_zero", "entity_ids": ["ananya_nair", "ananya_dev", "vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar Roastery", "evidence_ids": ["POST-AN-006"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-030", "timestamp": "2026-04-12 17:35:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Encrypted VoIP", "severity": "SUSPICIOUS", "description": "CipherCore PBX SIP trunk call to Ananya's primary phone at Indiranagar (360s)", "entity_ids": ["ananya_nair", "vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar 100ft Road", "evidence_ids": ["CDR-AN-010"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-031", "timestamp": "2026-04-12 18:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Venue Check-in", "severity": "NOTABLE", "description": "InstaPhoto check-in at Indiranagar Roastery cafe patio", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v05", "location_name": "Indiranagar Roastery", "evidence_ids": ["CHK-AN-004"], "confidence": 0.95, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-032", "timestamp": "2026-04-12 18:10:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NOTABLE", "description": "iPhone 15 Pro photo of evening coffee table setup before contract review", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v05", "location_name": "Indiranagar Roastery", "evidence_ids": ["IMG-AN-008"], "confidence": 0.98, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-033", "timestamp": "2026-04-12 19:15:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Voice Call", "severity": "NORMAL", "description": "Brief final call to Priya stating she would stay late at lab/coworking (45s)", "entity_ids": ["ananya_nair", "priya_k"], "location_id": "blr_v05", "location_name": "Indiranagar 100ft Road", "evidence_ids": ["CDR-AN-011"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-034", "timestamp": "2026-04-12 19:40:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Deleted Post", "severity": "CRITICAL", "description": "DELETED POST: @ananya_dev mentions contract NDA terms requiring immediate repository wipe", "entity_ids": ["ananya_nair", "ananya_dev"], "location_id": "blr_v05", "location_name": "Indiranagar Roastery", "evidence_ids": ["POST-AN-007"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-035", "timestamp": "2026-04-12 21:05:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "SUSPICIOUS", "description": "Captured iPhone photo showing watermark of confidential aerospace agreement", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v05", "location_name": "Indiranagar Roastery", "evidence_ids": ["IMG-AN-009"], "confidence": 0.98, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-036", "timestamp": "2026-04-12 21:30:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "Hardware Extraction", "severity": "CRITICAL", "description": "Cold storage Sabrent NVMe enclosure plugged in; full repository clone archived", "entity_ids": ["ananya_nair", "DEV-AN-005"], "location_id": "blr_v05", "location_name": "Indiranagar", "evidence_ids": ["DEV-AN-005"], "confidence": 0.94, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-037", "timestamp": "2026-04-12 22:45:00", "case_id": "MP-2026-0527", "source_type": "GitHub / Code", "event_type": "Force-Push Scrub", "severity": "CRITICAL", "description": "Commit f92a10b force-scrubbed proprietary telemetry headers via Netherlands exit node", "entity_ids": ["ananya_nair", "ananyan-dev"], "location_id": "blr_v05", "location_name": "Indiranagar", "evidence_ids": ["GH-AN-003"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-038", "timestamp": "2026-04-12 23:45:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "Disk Encryption Wipe", "severity": "CRITICAL", "description": "LUKS key wipe command executed on ThinkPad P1 Gen 6; primary drive rendered unreadable", "entity_ids": ["ananya_nair", "DEV-AN-001"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["DEV-AN-001"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-039", "timestamp": "2026-04-13 08:15:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "SIM Removal", "severity": "CRITICAL", "description": "Primary OnePlus 12 smartphone powered down; Airtel SIM physically removed in room", "entity_ids": ["ananya_nair", "DEV-AN-002"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["DEV-AN-002"], "confidence": 0.99, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-040", "timestamp": "2026-04-13 16:30:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Venue Check-in", "severity": "NOTABLE", "description": "Last public check-in at Cubbon Park Bamboo Grove from personal profile", "entity_ids": ["ananya_nair", "ananya.n"], "location_id": "blr_v06", "location_name": "Cubbon Park Bamboo Grove", "evidence_ids": ["CHK-AN-005"], "confidence": 0.95, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-041", "timestamp": "2026-04-14 02:10:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "Hardware Extraction", "severity": "CRITICAL", "description": "Raw JTAG programmer flash dump executed on Xilinx FPGA drone telemetry board in Lab 4", "entity_ids": ["ananya_nair", "DEV-AN-004"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["DEV-AN-004"], "confidence": 0.95, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-042", "timestamp": "2026-04-14 13:45:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "CRITICAL", "description": "Galaxy S23 photo showing desoldered EEPROM pins and scraped barcode serials on FPGA", "entity_ids": ["deepak_kernel"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["IMG-AN-010"], "confidence": 0.98, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-043", "timestamp": "2026-04-14 14:00:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Breach Alert", "severity": "SUSPICIOUS", "description": "Deepak Rao posts public alarm regarding scraped FPGA board barcodes in Lab 4", "entity_ids": ["deepak_kernel"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["POST-AN-008"], "confidence": 0.95, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-044", "timestamp": "2026-04-14 20:10:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "CRITICAL", "description": "Anonymous prepaid burner handset (+91-98801-0199) registers first ping at Indiranagar Metro", "entity_ids": ["ananya_nair", "void_null07"], "location_id": "blr_v05", "location_name": "Indiranagar Metro Sector", "evidence_ids": ["CDR-AN-012"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-045", "timestamp": "2026-04-14 20:10:00", "case_id": "MP-2026-0527", "source_type": "OSINT Correlation", "event_type": "Burner Correlation", "severity": "CRITICAL", "description": "Burner IMEI 863920194829104 matches ShadowNet active TLS connection session timestamps", "entity_ids": ["void_null07"], "location_id": "blr_v05", "location_name": "Indiranagar Metro Sector", "evidence_ids": ["OSINT-AN-004"], "confidence": 0.97, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-046", "timestamp": "2026-04-14 23:10:00", "case_id": "MP-2026-0527", "source_type": "GitHub / Code", "event_type": "Branch Force-Deletion", "severity": "CRITICAL", "description": "Commit e77b02c: bit-lab/hypermesh-core repository branch completely purged via Tor exit node", "entity_ids": ["ananya_nair", "void_null07"], "location_id": "blr_v07", "location_name": "Hebbal Lake Transit Hub", "evidence_ids": ["GH-AN-004"], "confidence": 1.0, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-047", "timestamp": "2026-04-15 11:30:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "SUSPICIOUS", "description": "Burner handset brief voice call (24s) routed through Cubbon Park / High Court sector", "entity_ids": ["void_null07", "deepak_kernel"], "location_id": "blr_v06", "location_name": "Cubbon Park / High Court", "evidence_ids": ["CDR-AN-013"], "confidence": 0.95, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-048", "timestamp": "2026-04-15 15:10:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Covert Check-in", "severity": "SUSPICIOUS", "description": "ShadowNet automated location check-in at Hebbal Lake Transit Hub", "entity_ids": ["void_null07"], "location_id": "blr_v07", "location_name": "Hebbal Lake Transit Hub", "evidence_ids": ["CHK-AN-006"], "confidence": 0.90, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-049", "timestamp": "2026-04-15 15:20:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Low-Res Photo", "severity": "NOTABLE", "description": "Nokia 105 640x480 snapshot capturing northern highway flyover pylon", "entity_ids": ["void_null07"], "location_id": "blr_v07", "location_name": "Hebbal Lake Transit Hub", "evidence_ids": ["IMG-AN-011"], "confidence": 0.92, "phase": "Digital Sanitization"},
        {"event_id": "EV-AN-050", "timestamp": "2026-04-15 16:45:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "SUSPICIOUS", "description": "Burner handset coordinates confirmed at Hebbal Flyover North sector (65s call)", "entity_ids": ["void_null07", "vector_zero"], "location_id": "blr_v07", "location_name": "Hebbal Flyover North", "evidence_ids": ["CDR-AN-014"], "confidence": 1.0, "phase": "Digital Sanitization"},

        # Phase 4: Terminal Transit & Radar Corridor (Apr 16 – Apr 17)
        {"event_id": "EV-AN-051", "timestamp": "2026-04-16 17:30:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Traffic ANPR Photo", "severity": "NOTABLE", "description": "Manyata Outer Ring Road surveillance camera frames dark transit SUV moving north", "entity_ids": ["ananya_nair"], "location_id": "blr_v12", "location_name": "Manyata Tech Park North", "evidence_ids": ["IMG-AN-012"], "confidence": 0.94, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-052", "timestamp": "2026-04-16 18:20:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "CRITICAL", "description": "Burner handset cell sector handover confirmed at Yelahanka Airbase Sector", "entity_ids": ["void_null07", "vector_zero"], "location_id": "blr_v11", "location_name": "Yelahanka Airbase Sector", "evidence_ids": ["CDR-AN-015"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-053", "timestamp": "2026-04-16 19:10:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Covert Transmission", "severity": "CRITICAL", "description": "@void_null07 broadcasts final covert transit dispatch heading toward Devanahalli gateway", "entity_ids": ["void_null07"], "location_id": "blr_v08", "location_name": "Devanahalli Logistics Corridor", "evidence_ids": ["POST-AN-009"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-054", "timestamp": "2026-04-16 19:40:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "CRITICAL", "description": "Burner handset voice link (48s) connects through Devanahalli Highway Corridor tower", "entity_ids": ["void_null07", "vector_zero"], "location_id": "blr_v08", "location_name": "Devanahalli Highway Corridor", "evidence_ids": ["CDR-AN-016"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-055", "timestamp": "2026-04-16 19:42:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "FASTAG Camera Photo", "severity": "CRITICAL", "description": "NH-44 Devanahalli Toll Plaza ANPR camera captures vehicle windshield RFID tag reading", "entity_ids": ["ananya_nair"], "location_id": "blr_v08", "location_name": "Devanahalli Logistics Corridor", "evidence_ids": ["IMG-AN-013"], "confidence": 0.99, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-056", "timestamp": "2026-04-16 20:45:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Covert Check-in", "severity": "CRITICAL", "description": "ShadowNet encrypted automated telemetry check-in at Nandi Hills Ridge Overlook", "entity_ids": ["void_null07"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["CHK-AN-007"], "confidence": 0.96, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-057", "timestamp": "2026-04-16 20:50:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Burner Handset Ping", "severity": "CRITICAL", "description": "Burner handset tower ping registered at Nandi Foot Base Station (BLR-TWR-8840)", "entity_ids": ["void_null07", "vector_zero"], "location_id": "blr_v09", "location_name": "Nandi Foot Base Station", "evidence_ids": ["CDR-AN-017"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-058", "timestamp": "2026-04-16 20:55:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "EXIF Photo", "severity": "NOTABLE", "description": "Sony A7M4 photo of dense mountain mist rolling over radar dome facility", "entity_ids": ["void_null07"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["IMG-AN-014"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-059", "timestamp": "2026-04-16 21:14:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "RF Telemetry Beacon", "severity": "CRITICAL", "description": "2.412 GHz autonomous UAV telemetry burst emitted by DJI Matrice RTK remote transponder", "entity_ids": ["void_null07", "DEV-AN-006"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["DEV-AN-006"], "confidence": 0.96, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-060", "timestamp": "2026-04-16 21:14:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Thermal FLIR Photo", "severity": "CRITICAL", "description": "Teledyne FLIR Boson 640 thermal sensor captures drone rotor thermal blooming signature", "entity_ids": ["void_null07"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["IMG-AN-015"], "confidence": 0.97, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-061", "timestamp": "2026-04-16 21:15:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Terminal Tower Ping", "severity": "CRITICAL", "description": "FINAL LKL PING: Burner handset registers terminal transmission on tower BLR-TWR-8841 before powering off", "entity_ids": ["void_null07", "ananya_nair"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Radar Sector", "evidence_ids": ["CDR-AN-018"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-062", "timestamp": "2026-04-16 21:15:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "Hardware Depower", "severity": "CRITICAL", "description": "Nokia 105 burner handset battery removed; RF signal ceases immediately", "entity_ids": ["ananya_nair", "DEV-AN-003"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["DEV-AN-003"], "confidence": 0.98, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-063", "timestamp": "2026-04-17 07:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Observation Gap", "severity": "NORMAL", "description": "Koramangala room observed vacant; bed undisturbed since previous night", "entity_ids": ["priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["DEV-AN-002"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-064", "timestamp": "2026-04-17 09:30:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Alarm Broadcast", "severity": "SUSPICIOUS", "description": "Roommate Priya broadcasts urgent missing person notice on InstaPhoto", "entity_ids": ["priya_k"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["POST-AN-004"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-065", "timestamp": "2026-04-17 11:45:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Lab Alert", "severity": "SUSPICIOUS", "description": "Rohan Sharma alerts faculty that Ananya missed capstone and repository is gone", "entity_ids": ["rohan_sys"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["GH-AN-004"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-066", "timestamp": "2026-04-17 12:00:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Red Herring Photo", "severity": "SUSPICIOUS", "description": "Spoofed tourist photo alleging sighting in Old Manali cafe circulated online", "entity_ids": ["tourist_bot_decoy"], "location_id": "blr_v14", "location_name": "Old Manali, Himachal Pradesh", "evidence_ids": ["IMG-AN-016"], "confidence": 0.25, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-067", "timestamp": "2026-04-17 14:00:00", "case_id": "MP-2026-0527", "source_type": "Social Media", "event_type": "Police Report", "severity": "NORMAL", "description": "BIT Department of CS files formal cybercrime police missing person report", "entity_ids": ["prof_menon_sys"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["POST-AN-001"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-068", "timestamp": "2026-04-17 15:30:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Red Herring Photo", "severity": "SUSPICIOUS", "description": "Scraped beach photo alleging Goa sighting detected with altered EXIF headers", "entity_ids": ["goa_decoy_account"], "location_id": "blr_v14", "location_name": "Anjuna, Goa", "evidence_ids": ["IMG-AN-017"], "confidence": 0.20, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-069", "timestamp": "2026-04-17 16:30:00", "case_id": "MP-2026-0527", "source_type": "OSINT Correlation", "event_type": "Entity Resolution", "severity": "NOTABLE", "description": "Cyber Forensics confirms CipherCore entity operating as unlicensed defense contractor", "entity_ids": ["vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar", "evidence_ids": ["OSINT-AN-005"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-070", "timestamp": "2026-04-17 17:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Police Dispatch", "severity": "NORMAL", "description": "Search teams dispatched along Bellary Road and NH-44 Devanahalli highway corridor", "entity_ids": ["ananya_nair"], "location_id": "blr_v13", "location_name": "Bellary Road Tollway Sector", "evidence_ids": ["CHK-AN-006"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-071", "timestamp": "2026-04-17 18:00:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Subpoena Request", "severity": "NORMAL", "description": "Court order issued to Vodafone SIP trunk carrier regarding incoming Indiranagar calls", "entity_ids": ["vector_zero"], "location_id": "blr_v05", "location_name": "Indiranagar 100ft Road", "evidence_ids": ["CDR-AN-006"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-072", "timestamp": "2026-04-17 19:00:00", "case_id": "MP-2026-0527", "source_type": "Device Artifact", "event_type": "Forensic Imaging", "severity": "NORMAL", "description": "ThinkPad P1 Gen 6 mirrored; SHA-256 hash verifies full LUKS sector entropy loss", "entity_ids": ["DEV-AN-001"], "location_id": "blr_v01", "location_name": "Koramangala 4th Block Housing", "evidence_ids": ["DEV-AN-001"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-073", "timestamp": "2026-04-17 20:00:00", "case_id": "MP-2026-0527", "source_type": "Physical Location", "event_type": "Ridge Inspection", "severity": "NOTABLE", "description": "Chikkaballapur patrol officers discover vehicle tire impressions at Nandi Ridge overlook", "entity_ids": ["ananya_nair"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["CHK-AN-007"], "confidence": 0.95, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-074", "timestamp": "2026-04-17 21:00:00", "case_id": "MP-2026-0527", "source_type": "OSINT Correlation", "event_type": "Identity Cluster", "severity": "NORMAL", "description": "Resolved identity cluster completed: Ananya Nair linked across 4 aliases and 2 phone numbers", "entity_ids": ["ananya_nair", "ananya_dev", "ananya.n", "ananyan-dev", "void_null07"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["OSINT-AN-002"], "confidence": 0.98, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-075", "timestamp": "2026-04-17 22:00:00", "case_id": "MP-2026-0527", "source_type": "Photo / EXIF", "event_type": "Evidence Sealed", "severity": "NORMAL", "description": "Full photographic evidence dossier cataloged with SHA-256 perceptual hashes", "entity_ids": ["ananya_nair"], "location_id": "blr_v02", "location_name": "Electronic City BIT Robotics Lab", "evidence_ids": ["IMG-AN-001"], "confidence": 1.0, "phase": "Terminal Transit"},
        {"event_id": "EV-AN-076", "timestamp": "2026-04-17 23:00:00", "case_id": "MP-2026-0527", "source_type": "Telecommunications", "event_type": "Tactical Summary", "severity": "CRITICAL", "description": "Case dossier finalized: High probability of autonomous drone exfiltration north of Nandi Hills", "entity_ids": ["ananya_nair", "vector_zero"], "location_id": "blr_v09", "location_name": "Nandi Hills Ridge Overlook", "evidence_ids": ["CDR-AN-018"], "confidence": 0.94, "phase": "Terminal Transit"}
    ]
    with open(target_dir / "timeline_events.json", "w", encoding="utf-8") as f:
        json.dump(timeline_events, f, indent=2)

    # ============================================================
    # 12. RESOLVED IDENTITIES (~38 Entities)
    # Target profile: ~38 Entities
    # ============================================================
    resolved_data = {
        "total_profiles_analyzed": 18,
        "resolved_clusters_count": 7,
        "multi_account_clusters_count": 1,
        "confirmed_links_count": 3,
        "ambiguous_links_count": 2,
        "clusters": [
            {
                "canonical_id": "ANANYA_NAIR",
                "canonical_name": "Ananya Nair",
                "is_primary_subject": True,
                "is_target": True,
                "accounts": ["ananya_dev", "ananya.n", "ananyan-dev", "void_null07"],
                "account_count": 4,
                "is_multi_account": True,
                "linked_phones": ["+91-98801-0144", "+91-98801-0199"],
                "linked_emails": ["ananya.nair.sys@fictional-mail.in", "ananya_personal@fictional-mail.in", "anon_blr07@proton-synthetic.me"],
                "linked_devices": ["DEV-AN-001", "DEV-AN-002", "DEV-AN-003", "DEV-AN-005"],
                "confidence": 0.99
            },
            {
                "canonical_id": "VECTOR_ZERO",
                "canonical_name": "Vector Zero / CipherCore",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["vector_zero"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0900"],
                "linked_emails": ["ops@ciphercore-vector.io"],
                "linked_devices": ["DEV-AN-006"],
                "confidence": 0.95
            },
            {
                "canonical_id": "PRIYA_KRISHNAMURTHY",
                "canonical_name": "Priya Krishnamurthy",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["priya_k"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0222"],
                "linked_emails": ["priya.k@biotech-blr.in"],
                "linked_devices": [],
                "confidence": 0.98
            },
            {
                "canonical_id": "ROHAN_SHARMA",
                "canonical_name": "Rohan Sharma",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["rohan_sys"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0333"],
                "linked_emails": ["rohan.sharma@fictional-bit.in"],
                "linked_devices": [],
                "confidence": 0.98
            },
            {
                "canonical_id": "VIKRAM_MENON",
                "canonical_name": "Dr. Vikram S. Menon",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["prof_menon_sys"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0444"],
                "linked_emails": ["vsmenon@bit-dept.ac.in"],
                "linked_devices": [],
                "confidence": 0.99
            },
            {
                "canonical_id": "KAVYA_PATEL",
                "canonical_name": "Kavya Patel",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["kavya_drone_ai"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0555"],
                "linked_emails": ["kavya.patel@aero-blr.in"],
                "linked_devices": [],
                "confidence": 0.95
            },
            {
                "canonical_id": "DEEPAK_RAO",
                "canonical_name": "Deepak Rao",
                "is_primary_subject": False,
                "is_target": False,
                "accounts": ["deepak_kernel"],
                "account_count": 1,
                "is_multi_account": False,
                "linked_phones": ["+91-98801-0777"],
                "linked_emails": ["d_rao@kernel-embed.in"],
                "linked_devices": [],
                "confidence": 0.96
            }
        ],
        "confirmed_links": [
            {"account_a": "ananya_dev", "account_b": "ananya.n", "confidence": 0.99, "rationale": "Shared mobile number +91-98801-0144 and mutual follower corroboration"},
            {"account_a": "ananya_dev", "account_b": "ananyan-dev", "confidence": 0.99, "rationale": "Matching corporate institutional email ananya.nair.sys@fictional-mail.in and repo commit author"},
            {"account_a": "ananyan-dev", "account_b": "void_null07", "confidence": 0.98, "rationale": "Cryptographic GPG Master Key 0x9E4B2F81A07C match on code commits and darknet pings"}
        ]
    }
    with open(target_dir / "resolved_identities.json", "w", encoding="utf-8") as f:
        json.dump(resolved_data, f, indent=2)

    ambiguous_data = {
        "ambiguous_links": [
            {
                "account_a": "void_null07",
                "account_b": "travel_bot_decoy",
                "confidence": 0.18,
                "evidence_count": 1,
                "evidence": [
                    {
                        "type": "REJECTED_RED_HERRING",
                        "detail": "Decoy IP hopping in Manali lacks device hash concordance with Sony ILCE-7M4 camera",
                        "weight": 0.18
                    }
                ],
                "rationale": "REJECTED_RED_HERRING: Decoy IP hopping in Manali lacks device hash concordance with Sony ILCE-7M4 camera"
            },
            {
                "account_a": "ananya_dev",
                "account_b": "aero_recruit_bot",
                "confidence": 0.35,
                "evidence_count": 1,
                "evidence": [
                    {
                        "type": "UNVERIFIED_SOLICITATION",
                        "detail": "Cold recruitment solicitation on technical forum without cryptographic handshake",
                        "weight": 0.35
                    }
                ],
                "rationale": "UNVERIFIED_SOLICITATION: Cold recruitment solicitation on technical forum without cryptographic handshake"
            }
        ]
    }
    with open(target_dir / "ambiguous_links.json", "w", encoding="utf-8") as f:
        json.dump(ambiguous_data, f, indent=2)

    # ============================================================
    # 13. MOVEMENT ANALYSIS & DBSCAN (Bengaluru & NH-44 Corridor)
    # ============================================================
    movement_data = {
        "spatial_clusters": [
            {
                "cluster_id": 0,
                "label": "Koramangala Residential Core",
                "center_lat": 12.9348,
                "center_lon": 77.6252,
                "points_count": 18,
                "first_seen": "2026-03-28 08:30:00",
                "last_seen": "2026-04-13 08:15:00",
                "description": "Student residence quarters and Third Wave Coffee morning routines"
            },
            {
                "cluster_id": 1,
                "label": "Electronic City Robotics Lab",
                "center_lat": 12.8452,
                "center_lon": 77.6602,
                "points_count": 24,
                "first_seen": "2026-03-28 09:15:00",
                "last_seen": "2026-04-14 02:10:00",
                "description": "BIT Robotics Lab hardware testbed and FPGA drone benches"
            },
            {
                "cluster_id": 2,
                "label": "Indiranagar Meeting Corridor",
                "center_lat": 12.9719,
                "center_lon": 77.6412,
                "points_count": 14,
                "first_seen": "2026-04-09 17:35:00",
                "last_seen": "2026-04-14 20:10:00",
                "description": "Confidential NDA dining meeting and initial burner handset activation"
            },
            {
                "cluster_id": 3,
                "label": "Hebbal / Devanahalli Highway Transit",
                "center_lat": 13.1446,
                "center_lon": 77.6518,
                "points_count": 12,
                "first_seen": "2026-04-15 15:10:00",
                "last_seen": "2026-04-16 19:42:00",
                "description": "Northbound transit via NH-44 expressway and toll plaza ANPR camera"
            },
            {
                "cluster_id": 4,
                "label": "Nandi Hills Ridge Overlook (LKL Candidate)",
                "center_lat": 13.3702,
                "center_lon": 77.6835,
                "points_count": 8,
                "first_seen": "2026-04-16 20:45:00",
                "last_seen": "2026-04-16 21:15:00",
                "description": "Terminal radar sector ping, thermal drone burst, and complete signal termination"
            }
        ],
        "trajectory": [
            [12.9345, 77.6258],
            [12.8452, 77.6602],
            [12.9352, 77.6245],
            [12.9715, 77.6074],
            [12.9719, 77.6412],
            [12.9763, 77.5929],
            [13.0410, 77.5910],
            [13.1007, 77.5963],
            [13.2483, 77.7126],
            [13.3412, 77.6890],
            [13.3702, 77.6835]
        ],
        "candidate_lkl": {
            "name": "Nandi Hills Ridge Overlook",
            "latitude": 13.3702,
            "longitude": 77.6835,
            "timestamp": "2026-04-16 21:15:00",
            "confidence": 0.945,
            "evidence_basis": "Final cell tower sector ping (BLR-TWR-8841), 2.4 GHz drone beacon emission, and FASTAG trajectory heading north"
        }
    }
    with open(target_dir / "movement_analysis.json", "w", encoding="utf-8") as f:
        json.dump(movement_data, f, indent=2)

    # ============================================================
    # 14. HYPOTHESES EVALUATION (Tailored to Ananya Case)
    # ============================================================
    hypotheses = [
        {
            "hypothesis_id": "HYP-01-CIPHERCORE-UAV-EXFILTRATION",
            "id": "H1",
            "title": "Coercive Corporate / Defense UAV Exfiltration by CipherCore",
            "status": "SUPPORTED",
            "confidence_score": 0.88,
            "confidence": 0.88,
            "prior": 0.30,
            "posterior": 0.88,
            "summary": "Subject recruited or coerced under stealth defense NDA by CipherCore; hardware and firmware extracted northbound towards Nandi Hills.",
            "supporting_evidence": [
                {
                    "item": "Inbound Pitch and Deleted Meeting",
                    "detail": "Deleted post POST-AN-006 confirms confidential meeting with @vector_zero at Indiranagar Roastery on April 14.",
                    "weight": 0.85
                },
                {
                    "item": "Encrypted PBX Telecommunications",
                    "detail": "CDR-AN-010 registers 360-second encrypted PBX call from CipherCore SIP trunk (+91-98801-0900).",
                    "weight": 0.88
                },
                {
                    "item": "Northbound Highway ANPR Tracking",
                    "detail": "FASTAG toll camera (IMG-AN-013) captured transport vehicle passing Devanahalli toll plaza northbound at 19:42 UTC.",
                    "weight": 0.92
                },
                {
                    "item": "Terminal RF Telemetry Beacon",
                    "detail": "Teledyne FLIR (IMG-AN-015) and 2.412 GHz autonomous UAV telemetry beacon recorded at Nandi Ridge before tower shut down.",
                    "weight": 0.95
                }
            ],
            "contradicting_evidence": [
                {
                    "item": "Voluntary Contract Sign-Off",
                    "detail": "Draft consulting agreement indicates subject voluntarily signed NDA for autonomous mesh routing."
                }
            ],
            "recommended_actions": [
                "Issue urgent court order to Vodafone and Airtel for subscriber records of CipherCore PBX SIP trunk (+91-98801-0900).",
                "Deploy Chikkaballapur Search and Rescue teams to Nandi Hills Ridge Radar Sector (13.3702, 77.6835).",
                "Subpoena Indiranagar Roastery high-definition surveillance feeds for April 14, 18:00-20:00 IST."
            ]
        },
        {
            "hypothesis_id": "HYP-02-VOLUNTARY-INDUSTRY-DEFECTION",
            "id": "H2",
            "title": "Voluntary Covert Industry Defection and Self-Extraction",
            "status": "STRONGLY_SUPPORTED",
            "confidence_score": 0.92,
            "confidence": 0.92,
            "prior": 0.25,
            "posterior": 0.92,
            "summary": "Ananya deliberately scrubbed her digital footprint (LUKS full-disk wipe, force-deleted git branches, SIM removal) to transition to an unmonitored private defense research facility.",
            "supporting_evidence": [
                {
                    "item": "LUKS Full-Disk Cryptographic Wipe",
                    "detail": "Workstation (DEV-AN-001) mirrored with all LUKS encryption headers permanently erased via /dev/urandom.",
                    "weight": 0.95
                },
                {
                    "item": "Destructive Repository Force-Deletion",
                    "detail": "bit-lab/hypermesh-core repository branch deleted using personal admin token routed over Tor exit node.",
                    "weight": 0.90
                },
                {
                    "item": "Clean SIM Extraction and Physical Staging",
                    "detail": "Airtel postpaid SIM (+91-98801-0144) was extracted and left cleanly on her Koramangala room desk.",
                    "weight": 0.92
                },
                {
                    "item": "Simultaneous Burner Activation",
                    "detail": "Prepaid Nokia 105 handset (+91-98801-0199) activated concurrently at Indiranagar with zero prior social footprint.",
                    "weight": 0.88
                }
            ],
            "contradicting_evidence": [
                {
                    "item": "Faculty Warning Advisory",
                    "detail": "Dr. Kavya Patel published advisories warning robotics students about predatory recruiters posing as stealth defense ventures."
                }
            ],
            "recommended_actions": [
                "Audit institutional GitHub enterprise access logs for Tor exit node IP clusters matching the admin token deletion.",
                "Analyze SHA-256 entropy on mirrored workstation drive DEV-AN-001 to identify potential cold-boot remnants.",
                "Cross-reference prepaid SIM cash recharge records at Koramangala retail vendor."
            ]
        },
        {
            "hypothesis_id": "HYP-03-ACADEMIC-BURNOUT-SABBATICAL",
            "id": "H3",
            "title": "Academic Burnout / Personal Sabbatical (Disproven Red Herring)",
            "status": "CONTRADICTED_RED_HERRING",
            "confidence_score": 0.12,
            "confidence": 0.12,
            "prior": 0.25,
            "posterior": 0.12,
            "summary": "Initial suspicion that Ananya took an unannounced sabbatical to decompress from doctoral research pressures is refuted by deliberate hardware destruction and covert communications.",
            "supporting_evidence": [
                {
                    "item": "Social Reflection on Deadlines",
                    "detail": "Cubbon Park post POST-AN-004 reflects on hectic capstone milestone schedules and burnout.",
                    "weight": 0.40
                }
            ],
            "contradicting_evidence": [
                {
                    "item": "JTAG Hardware EEPROM Scrubbing",
                    "detail": "Testbench FPGA chips were desoldered, flashed with null bytes, and PCB serial numbers scraped clean."
                },
                {
                    "item": "Exclusive Burner Telecommunications",
                    "detail": "Burner handset was used exclusively to communicate with defense recruiter PBX, not friends or family."
                },
                {
                    "item": "Destructive Git Sabotage",
                    "detail": "Repository force-deletion destroyed shared team research, inconsistent with a simple sabbatical."
                }
            ],
            "recommended_actions": [
                "Deprioritize student sabbatical inquiries; classify case under technical asset extraction."
            ]
        },
        {
            "hypothesis_id": "HYP-04-OPPORTUNISTIC-KIDNAPPING",
            "id": "H4",
            "title": "Opportunistic Street Kidnapping / Foul Play (Weakly Supported)",
            "status": "WEAKLY_SUPPORTED",
            "confidence_score": 0.18,
            "confidence": 0.18,
            "prior": 0.20,
            "posterior": 0.18,
            "summary": "Hypothesis of street abduction during transit is contradicted by voluntary PGP key handshakes and deliberate digital footprint sanitization.",
            "supporting_evidence": [
                {
                    "item": "Robotics Lab Hardware Theft",
                    "detail": "High-value custom sensor boards were removed without BIT department sign-off.",
                    "weight": 0.50
                },
                {
                    "item": "Cellular Signal Termination",
                    "detail": "Burner handset connection ceased abruptly at remote ridge overlook.",
                    "weight": 0.70
                }
            ],
            "contradicting_evidence": [
                {
                    "item": "Cryptographic PGP Signature",
                    "detail": "Escrow confirmation message was signed with Ananya's private PGP key, verifying keyholder intent."
                },
                {
                    "item": "Pre-arranged Transport Route",
                    "detail": "FASTAG toll records corroborate a direct, non-erratic transit path along NH-44 highway."
                }
            ],
            "recommended_actions": [
                "Maintain radar overlook search while tracking secondary financial escrow release addresses."
            ]
        }
    ]
    with open(target_dir / "hypotheses_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(hypotheses, f, indent=2)

    # ============================================================
    # 15. EVALUATION METRICS & GROUND TRUTH
    # ============================================================
    evaluation = {
        "ground_truth": {
            "case_id": "MP-2026-0527",
            "subject": "Ananya Nair",
            "last_known_location": "Nandi Hills Ridge Overlook",
            "coordinates": [13.3702, 77.6835],
            "terminal_timestamp": "2026-04-16 21:15:00",
            "primary_hypothesis": "H2: Voluntary Covert Industry Defection & Self-Extraction",
            "secondary_hypothesis": "H1: Coercive Corporate/Defense UAV Exfiltration by CipherCore"
        },
        "metrics": {
            "precision": 0.942,
            "recall": 0.918,
            "f1": 0.930,
            "accuracy": 0.936,
            "auc_roc": 0.965,
            "coverage": 0.895,
            "confidence_score": 0.924
        }
    }
    with open(target_dir / "evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2)

    # ============================================================
    # 16. GRAPH GENERATION (NetworkX -> Vis.js HTML)
    # ============================================================
    from graph.build_networkx import build_investigation_graph
    G = build_investigation_graph(target_dir)

    # Save Graph Analytics
    analytics = {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "density": round(nx.density(G), 4),
        "target_centrality": 0.884,
        "poi_centrality": 0.742
    }
    with open(target_dir / "graph_analytics.json", "w", encoding="utf-8") as f:
        json.dump(analytics, f, indent=2)

    # Vis.js node conversion
    vis_nodes = []
    vis_edges = []
    node_color_map = {
        "Person": "#00E5A3",
        "Account": "#3A6BFF",
        "Phone": "#00D2D3",
        "Location": "#EC4899",
        "Post": "#A855F7",
        "Photo": "#F5B942",
        "Device": "#F97316",
        "GitCommit": "#10B981",
        "OSINTCorrelation": "#E11D48"
    }

    for n, d in G.nodes(data=True):
        ntype = d.get("node_type", "Unknown")
        color = node_color_map.get(ntype, "#64748B")
        if d.get("is_target", False):
            color = "#FF4757"
        vis_nodes.append({
            "id": str(n),
            "label": str(d.get("label", n)),
            "group": ntype,
            "color": color,
            "size": 22 if d.get("is_target") else 14
        })

    for u, v, k, d in G.edges(keys=True, data=True):
        vis_edges.append({
            "from": str(u),
            "to": str(v),
            "label": str(d.get("edge_type", "")),
            "color": {"color": "rgba(100, 116, 139, 0.4)"}
        })

    # Render Vis.js Stationary HTML
    vis_html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Ananya Nair Investigation Graph</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; background: #0E1231; overflow: hidden; }}
    #network {{ width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="network"></div>
  <script>
    var nodes = new vis.DataSet({json.dumps(vis_nodes)});
    var edges = new vis.DataSet({json.dumps(vis_edges)});
    var container = document.getElementById('network');
    var data = {{ nodes: nodes, edges: edges }};
    var options = {{
      nodes: {{
        shape: 'dot',
        font: {{ color: '#FFFFFF', size: 12, face: 'Inter' }},
        borderWidth: 2
      }},
      edges: {{
        arrows: 'to',
        font: {{ color: '#98A7CE', size: 10, align: 'middle' }},
        smooth: {{ type: 'continuous' }}
      }},
      physics: {{
        stabilization: {{ iterations: 120 }},
        barnesHut: {{ gravitationalConstant: -3000, springLength: 120 }}
      }}
    }};
    var network = new vis.Network(container, data, options);
  </script>
</body>
</html>"""
    with open(target_dir / "investigation_graph_physics.html", "w", encoding="utf-8") as f:
        f.write(vis_html_content)
    with open(target_dir / "investigation_graph_hierarchical.html", "w", encoding="utf-8") as f:
        f.write(vis_html_content)

    # ============================================================
    # 17. FOLIUM MAP GENERATION (Bengaluru / NH-44 / Nandi Hills)
    # ============================================================
    m = folium.Map(
        location=[13.12, 77.65],
        zoom_start=10,
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="OpenStreetMap"
    )
    dark_css = """
    <style>
        .leaflet-container { background-color: #0E1231 !important; font-family: 'Inter', sans-serif !important; }
        .leaflet-tile-pane { filter: brightness(0.65) invert(1) contrast(2.8) hue-rotate(200deg) saturate(0.35) brightness(0.7) !important; }
        .leaflet-popup-content-wrapper, .leaflet-popup-tip { background: #1A2254 !important; color: #FFFFFF !important; border: 1px solid #2C3979 !important; border-radius: 8px !important; font-size: 11px !important; }
        .leaflet-control-attribution { display: none !important; }
    </style>
    """
    m.get_root().html.add_child(folium.Element(dark_css))

    # Add trajectory
    folium.PolyLine(
        movement_data["trajectory"],
        color="#3A6BFF",
        weight=3,
        opacity=0.8,
        dash_array="6, 6"
    ).add_to(m)

    # Add markers
    for v in venues:
        is_lkl = "blr_v09" in v["id"]
        icon_color = "red" if is_lkl else "blue"
        folium.CircleMarker(
            location=[v["latitude"], v["longitude"]],
            radius=9 if is_lkl else 6,
            color="#FF4757" if is_lkl else "#00E5A3",
            fill=True,
            fill_color="#FF4757" if is_lkl else "#00E5A3",
            fill_opacity=0.85,
            popup=f"<b>{v['name']}</b><br/>{v['category']}<br/>{v['address']}"
        ).add_to(m)

    m.save(str(target_dir / "investigation_map.html"))

    # Also generate overview corridor map
    from generator.generate_overview_corridor_maps import generate_all_corridor_maps
    generate_all_corridor_maps()

    print(f"Case MP-2026-0527 (Ananya Nair) generated successfully at: {target_dir}")
    print(f"  Evidence: 9 posts, 18 calls, 7 checkins, 17 photos, 6 devices, 4 commits, 5 osint links = 66 total")
    print(f"  Timeline Events: {len(timeline_events)} structured events")
    print(f"  Venues: {len(venues)} locations")
    print(f"  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return target_dir

if __name__ == "__main__":
    generate_ananya_dataset()
