"""
Persona and identity definitions loaded from case_bible.yaml.
Deterministic synthesis of personal and demographic attributes.
"""
from __future__ import annotations
from typing import Dict, Any, List
import yaml
from pathlib import Path

def load_case_bible(case_path: Path | str | None = None) -> Dict[str, Any]:
    if case_path is None:
        case_path = Path(__file__).resolve().parent.parent / "case" / "case_bible.yaml"
    else:
        case_path = Path(case_path)
    with open(case_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_target_identities(case_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return case_data.get("digital_identities", [])

def get_associates(case_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return case_data.get("associates", [])

def get_venues(case_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return case_data.get("venues", [])
