"""
Synthesizes social media account profiles based on the case bible and random seed.
"""
from __future__ import annotations
import random
from typing import Dict, Any, List
from faker import Faker

def generate_profiles(case_data: Dict[str, Any], seed: int = 42) -> List[Dict[str, Any]]:
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    profiles: List[Dict[str, Any]] = []

    # 1. Target identities
    target = case_data.get("missing_person", {})
    for idx, ident in enumerate(case_data.get("digital_identities", [])):
        profiles.append({
            "account_id": f"acc_target_{idx+1:02d}",
            "handle": ident["handle"],
            "display_name": ident["display_name"],
            "platform": ident["platform"],
            "account_type": ident.get("account_type", "standard"),
            "bio": ident.get("bio", ""),
            "email": ident.get("email"),
            "phone": ident.get("phone_reference"),
            "avatar_image": f"avatar_{ident['handle']}.jpg",
            "is_private": ident.get("visibility") == "private",
            "joined_date": "2023-08-15" if ident["handle"] == "pixel_maya" else ("2026-03-03" if ident["handle"] == "m.shadow_7" else "2024-01-10"),
            "followers_count": 1420 if ident["handle"] == "mayalin_art" else (310 if ident["handle"] == "m_lin99" else 12),
            "following_count": 280 if ident["handle"] == "mayalin_art" else 145,
            "real_name_reference": target.get("full_name"),
            "is_target_identity": True
        })

    # 2. Associates
    for idx, assoc in enumerate(case_data.get("associates", [])):
        profiles.append({
            "account_id": f"acc_assoc_{idx+1:02d}",
            "handle": assoc["handle"],
            "display_name": assoc["name"],
            "platform": "InstaPhoto" if idx % 2 == 0 else "ChirpNet",
            "account_type": "associate",
            "bio": f"{assoc['relationship']} | Creative & Student | Contact: {assoc['name'].lower().replace(' ', '.')}@fictional-domain.org",
            "email": f"{assoc['name'].lower().replace(' ', '.')}@fictional-domain.org",
            "phone": assoc.get("phone"),
            "avatar_image": f"avatar_{assoc['handle']}.jpg",
            "is_private": False if idx % 4 != 0 else True,
            "joined_date": "2023-05-20",
            "followers_count": random.randint(120, 1800),
            "following_count": random.randint(90, 600),
            "relationship_to_target": assoc["relationship"],
            "relationship_strength": assoc.get("strength", 0.5),
            "is_target_identity": False
        })

    # 3. Red Herring Profiles
    profiles.append({
        "account_id": "acc_redherring_01",
        "handle": "mayalin_travels",
        "display_name": "Maya L. Travel Escapes",
        "platform": "InstaPhoto",
        "account_type": "red_herring",
        "bio": "Escaped the fog! Living the sunny beach dream in Mexico. DM for collabs. #wanderlust",
        "email": "traveler_beach_fun99@temp-synth.net",
        "phone": "+1-555-0100",
        "avatar_image": "avatar_mayalin_travels.jpg",
        "is_private": False,
        "joined_date": "2026-03-13",
        "followers_count": 48,
        "following_count": 12,
        "is_target_identity": False
    })

    # 4. Background noise accounts
    for i in range(1, 6):
        h_name = fake.user_name()
        profiles.append({
            "account_id": f"acc_noise_{i:02d}",
            "handle": f"{h_name}_bay",
            "display_name": fake.name(),
            "platform": "ChirpNet",
            "account_type": "bystander",
            "bio": fake.catch_phrase(),
            "email": f"{h_name}@example-synthetic.org",
            "phone": f"+1-555-01{70+i}",
            "avatar_image": f"avatar_noise_{i}.jpg",
            "is_private": False,
            "joined_date": "2024-11-02",
            "followers_count": random.randint(50, 400),
            "following_count": random.randint(50, 300),
            "is_target_identity": False
        })

    return profiles
