"""
Digital Forensics EXIF Metadata Extractor.
Parses camera signatures, timestamps, GPS coordinates (DMS -> DD),
flags stripped metadata, and flags evidentiary anomalies (temporal skew, device shifts).
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from PIL import Image
import piexif
import imagehash

def _dms_rational_to_decimal(dms_tuples: Tuple, ref: str) -> Optional[float]:
    """Converts EXIF rational DMS ((deg_num, deg_den), ...) to signed decimal degrees."""
    try:
        deg = dms_tuples[0][0] / dms_tuples[0][1]
        minute = dms_tuples[1][0] / dms_tuples[1][1]
        sec = dms_tuples[2][0] / dms_tuples[2][1]
        dec = deg + (minute / 60.0) + (sec / 3600.0)
        if ref.upper() in ["S", "W"]:
            dec = -dec
        return round(dec, 6)
    except Exception:
        return None

def extract_image_forensics(
    image_path: Path | str,
    known_devices: Optional[list] = None,
    expected_bounding_box: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Extracts forensic metadata from an image file, including hashes, EXIF, and anomaly detection.
    """
    path = Path(image_path)
    if not path.exists():
        return {"filename": path.name, "error": "File does not exist", "valid": False}

    # 1. Cryptographic hash (SHA-256)
    with open(path, "rb") as f:
        data_bytes = f.read()
    sha256_hash = hashlib.sha256(data_bytes).hexdigest()

    # 2. Perceptual hash
    try:
        with Image.open(path) as img:
            phash_val = str(imagehash.phash(img))
            dimensions = (img.width, img.height)
    except Exception as e:
        return {"filename": path.name, "error": f"Corrupt image: {str(e)}", "valid": False}

    # 3. EXIF parsing
    exif_raw = None
    try:
        exif_raw = piexif.load(str(path))
    except Exception:
        pass

    has_exif = bool(exif_raw and any(exif_raw.get(k) for k in ["0th", "Exif", "GPS"]))

    make = None
    model = None
    software = None
    datetime_original = None
    lat = None
    lon = None
    altitude = None

    if has_exif:
        zeroth = exif_raw.get("0th", {})
        if piexif.ImageIFD.Make in zeroth:
            make = zeroth[piexif.ImageIFD.Make].decode("utf-8", errors="ignore").strip()
        if piexif.ImageIFD.Model in zeroth:
            model = zeroth[piexif.ImageIFD.Model].decode("utf-8", errors="ignore").strip()
        if piexif.ImageIFD.Software in zeroth:
            software = zeroth[piexif.ImageIFD.Software].decode("utf-8", errors="ignore").strip()

        exif_sub = exif_raw.get("Exif", {})
        if piexif.ExifIFD.DateTimeOriginal in exif_sub:
            dt_raw = exif_sub[piexif.ExifIFD.DateTimeOriginal].decode("utf-8", errors="ignore").strip()
            # Parse YYYY:MM:DD HH:MM:SS
            try:
                dt_parsed = datetime.strptime(dt_raw, "%Y:%m:%d %H:%M:%S")
                datetime_original = dt_parsed.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                datetime_original = dt_raw

        gps_data = exif_raw.get("GPS", {})
        if piexif.GPSIFD.GPSLatitude in gps_data and piexif.GPSIFD.GPSLongitude in gps_data:
            lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef, b"N").decode("utf-8", errors="ignore")
            lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef, b"W").decode("utf-8", errors="ignore")
            lat = _dms_rational_to_decimal(gps_data[piexif.GPSIFD.GPSLatitude], lat_ref)
            lon = _dms_rational_to_decimal(gps_data[piexif.GPSIFD.GPSLongitude], lon_ref)

        if piexif.GPSIFD.GPSAltitude in gps_data:
            alt_tup = gps_data[piexif.GPSIFD.GPSAltitude]
            if alt_tup[1] != 0:
                altitude = round(alt_tup[0] / alt_tup[1], 1)

    # 4. Evidentiary Anomaly Detection
    anomalies = []
    
    # Metadata stripping flag
    is_stripped = not has_exif or (make is None and model is None and lat is None)
    if is_stripped:
        anomalies.append("EXIF_METADATA_STRIPPED")

    # GPS presence
    has_gps = lat is not None and lon is not None
    if has_exif and not has_gps:
        anomalies.append("NO_GPS_COORDINATES")

    # Temporal Anomaly (e.g. photo timestamp significantly older than 2026)
    if datetime_original:
        try:
            year = int(datetime_original[:4])
            if year < 2026:
                anomalies.append(f"HISTORICAL_OR_ARCHIVAL_TIMESTAMP (Year: {year} vs Case Year: 2026)")
        except Exception:
            pass

    # Device Mismatch Check
    if known_devices and model:
        if not any(known.lower() in model.lower() for known in known_devices):
            anomalies.append(f"UNEXPECTED_CAMERA_HARDWARE ({model} not in known victim profile)")

    # Geographic boundary check (e.g. expected Bay Area: lat ~37.2 to 38.5, lon ~ -123.0 to -121.8)
    if expected_bounding_box and lat is not None and lon is not None:
        min_lat = expected_bounding_box.get("min_lat", 37.0)
        max_lat = expected_bounding_box.get("max_lat", 38.5)
        min_lon = expected_bounding_box.get("min_lon", -123.5)
        max_lon = expected_bounding_box.get("max_lon", -121.5)
        if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
            anomalies.append(f"GEOGRAPHIC_OUTLIER (Lat: {lat}, Lon: {lon} outside expected area)")

    return {
        "filename": path.name,
        "filepath": str(path),
        "sha256": sha256_hash,
        "phash": phash_val,
        "dimensions": dimensions,
        "has_exif": has_exif,
        "camera_make": make,
        "camera_model": model,
        "software": software,
        "datetime_original": datetime_original,
        "latitude": lat,
        "longitude": lon,
        "altitude_meters": altitude,
        "is_stripped": is_stripped,
        "anomalies": anomalies,
        "valid": True
    }
