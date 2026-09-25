"""
Improved Timeline Builder with Professional Forensic Investigation UX
Fixes overlapping legends, unreadable collision labels, time compression, and clutter.
Provides 5 multi-modal lanes, intelligent 6-hour clustering, milestone flags, and dark styling.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Forensic semantic colors
TIMELINE_COLORS = {
    "Deleted Post": "#EF4444",          # Critical Red
    "Public Post": "#3B82F6",           # Blue
    "Burner Handset Ping": "#EF4444",   # Critical Red
    "Voice Call": "#10B981",            # Green
    "Venue Check-in": "#06B6D4",        # Cyan
    "Red Herring Photo": "#F59E0B",     # Amber/Orange Warning
    "Captured Photo": "#8B5CF6",        # Purple
    "Behavioral Milestone": "#EF4444"   # Red Inflection
}

LANE_ORDER = [
    "5. OSINT & Behavioral",
    "4. Photo EXIF Signatures",
    "3. Physical Check-ins",
    "2. Telecommunications (CDR)",
    "1. Social Media Posts"
]

def cluster_events(events_df: pd.DataFrame, time_window_hours: int = 6) -> pd.DataFrame:
    """
    Cluster dense events occurring within a sliding time window to prevent visual crowding.
    """
    if len(events_df) == 0:
        return events_df
    
    events_df = events_df.sort_values("dt").copy()
    events_df["cluster_id"] = 0
    
    current_cluster = 0
    cluster_start = events_df.iloc[0]["dt"]
    
    for idx, row in events_df.iterrows():
        time_diff = (row["dt"] - cluster_start).total_seconds() / 3600
        if time_diff > time_window_hours:
            current_cluster += 1
            cluster_start = row["dt"]
        events_df.at[idx, "cluster_id"] = current_cluster
    
    # Check cluster counts per lane
    events_df["cluster_key"] = events_df["lane"] + "_" + events_df["cluster_id"].astype(str)
    counts = events_df.groupby("cluster_key").size()
    events_df["is_clustered"] = events_df["cluster_key"].map(counts) >= 4
    
    return events_df

def build_improved_timeline(
    data_dir: Path | None = None,
    output_html_path: Path | None = None
) -> Dict[str, Any]:
    """
    Construct high-fidelity forensic timeline with:
    - 5 investigation lanes
    - Legend placed cleanly at bottom outside graph canvas (zero overlap with annotations)
    - Default view focused on Active Case Window (Feb 15 - Mar 16, 2026)
    - Clean numbered milestone badges with dedicated reference
    - Hover cards with full multi-modal metadata
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
    if output_html_path is None:
        output_html_path = data_dir / "investigation_timeline.html"

    events = []

    # 1. Social Posts
    posts_path = data_dir / "posts.csv"
    if posts_path.exists():
        pdf = pd.read_csv(posts_path)
        for _, r in pdf.iterrows():
            is_del = bool(r.get("deleted", False))
            etype = "Deleted Post" if is_del else "Public Post"
            events.append({
                "lane": "1. Social Media Posts",
                "timestamp": r["timestamp_utc_iso"],
                "label": f"POST-{r['post_id']}",
                "details": f"<b>@{r['account']}</b> ({'DELETED RECOVERED' if is_del else 'PUBLIC'})<br/>{r['text']}",
                "event_type": etype,
                "color": TIMELINE_COLORS[etype],
                "symbol": "x" if is_del else "circle",
                "size": 11 if is_del else 8
            })

    # 2. Telephony & CDR
    cdrs_path = data_dir / "call_records.csv"
    if cdrs_path.exists():
        cdf = pd.read_csv(cdrs_path)
        for _, r in cdf.iterrows():
            caller = str(r["caller_number"])
            is_burner = caller.endswith("0199")
            etype = "Burner Handset Ping" if is_burner else "Voice Call"
            events.append({
                "lane": "2. Telecommunications (CDR)",
                "timestamp": r["timestamp_utc"],
                "label": f"CDR-{r['call_id']}",
                "details": f"<b>{'BURNER (+1-555-0199)' if is_burner else 'PRIMARY'}</b><br/>Tower: {r['cell_tower_sector']}<br/>Duration: {r['duration_sec']}s",
                "event_type": etype,
                "color": TIMELINE_COLORS[etype],
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
                "label": f"CHK-{r['checkin_id']}",
                "details": f"<b>{r['venue_name']}</b><br/>Account: @{r['account']}<br/>Platform: {r['platform']}",
                "event_type": "Venue Check-in",
                "color": TIMELINE_COLORS["Venue Check-in"],
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
                etype = "Red Herring Photo" if is_rh else "Captured Photo"
                events.append({
                    "lane": "4. Photo EXIF Signatures",
                    "timestamp": ph["timestamp_utc"],
                    "label": f"PHOTO-{ph['photo_id']}",
                    "details": f"<b>{'⚠️ RED HERRING' if is_rh else 'AUTHENTIC PHOTO'}</b><br/>Camera: {ph.get('camera_make')} {ph.get('camera_model')}<br/>Caption: {ph.get('caption')}",
                    "event_type": etype,
                    "color": TIMELINE_COLORS[etype],
                    "symbol": "triangle-up" if not is_rh else "triangle-down",
                    "size": 10
                })

    # 5. OSINT & Behavioral Milestones
    milestones = [
        ("2026-02-18 16:20:00", "Breakup with Lucas Reed (Hostile public comments)", "Milestone 1"),
        ("2026-03-01 14:10:00", "Inbound contact from @kaelen_v (Private shoot offer)", "Milestone 2"),
        ("2026-03-03 22:45:00", "Behavioral Shift: First expressions of surveillance paranoia", "Milestone 3"),
        ("2026-03-06 18:00:00", "Covert Persona: @m.shadow_7 account activated", "Milestone 4"),
        ("2026-03-10 11:30:00", "Handset Shift: Primary (+1-555-0144) dark; Burner activated", "Milestone 5"),
        ("2026-03-12 09:15:00", "Evidence Sanitization: 3 posts deleted referencing Diner meeting", "Milestone 6"),
        ("2026-03-14 21:45:00", "TERMINAL EVENT: Final cell tower ping at Whispering Pines", "Milestone 7")
    ]
    for ts_str, desc, tag in milestones:
        events.append({
            "lane": "5. OSINT & Behavioral",
            "timestamp": ts_str,
            "label": tag,
            "details": f"<b>{tag}</b><br/>{desc}",
            "event_type": "Behavioral Milestone",
            "color": TIMELINE_COLORS["Behavioral Milestone"],
            "symbol": "star",
            "size": 13
        })

    df_ev = pd.DataFrame(events)
    df_ev["dt"] = pd.to_datetime(df_ev["timestamp"], format="mixed", utc=True)
    df_ev = df_ev.sort_values(by="dt").reset_index(drop=True)

    # Apply 6-hour clustering to dense events
    df_ev = cluster_events(df_ev, time_window_hours=6)

    fig = go.Figure()

    # Plot Non-clustered events
    non_clustered = df_ev[~df_ev["is_clustered"]]
    for etype in non_clustered["event_type"].unique():
        subset = non_clustered[non_clustered["event_type"] == etype]
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
                line=dict(color="#05070A", width=1.2)
            ),
            text=subset["label"],
            customdata=subset["details"],
            hovertemplate="<b>%{y}</b><br/><span style='color:#7D8998;'>Time:</span> %{x|%Y-%m-%d %H:%M UTC}<br/>%{customdata}<extra></extra>",
            showlegend=True
        ))

    # Plot Clustered events
    clustered = df_ev[df_ev["is_clustered"]]
    for ckey in clustered["cluster_key"].unique():
        grp = clustered[clustered["cluster_key"] == ckey]
        if len(grp) == 0:
            continue
        lane = grp["lane"].iloc[0]
        med_time = grp["dt"].iloc[len(grp) // 2]
        common_type = grp["event_type"].mode()[0]
        cluster_color = TIMELINE_COLORS.get(common_type, "#3B82F6")
        
        detail_lines = "<br/>".join([f"• <b>{r['label']}</b>: {r['details'][:60]}" for _, r in grp.head(6).iterrows()])
        if len(grp) > 6:
            detail_lines += f"<br/><em>+ {len(grp) - 6} more events...</em>"

        fig.add_trace(go.Scatter(
            x=[med_time],
            y=[lane],
            mode="markers+text",
            name=f"Clustered Group",
            text=[f"[{len(grp)}]"],
            textposition="top center",
            textfont=dict(size=9, color="#E6EDF3"),
            marker=dict(
                color=cluster_color,
                symbol="circle",
                size=18,
                line=dict(color="#FFFFFF", width=1.5)
            ),
            customdata=[f"<b>Cluster ({len(grp)} Events):</b><br/>{detail_lines}"],
            hovertemplate="%{customdata}<extra></extra>",
            showlegend=False
        ))

    # Add Subtle Milestone Vertical Dotted Lines (Without Overlapping Text)
    for ts_str, desc, tag in milestones:
        fig.add_vline(
            x=pd.to_datetime(ts_str, utc=True),
            line_width=1,
            line_dash="dot",
            line_color="rgba(239, 68, 68, 0.45)"
        )

    # Workstation Dark Layout
    fig.update_layout(
        template="plotly_dark",
        height=620,
        margin=dict(l=160, r=40, t=30, b=80),
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#202833",
            tickfont=dict(size=11, color="#7D8998"),
            # DEFAULT FOCUS: Active Case Window (Feb 15 - Mar 16, 2026)
            range=["2026-02-15 00:00:00", "2026-03-16 00:00:00"],
            rangeselector=dict(
                bgcolor="#10151C",
                bordercolor="#202833",
                borderwidth=1,
                font=dict(color="#E6EDF3", size=10),
                buttons=list([
                    dict(count=3, label="Final 72H", step="day", stepmode="backward"),
                    dict(count=7, label="7 Days", step="day", stepmode="backward"),
                    dict(count=30, label="Case 30D", step="day", stepmode="backward"),
                    dict(step="all", label="All (2Y)")
                ])
            )
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#202833",
            tickfont=dict(size=12, color="#E6EDF3", family="Inter, sans-serif"),
            categoryorder="array",
            categoryarray=LANE_ORDER,
            fixedrange=True
        ),
        # LEGEND AT BOTTOM (NEVER OVERLAPPING CHART OR ANNOTATIONS)
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.14,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#7D8998"),
            bgcolor="rgba(16, 21, 28, 0.8)",
            bordercolor="#202833",
            borderwidth=1
        ),
        plot_bgcolor="#080B10",
        paper_bgcolor="#05070A",
        hoverlabel=dict(
            bgcolor="#10151C",
            bordercolor="#202833",
            font=dict(size=11, color="#E6EDF3", family="Inter, sans-serif")
        )
    )

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html_path), include_plotlyjs="cdn")

    return {
        "total_events": len(df_ev),
        "clustered_events": len(clustered),
        "lanes": df_ev["lane"].unique().tolist(),
        "html_file": str(output_html_path)
    }

if __name__ == "__main__":
    res = build_improved_timeline()
    print("Timeline Built Successfully:", res)
