"""
Generate structured timeline events for Case MP-2026-0419 (Maya Lin).
Generates missing-person-osint/data/timeline_events.json containing 92 structured forensic events
derived 1-to-1 from Maya's evidence records (31 posts, 24 calls, 27 checkins, 10 photos).
"""
import json
from pathlib import Path
import pandas as pd

def generate_maya_timeline_events():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    
    events = []
    
    # 1. Social Posts (31 items)
    posts_path = data_dir / "posts.csv"
    if posts_path.exists():
        pdf = pd.read_csv(posts_path)
        for _, r in pdf.iterrows():
            is_del = bool(r.get("deleted", False))
            pid = str(r["post_id"])
            ts = str(r.get("timestamp_utc_iso") or r.get("timestamp_raw", ""))
            
            severity = "CRITICAL" if is_del else ("NOTABLE" if "kaelen" in str(r.get("mentions", "")).lower() or "kaelen" in str(r.get("text", "")).lower() else "NORMAL")
            phase = "Digital Sanitization" if is_del else ("Inbound Outreach" if "kaelen" in str(r.get("text", "")).lower() else "Baseline Activity")
            
            events.append({
                "event_id": f"EV-ML-P{pid}",
                "timestamp": ts,
                "case_id": "MP-2026-0419",
                "source_type": "Social Media",
                "event_type": "Deleted Post" if is_del else "Public Post",
                "severity": severity,
                "description": f"@{r['account']}: {str(r['text'])[:90]}",
                "entity_ids": ["maya_lin", f"@{r['account']}"],
                "location_id": "venue_01",
                "location_name": str(r.get("location_tag") or "San Francisco Bay Area"),
                "evidence_ids": [pid],
                "confidence": 1.0,
                "phase": phase
            })

    # 2. Telecom CDR (24 items)
    calls_path = data_dir / "call_records.csv"
    if calls_path.exists():
        cdf = pd.read_csv(calls_path)
        for _, r in cdf.iterrows():
            cid = str(r["call_id"])
            caller = str(r["caller_number"])
            is_burner = caller.endswith("0199") or str(r["receiver_number"]).endswith("0199")
            is_terminal = "whispering" in str(r.get("cell_tower_sector", "")).lower() or cid == "CDR-0142"
            
            severity = "CRITICAL" if (is_terminal or is_burner) else "NORMAL"
            phase = "Terminal LKL" if is_terminal else ("Digital Sanitization" if is_burner else "Baseline Activity")
            
            events.append({
                "event_id": f"EV-ML-C{cid}",
                "timestamp": str(r["timestamp_utc"]),
                "case_id": "MP-2026-0419",
                "source_type": "Telecommunications",
                "event_type": "Burner Handset Ping" if is_burner else "Voice Call",
                "severity": severity,
                "description": f"CDR: {caller} -> {r['receiver_number']} ({r['duration_sec']}s) sector {r['cell_tower_sector']}",
                "entity_ids": ["maya_lin", caller, str(r["receiver_number"])],
                "location_id": "tower_loc",
                "location_name": str(r.get("cell_tower_sector", "Cell Sector")),
                "evidence_ids": [cid],
                "confidence": 1.0,
                "phase": phase
            })

    # 3. Check-ins (27 items)
    chk_path = data_dir / "checkins.csv"
    if chk_path.exists():
        chdf = pd.read_csv(chk_path)
        for _, r in chdf.iterrows():
            chid = str(r["checkin_id"])
            vname = str(r["venue_name"])
            is_suspicious = "pacific horizon" in vname.lower() or "overlook" in vname.lower()
            severity = "SUSPICIOUS" if is_suspicious else "NORMAL"
            phase = "Inbound Outreach" if "pacific horizon" in vname.lower() else "Baseline Activity"
            
            events.append({
                "event_id": f"EV-ML-K{chid}",
                "timestamp": str(r["timestamp_utc"]),
                "case_id": "MP-2026-0419",
                "source_type": "Physical Location",
                "event_type": "Venue Check-in",
                "severity": severity,
                "description": f"@{r['account']} checked in at {vname} ({r.get('platform', 'Geo')})",
                "entity_ids": ["maya_lin", f"@{r['account']}"],
                "location_id": str(r.get("venue_id", "venue")),
                "location_name": vname,
                "evidence_ids": [chid],
                "confidence": 0.95,
                "phase": phase
            })

    # 4. Photos EXIF (10 items)
    ph_path = data_dir / "photos_metadata.json"
    if ph_path.exists():
        with open(ph_path, "r", encoding="utf-8") as f:
            photos = json.load(f)
            for ph in photos:
                phid = str(ph["photo_id"])
                is_rh = bool(ph.get("is_red_herring", False))
                severity = "SUSPICIOUS" if is_rh else "NOTABLE"
                
                events.append({
                    "event_id": f"EV-ML-F{phid}",
                    "timestamp": str(ph.get("timestamp_utc", "")),
                    "case_id": "MP-2026-0419",
                    "source_type": "Photo / EXIF",
                    "event_type": "Red Herring Photo" if is_rh else "EXIF Photo",
                    "severity": severity,
                    "description": f"EXIF photo capture: {ph['filename']} ({ph.get('camera_model', 'Camera')})",
                    "entity_ids": ["maya_lin", f"@{ph.get('account', 'maya')}"],
                    "location_id": str(ph.get("venue_id", "photo_loc")),
                    "location_name": f"{ph.get('latitude', '')}, {ph.get('longitude', '')}" if ph.get("latitude") else "Stripped EXIF",
                    "evidence_ids": [phid],
                    "confidence": 0.35 if is_rh else 0.98,
                    "phase": "Digital Sanitization" if is_rh else "Baseline Activity"
                })

    # Sort chronologically
    events.sort(key=lambda x: str(x["timestamp"]))
    
    out_path = data_dir / "timeline_events.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
    
    print(f"Generated Maya timeline_events.json: {len(events)} structured events at {out_path}")
    return len(events)

if __name__ == "__main__":
    generate_maya_timeline_events()
