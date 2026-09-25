"""
Synthetic Data Generator for Case MP-2026-0527: Ananya Nair (Bengaluru, India).
Generates complete, internally consistent forensic investigation dataset:
- Case Bible (JSON) with full metadata and venues
- Profiles (JSON) for all subjects, POIs, and contacts
- Posts (CSV) with hashtags, mentions, deleted status, and timestamps
- Call Detail Records (CSV) with tower locations and sector pings
- Physical Check-ins (CSV) with venue IDs and coordinates
- Phones (CSV) with registration info and handset links
- Social Connections (CSV)
- Photos & EXIF metadata (JSON)
- Resolved Identities (JSON) with canonical cluster PERSON_ANANYA_NAIR
- Ambiguous Links (JSON)
- Movement Analysis & DBSCAN (JSON)
- Hypotheses Evaluation (JSON)
- Evaluation Metrics & Ground Truth (JSON)
- Real NetworkX Investigation Graph -> High-performance stationary Vis.js HTML files
- Graph Analytics (JSON)
- Interactive Folium Tactical Map (Bengaluru / Nandi Hills)
- Interactive Overview Corridor Map
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

    # 1. CASE BIBLE & VENUES
    case_bible = {
        "case_metadata": {
            "case_id": "MP-2026-0527",
            "investigation_title": "Disappearance of Ananya Nair",
            "status": "OPEN",
            "date_reported": "2026-04-18T09:00:00Z",
            "assigned_team": "Central Cyber Forensics & OSINT Squad",
            "jurisdiction": "Bengaluru Central / Electronic City Division"
        },
        "missing_person": {
            "full_name": "Ananya Nair",
            "age": 22,
            "pronouns": "she/her",
            "occupation": "Software Engineering Student & Open-Source Contributor",
            "institution": "Bengaluru Institute of Technology",
            "last_seen_date": "2026-04-16T21:15:00Z",
            "last_seen_location_name": "Nandi Hills Ridge Overlook",
            "last_seen_coordinates": {
                "latitude": 13.3702,
                "longitude": 77.6835
            },
            "routine_description": (
                "Final-year B.Tech Computer Science student. Daily commute between Koramangala "
                "student housing and Electronic City tech campus. Worked remote shifts from "
                "Indiranagar cafes on Thursdays. Disappeared during final capstone deployment week."
            )
        },
        "digital_identities": [
            {
                "platform": "ChirpNet",
                "handle": "ananya_dev",
                "display_name": "Ananya Nair | Systems & AI",
                "account_type": "primary",
                "status": "active",
                "bio": "CS Senior @ BIT Bengaluru. Distributed ML, kernels, Rust. Mail: ananya.nair.sys@fictional-mail.in",
                "email": "ananya.nair.sys@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "InstaPhoto",
                "handle": "ananya.n",
                "display_name": "Ananya N.",
                "account_type": "variant_alias",
                "status": "active",
                "bio": "filter coffee, terminal windows & western ghats treks",
                "email": "ananya_personal@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "CodeHub",
                "handle": "ananyan-dev",
                "display_name": "Ananya Nair",
                "account_type": "dormant_developer",
                "status": "active",
                "bio": "Compilers & distributed storage contributor",
                "email": "ananya.nair.sys@fictional-mail.in",
                "phone_reference": "+91-98801-0144"
            },
            {
                "platform": "ShadowNet",
                "handle": "void_null07",
                "display_name": "null_ptr",
                "account_type": "covert_burner",
                "status": "active",
                "bio": "ephemeral nodes & cold corridors",
                "email": "anon_blr07@proton-synthetic.me",
                "phone_reference": "+91-98801-0199"
            }
        ],
        "venues": [
            {"id": "blr_v01", "name": "Koramangala 4th Block Housing", "category": "Residence", "latitude": 12.9345, "longitude": 77.6258, "address": "Koramangala 4th Block, Bengaluru"},
            {"id": "blr_v02", "name": "Electronic City Tech Campus", "category": "Academic", "latitude": 12.8452, "longitude": 77.6602, "address": "Electronics City Phase 1, Hosur Road, Bengaluru"},
            {"id": "blr_v03", "name": "Third Wave Coffee Koramangala", "category": "Cafe", "latitude": 12.9352, "longitude": 77.6245, "address": "80 Feet Road, 4th Block, Koramangala"},
            {"id": "blr_v04", "name": "Indiranagar Roastery", "category": "Cafe/Meeting", "latitude": 12.9719, "longitude": 77.6412, "address": "100 Feet Road, Indiranagar, Bengaluru"},
            {"id": "blr_v05", "name": "Cubbon Park Bamboo Grove", "category": "Park", "latitude": 12.9763, "longitude": 77.5929, "address": "Kasturba Road, Bengaluru"},
            {"id": "blr_v06", "name": "Hebbal Lake Watchtower", "category": "Transit/Observation", "latitude": 13.0410, "longitude": 77.5910, "address": "Bellary Road, Hebbal, Bengaluru"},
            {"id": "blr_v07", "name": "Nandi Hills Ridge Overlook", "category": "Scenic/Terminal", "latitude": 13.3702, "longitude": 77.6835, "address": "Nandi Hills Ridge, Chikkaballapur District"}
        ]
    }
    with open(target_dir / "case_bible.json", "w", encoding="utf-8") as f:
        json.dump(case_bible, f, indent=2)

    # 2. PROFILES
    profiles = [
        {
            "account_id": "acc_target_an_01",
            "handle": "ananya_dev",
            "display_name": "Ananya Nair | Systems & AI",
            "platform": "ChirpNet",
            "account_type": "primary",
            "bio": "CS Senior @ BIT Bengaluru. Distributed ML, kernels, Rust. Mail: ananya.nair.sys@fictional-mail.in",
            "email": "ananya.nair.sys@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 2840,
            "following_count": 310,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_02",
            "handle": "ananya.n",
            "display_name": "Ananya N.",
            "platform": "InstaPhoto",
            "account_type": "personal",
            "bio": "filter coffee, terminal windows & western ghats treks",
            "email": "ananya_personal@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 940,
            "following_count": 420,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_03",
            "handle": "ananyan-dev",
            "display_name": "Ananya Nair",
            "platform": "CodeHub",
            "account_type": "portfolio",
            "bio": "Compilers & distributed storage contributor",
            "email": "ananya.nair.sys@fictional-mail.in",
            "phone": "+91-98801-0144",
            "is_private": False,
            "followers_count": 182,
            "following_count": 45,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_target_an_04",
            "handle": "void_null07",
            "display_name": "null_ptr",
            "platform": "ShadowNet",
            "account_type": "covert_burner",
            "bio": "ephemeral nodes & cold corridors",
            "email": "anon_blr07@proton-synthetic.me",
            "phone": "+91-98801-0199",
            "is_private": True,
            "followers_count": 8,
            "following_count": 14,
            "real_name_reference": "Ananya Nair",
            "is_target_identity": True
        },
        {
            "account_id": "acc_cont_01",
            "handle": "vector_zero",
            "display_name": "Vector Zero",
            "platform": "ChirpNet",
            "account_type": "poi",
            "bio": "Autonomous intelligence architect. Stealth protocol recruiter.",
            "email": "recruiter@vector-zero.io",
            "phone": "+91-98801-0900",
            "is_private": False,
            "followers_count": 4120,
            "following_count": 180,
            "real_name_reference": "Vector Zero",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_02",
            "handle": "priya_k",
            "display_name": "Priya Krishnamurthy",
            "platform": "InstaPhoto",
            "account_type": "roommate",
            "bio": "Biotech grad @ IISc · Ananya's flatmate",
            "email": "priya.k@biotech-blr.in",
            "phone": "+91-98801-0222",
            "is_private": True,
            "followers_count": 620,
            "following_count": 510,
            "real_name_reference": "Priya Krishnamurthy",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_03",
            "handle": "rohan_tech",
            "display_name": "Rohan Sharma",
            "platform": "ChirpNet",
            "account_type": "colleague",
            "bio": "Fullstack engineer & capstone partner @ BIT",
            "email": "rohan.sharma@fictional-bit.in",
            "phone": "+91-98801-0333",
            "is_private": False,
            "followers_count": 340,
            "following_count": 290,
            "real_name_reference": "Rohan Sharma",
            "is_target_identity": False
        },
        {
            "account_id": "acc_cont_04",
            "handle": "prof_menon_sys",
            "display_name": "Prof. K. Menon",
            "platform": "ChirpNet",
            "account_type": "faculty",
            "bio": "Chair of Distributed Systems & CS Dept @ BIT",
            "email": "kmenon@bit-dept.ac.in",
            "phone": "+91-98801-0444",
            "is_private": False,
            "followers_count": 1280,
            "following_count": 140,
            "real_name_reference": "Prof. K. Menon",
            "is_target_identity": False
        }
    ]
    with open(target_dir / "profiles.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)

    # 3. POSTS
    posts = [
        {"post_id": "P-101", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-03-28 09:15:00 UTC", "timestamp_utc_iso": "2026-03-28T09:15:00Z", "text": "Finally resolved race conditions in the distributed raft consensus module. Bengaluru rain making debugging bearable.", "hashtags": "#distributed #raft #rust", "mentions": "@rohan_tech", "location_tag": "Koramangala 4th Block", "likes": 42, "photo_id": "PH-701", "deleted": False, "sentiment_label": "POSITIVE"},
        {"post_id": "P-102", "account": "ananya.n", "platform": "InstaPhoto", "timestamp_raw": "2026-04-01 14:20:00 UTC", "timestamp_utc_iso": "2026-04-01T14:20:00Z", "text": "Hustle at Electronic City campus. Final semester project presentation in two weeks.", "hashtags": "#campus #capstone", "mentions": "@priya_k", "location_tag": "Electronic City Tech Campus", "likes": 68, "photo_id": None, "deleted": False, "sentiment_label": "NEUTRAL"},
        {"post_id": "P-103", "account": "vector_zero", "platform": "ChirpNet", "timestamp_raw": "2026-04-03 18:40:00 UTC", "timestamp_utc_iso": "2026-04-03T18:40:00Z", "text": "@ananya_dev Reviewed your distributed cache benchmarks. Exceptional architectural depth. We have an off-grid R&D initiative in Karnataka. Check direct dispatch.", "hashtags": "#stealth #ai #recruiting", "mentions": "@ananya_dev", "location_tag": "Indiranagar", "likes": 12, "photo_id": None, "deleted": False, "sentiment_label": "NEUTRAL"},
        {"post_id": "P-104", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-05 22:10:00 UTC", "timestamp_utc_iso": "2026-04-05T22:10:00Z", "text": "Some opportunities require uncoupling from conventional academic trajectories. Contemplating the next pivot.", "hashtags": "#career #reflection", "mentions": None, "location_tag": "Indiranagar 100ft Rd", "likes": 28, "photo_id": None, "deleted": False, "sentiment_label": "SUSPICIOUS"},
        {"post_id": "P-105", "account": "void_null07", "platform": "ShadowNet", "timestamp_raw": "2026-04-09 23:45:00 UTC", "timestamp_utc_iso": "2026-04-09T23:45:00Z", "text": "Keys rotated. Secondary handset provisioned. Signal clear on encrypted uplink.", "hashtags": "#covert #pgp", "mentions": None, "location_tag": "Hebbal Junction", "likes": 3, "photo_id": None, "deleted": False, "sentiment_label": "COVERT"},
        {"post_id": "P-106", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-12 16:30:00 UTC", "timestamp_utc_iso": "2026-04-12T16:30:00Z", "text": "Meeting client representative at Indiranagar Roastery tonight at 8 PM to finalize research contract NDA.", "hashtags": "#contract #nda", "mentions": "@vector_zero", "location_tag": "Indiranagar Roastery", "likes": 15, "photo_id": "PH-702", "deleted": True, "sentiment_label": "CRITICAL_DELETED"},
        {"post_id": "P-107", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-12 19:15:00 UTC", "timestamp_utc_iso": "2026-04-12T19:15:00Z", "text": "Contract terms require complete radio silence for first quarter. Laptop transitioning to cold storage.", "hashtags": "#stealth", "mentions": None, "location_tag": "Indiranagar Roastery", "likes": 9, "photo_id": None, "deleted": True, "sentiment_label": "CRITICAL_DELETED"},
        {"post_id": "P-108", "account": "ananya_dev", "platform": "ChirpNet", "timestamp_raw": "2026-04-13 08:00:00 UTC", "timestamp_utc_iso": "2026-04-13T08:00:00Z", "text": "Deleted previous updates regarding client agreement.", "hashtags": None, "mentions": None, "location_tag": "Indiranagar", "likes": 4, "photo_id": None, "deleted": True, "sentiment_label": "CRITICAL_DELETED"},
        {"post_id": "P-109", "account": "priya_k", "platform": "InstaPhoto", "timestamp_raw": "2026-04-17 11:00:00 UTC", "timestamp_utc_iso": "2026-04-17T11:00:00Z", "text": "Has anyone seen @ananya_dev? Her phone has been switched off since Thursday night and she didn't attend the capstone review.", "hashtags": "#missing #help", "mentions": "@ananya_dev", "location_tag": "Koramangala", "likes": 142, "photo_id": None, "deleted": False, "sentiment_label": "ALARM"},
        {"post_id": "P-110", "account": "rohan_tech", "platform": "ChirpNet", "timestamp_raw": "2026-04-17 13:20:00 UTC", "timestamp_utc_iso": "2026-04-17T13:20:00Z", "text": "@prof_menon_sys We could not present the distributed raft module. Ananya did not arrive and her Git commit log abruptly ceased Thursday night.", "hashtags": "#bit #capstone", "mentions": "@prof_menon_sys;@ananya_dev", "location_tag": "Electronic City Tech Campus", "likes": 35, "photo_id": None, "deleted": False, "sentiment_label": "ALARM"}
    ]
    posts_df = pd.DataFrame(posts)
    posts_df.to_csv(target_dir / "posts.csv", index=False)

    # 4. CALL DETAIL RECORDS (CDR)
    calls = [
        {"call_id": "CDR-901", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0222", "call_type": "Voice", "timestamp_utc": "2026-04-11 18:30:00", "duration_sec": 145, "cell_tower_id": "BLR-TWR-401", "cell_tower_sector": "Koramangala 4th Block", "tower_latitude": 12.9345, "tower_longitude": 77.6258},
        {"call_id": "CDR-902", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0333", "call_type": "Voice", "timestamp_utc": "2026-04-12 10:15:00", "duration_sec": 84, "cell_tower_id": "BLR-TWR-102", "cell_tower_sector": "Electronic City Phase 1", "tower_latitude": 12.8399, "tower_longitude": 77.6770},
        {"call_id": "CDR-903", "caller_number": "+91-98801-0144", "receiver_number": "+91-98801-0900", "call_type": "Voice", "timestamp_utc": "2026-04-12 17:45:00", "duration_sec": 210, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar 100ft Road", "tower_latitude": 12.9719, "tower_longitude": 77.6412},
        {"call_id": "CDR-904", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-14 20:30:00", "duration_sec": 35, "cell_tower_id": "BLR-TWR-504", "cell_tower_sector": "Indiranagar Metro Sector", "tower_latitude": 12.9784, "tower_longitude": 77.6385},
        {"call_id": "CDR-905", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-15 14:10:00", "duration_sec": 42, "cell_tower_id": "BLR-TWR-712", "cell_tower_sector": "Hebbal Flyover North", "tower_latitude": 13.0358, "tower_longitude": 77.5970},
        {"call_id": "CDR-906", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 19:40:00", "duration_sec": 60, "cell_tower_id": "BLR-TWR-810", "cell_tower_sector": "Devanahalli Highway Corridor", "tower_latitude": 13.2483, "tower_longitude": 77.7126},
        {"call_id": "CDR-907", "caller_number": "+91-98801-0199", "receiver_number": "+91-98801-0900", "call_type": "Burner Handset Ping", "timestamp_utc": "2026-04-16 21:15:00", "duration_sec": 18, "cell_tower_id": "BLR-TWR-8841", "cell_tower_sector": "Nandi Hills Ridge Sector", "tower_latitude": 13.3702, "tower_longitude": 77.6835}
    ]
    calls_df = pd.DataFrame(calls)
    calls_df.to_csv(target_dir / "call_records.csv", index=False)

    # 5. CHECK-INS
    checkins = [
        {"checkin_id": "CHK-501", "account": "ananya_dev", "venue_id": "blr_v03", "venue_name": "Third Wave Coffee Koramangala", "timestamp_utc": "2026-04-08 11:30:00", "latitude": 12.9352, "longitude": 77.6245, "platform": "ChirpNet"},
        {"checkin_id": "CHK-502", "account": "ananya.n", "venue_id": "blr_v02", "venue_name": "Electronic City Tech Campus", "timestamp_utc": "2026-04-10 14:00:00", "latitude": 12.8452, "longitude": 77.6602, "platform": "InstaPhoto"},
        {"checkin_id": "CHK-503", "account": "ananya.n", "venue_id": "blr_v04", "venue_name": "Indiranagar Roastery", "timestamp_utc": "2026-04-12 18:00:00", "latitude": 12.9719, "longitude": 77.6412, "platform": "InstaPhoto"},
        {"checkin_id": "CHK-504", "account": "ananya_dev", "venue_id": "blr_v05", "venue_name": "Cubbon Park Bamboo Grove", "timestamp_utc": "2026-04-13 16:45:00", "latitude": 12.9763, "longitude": 77.5929, "platform": "ChirpNet"},
        {"checkin_id": "CHK-505", "account": "void_null07", "venue_id": "blr_v06", "venue_name": "Hebbal Lake Watchtower", "timestamp_utc": "2026-04-15 15:20:00", "latitude": 13.0410, "longitude": 77.5910, "platform": "ShadowNet"},
        {"checkin_id": "CHK-506", "account": "void_null07", "venue_id": "blr_v07", "venue_name": "Nandi Hills Ridge Overlook", "timestamp_utc": "2026-04-16 20:50:00", "latitude": 13.3702, "longitude": 77.6835, "platform": "ShadowNet"}
    ]
    checkins_df = pd.DataFrame(checkins)
    checkins_df.to_csv(target_dir / "checkins.csv", index=False)

    # 6. PHONES
    phones = [
        {"phone_number": "+91-98801-0144", "registered_owner": "Ananya Nair", "account_link_hint": "ananya_dev", "carrier": "Airtel Karnataka", "plan_type": "Postpaid", "status": "Suspended / Offline", "first_seen": "2024-08-01", "last_seen": "2026-04-12"},
        {"phone_number": "+91-98801-0199", "registered_owner": "Cash Purchase (Anonymous SIM)", "account_link_hint": "void_null07", "carrier": "Jio Prepaid", "plan_type": "Prepaid Burner", "status": "De-registered after 21:15 UTC", "first_seen": "2026-04-14", "last_seen": "2026-04-16"},
        {"phone_number": "+91-98801-0900", "registered_owner": "Vector Zero Systems Ltd", "account_link_hint": "vector_zero", "carrier": "Vi Business", "plan_type": "Corporate Encrypted", "status": "Active", "first_seen": "2025-11-15", "last_seen": "2026-04-18"},
        {"phone_number": "+91-98801-0222", "registered_owner": "Priya Krishnamurthy", "account_link_hint": "priya_k", "carrier": "Airtel Karnataka", "plan_type": "Postpaid", "status": "Active", "first_seen": "2024-06-10", "last_seen": "2026-04-18"},
        {"phone_number": "+91-98801-0333", "registered_owner": "Rohan Sharma", "account_link_hint": "rohan_tech", "carrier": "Jio Karnataka", "plan_type": "Prepaid", "status": "Active", "first_seen": "2024-08-20", "last_seen": "2026-04-18"}
    ]
    pd.DataFrame(phones).to_csv(target_dir / "phones.csv", index=False)

    # 7. SOCIAL CONNECTIONS
    connections = [
        {"source": "ananya_dev", "target": "vector_zero", "relationship_type": "CONTACTED", "weight": 1.0, "context": "Inbound recruiting pitch regarding raft distributed benchmarks"},
        {"source": "vector_zero", "target": "ananya_dev", "relationship_type": "MENTIONS", "weight": 0.9, "context": "Public commendation of cache repo"},
        {"source": "ananya_dev", "target": "priya_k", "relationship_type": "FOLLOWS", "weight": 1.0, "context": "Flatmate & roommate connection"},
        {"source": "ananya_dev", "target": "rohan_tech", "relationship_type": "FOLLOWS", "weight": 1.0, "context": "Capstone engineering partner"},
        {"source": "ananya_dev", "target": "prof_menon_sys", "relationship_type": "FOLLOWS", "weight": 0.8, "context": "Academic advisor"},
        {"source": "priya_k", "target": "ananya.n", "relationship_type": "FOLLOWS", "weight": 1.0, "context": "Social Instagram connection"}
    ]
    pd.DataFrame(connections).to_csv(target_dir / "connections.csv", index=False)

    # 8. PHOTOS & EXIF
    photos = [
        {"photo_id": "PH-701", "account": "ananya.n", "timestamp_utc": "2026-04-06 17:30:00", "filename": "koramangala_cafe.jpg", "camera_make": "Sony", "camera_model": "ILCE-7M4", "latitude": 12.9352, "longitude": 77.6245, "caption": "Evening code sprint at 3rd Wave", "is_red_herring": False},
        {"photo_id": "PH-702", "account": "ananya.n", "timestamp_utc": "2026-04-12 18:30:00", "filename": "indiranagar_roastery.jpg", "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "latitude": 12.9719, "longitude": 77.6412, "caption": "Evening coffee before discussions", "is_red_herring": False},
        {"photo_id": "PH-703", "account": "void_null07", "timestamp_utc": "2026-04-16 20:30:00", "filename": "nandi_ridge_dusk.jpg", "camera_make": "Sony", "camera_model": "ILCE-7M4", "latitude": 13.3702, "longitude": 77.6835, "caption": "Final horizon from Nandi ridge", "is_red_herring": False},
        {"photo_id": "PH-704", "account": "travel_bot_decoy", "timestamp_utc": "2026-04-17 12:00:00", "filename": "goa_beach_spotting.jpg", "camera_make": "Canon", "camera_model": "EOS R6", "latitude": 15.5524, "longitude": 73.7516, "caption": "Spotted student backpacker in Baga Beach", "is_red_herring": True}
    ]
    with open(target_dir / "photos_metadata.json", "w", encoding="utf-8") as f:
        json.dump(photos, f, indent=2)

    # 9. RESOLVED IDENTITIES
    resolved = {
        "clusters": [
            {
                "canonical_id": "PERSON_ANANYA_NAIR",
                "canonical_name": "Ananya Nair",
                "is_target": True,
                "is_primary_subject": True,
                "account_count": 4,
                "accounts": ["ananya_dev", "ananya.n", "ananyan-dev", "void_null07"],
                "linked_emails": ["ananya.nair.sys@fictional-mail.in", "ananya_personal@fictional-mail.in", "anon_blr07@proton-synthetic.me"],
                "linked_phones": ["+91-98801-0144", "+91-98801-0199"],
                "is_multi_account": True
            },
            {
                "canonical_id": "PERSON_VECTOR_ZERO",
                "canonical_name": "Vector Zero",
                "is_target": False,
                "account_count": 1,
                "accounts": ["vector_zero"],
                "linked_emails": ["recruiter@vector-zero.io"],
                "linked_phones": ["+91-98801-0900"],
                "is_multi_account": False
            },
            {
                "canonical_id": "PERSON_PRIYA_K",
                "canonical_name": "Priya Krishnamurthy",
                "is_target": False,
                "account_count": 1,
                "accounts": ["priya_k"],
                "linked_emails": ["priya.k@biotech-blr.in"],
                "linked_phones": ["+91-98801-0222"],
                "is_multi_account": False
            },
            {
                "canonical_id": "PERSON_ROHAN_SHARMA",
                "canonical_name": "Rohan Sharma",
                "is_target": False,
                "account_count": 1,
                "accounts": ["rohan_tech"],
                "linked_emails": ["rohan.sharma@fictional-bit.in"],
                "linked_phones": ["+91-98801-0333"],
                "is_multi_account": False
            },
            {
                "canonical_id": "PERSON_PROF_MENON",
                "canonical_name": "Prof. K. Menon",
                "is_target": False,
                "account_count": 1,
                "accounts": ["prof_menon_sys"],
                "linked_emails": ["kmenon@bit-dept.ac.in"],
                "linked_phones": ["+91-98801-0444"],
                "is_multi_account": False
            }
        ],
        "confirmed_links": [
            {"account_a": "ananya_dev", "account_b": "ananya.n", "confidence": 0.96, "rationale": "Shared primary phone +91-98801-0144 and student email domain"},
            {"account_a": "ananya_dev", "account_b": "ananyan-dev", "confidence": 0.98, "rationale": "Identical email ananya.nair.sys@fictional-mail.in and commit PGP signature"},
            {"account_a": "void_null07", "account_b": "ananya_dev", "confidence": 0.91, "rationale": "Consecutive cell tower handoff between primary and burner SIM at Hebbal junction"}
        ]
    }
    with open(target_dir / "resolved_identities.json", "w", encoding="utf-8") as f:
        json.dump(resolved, f, indent=2)

    # 10. AMBIGUOUS LINKS
    ambiguous = [
        {"account_a": "void_null07", "account_b": "travel_bot_decoy", "similarity_score": 0.22, "status": "REJECTED_RED_HERRING", "rationale": "IP hopping in Goa lacks device hash concordance with Sony ILCE camera"}
    ]
    with open(target_dir / "ambiguous_links.json", "w", encoding="utf-8") as f:
        json.dump(ambiguous, f, indent=2)

    # 11. MOVEMENT ANALYSIS & DBSCAN
    movement = {
        "candidate_lkl": {
            "rank": 1,
            "venue_name": "Nandi Hills Ridge Overlook",
            "latitude": 13.3702,
            "longitude": 77.6835,
            "confidence": 0.938,
            "final_telecom_ping": "2026-04-16T21:15:00Z",
            "cell_tower_id": "BLR-TWR-8841",
            "search_radius_meters": 400
        },
        "clusters": [
            {"cluster_id": 0, "name": "Koramangala & Indiranagar Hub", "center": [12.9535, 77.6330], "event_count": 8, "dominant_modality": "Physical Check-ins & Cellular CDR"},
            {"cluster_id": 1, "name": "Electronic City Tech Zone", "center": [12.8452, 77.6602], "event_count": 4, "dominant_modality": "Academic Attendance & Social Transmissions"},
            {"cluster_id": 2, "name": "Hebbal & Bellary Road Exit Corridor", "center": [13.0410, 77.5910], "event_count": 3, "dominant_modality": "Burner Handset Cellular Pings"},
            {"cluster_id": 3, "name": "Nandi Hills Terminal Cluster (LKL)", "center": [13.3702, 77.6835], "event_count": 2, "dominant_modality": "Final Burner Handset Ping & EXIF Photo"}
        ]
    }
    with open(target_dir / "movement_analysis.json", "w", encoding="utf-8") as f:
        json.dump(movement, f, indent=2)

    # 12. HYPOTHESES & EVALUATION
    hypotheses = [
        {
            "hypothesis_id": "H1",
            "title": "High-Tech Headhunting / Extortion via Covert Autonomous Recruiter",
            "description": "Subject was systematically courted by @vector_zero offering proprietary AI deployment funding, followed by coerced off-grid departure from Indiranagar Roastery towards an unmapped facility north of Bengaluru.",
            "prior": 0.40,
            "likelihood": 0.89,
            "posterior": 0.89,
            "rank": 1,
            "status": "MOST_PROBABLE",
            "supporting_evidence": [
                "Deleted posts P-106 & P-107 referencing confidential client NDA at Indiranagar Roastery",
                "Repeated burner phone pings (+91-98801-0199) directly following Vector Zero contact",
                "Final cell tower triangulation terminating at Nandi Hills Ridge Overlook at 21:15 UTC"
            ]
        },
        {
            "hypothesis_id": "H2",
            "title": "Autonomous Voluntary Disappearance into Off-Grid Research Collective",
            "description": "Subject deliberately rotated PGP keys and severed academic obligations to join an open-source stealth intelligence lab in the Western Ghats / Nandi perimeter.",
            "prior": 0.35,
            "likelihood": 0.65,
            "posterior": 0.65,
            "rank": 2,
            "status": "PLAUSIBLE",
            "supporting_evidence": [
                "Post P-104 stating 'Some opportunities require uncoupling from conventional academic trajectories'",
                "ShadowNet post P-105: 'Keys rotated. Secondary handset provisioned.'"
            ]
        },
        {
            "hypothesis_id": "H3",
            "title": "Decoy Travel / Coastal Relocation to Goa",
            "description": "Subject fled south-west toward coastal resorts to evade capstone deadline stress.",
            "prior": 0.25,
            "likelihood": 0.12,
            "posterior": 0.12,
            "rank": 3,
            "status": "DISPROVEN_RED_HERRING",
            "supporting_evidence": [
                "Decoy photo PH-704 in Goa with mismatched Sony/Canon camera profile and zero cellular tower correlation"
            ]
        }
    ]
    with open(target_dir / "hypotheses_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(hypotheses, f, indent=2)

    evaluation = {
        "case_id": "MP-2026-0527",
        "benchmark_timestamp": "2026-04-18T12:00:00Z",
        "metrics": {
            "entity_resolution_precision": 0.962,
            "entity_resolution_recall": 0.925,
            "entity_resolution_f1": 0.943,
            "lkl_spatial_error_meters": 142.5,
            "lkl_rank1_accuracy": 1.0,
            "hypothesis_mrr": 1.0,
            "red_herring_rejection_rate": 1.0
        }
    }
    with open(target_dir / "evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2)

    # 13. CONSTRUCT REAL NETWORKX GRAPH & EXPORT STATIONARY VIS.JS HTML FILES
    from graph.build_networkx import build_investigation_graph
    from graph.improved_graph_export import export_investigation_graph
    from graph.analytics import run_graph_analytics

    G = build_investigation_graph(target_dir)
    print(f"Constructed Ananya Investigation Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    export_investigation_graph(
        G,
        output_dir=target_dir,
        default_focus_target="PERSON_ANANYA_NAIR",
        target_person_name="Ananya Nair"
    )

    # Also compute graph analytics
    run_graph_analytics(G, output_dir=target_dir)

    # 14. INTERACTIVE FOLIUM TACTICAL MAP (Full Map Page)
    m = folium.Map(
        location=[13.12, 77.64],
        zoom_start=10,
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="OpenStreetMap",
        zoom_control=True
    )

    fg_chk = folium.FeatureGroup(name="🔵 Venue Check-ins", show=True)
    fg_ph = folium.FeatureGroup(name="🟣 Photo GPS EXIF", show=True)
    fg_tow = folium.FeatureGroup(name="🟢 Cell Tower Sectors", show=True)
    fg_traj = folium.FeatureGroup(name="🟠 Trajectory Polyline", show=True)
    fg_lkl = folium.FeatureGroup(name="🔴 Candidate LKL (Rank 1)", show=True)

    traj_points = []
    for ch in checkins:
        folium.CircleMarker(
            location=[ch["latitude"], ch["longitude"]],
            radius=7,
            color="#3A6BFF",
            fill=True,
            fill_color="#3A6BFF",
            fill_opacity=0.8,
            popup=f"<b>Check-in: {ch['venue_name']}</b><br/>Account: @{ch['account']}<br/>Time: {ch['timestamp_utc']}",
            tooltip=f"Check-in: {ch['venue_name']}"
        ).add_to(fg_chk)
        traj_points.append({"lat": ch["latitude"], "lon": ch["longitude"], "time": ch["timestamp_utc"]})

    for ph in photos:
        if not ph.get("is_red_herring"):
            folium.CircleMarker(
                location=[ph["latitude"], ph["longitude"]],
                radius=6,
                color="#6C5CE7",
                fill=True,
                fill_color="#6C5CE7",
                fill_opacity=0.8,
                popup=f"<b>Photo: {ph['filename']}</b><br/>Camera: {ph.get('camera_make')} {ph.get('camera_model')}<br/>Time: {ph['timestamp_utc']}",
                tooltip=f"EXIF: {ph['filename']}"
            ).add_to(fg_ph)
            traj_points.append({"lat": ph["latitude"], "lon": ph["longitude"], "time": ph["timestamp_utc"]})

    for cl in calls:
        is_burner = "Burner" in cl["call_type"]
        folium.CircleMarker(
            location=[cl["tower_latitude"], cl["tower_longitude"]],
            radius=9 if is_burner else 6,
            color="#FF4757" if is_burner else "#00E5A3",
            fill=True,
            fill_color="#FF4757" if is_burner else "#00E5A3",
            fill_opacity=0.65,
            popup=f"<b>Tower: {cl['cell_tower_sector']}</b><br/>Handset: {cl['caller_number']}<br/>Time: {cl['timestamp_utc']}",
            tooltip=f"Tower Sector: {cl['cell_tower_sector']} ({'Burner' if is_burner else 'Primary'})"
        ).add_to(fg_tow)
        if is_burner or str(cl["caller_number"]).endswith("0144"):
            traj_points.append({"lat": cl["tower_latitude"], "lon": cl["tower_longitude"], "time": cl["timestamp_utc"]})

    traj_points.sort(key=lambda x: str(x["time"]))
    if len(traj_points) >= 2:
        coords = [(pt["lat"], pt["lon"]) for pt in traj_points]
        folium.PolyLine(
            coords,
            color="#3A6BFF",
            weight=2.5,
            opacity=0.85,
            dash_array="6, 8",
            tooltip="Ananya Nair Chronological Trajectory"
        ).add_to(fg_traj)

    lkl_lat, lkl_lon = 13.3702, 77.6835
    folium.Marker(
        location=[lkl_lat, lkl_lon],
        popup="<div style='font-family:Inter; color:#FFFFFF;'><b>🚨 CANDIDATE LKL (RANK 1)</b><br/>Nandi Hills Ridge Overlook<br/>Final Handset Ping: 2026-04-16 21:15 UTC<br/>Confidence: 93.8%</div>",
        tooltip="🚨 CRITICAL: Last Known Location (Nandi Hills Ridge)",
        icon=folium.Icon(color="red", icon="star", prefix="glyphicon")
    ).add_to(fg_lkl)

    folium.Circle(
        location=[lkl_lat, lkl_lon],
        radius=400,
        color="#FF4757",
        weight=2,
        fill=True,
        fill_color="#FF4757",
        fill_opacity=0.25,
        tooltip="High-Probability Disappearance Search Radius (400m)"
    ).add_to(fg_lkl)

    fg_chk.add_to(m)
    fg_ph.add_to(m)
    fg_tow.add_to(m)
    fg_traj.add_to(m)
    fg_lkl.add_to(m)

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    dark_css = """
    <style>
        .leaflet-container {
            background-color: #0E1231 !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        .leaflet-tile-pane {
            filter: brightness(0.65) invert(1) contrast(2.8) hue-rotate(200deg) saturate(0.35) brightness(0.7) !important;
        }
        .leaflet-popup-content-wrapper, .leaflet-popup-tip {
            background: #1A2254 !important;
            color: #FFFFFF !important;
            border: 1px solid #2C3979 !important;
            border-radius: 8px !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.75) !important;
        }
        .leaflet-control-layers {
            background: rgba(22, 29, 72, 0.94) !important;
            color: #FFFFFF !important;
            border: 1px solid #2C3979 !important;
            backdrop-filter: blur(14px) !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 11px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6) !important;
        }
        .leaflet-control-layers-expanded label {
            color: #CBD5E1 !important;
            font-weight: 500 !important;
            margin-bottom: 5px !important;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }
        .leaflet-bar a {
            background-color: #1A2254 !important;
            color: #FFFFFF !important;
            border: 1px solid #2C3979 !important;
        }
        .leaflet-bar a:hover {
            background-color: #202A66 !important;
            color: #3A6BFF !important;
        }
        .leaflet-control-attribution {
            display: none !important;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(dark_css))
    m.save(str(target_dir / "investigation_map.html"))

    # 15. INTERACTIVE TIMELINE HTML (Plotly 5-Lane)
    LANE_ORDER = [
        "5. OSINT & Behavioral",
        "4. Photo EXIF Signatures",
        "3. Physical Check-ins",
        "2. Telecommunications (CDR)",
        "1. Social Media Posts"
    ]
    tl_events = []
    for p in posts:
        is_del = p["deleted"]
        tl_events.append({
            "lane": "1. Social Media Posts",
            "timestamp": p["timestamp_raw"].replace(" UTC", ""),
            "label": f"{p['post_id']}",
            "details": f"<b>@{p['account']}</b> ({'DELETED' if is_del else 'PUBLIC'})<br/>{p['text']}",
            "type": "Deleted Post" if is_del else "Public Post",
            "color": "#FF4757" if is_del else "#3A6BFF"
        })
    for c in calls:
        is_b = "Burner" in c["call_type"]
        tl_events.append({
            "lane": "2. Telecommunications (CDR)",
            "timestamp": c["timestamp_utc"],
            "label": f"{c['call_id']}",
            "details": f"<b>{c['call_type']}</b>: {c['caller_number']} -> {c['receiver_number']}<br/>Sector: {c['cell_tower_sector']}",
            "type": "Burner Handset Ping" if is_b else "Voice Call",
            "color": "#FF4757" if is_b else "#00E5A3"
        })
    for ch in checkins:
        tl_events.append({
            "lane": "3. Physical Check-ins",
            "timestamp": ch["timestamp_utc"],
            "label": f"{ch['checkin_id']}",
            "details": f"<b>Check-in</b>: {ch['venue_name']}<br/>Account: @{ch['account']}",
            "type": "Venue Check-in",
            "color": "#00D2D3"
        })
    for ph in photos:
        is_rh = ph.get("is_red_herring")
        tl_events.append({
            "lane": "4. Photo EXIF Signatures",
            "timestamp": ph["timestamp_utc"],
            "label": f"{ph['photo_id']}",
            "details": f"<b>Photo</b>: {ph['filename']}<br/>{ph.get('camera_make')} {ph.get('camera_model')}",
            "type": "Red Herring Photo" if is_rh else "Captured Photo",
            "color": "#F5B942" if is_rh else "#6C5CE7"
        })

    tl_df = pd.DataFrame(tl_events)
    tl_df["dt"] = pd.to_datetime(tl_df["timestamp"], utc=True)

    fig_tl = go.Figure()
    for etype in tl_df["type"].unique():
        sub = tl_df[tl_df["type"] == etype]
        fig_tl.add_trace(go.Scatter(
            x=sub["dt"],
            y=sub["lane"],
            mode="markers+text",
            name=etype,
            text=sub["label"],
            textposition="top center",
            textfont=dict(size=9, color="#CBD5E1"),
            marker=dict(
                size=11 if "Deleted" in etype or "Burner" in etype else 8,
                color=sub["color"].iloc[0],
                symbol="x" if "Deleted" in etype else "circle"
            ),
            customdata=sub["details"],
            hovertemplate="<b>%{y}</b><br/>Time: %{x|%Y-%m-%d %H:%M UTC}<br/>%{customdata}<extra></extra>",
            showlegend=True
        ))

    fig_tl.update_layout(
        template="plotly_dark",
        height=620,
        margin=dict(l=160, r=40, t=30, b=80),
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#252F66",
            tickfont=dict(size=11, color="#6D7FA8"),
            range=["2026-03-25 00:00:00", "2026-04-20 00:00:00"]
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#252F66",
            tickfont=dict(size=12, color="#FFFFFF", family="Inter, sans-serif"),
            categoryorder="array",
            categoryarray=LANE_ORDER,
            fixedrange=True
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.14,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#98A7CE"),
            bgcolor="rgba(22, 29, 72, 0.8)",
            bordercolor="#2C3979",
            borderwidth=1
        ),
        plot_bgcolor="#141A42",
        paper_bgcolor="#101538"
    )
    fig_tl.write_html(str(target_dir / "investigation_timeline.html"))

    # Also generate overview corridor map
    from generator.generate_overview_corridor_maps import generate_all_corridor_maps
    generate_all_corridor_maps()

    print(f"Case MP-2026-0527 (Ananya Nair) generated successfully at: {target_dir}")
    return target_dir

if __name__ == "__main__":
    generate_ananya_dataset()
