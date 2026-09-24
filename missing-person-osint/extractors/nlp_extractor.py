"""
Natural Language Processing (NLP) Information Extractor for OSINT evidence.
Extracts Named Entities (PERSON, GPE/LOC, DATE, ORG) using spaCy,
classifies sentiment/emotional tone, detects high-risk keyword clusters (rendezvous, fear, secrecy),
and calculates behavioral change points over the investigation timeline.
"""
from __future__ import annotations
import re
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

# Load spaCy NLP model
nlp_model = None
try:
    import spacy
    nlp_model = spacy.load("en_core_web_sm")
except Exception:
    nlp_model = None

# Lexical dictionaries for domain-specific OSINT intelligence
KEYWORD_CLUSTERS = {
    "rendezvous_plans": [
        "meeting", "meet", "appointment", "contract", "commission", "shoot",
        "preview", "exhibition", "private", "client", "schedule", "arrived"
    ],
    "fear_and_paranoia": [
        "watched", "watching", "followed", "uneasy", "anxiety", "scared",
        "fear", "nervous", "strange", "dark", "creepy", "shadow", "threat"
    ],
    "conflict_and_dispute": [
        "ignoring", "calls", "return", "microphones", "toxic", "drama",
        "argue", "breakup", "stolen", "dispute", "blame", "hostile"
    ],
    "security_and_secrecy": [
        "pgp", "burner", "switch", "offline", "unlisted", "secure channel",
        "new phone", "line", "cash", "off-grid", "signal", "deleted"
    ],
    "geographic_clues": [
        "ridge", "harbor", "overlook", "pines", "diner", "shoreline",
        "highway", "beach", "sfo", "airport", "gate", "motel", "cabo"
    ]
}

# Simple rule-based polarity lexicon for reliable self-contained sentiment
POSITIVE_WORDS = {"great", "good", "serenity", "stunning", "best", "freedom", "excited", "well", "peace", "sunny", "opportunity"}
NEGATIVE_WORDS = {"watched", "anxiety", "dread", "ignoring", "toxic", "nervous", "tense", "panic", "emergency", "broken", "died", "annoyed", "bitter", "fear"}

def analyze_sentiment(text: str) -> Tuple[float, str]:
    """Calculates sentiment polarity score [-1.0 to 1.0] and emotional label."""
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return 0.0, "neutral"

    pos_count = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_WORDS)

    score = 0.0
    if (pos_count + neg_count) > 0:
        score = (pos_count - neg_count) / (pos_count + neg_count)

    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    # Nuanced contextual override
    if any(w in tokens for w in ["watched", "anxiety", "fear", "scared"]):
        label = "fear/anxiety"
    elif any(w in tokens for w in ["emergency", "panic", "findmaya"]):
        label = "urgent_distress"
    elif any(w in tokens for w in ["toxic", "ignoring", "drama"]):
        label = "conflict"

    return round(score, 3), label

def extract_entities_and_topics(text: str) -> Dict[str, Any]:
    """Extracts entities, matched keywords, and extracted mentions/hashtags from text."""
    # 1. Regex handles and hashtags
    handles = re.findall(r"@(\w+)", text)
    hashtags = re.findall(r"#(\w+)", text)

    # 2. Named Entity Recognition
    entities: List[Dict[str, str]] = []
    if nlp_model:
        doc = nlp_model(text)
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })
    else:
        # Fallback entity heuristic
        cap_words = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
        for w in cap_words:
            entities.append({"text": w, "label": "PROPN"})

    # 3. Keyword cluster matching
    matched_topics = {}
    lower_text = text.lower()
    for cluster_name, terms in KEYWORD_CLUSTERS.items():
        matches = [t for t in terms if re.search(r"\b" + re.escape(t) + r"\b", lower_text)]
        if matches:
            matched_topics[cluster_name] = matches

    sentiment_score, sentiment_label = analyze_sentiment(text)

    return {
        "text": text,
        "mentions": handles,
        "hashtags": hashtags,
        "entities": entities,
        "matched_topics": matched_topics,
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label
    }

def detect_behavioral_change_points(posts_df: pd.DataFrame, window_size: int = 5) -> Dict[str, Any]:
    """
    Analyzes temporal trends across posts to pinpoint significant behavioral inflection points.
    Returns detected change point timestamp and summary indicators.
    """
    if posts_df.empty or "text" not in posts_df.columns:
        return {"change_points": [], "detected": False}

    records = []
    for idx, row in posts_df.iterrows():
        nlp_res = extract_entities_and_topics(str(row["text"]))
        records.append({
            "post_id": row.get("post_id", f"P-{idx}"),
            "account": row.get("account"),
            "timestamp": row.get("timestamp_utc_iso", row.get("timestamp_raw")),
            "sentiment_score": nlp_res["sentiment_score"],
            "has_fear": "fear_and_paranoia" in nlp_res["matched_topics"],
            "has_plans": "rendezvous_plans" in nlp_res["matched_topics"],
            "has_secrecy": "security_and_secrecy" in nlp_res["matched_topics"]
        })

    eval_df = pd.DataFrame(records).sort_values(by="timestamp").reset_index(drop=True)
    
    # Calculate rolling sentiment mean
    eval_df["rolling_sentiment"] = eval_df["sentiment_score"].rolling(window=window_size, min_periods=2).mean()

    # Identify inflection points where negative/fear score jumps or secrecy begins
    fear_or_secrecy_indices = eval_df[eval_df["has_fear"] | eval_df["has_secrecy"]].index.tolist()

    first_anomaly_ts = None
    if fear_or_secrecy_indices:
        first_idx = fear_or_secrecy_indices[0]
        first_anomaly_ts = eval_df.loc[first_idx, "timestamp"]

    # Sentiment drop detection
    drop_threshold = -0.15
    significant_drops = eval_df[eval_df["rolling_sentiment"] < drop_threshold]
    drop_ts = significant_drops.iloc[0]["timestamp"] if not significant_drops.empty else None

    return {
        "detected": bool(first_anomaly_ts or drop_ts),
        "first_secrecy_or_fear_timestamp": first_anomaly_ts,
        "sentiment_divergence_timestamp": drop_ts,
        "total_posts_evaluated": len(eval_df),
        "post_evaluations": eval_df.to_dict(orient="records")
    }
