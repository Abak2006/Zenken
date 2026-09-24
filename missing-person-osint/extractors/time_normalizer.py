"""
Standardizes timestamps from mixed, inconsistent formats into ISO 8601 UTC,
while tracking and preserving the original source string and time zone.
"""
from __future__ import annotations
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from dateutil import parser as date_parser

# Common timezone offset mapping for colloquial abbreviations
TZ_OFFSETS = {
    "PST": -8,
    "PDT": -7,
    "EST": -5,
    "EDT": -4,
    "CST": -6,
    "CDT": -5,
    "MST": -7,
    "MDT": -6,
    "UTC": 0,
    "GMT": 0,
    "Z": 0
}

def normalize_timestamp(raw_value: Any, default_tz: str = "UTC") -> Dict[str, Any]:
    """
    Parses a raw timestamp string, int, or float and normalizes it to UTC.
    Returns a structured dictionary with normalized UTC ISO string, unix epoch, and provenance.
    """
    if raw_value is None or (isinstance(raw_value, float) and str(raw_value) == "nan"):
        return {
            "raw": None,
            "iso_utc": None,
            "epoch_sec": None,
            "detected_tz": None,
            "valid": False,
            "notes": "Missing timestamp"
        }

    raw_str = str(raw_value).strip()

    # 1. Check if numeric Unix epoch
    if re.match(r"^\d{9,12}(\.\d+)?$", raw_str):
        epoch_val = float(raw_str)
        dt_utc = datetime.fromtimestamp(epoch_val, tz=timezone.utc)
        return {
            "raw": raw_str,
            "iso_utc": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "epoch_sec": int(epoch_val),
            "detected_tz": "UNIX_EPOCH",
            "valid": True,
            "notes": "Parsed from numeric Unix timestamp"
        }

    # 2. Check for explicit timezone abbreviation like 'PST', 'PDT'
    detected_tz = None
    cleaned_str = raw_str
    for tz_name, offset_hours in TZ_OFFSETS.items():
        pattern = rf"\b{tz_name}\b"
        if re.search(pattern, raw_str, re.IGNORECASE):
            detected_tz = tz_name.upper()
            cleaned_str = re.sub(pattern, "", raw_str, flags=re.IGNORECASE).strip()
            break

    try:
        dt = date_parser.parse(cleaned_str)
        if dt.tzinfo is None:
            if detected_tz and detected_tz in TZ_OFFSETS:
                offset = timedelta(hours=TZ_OFFSETS[detected_tz])
                tz = timezone(offset)
                dt = dt.replace(tzinfo=tz)
            else:
                # Default to UTC if no other clue
                dt = dt.replace(tzinfo=timezone.utc)
                detected_tz = default_tz
        else:
            if not detected_tz:
                detected_tz = str(dt.tzinfo)

        # Convert to UTC
        dt_utc = dt.astimezone(timezone.utc)
        iso_str = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "raw": raw_str,
            "iso_utc": iso_str,
            "epoch_sec": int(dt_utc.timestamp()),
            "detected_tz": detected_tz,
            "valid": True,
            "notes": f"Normalized from {detected_tz} to UTC"
        }

    except Exception as e:
        return {
            "raw": raw_str,
            "iso_utc": None,
            "epoch_sec": None,
            "detected_tz": None,
            "valid": False,
            "notes": f"Normalization failed: {str(e)}"
        }
