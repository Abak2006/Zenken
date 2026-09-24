"""
Chain of Custody and Evidence Integrity Ledger.
Calculates cryptographic SHA-256 hashes, maintains immutable provenance records,
and ensures evidence auditability across the digital forensic pipeline.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

class ChainOfCustody:
    def __init__(self, ledger_path: Path | str | None = None):
        if ledger_path is None:
            self.ledger_path = Path(__file__).resolve().parent.parent / "data" / "chain_of_custody.jsonl"
        else:
            self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def calculate_sha256(data_bytes: bytes) -> str:
        """Computes hexadecimal SHA-256 digest."""
        return hashlib.sha256(data_bytes).hexdigest()

    def record_artifact(
        self,
        artifact_id: str,
        source: str,
        content_type: str,
        raw_data: bytes | str,
        collector_name: str = "MockCollector/1.0",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Logs a newly collected digital forensic artifact to the chain of custody ledger.
        """
        if isinstance(raw_data, str):
            raw_bytes = raw_data.encode("utf-8")
        else:
            raw_bytes = raw_data

        sha256_hash = self.calculate_sha256(raw_bytes)
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        entry = {
            "entry_id": f"COC-{int(datetime.now().timestamp()*1000)}",
            "artifact_id": artifact_id,
            "timestamp_utc": now_iso,
            "collector": collector_name,
            "source_uri": source,
            "content_type": content_type,
            "byte_size": len(raw_bytes),
            "sha256_hash": sha256_hash,
            "metadata": metadata or {}
        }

        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def read_ledger(self) -> List[Dict[str, Any]]:
        """Reads all entries from the audit ledger."""
        if not self.ledger_path.exists():
            return []
        entries = []
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries
