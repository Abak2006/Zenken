"""
Generates the social network edges: follows, tags, mentions, comments, and mutual connections.
"""
from __future__ import annotations
import random
from typing import Dict, Any, List
import pandas as pd

def generate_connections(
    profiles: List[Dict[str, Any]],
    posts_df: pd.DataFrame,
    seed: int = 42
) -> pd.DataFrame:
    random.seed(seed)
    connections: List[Dict[str, Any]] = []

    profile_map = {p["handle"]: p for p in profiles}

    # 1. Follow graph
    # Maya's main handles
    main_friends = [
        "chloe_creative", "david_lin_tech", "prof_vance_art", "elena_prints",
        "sara_chen_photo", "tariq_beans", "hannah_w_lens", "zoe_p_design"
    ]

    for friend in main_friends:
        if friend in profile_map:
            # Bidirectional follow
            connections.append({
                "source": "mayalin_art",
                "target": friend,
                "relationship_type": "FOLLOWS",
                "weight": 1.0,
                "context": "mutual_social_circle"
            })
            connections.append({
                "source": friend,
                "target": "mayalin_art",
                "relationship_type": "FOLLOWS",
                "weight": 1.0,
                "context": "mutual_social_circle"
            })

    # Variant handle m_lin99 shares close circle
    for friend in ["chloe_creative", "david_lin_tech", "elena_prints", "lucas_r_sound"]:
        if friend in profile_map:
            connections.append({
                "source": "m_lin99",
                "target": friend,
                "relationship_type": "FOLLOWS",
                "weight": 0.9,
                "context": "casual_social_circle"
            })

    # Covert handle m.shadow_7 only connected to kaelen_v
    connections.append({
        "source": "m.shadow_7",
        "target": "kaelen_v",
        "relationship_type": "FOLLOWS",
        "weight": 0.85,
        "context": "clandestine_contact"
    })
    connections.append({
        "source": "kaelen_v",
        "target": "m.shadow_7",
        "relationship_type": "FOLLOWS",
        "weight": 0.85,
        "context": "clandestine_contact"
    })
    connections.append({
        "source": "kaelen_v",
        "target": "mayalin_art",
        "relationship_type": "FOLLOWS",
        "weight": 0.7,
        "context": "solicitation"
    })

    # Red herring accounts
    connections.append({
        "source": "mayalin_travels",
        "target": "mayalin_art",
        "relationship_type": "FOLLOWS",
        "weight": 0.2,
        "context": "impersonator"
    })

    # 2. Extract mentions and tags from posts_df
    for _, row in posts_df.iterrows():
        src = row["account"]
        mentions = str(row["mentions"]).split(";") if pd.notna(row["mentions"]) and row["mentions"] else []
        for m in mentions:
            m_clean = m.strip().lstrip("@")
            if m_clean and m_clean in profile_map:
                connections.append({
                    "source": src,
                    "target": m_clean,
                    "relationship_type": "MENTIONS",
                    "weight": 0.6,
                    "context": f"Post {row['post_id']} mention"
                })

    # 3. Add explicit comments / interactions
    comments = [
        ("chloe_creative", "mayalin_art", "COMMENTED", 0.9, "Stunning composition Maya!"),
        ("prof_vance_art", "mayalin_art", "COMMENTED", 0.75, "Bring this print to Tuesday critique."),
        ("lucas_r_sound", "mayalin_art", "COMMENTED", 0.6, "Answer your DMs."),
        ("elena_prints", "m_lin99", "COMMENTED", 0.8, "Saved a space in drying rack 2 for you."),
        ("david_lin_tech", "mayalin_art", "COMMENTED", 0.95, "Mom said call her this weekend!")
    ]
    for src, tgt, rel, w, ctx in comments:
        connections.append({
            "source": src,
            "target": tgt,
            "relationship_type": rel,
            "weight": w,
            "context": ctx
        })

    df = pd.DataFrame(connections).drop_duplicates()
    return df
