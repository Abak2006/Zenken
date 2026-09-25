"""
Geospatial Map Builder using Folium.
Renders interactive multi-layer digital forensic tactical map with dark CartoDB tiles:
- Check-in & Photo GPS markers
- Cellular tower pings
- Chronological movement polyline
- Kernel density heatmap
- Prominent Last Known Location (LKL) marker
- TimestampedGeoJson chronological slider
- Full forensic dark theme styling
"""
from __future__ import annotations
import os
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
    m = folium.Map(
        location=[37.84, -122.50],
        zoom_start=11,
        tiles=None,
        prefer_canvas=True
    )

    # Resolve tile provider and authentication
    map_key = os.environ.get("MAP_API_KEY", "").strip()
    tile_provider = os.environ.get("MAP_TILE_PROVIDER", "dark_osm").lower()

    if tile_provider == "carto" and map_key:
        tile_url = f"https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={map_key}"
        attr = '&copy; <a href="https://carto.com/">CARTO</a>'
        use_dark_filter = False
    elif tile_provider == "stadia" and map_key:
        tile_url = f"https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={map_key}"
        attr = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>'
        use_dark_filter = False
    else:
        # High-reliability OpenStreetMap with dark tactical CSS filter (zero watermarks, no key required)
        tile_url = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        use_dark_filter = True

    # Base layer with control=False to prevent ugly raw URL in layer switchers
    folium.TileLayer(
        tiles=tile_url,
        attr=attr,
        name="Tactical Basemap",
        control=False,
        max_zoom=19
    ).add_to(m)

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
            <div style="font-family: 'Inter', sans-serif; font-size: 11px; color: #E6EDF3; padding: 4px;">
                <b style="font-size: 13px; color: #3B82F6;">{row['venue_name']}</b><br/>
                <hr style="border:none; border-top:1px solid #202833; margin: 4px 0;"/>
                <span style="color:#7D8998;">Account:</span> <b>@{acc}</b><br/>
                <span style="color:#7D8998;">Time (UTC):</span> <code style="color:#10B981;">{row['timestamp_utc']}</code><br/>
                <span style="color:#7D8998;">Platform:</span> {row['platform']}
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=260),
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
                    rh_badge = '<div style="background:rgba(239,68,68,0.2);color:#EF4444;padding:2px 6px;border-radius:3px;font-size:10px;margin-top:4px;border:1px solid #EF4444;">⚠️ RED HERRING PHOTO</div>' if is_rh else ''
                    
                    popup_ph = f"""
                    <div style="font-family: 'Inter', sans-serif; font-size: 11px; color: #E6EDF3; padding: 4px;">
                        <b style="font-size: 13px; color: #8B5CF6;">Photo {ph['photo_id']}</b> ({ph.get('filename')})<br/>
                        <hr style="border:none; border-top:1px solid #202833; margin: 4px 0;"/>
                        <span style="color:#7D8998;">Account:</span> <b>@{ph['account']}</b><br/>
                        <span style="color:#7D8998;">Camera:</span> {ph.get('camera_make')} {ph.get('camera_model')}<br/>
                        <span style="color:#7D8998;">Timestamp:</span> <code style="color:#10B981;">{ph.get('timestamp_utc')}</code><br/>
                        <span style="color:#7D8998;">Caption:</span> <em>"{ph.get('caption')}"</em>
                        {rh_badge}
                    </div>
                    """
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_ph, max_width=270),
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
            t_color = "#EF4444" if is_burner else "#10B981"

            popup_cdr = f"""
            <div style="font-family: 'Inter', sans-serif; font-size: 11px; color: #E6EDF3; padding: 4px;">
                <b style="font-size: 13px; color: {'#EF4444' if is_burner else '#10B981'};">Sector: {row['cell_tower_sector']}</b><br/>
                <hr style="border:none; border-top:1px solid #202833; margin: 4px 0;"/>
                <span style="color:#7D8998;">Handset:</span> <code>{row['caller_number']}</code><br/>
                <span style="color:#7D8998;">Recipient:</span> <code>{row['receiver_number']}</code><br/>
                <span style="color:#7D8998;">Call ID:</span> {row['call_id']} ({row['call_type']})<br/>
                <span style="color:#7D8998;">Time (UTC):</span> <code>{row['timestamp_utc']}</code>
            </div>
            """
            folium.CircleMarker(
                location=[t_lat, t_lon],
                radius=9 if is_burner else 6,
                color=t_color,
                fill=True,
                fill_color=t_color,
                fill_opacity=0.65,
                popup=folium.Popup(popup_cdr, max_width=250),
                tooltip=f"Tower Sector: {row['cell_tower_sector']} ({'Burner Handset' if is_burner else 'Primary'})"
            ).add_to(fg_towers)

            if is_burner or str(row["caller_number"]).endswith("0144"):
                tower_points.append({
                    "lat": t_lat,
                    "lon": t_lon,
                    "timestamp": row["timestamp_utc"],
                    "label": f"CDR: {row['cell_tower_sector']}"
                })

    # 4. Trajectory Path (Chronological path of Maya Lin)
    all_target_movements = checkin_points + photo_points + tower_points
    all_target_movements = [pt for pt in all_target_movements if pt["timestamp"]]
    all_target_movements.sort(key=lambda x: str(x["timestamp"]))

    if len(all_target_movements) >= 2:
        path_coords = [(pt["lat"], pt["lon"]) for pt in all_target_movements]
        folium.PolyLine(
            path_coords,
            color="#3B82F6",
            weight=2.5,
            opacity=0.85,
            dash_array="6, 8",
            tooltip="Target Chronological Movement Trajectory"
        ).add_to(fg_path)

    # 5. Last Known Location Marker (Distinct Red Star / Tactical Perimeter)
    lkl_lat, lkl_lon = 37.8924, -122.5719
    lkl_popup = """
    <div style="font-family: 'Inter', sans-serif; font-size: 12px; width: 250px; border-left: 3px solid #EF4444; padding-left: 8px; color: #E6EDF3;">
        <span style="background:rgba(239,68,68,0.2);color:#EF4444;padding:2px 6px;border-radius:3px;font-size:9px;font-weight:700;letter-spacing:0.5px;">CANDIDATE LKL (RANK 1)</span>
        <h4 style="margin: 6px 0 4px 0; color: #EF4444; font-size: 14px;">Whispering Pines Overlook</h4>
        <div style="font-size: 11px; line-height: 1.6; color: #7D8998;">
            <b style="color:#E6EDF3;">Coordinates:</b> 37.8924° N, 122.5719° W<br/>
            <b style="color:#E6EDF3;">Final Ping:</b> 2026-03-14 21:45:00 UTC<br/>
            <b style="color:#E6EDF3;">Confidence:</b> 94.0%<br/>
            <span style="color:#E6EDF3;">Burner handset (+1-555-0199) powered down after this sector ping.</span>
        </div>
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
        color="#EF4444",
        weight=2,
        fill=True,
        fill_color="#EF4444",
        fill_opacity=0.25,
        tooltip="High-Probability Disappearance Search Radius (350m)"
    ).add_to(fg_lkl)

    # 6. HeatMap of routine activity
    heat_data = [[pt["lat"], pt["lon"], 1.0] for pt in all_target_movements]
    if heat_data:
        HeatMap(heat_data, name="Activity Density Heatmap", radius=22, blur=15, min_opacity=0.3, show=False).add_to(m)

    # 7. TimestampedGeoJson time slider
    features = []
    for pt in all_target_movements:
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
                    "popup": f"<b>{pt['label']}</b><br/>Time: {pt['timestamp']}",
                    "icon": "circle",
                    "iconstyle": {
                        "fillColor": "#3B82F6",
                        "fillOpacity": 0.9,
                        "stroke": "true",
                        "color": "#E6EDF3",
                        "weight": 1,
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

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    # Custom CSS Injection for Dark Workstation Leaflet UI
    tile_filter_css = """
        .leaflet-tile-pane {
            filter: brightness(0.65) invert(1) contrast(2.8) hue-rotate(200deg) saturate(0.35) brightness(0.7) !important;
        }
    """ if use_dark_filter else ""

    dark_css = f"""
    <style>
        .leaflet-container {{
            background-color: #05070B !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }}
        {tile_filter_css}
        .leaflet-popup-content-wrapper, .leaflet-popup-tip {{
            background: #10151D !important;
            color: #E2E8F0 !important;
            border: 1px solid #222B38 !important;
            border-radius: 8px !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.75) !important;
        }}
        .leaflet-popup-content {{
            margin: 8px 12px !important;
            line-height: 1.5 !important;
        }}
        .leaflet-control-layers {{
            background: rgba(16, 21, 29, 0.94) !important;
            color: #E2E8F0 !important;
            border: 1px solid #222B38 !important;
            backdrop-filter: blur(14px) !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 11px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6) !important;
        }}
        .leaflet-control-layers-expanded label {{
            color: #CBD5E1 !important;
            font-weight: 500 !important;
            margin-bottom: 5px !important;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }}
        .leaflet-control-layers-separator {{
            border-top: 1px solid #222B38 !important;
            margin: 8px 0 !important;
        }}
        .leaflet-bar a {{
            background-color: #10151D !important;
            color: #E2E8F0 !important;
            border: 1px solid #222B38 !important;
        }}
        .leaflet-bar a:hover {{
            background-color: #141A23 !important;
            color: #4F7CFF !important;
        }}
        .leaflet-control-attribution {{
            background: rgba(5, 7, 11, 0.85) !important;
            color: #64748B !important;
            font-size: 10px !important;
        }}
        .leaflet-control-attribution a {{
            color: #4F7CFF !important;
        }}
    </style>
    """
    m.get_root().html.add_child(folium.Element(dark_css))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    return str(output_path)

if __name__ == "__main__":
    out = build_folium_map()
    print(f"Investigation Map Saved to: {out}")
