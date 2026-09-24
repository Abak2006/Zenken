"""
Geospatial Map Builder using Folium.
Renders interactive multi-layer digital forensic map with:
- Check-in & Photo GPS markers
- Cellular tower pings
- Chronological movement polyline
- Kernel density heatmap
- Prominent Last Known Location (LKL) marker
- TimestampedGeoJson chronological slider
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import folium
from folium.plugins import HeatMap, TimestampedGeoJson
import pandas as pd

def build_folium_map(
    data_dir: Path | None = None,
    output_path: Path | None = None
) -> str:
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
    if output_path is None:
        output_path = data_dir / "investigation_map.html"

    # Map center: San Francisco Bay / Marin coastal area
    m = folium.Map(location=[37.83, -122.47], zoom_start=11, tiles="OpenStreetMap")

    # Feature groups for toggleable layers
    fg_checkins = folium.FeatureGroup(name="Venue Check-ins (Social)", show=True)
    fg_photos = folium.FeatureGroup(name="Photo EXIF GPS Pins", show=True)
    fg_towers = folium.FeatureGroup(name="Cell Tower CDR Pings", show=True)
    fg_path = folium.FeatureGroup(name="Movement Trajectory Path", show=True)
    fg_lkl = folium.FeatureGroup(name="Last Known Location (LKL)", show=True)

    # 1. Load and plot check-ins
    checkins_path = data_dir / "checkins.csv"
    checkin_points = []
    if checkins_path.exists():
        chk_df = pd.read_csv(checkins_path)
        for _, row in chk_df.iterrows():
            lat, lon = row["latitude"], row["longitude"]
            acc = row["account"]
            is_target = acc in ["mayalin_art", "m_lin99", "m.shadow_7"]
            color = "blue" if is_target else "gray"
            icon_name = "map-marker" if is_target else "info-sign"

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; width: 200px;">
                <b>{row['venue_name']}</b><br>
                <b>Account:</b> @{acc}<br>
                <b>Time:</b> {row['timestamp_utc']}<br>
                <b>Platform:</b> {row['platform']}
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"@{acc} @ {row['venue_name']}",
                icon=folium.Icon(color=color, icon=icon_name, prefix="glyphicon")
            ).add_to(fg_checkins)

            if is_target:
                checkin_points.append({
                    "lat": lat,
                    "lon": lon,
                    "timestamp": row["timestamp_utc"],
                    "label": f"Check-in: {row['venue_name']}"
                })

    # 2. Load and plot Photo GPS
    photos_path = data_dir / "photos_metadata.json"
    photo_points = []
    if photos_path.exists():
        with open(photos_path, "r", encoding="utf-8") as f:
            photos_data = json.load(f)
            for ph in photos_data:
                lat, lon = ph.get("latitude"), ph.get("longitude")
                if lat is not None and lon is not None:
                    is_rh = ph.get("is_red_herring", False)
                    p_color = "purple" if not is_rh else "orange"
                    rh_tag = '<b style="color:red;">RED HERRING PHOTO</b>' if is_rh else ''
                    popup_ph = f"""
                    <div style="font-family: sans-serif; font-size: 12px; width: 220px;">
                        <b>Photo: {ph['photo_id']}</b> ({ph.get('filename')})<br>
                        <b>Account:</b> @{ph['account']}<br>
                        <b>Camera:</b> {ph.get('camera_make')} {ph.get('camera_model')}<br>
                        <b>Time:</b> {ph.get('timestamp_utc')}<br>
                        <b>Caption:</b> {ph.get('caption')}<br>
                        {rh_tag}
                    </div>
                    """
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_ph, max_width=250),
                        tooltip=f"Photo {ph['photo_id']} (@{ph['account']})",
                        icon=folium.Icon(color=p_color, icon="camera", prefix="glyphicon")
                    ).add_to(fg_photos)

                    if not is_rh:
                        photo_points.append({
                            "lat": lat,
                            "lon": lon,
                            "timestamp": ph.get("timestamp_utc"),
                            "label": f"Photo: {ph['photo_id']}"
                        })

    # 3. Load Cell Tower pings
    cdr_path = data_dir / "call_records.csv"
    tower_points = []
    if cdr_path.exists():
        cdr_df = pd.read_csv(cdr_path)
        for _, row in cdr_df.iterrows():
            t_lat, t_lon = row["tower_latitude"], row["tower_longitude"]
            is_burner = str(row["caller_number"]).endswith("0199")
            t_color = "red" if is_burner else "darkgreen"

            popup_cdr = f"""
            <div style="font-family: sans-serif; font-size: 12px; width: 210px;">
                <b>Cell Tower: {row['cell_tower_sector']}</b><br>
                <b>Handset:</b> {row['caller_number']}<br>
                <b>Recipient:</b> {row['receiver_number']}<br>
                <b>Call ID:</b> {row['call_id']} ({row['call_type']})<br>
                <b>Time:</b> {row['timestamp_utc']}
            </div>
            """
            folium.CircleMarker(
                location=[t_lat, t_lon],
                radius=9 if is_burner else 6,
                color=t_color,
                fill=True,
                fill_color=t_color,
                fill_opacity=0.6,
                popup=folium.Popup(popup_cdr, max_width=250),
                tooltip=f"Tower Sector: {row['cell_tower_sector']}"
            ).add_to(fg_towers)

            if is_burner or str(row["caller_number"]).endswith("0144"):
                tower_points.append({
                    "lat": t_lat,
                    "lon": t_lon,
                    "timestamp": row["timestamp_utc"],
                    "label": f"CDR: {row['cell_tower_sector']}"
                })

    # 4. Trajectory Path (Ordered movement of target identity)
    all_target_movements = checkin_points + photo_points + tower_points
    all_target_movements = [pt for pt in all_target_movements if pt["timestamp"]]
    all_target_movements.sort(key=lambda x: str(x["timestamp"]))

    if len(all_target_movements) >= 2:
        path_coords = [(pt["lat"], pt["lon"]) for pt in all_target_movements]
        folium.PolyLine(
            path_coords,
            color="#ef4444",
            weight=3,
            opacity=0.8,
            dash_array="6, 8",
            tooltip="Target Chronological Movement Trajectory"
        ).add_to(fg_path)

    # 5. Last Known Location Marker (Distinct star / marker)
    # Whispering Pines Overlook: 37.8924, -122.5719
    lkl_lat, lkl_lon = 37.8924, -122.5719
    lkl_popup = """
    <div style="font-family: sans-serif; font-size: 13px; width: 240px; border-left: 4px solid red; padding-left: 8px;">
        <h4 style="margin: 0 0 6px 0; color: #b91c1c;">TRUE LAST KNOWN LOCATION</h4>
        <b>Venue:</b> Whispering Pines Overlook<br>
        <b>Coordinates:</b> 37.8924, -122.5719<br>
        <b>Last Signal:</b> 2026-03-14 21:45:00 UTC<br>
        <b>Source:</b> Burner phone (+1-555-0199) final cell tower ping before device powered down.
    </div>
    """
    folium.Marker(
        location=[lkl_lat, lkl_lon],
        popup=folium.Popup(lkl_popup, max_width=300),
        tooltip="🚨 CRITICAL: Last Known Location (2026-03-14 21:45 UTC)",
        icon=folium.Icon(color="red", icon="star", prefix="glyphicon")
    ).add_to(fg_lkl)

    folium.Circle(
        location=[lkl_lat, lkl_lon],
        radius=350,
        color="#b91c1c",
        fill=True,
        fill_color="#f87171",
        fill_opacity=0.35,
        tooltip="High-Probability Disappearance Search Radius (350m)"
    ).add_to(fg_lkl)

    # 6. HeatMap of routine activity
    heat_data = [[pt["lat"], pt["lon"], 1.0] for pt in all_target_movements]
    if heat_data:
        HeatMap(heat_data, name="Activity Density Heatmap", radius=22, blur=15, min_opacity=0.3, show=False).add_to(m)

    # 7. TimestampedGeoJson time slider
    features = []
    for pt in all_target_movements:
        # Standard ISO timestamp format required by leaflet plugin
        ts_clean = str(pt["timestamp"]).replace("Z", "")
        if "T" in ts_clean:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [pt["lon"], pt["lat"]]
                },
                "properties": {
                    "time": ts_clean,
                    "popup": f"<b>{pt['label']}</b><br>Time: {pt['timestamp']}",
                    "icon": "circle",
                    "iconstyle": {
                        "fillColor": "#e11d48",
                        "fillOpacity": 0.8,
                        "stroke": "true",
                        "radius": 7
                    }
                }
            }
            features.append(feature)

    if features:
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        TimestampedGeoJson(
            geojson_data,
            period="PT6H",
            add_last_point=True,
            auto_play=False,
            loop=False,
            max_speed=2,
            loop_button=True,
            date_options="YYYY-MM-DD HH:mm",
            time_slider_drag_update=True
        ).add_to(m)

    # Attach all feature groups to map
    fg_checkins.add_to(m)
    fg_photos.add_to(m)
    fg_towers.add_to(m)
    fg_path.add_to(m)
    fg_lkl.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    return str(output_path)

if __name__ == "__main__":
    out = build_folium_map()
    print(f"Investigation Map Saved to: {out}")
