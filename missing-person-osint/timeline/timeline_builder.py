"""
Interactive Multi-Lane Timeline Builder using Plotly.
Plots distinct swimlanes for Social Posts, Telecommunications (CDR), Geo Check-ins, and Photos,
with forensic annotations highlighting behavioral change points, deleted evidence, and terminal pings.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from typing import Dict, Any, List
import pandas as pd
import plotly.graph_objects as go

def build_investigation_timeline(
    data_dir: Path | None = None,
    output_html_path: Path | None = None
) -> Dict[str, Any]:
    """
    Build investigation timeline using improved visualization.
    This wrapper uses the improved timeline builder for better UX.
    """
    from timeline.improved_timeline import build_improved_timeline
    return build_improved_timeline(data_dir, output_html_path)

# Legacy function kept for backward compatibility
def build_legacy_timeline(
    data_dir: Path | None = None,
    output_html_path: Path | None = None
) -> Dict[str, Any]:
    """Legacy timeline builder (kept for reference)."""
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
    if output_html_path is None:
        output_html_path = data_dir / "investigation_timeline_legacy.html"

    # Collect multi-source events
    events = []

    # 1. Social Posts
    posts_path = data_dir / "posts.csv"
    if posts_path.exists():
        pdf = pd.read_csv(posts_path)
        for _, r in pdf.iterrows():
            is_del = bool(r.get("deleted", False))
            events.append({
                "lane": "1. Social Media Posts",
                "timestamp": r["timestamp_utc_iso"],
                "label": f"@{r['account']}: {str(r['text'])[:45]}...",
                "details": f"Post ID: {r['post_id']}<br>Author: @{r['account']}<br>Deleted: {is_del}<br>Text: {r['text']}",
                "event_type": "Deleted Post" if is_del else "Public Post",
                "color": "#ef4444" if is_del else "#3b82f6",
                "symbol": "x" if is_del else "circle",
                "size": 12 if is_del else 8
            })

    # 2. Telephony & CDR
    cdrs_path = data_dir / "call_records.csv"
    if cdrs_path.exists():
        cdf = pd.read_csv(cdrs_path)
        for _, r in cdf.iterrows():
            caller = str(r["caller_number"])
            is_burner = caller.endswith("0199")
            events.append({
                "lane": "2. Telecommunications (CDR)",
                "timestamp": r["timestamp_utc"],
                "label": f"Call {r['call_id']} ({r['duration_sec']}s)",
                "details": f"Caller: {r['caller_number']}<br>Receiver: {r['receiver_number']}<br>Tower: {r['cell_tower_sector']}<br>Duration: {r['duration_sec']}s",
                "event_type": "Burner Handset Ping" if is_burner else "Voice Call",
                "color": "#f97316" if is_burner else "#10b981",
                "symbol": "diamond" if is_burner else "circle",
                "size": 11 if is_burner else 8
            })

    # 3. Geo Check-ins
    checkins_path = data_dir / "checkins.csv"
    if checkins_path.exists():
        chdf = pd.read_csv(checkins_path)
        for _, r in chdf.iterrows():
            events.append({
                "lane": "3. Physical Check-ins",
                "timestamp": r["timestamp_utc"],
                "label": f"Check-in: {r['venue_name']}",
                "details": f"Check-in ID: {r['checkin_id']}<br>Account: @{r['account']}<br>Venue: {r['venue_name']}<br>Platform: {r['platform']}",
                "event_type": "Venue Check-in",
                "color": "#eab308",
                "symbol": "square",
                "size": 9
            })

    # 4. Photos
    photos_path = data_dir / "photos_metadata.json"
    if photos_path.exists():
        with open(photos_path, "r", encoding="utf-8") as f:
            pdata = json.load(f)
            for ph in pdata:
                is_rh = ph.get("is_red_herring", False)
                events.append({
                    "lane": "4. Photo EXIF Signatures",
                    "timestamp": ph["timestamp_utc"],
                    "label": f"Photo {ph['photo_id']} ({ph.get('camera_model')})",
                    "details": f"Photo ID: {ph['photo_id']}<br>Account: @{ph['account']}<br>Camera: {ph.get('camera_make')} {ph.get('camera_model')}<br>EXIF Stripped: {ph.get('exif_stripped')}<br>Caption: {ph.get('caption')}",
                    "event_type": "Red Herring Photo" if is_rh else "Captured Photo",
                    "color": "#ec4899" if is_rh else "#06b6d4",
                    "symbol": "triangle-up",
                    "size": 10
                })

    df_ev = pd.DataFrame(events)
    df_ev["dt"] = pd.to_datetime(df_ev["timestamp"])
    df_ev = df_ev.sort_values(by="dt").reset_index(drop=True)

    # Build Plotly Multi-Lane Figure
    fig = go.Figure()

    for etype in df_ev["event_type"].unique():
        subset = df_ev[df_ev["event_type"] == etype]
        first_row = subset.iloc[0]
        fig.add_trace(go.Scatter(
            x=subset["dt"],
            y=subset["lane"],
            mode="markers",
            name=etype,
            marker=dict(
                color=first_row["color"],
                symbol=first_row["symbol"],
                size=first_row["size"],
                line=dict(color="#ffffff", width=1)
            ),
            text=subset["label"],
            customdata=subset["details"],
            hovertemplate="<b>%{y}</b><br>Time: %{x}<br>%{customdata}<extra></extra>"
        ))

    # Forensic Annotations for Milestone Inflection Points
    annotations = [
        ("2026-02-18 16:20:00", "Breakup with Lucas Reed (Argumentative posts)", "#f87171"),
        ("2026-03-01 14:10:00", "Inbound contact from @kaelen_v (Off-grid commission)", "#60a5fa"),
        ("2026-03-03 22:45:00", "Behavioral Shift: Fear & Surveillance mentions", "#fbbf24"),
        ("2026-03-10 11:30:00", "Burner Phone (+1-555-0199) Activated", "#fb923c"),
        ("2026-03-12 09:15:00", "Evidence Sanitization: 3 Posts Deleted", "#ef4444"),
        ("2026-03-14 21:45:00", "TERMINAL EVENT: Last Tower Ping (Whispering Pines)", "#dc2626")
    ]

    for dt_str, text, col in annotations:
        fig.add_vline(
            x=pd.to_datetime(dt_str),
            line_width=1.5,
            line_dash="dash",
            line_color=col,
            annotation_text=text,
            annotation_position="top left",
            annotation_font_size=10,
            annotation_font_color=col
        )

    fig.update_layout(
        title="Multi-Lane OSINT Forensic Timeline: Disappearance of Maya Lin",
        template="plotly_dark",
        height=650,
        margin=dict(l=40, r=40, t=80, b=40),
        xaxis=dict(
            title="Chronological Timeline (UTC)",
            showgrid=True,
            gridcolor="#334155"
        ),
        yaxis=dict(
            title="Evidence Source Lanes",
            showgrid=True,
            gridcolor="#334155",
            autorange="reversed"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html_path))

    return {
        "total_events": len(df_ev),
        "lanes": df_ev["lane"].unique().tolist(),
        "earliest_event": df_ev["timestamp"].min(),
        "latest_event": df_ev["timestamp"].max(),
        "html_file": str(output_html_path)
    }

if __name__ == "__main__":
    res = build_investigation_timeline()
    print("Timeline Built Successfully:", res)
