"""
Generate compact, usable Geospatial Tactical Corridor maps for Overview command center.
Zero API keys required, dark tactical styling, clean embedded iframe compatibility.
"""
from pathlib import Path
import folium

def generate_overview_map(
    center: list,
    zoom: int,
    locations: list,
    trajectory: list,
    lkl: dict,
    output_path: Path
):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="OpenStreetMap",
        zoom_control=True
    )

    dark_css = """
    <style>
        .leaflet-container { 
            background-color: #0E1231 !important; 
            font-family: 'Inter', -apple-system, sans-serif !important; 
        }
        .leaflet-tile-pane { 
            filter: brightness(0.65) invert(1) contrast(2.8) hue-rotate(200deg) saturate(0.35) brightness(0.7) !important; 
        }
        .leaflet-popup-content-wrapper, .leaflet-popup-tip { 
            background: #1A2254 !important; 
            color: #FFFFFF !important; 
            border: 1px solid #2C3979 !important; 
            border-radius: 8px !important; 
            font-size: 11px !important;
        }
        .leaflet-bar a { 
            background-color: #1A2254 !important; 
            color: #FFFFFF !important; 
            border: 1px solid #2C3979 !important; 
        }
        .leaflet-bar a:hover {
            background-color: #242E70 !important;
            color: #00E5A3 !important;
        }
        .leaflet-control-attribution { 
            display: none !important; 
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(dark_css))

    # Trajectory polyline
    if trajectory and len(trajectory) >= 2:
        folium.PolyLine(
            trajectory,
            color="#3A6BFF",
            weight=3,
            opacity=0.85,
            dash_array="6, 8",
            tooltip="Tactical Movement Corridor"
        ).add_to(m)

    # Key forensic locations
    for loc in locations:
        folium.CircleMarker(
            location=[loc["lat"], loc["lon"]],
            radius=loc.get("radius", 6),
            color=loc.get("color", "#00E5A3"),
            fill=True,
            fill_color=loc.get("color", "#00E5A3"),
            fill_opacity=0.8,
            popup=f"<b>{loc['name']}</b><br/>{loc.get('desc', '')}",
            tooltip=f"{loc.get('tag', '📍')} {loc['name']}"
        ).add_to(m)

    # Candidate Last Known Location (LKL)
    folium.Marker(
        location=[lkl["lat"], lkl["lon"]],
        popup=f"<div style='font-family:Inter;'><b>🚨 CANDIDATE LKL (RANK 1)</b><br/>{lkl['name']}<br/>Confidence: {lkl.get('conf', '90+%')}<br/>{lkl.get('desc', '')}</div>",
        tooltip=f"🚨 CRITICAL LKL: {lkl['name']}",
        icon=folium.Icon(color="red", icon="star", prefix="glyphicon")
    ).add_to(m)

    folium.Circle(
        location=[lkl["lat"], lkl["lon"]],
        radius=lkl.get("radius", 450),
        color="#FF4757",
        weight=2,
        fill=True,
        fill_color="#FF4757",
        fill_opacity=0.25,
        tooltip=f"High-Probability LKL Radius ({lkl.get('radius', 450)}m)"
    ).add_to(m)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    print(f"Generated overview corridor map at: {output_path}")

def generate_all_corridor_maps():
    base_dir = Path(__file__).resolve().parent.parent

    # 1. Maya Lin (San Francisco Bay Area Corridor)
    maya_output = base_dir / "data" / "overview_corridor_map.html"
    generate_overview_map(
        center=[37.84, -122.50],
        zoom=11,
        locations=[
            {"lat": 37.788, "lon": -122.408, "name": "Bayview Arts Institute", "desc": "Last Physical Sighting (Morning)", "color": "#00E5A3", "radius": 7, "tag": "🏫"},
            {"lat": 37.824, "lon": -122.485, "name": "Pacific Horizon Diner", "desc": "Off-grid Dinner Meeting with @kaelen_v", "color": "#6C5CE7", "radius": 7, "tag": "☕"},
            {"lat": 37.830, "lon": -122.478, "name": "Battery Spencer Overlook", "desc": "Photographic EXIF Timestamp Match", "color": "#00D2D3", "radius": 6, "tag": "📷"},
            {"lat": 37.785, "lon": -122.405, "name": "Bayview South Cell Tower", "desc": "Handset +1-555-0144 CDR Ping", "color": "#F5B942", "radius": 6, "tag": "📡"}
        ],
        trajectory=[
            [37.788, -122.408],
            [37.824, -122.485],
            [37.830, -122.478],
            [37.892, -122.585]
        ],
        lkl={
            "lat": 37.892,
            "lon": -122.585,
            "name": "Whispering Pines Overlook",
            "conf": "91.4%",
            "desc": "Terminal Burner Handset Ping (+1-555-0199) at 21:45 UTC",
            "radius": 450
        },
        output_path=maya_output
    )

    # 2. Ananya Nair (Bengaluru -> Nandi Hills Ridge Corridor)
    ananya_output = base_dir / "data" / "cases" / "MP-2026-0527" / "overview_corridor_map.html"
    generate_overview_map(
        center=[13.12, 77.64],
        zoom=10,
        locations=[
            {"lat": 12.8452, "lon": 77.6602, "name": "Electronic City Tech Campus", "desc": "Last Physical Sight (Capstone review)", "color": "#00E5A3", "radius": 7, "tag": "🏫"},
            {"lat": 12.9352, "lon": 77.6245, "name": "Third Wave Coffee Koramangala", "desc": "Frequent Coding Hub & Check-in", "color": "#6C5CE7", "radius": 6, "tag": "☕"},
            {"lat": 12.9719, "lon": 77.6412, "name": "Indiranagar Roastery", "desc": "Deleted Meeting Post with @vector_zero", "color": "#F5B942", "radius": 7, "tag": "🗑️"},
            {"lat": 13.0410, "lon": 77.5910, "name": "Hebbal Lake Watchtower", "desc": "ShadowNet Secondary Uplink Active", "color": "#00D2D3", "radius": 6, "tag": "🛡️"},
            {"lat": 13.2483, "lon": 77.7126, "name": "Devanahalli Highway Corridor", "desc": "Burner Mobile Tower Sector Ping", "color": "#A29BFE", "radius": 6, "tag": "📡"}
        ],
        trajectory=[
            [12.8452, 77.6602],
            [12.9352, 77.6245],
            [12.9719, 77.6412],
            [13.0410, 77.5910],
            [13.2483, 77.7126],
            [13.3702, 77.6835]
        ],
        lkl={
            "lat": 13.3702,
            "lon": 77.6835,
            "name": "Nandi Hills Ridge Overlook",
            "conf": "93.8%",
            "desc": "Terminal Burner Handset Ping (+91-98801-0199) at 21:15 UTC",
            "radius": 400
        },
        output_path=ananya_output
    )

if __name__ == "__main__":
    generate_all_corridor_maps()
