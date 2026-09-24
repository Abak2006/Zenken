"""
Generates synthetic placeholder photos using Pillow (geometric landscape/abstract)
and injects synthetic EXIF metadata (GPS, camera models, timestamps) using piexif.
Simulates EXIF stripping, perceptual hashing, and tampering.
"""
from __future__ import annotations
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from PIL import Image, ImageDraw
import piexif
import imagehash

def _decimal_to_dms_rational(deg_float: float) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """Converts decimal degrees to rational tuple ((deg, 1), (min, 1), (sec*100, 100))."""
    abs_deg = abs(deg_float)
    d = int(abs_deg)
    m_float = (abs_deg - d) * 60.0
    m = int(m_float)
    s = round((m_float - m) * 60.0, 3)
    s_int = int(s * 1000)
    return ((d, 1), (m, 1), (s_int, 1000))

def create_synthetic_image(
    filename: str,
    output_dir: Path,
    title: str,
    seed: int = 42,
    palette_type: str = "sunset"
) -> Image.Image:
    """Draws an abstract geometric landscape placeholder (no human faces)."""
    random.seed(seed)
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)

    palettes = {
        "sunset": [(255, 120, 70), (220, 60, 90), (100, 40, 90), (40, 20, 60)],
        "coastal": [(60, 140, 190), (40, 90, 150), (20, 50, 90), (230, 220, 190)],
        "forest": [(34, 139, 34), (46, 117, 89), (19, 70, 45), (140, 180, 120)],
        "urban": [(120, 120, 130), (70, 75, 85), (40, 45, 50), (200, 190, 160)],
    }
    colors = palettes.get(palette_type, palettes["sunset"])

    # Gradient sky
    for y in range(height // 2):
        factor = y / (height / 2)
        r = int(colors[0][0] * (1 - factor) + colors[1][0] * factor)
        g = int(colors[0][1] * (1 - factor) + colors[1][1] * factor)
        b = int(colors[0][2] * (1 - factor) + colors[1][2] * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Celestial circle (Sun or Moon)
    sun_x = random.randint(200, 600)
    sun_y = random.randint(80, 180)
    sun_r = random.randint(40, 70)
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=(255, 245, 200))

    # Abstract Mountain ridges
    mountain_points = [
        (0, height // 2 + 50),
        (200, height // 2 - 80),
        (420, height // 2 + 30),
        (650, height // 2 - 110),
        (width, height // 2 + 10),
        (width, height),
        (0, height)
    ]
    draw.polygon(mountain_points, fill=colors[2])

    # Foreground ground / water
    draw.rectangle([0, int(height * 0.75), width, height], fill=colors[3])

    # Decorative geometric lines / grids to give modern graphic aesthetic
    for i in range(5):
        lx = (i + 1) * 130
        draw.line([(lx, int(height * 0.75)), (lx - 80, height)], fill=(colors[0][0], colors[0][1], colors[0][2], 80), width=2)

    return img

def inject_exif_metadata(
    image_path: Path,
    dt: datetime,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    camera_make: str = "Sony",
    camera_model: str = "ILCE-7M4",
    altitude_m: float = 45.0
) -> None:
    """Injects standard EXIF tags and GPS IFD using piexif."""
    date_str = dt.strftime("%Y:%m:%d %H:%M:%S")

    zeroth_ifd = {
        piexif.ImageIFD.Make: camera_make.encode("utf-8"),
        piexif.ImageIFD.Model: camera_model.encode("utf-8"),
        piexif.ImageIFD.DateTime: date_str.encode("utf-8"),
        piexif.ImageIFD.Software: b"SynthFirmware 2.10",
    }

    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: date_str.encode("utf-8"),
        piexif.ExifIFD.DateTimeDigitized: date_str.encode("utf-8"),
        piexif.ExifIFD.LensModel: b"FE 24-70mm F2.8 GM II",
    }

    gps_ifd = {}
    if lat is not None and lon is not None:
        lat_ref = b"N" if lat >= 0 else b"S"
        lon_ref = b"E" if lon >= 0 else b"W"
        lat_rational = _decimal_to_dms_rational(lat)
        lon_rational = _decimal_to_dms_rational(lon)
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: lat_ref,
            piexif.GPSIFD.GPSLatitude: lat_rational,
            piexif.GPSIFD.GPSLongitudeRef: lon_ref,
            piexif.GPSIFD.GPSLongitude: lon_rational,
            piexif.GPSIFD.GPSAltitude: (int(altitude_m * 10), 10),
            piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0)
        }

    exif_dict = {
        "0th": zeroth_ifd,
        "Exif": exif_ifd,
        "GPS": gps_ifd,
        "1st": {},
        "thumbnail": None
    }
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, str(image_path))

def generate_photo_catalog(
    case_data: Dict[str, Any],
    output_dir: Path,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """Generates the full photo evidence catalog with images, EXIF, and pHash."""
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(seed)

    venues = {v["id"]: v for v in case_data.get("venues", [])}
    catalog: List[Dict[str, Any]] = []

    photo_blueprints = [
        # Normal routine photos
        {"photo_id": "PH-001", "account": "mayalin_art", "day_offset": 5, "hour": 17, "venue_id": "venue_03", "palette": "sunset", "camera": ("Sony", "ILCE-7M4"), "strip_exif": False, "caption": "Golden hour ridge gradients"},
        {"photo_id": "PH-002", "account": "mayalin_art", "day_offset": 12, "hour": 9, "venue_id": "venue_02", "palette": "urban", "camera": ("Google", "Pixel 7"), "strip_exif": False, "caption": "Morning reflections and espresso"},
        {"photo_id": "PH-003", "account": "pixel_maya", "day_offset": -100, "hour": 15, "venue_id": "venue_01", "palette": "coastal", "camera": ("Sony", "ILCE-7M4"), "strip_exif": False, "caption": "Archived studio studies"},
        {"photo_id": "PH-004", "account": "mayalin_art", "day_offset": 20, "hour": 18, "venue_id": "venue_05", "palette": "coastal", "camera": ("Sony", "ILCE-7M4"), "strip_exif": False, "caption": "Whispering Pines evening breeze"},
        {"photo_id": "PH-005", "account": "m_lin99", "day_offset": 26, "hour": 12, "venue_id": "venue_01", "palette": "urban", "camera": ("Google", "Pixel 7"), "strip_exif": True, "caption": "Darkroom test prints (stripped)"},
        
        # Behavioral shift phase
        {"photo_id": "PH-006", "account": "mayalin_art", "day_offset": 32, "hour": 19, "venue_id": "venue_06", "palette": "forest", "camera": ("Sony", "ILCE-7M4"), "strip_exif": False, "caption": "Shadows over shoreline"},
        {"photo_id": "PH-007", "account": "m.shadow_7", "day_offset": 36, "hour": 22, "venue_id": "venue_05", "palette": "sunset", "camera": ("Motorola", "Moto G Play Synthetic"), "strip_exif": False, "caption": "Late trail inspection"},

        # Critical final 72h evidence
        {"photo_id": "PH-008", "account": "mayalin_art", "day_offset": 42, "hour": 16, "venue_id": "venue_06", "palette": "coastal", "camera": ("Google", "Pixel 7"), "strip_exif": False, "caption": "Awaiting appointment at the shoreline"},
        {"photo_id": "PH-009", "account": "m.shadow_7", "day_offset": 44, "hour": 21, "venue_id": "venue_05", "palette": "forest", "camera": ("Motorola", "Moto G Play Synthetic"), "strip_exif": False, "caption": "Final horizon from the pines"},

        # Red Herring 2 Photo (Alleged Mexico beach post from @mayalin_travels)
        {"photo_id": "PH-010", "account": "mayalin_travels", "day_offset": 44, "hour": 14, "venue_id": "venue_08", "palette": "sunset", "camera": ("Apple", "iPhone 8"), "strip_exif": False, "is_red_herring": True, "caption": "Sunny beach freedom in Cabo!"}
    ]

    base_date = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)

    for bp in photo_blueprints:
        filename = f"{bp['photo_id']}.jpg"
        filepath = output_dir / filename

        img = create_synthetic_image(
            filename=filename,
            output_dir=output_dir,
            title=bp["caption"],
            seed=seed + int(bp["photo_id"].replace("PH-", "")),
            palette_type=bp["palette"]
        )
        img.save(filepath, "JPEG", quality=92)

        # Perceptual hash
        phash_val = str(imagehash.phash(img))

        # Date calculation
        photo_dt = datetime.fromtimestamp(base_date.timestamp() + bp["day_offset"] * 86400 + bp["hour"] * 3600, tz=timezone.utc)

        venue = venues.get(bp["venue_id"], {})
        lat = venue.get("latitude")
        lon = venue.get("longitude")

        # For the red herring photo, deliberately mismatch EXIF GPS to 2024 or different coordinates
        if bp.get("is_red_herring"):
            photo_dt = datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
            lat = 22.8905 # Cabo San Lucas latitude
            lon = -109.9167

        if not bp["strip_exif"]:
            inject_exif_metadata(
                image_path=filepath,
                dt=photo_dt,
                lat=lat,
                lon=lon,
                camera_make=bp["camera"][0],
                camera_model=bp["camera"][1]
            )

        catalog.append({
            "photo_id": bp["photo_id"],
            "filename": filename,
            "filepath": str(filepath.relative_to(output_dir.parent)),
            "account": bp["account"],
            "caption": bp["caption"],
            "timestamp_utc": photo_dt.isoformat(),
            "venue_id": bp["venue_id"],
            "venue_name": venue.get("name", "Unknown"),
            "latitude": lat if not bp["strip_exif"] else None,
            "longitude": lon if not bp["strip_exif"] else None,
            "camera_make": bp["camera"][0] if not bp["strip_exif"] else None,
            "camera_model": bp["camera"][1] if not bp["strip_exif"] else None,
            "exif_stripped": bp["strip_exif"],
            "phash": phash_val,
            "is_red_herring": bp.get("is_red_herring", False)
        })

    return catalog
