"""
Synthesizes social media microblog posts across accounts with realistic temporal cadence,
mixed time zone formatting, intentional noise/typos, deleted flags, and behavioral shifts.
"""
from __future__ import annotations
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd

def format_mixed_timestamp(dt_utc: datetime, mode: int) -> str:
    """Simulates realistic messy formats found in wild social media logs and HTML scrapes."""
    pst_dt = dt_utc - timedelta(hours=8)
    if mode == 0:
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    elif mode == 1:
        return pst_dt.strftime("%Y-%m-%d %H:%M:%S PST")
    elif mode == 2:
        return dt_utc.strftime("%a, %d %b %Y %H:%M:%S +0000")
    elif mode == 3:
        # ISO with fractional seconds and +00:00
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
    elif mode == 4:
        # Unix epoch string
        return str(int(dt_utc.timestamp()))
    else:
        return pst_dt.strftime("%m/%d/%Y %I:%M %p")

def generate_posts(
    case_data: Dict[str, Any],
    photo_catalog: List[Dict[str, Any]],
    seed: int = 42,
    days: int = 45
) -> pd.DataFrame:
    random.seed(seed)
    base_date = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)
    venues = case_data.get("venues", [])
    posts: List[Dict[str, Any]] = []

    # Map photos to accounts
    photo_map = {p["photo_id"]: p for p in photo_catalog}

    # 1. Phase 1: Routine Posts (Days 1 to 30)
    routine_texts = [
        ("Setting up the tripod at Bayview Arts Hall for lighting studies. #analogue #artschool", ["#analogue", "#artschool"], ["@chloe_creative"], "Bayview Arts Institute - Fine Arts Hall"),
        ("Late cold brew at Harbor Light Cafe. Editing coastal fog negatives all morning.", ["#coffee", "#photodump"], ["@tariq_beans"], "Harbor Light Cafe"),
        ("Redwood Ridge light leaks hit different around 5pm. Film still wet.", ["#35mm", "#redwood"], [], "Redwood Ridge Scenic Park"),
        ("Studio critique with Prof Vance went well! He suggested larger formats.", ["#fineart", "#mentorship"], ["@prof_vance_art"], "Bayview Arts Institute - Fine Arts Hall"),
        ("Why does the darkroom always smell like vinegar and existential dread? haha", ["#filmisnotdead"], ["@elena_prints", "@sara_chen_photo"], None),
        ("Golden hour ridge gradients. Pure serenity out here.", ["#coastal", "#landscape"], [], "Redwood Ridge Scenic Park"),
        ("Dinner with @david_lin_tech in town. Reminding me to eat actual food.", ["#family"], ["@david_lin_tech"], "Harbor Light Cafe"),
    ]

    post_idx = 1
    for day in range(1, 30):
        # 1-2 posts per day across accounts
        if random.random() < 0.65:
            text_tpl, htags, mentions, loc = random.choice(routine_texts)
            post_dt = base_date + timedelta(days=day, hours=random.randint(9, 21), minutes=random.randint(0, 59))
            acc = "mayalin_art" if random.random() < 0.8 else "m_lin99"
            posts.append({
                "post_id": f"POST-{post_idx:04d}",
                "account": acc,
                "timestamp_raw": format_mixed_timestamp(post_dt, random.randint(0, 5)),
                "timestamp_utc_iso": post_dt.isoformat(),
                "text": text_tpl,
                "hashtags": ";".join(htags),
                "mentions": ";".join(mentions),
                "location_tag": loc if random.random() < 0.75 else None,
                "likes": random.randint(35, 320),
                "photo_id": "PH-001" if "ridge" in text_tpl.lower() else ("PH-002" if "harbor" in text_tpl.lower() else None),
                "deleted": False,
                "sentiment_label": "positive"
            })
            post_idx += 1

    # Breakup dispute posts (Day 20-22)
    breakup_dt = base_date + timedelta(days=20, hours=19, minutes=15)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "lucas_r_sound",
        "timestamp_raw": format_mixed_timestamp(breakup_dt, 1),
        "timestamp_utc_iso": breakup_dt.isoformat(),
        "text": "@mayalin_art Stop ignoring my calls. You still have my studio microphones and audio interface.",
        "hashtags": "",
        "mentions": "@mayalin_art",
        "location_tag": "Bayside Living Apartments",
        "likes": 2,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "angry"
    })
    post_idx += 1

    # 2. Phase 2: Behavioral Shift & Inbound Contact (Days 31 to 38)
    contact_dt = base_date + timedelta(days=31, hours=14, minutes=10)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "kaelen_v",
        "timestamp_raw": format_mixed_timestamp(contact_dt, 0),
        "timestamp_utc_iso": contact_dt.isoformat(),
        "text": "@mayalin_art Impressed by your architectural shadow work. We have a private coastal commission with high honorarium. DM or reach out on secure channel.",
        "hashtags": "#artcollector #commission",
        "mentions": "@mayalin_art",
        "location_tag": None,
        "likes": 5,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "neutral"
    })
    post_idx += 1

    shift_dt = base_date + timedelta(days=33, hours=22, minutes=45)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "m_lin99",
        "timestamp_raw": format_mixed_timestamp(shift_dt, 2),
        "timestamp_utc_iso": shift_dt.isoformat(),
        "text": "feeling strangely watched lately. maybe just exhaustion from final portfolio reviews... or maybe not.",
        "hashtags": "#anxiety",
        "mentions": "",
        "location_tag": None,
        "likes": 18,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "fear"
    })
    post_idx += 1

    covert_dt = base_date + timedelta(days=36, hours=22, minutes=5)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "m.shadow_7",
        "timestamp_raw": format_mixed_timestamp(covert_dt, 0),
        "timestamp_utc_iso": covert_dt.isoformat(),
        "text": "Location secured for preview shoot. Coastal fog coordinates verified. PGP key updated.",
        "hashtags": "#shadow #exclusive",
        "mentions": "",
        "location_tag": "Whispering Pines Overlook",
        "likes": 1,
        "photo_id": "PH-007",
        "deleted": False,
        "sentiment_label": "cautious"
    })
    post_idx += 1

    # 3. Phase 3: Deleted Posts & Final Days (Days 39 to 45)
    # 3 DELETED posts (critical clues)
    del_dt1 = base_date + timedelta(days=40, hours=11, minutes=30)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "mayalin_art",
        "timestamp_raw": format_mixed_timestamp(del_dt1, 3),
        "timestamp_utc_iso": del_dt1.isoformat(),
        "text": "Meeting with K at Pacific Horizon Diner on Friday to finalize the private gallery contract. Super nervous!!",
        "hashtags": "#opportunity #secretproject",
        "mentions": "@kaelen_v",
        "location_tag": "Pacific Horizon Diner",
        "likes": 42,
        "photo_id": None,
        "deleted": True,
        "sentiment_label": "anxious_excited"
    })
    post_idx += 1

    del_dt2 = base_date + timedelta(days=41, hours=15, minutes=0)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "m_lin99",
        "timestamp_raw": format_mixed_timestamp(del_dt2, 1),
        "timestamp_utc_iso": del_dt2.isoformat(),
        "text": "Switching to new phone line soon. Don't call the 0144 number after tomorrow morning.",
        "hashtags": "",
        "mentions": "",
        "location_tag": None,
        "likes": 8,
        "photo_id": None,
        "deleted": True,
        "sentiment_label": "neutral"
    })
    post_idx += 1

    del_dt3 = base_date + timedelta(days=42, hours=16, minutes=20)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "mayalin_art",
        "timestamp_raw": format_mixed_timestamp(del_dt3, 0),
        "timestamp_utc_iso": del_dt3.isoformat(),
        "text": "Awaiting appointment at the shoreline. Fog is coming in fast.",
        "hashtags": "#coastal #fog",
        "mentions": "",
        "location_tag": "Pacific Horizon Diner",
        "likes": 25,
        "photo_id": "PH-008",
        "deleted": True,
        "sentiment_label": "tense"
    })
    post_idx += 1

    # Final post from covert account before turning dark
    final_post_dt = base_date + timedelta(days=44, hours=21, minutes=10) # 2026-03-14T21:10:00Z
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "m.shadow_7",
        "timestamp_raw": format_mixed_timestamp(final_post_dt, 0),
        "timestamp_utc_iso": final_post_dt.isoformat(),
        "text": "Vehicle arrived. Headlights on the upper ridge. Meeting now.",
        "hashtags": "",
        "mentions": "",
        "location_tag": "Whispering Pines Overlook",
        "likes": 0,
        "photo_id": "PH-009",
        "deleted": False,
        "sentiment_label": "ominous"
    })
    post_idx += 1

    # 4. Red Herring Posts
    # RH 1: Lucas angry post followed by his flight to Seattle
    rh1_dt = base_date + timedelta(days=44, hours=18, minutes=0)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "lucas_r_sound",
        "timestamp_raw": format_mixed_timestamp(rh1_dt, 1),
        "timestamp_utc_iso": rh1_dt.isoformat(),
        "text": "Sitting at SFO airport gate 82 waiting for SEA-441. Leaving this toxic drama behind. Peace out Bayview.",
        "hashtags": "#travel #movingon",
        "mentions": "",
        "location_tag": "SFO Airport Marriott Gateway",
        "likes": 19,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "bitter"
    })
    post_idx += 1

    # RH 2: Fake Mexico travel account
    rh2_dt = base_date + timedelta(days=44, hours=14, minutes=0)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "mayalin_travels",
        "timestamp_raw": format_mixed_timestamp(rh2_dt, 0),
        "timestamp_utc_iso": rh2_dt.isoformat(),
        "text": "Escaped all the stress! Sunny beach freedom in Cabo! Best decision ever #mexico #escape #newlife",
        "hashtags": "#mexico #escape #newlife",
        "mentions": "",
        "location_tag": "Silver Sands Motel",
        "likes": 3,
        "photo_id": "PH-010",
        "deleted": False,
        "sentiment_label": "excited"
    })
    post_idx += 1

    # RH 3: Marcus Cole car trouble
    rh3_dt = base_date + timedelta(days=44, hours=20, minutes=30)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "marcus_c_drift",
        "timestamp_raw": format_mixed_timestamp(rh3_dt, 0),
        "timestamp_utc_iso": rh3_dt.isoformat(),
        "text": "My civic died right past the scenic turnoff out of gas. Waiting for tow truck. Great start to Saturday.",
        "hashtags": "#broken #strandeed", # typo injected
        "mentions": "@liam_drift_auto",
        "location_tag": "Silver Sands Motel",
        "likes": 4,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "annoyed"
    })
    post_idx += 1

    # Concern from Roommate on Day 45 morning
    concern_dt = base_date + timedelta(days=45, hours=8, minutes=15)
    posts.append({
        "post_id": f"POST-{post_idx:04d}",
        "account": "chloe_creative",
        "timestamp_raw": format_mixed_timestamp(concern_dt, 1),
        "timestamp_utc_iso": concern_dt.isoformat(),
        "text": "Has anyone seen @mayalin_art since yesterday evening?? Her car is gone and her phone goes straight to voicemail. Please message me if you know anything!!",
        "hashtags": "#emergency #bayview #findmaya",
        "mentions": "@mayalin_art @david_lin_tech",
        "location_tag": "Bayside Living Apartments",
        "likes": 184,
        "photo_id": None,
        "deleted": False,
        "sentiment_label": "panic"
    })

    df = pd.DataFrame(posts)
    # Sort chronologically by true timestamp
    df = df.sort_values(by="timestamp_utc_iso").reset_index(drop=True)
    return df
