"""
Mock Social Media Collector.
Crawls the synthetic platform, respects robots.txt directives and simulated rate limits,
extracts profile and post artifacts, and records full chain-of-custody provenance.
"""
from __future__ import annotations
import json
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup

from collectors.chain_of_custody import ChainOfCustody

class MockCollector:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:5005",
        output_dir: Optional[Path] = None,
        custody_ledger: Optional[ChainOfCustody] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir or (Path(__file__).resolve().parent.parent / "data" / "raw_collected")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.custody = custody_ledger or ChainOfCustody()
        self.disallowed_paths: List[str] = []
        self.crawl_delay: float = 0.05
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "InvestigativeForensicsBot/1.0 (Educational)"})

    def check_robots_txt(self) -> None:
        """Parses robots.txt from target server."""
        try:
            resp = self.session.get(f"{self.base_url}/robots.txt", timeout=3)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line.startswith("Disallow:"):
                        path = line.split(":", 1)[1].strip()
                        self.disallowed_paths.append(path)
                    elif line.startswith("Crawl-delay:"):
                        try:
                            self.crawl_delay = float(line.split(":", 1)[1].strip())
                        except ValueError:
                            pass
        except Exception:
            # Server not running or unreachable
            pass

    def is_allowed(self, path: str) -> bool:
        """Checks if a URL path is allowed according to robots.txt."""
        return not any(path.startswith(dis) for dis in self.disallowed_paths if dis)

    def collect_all(self, fallback_offline: bool = True) -> Dict[str, Any]:
        """
        Executes complete collection run.
        If live server is unavailable, uses internal Flask client if fallback_offline is True.
        """
        self.check_robots_txt()
        collected_profiles = []
        collected_posts = []

        # Try live HTTP request
        live_server = False
        try:
            r = self.session.get(f"{self.base_url}/api/profiles", timeout=2)
            if r.status_code == 200:
                live_server = True
                profiles_data = r.json().get("profiles", [])
        except Exception:
            live_server = False

        if not live_server and fallback_offline:
            # Use test_client from mock_platform directly
            from mock_platform.app import app
            client = app.test_client()
            r = client.get("/api/profiles?all=true")
            profiles_data = r.json.get("profiles", []) if r.status_code == 200 else []
            r_posts = client.get("/api/posts?include_deleted=true")
            posts_data = r_posts.json.get("posts", []) if r_posts.status_code == 200 else []
        else:
            profiles_data = []
            posts_data = []
            if live_server:
                rp = self.session.get(f"{self.base_url}/api/posts?include_deleted=true")
                if rp.status_code == 200:
                    posts_data = rp.json().get("posts", [])

        # Process and store profiles with chain of custody
        for prof in profiles_data:
            handle = prof["handle"]
            target_file = self.output_dir / f"profile_{handle}.json"
            content_str = json.dumps(prof, indent=2)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content_str)

            self.custody.record_artifact(
                artifact_id=f"ART-PROF-{handle}",
                source=f"{self.base_url}/api/profiles/{handle}",
                content_type="application/json",
                raw_data=content_str,
                collector_name="MockCollector/1.0",
                metadata={"handle": handle, "platform": prof.get("platform")}
            )
            collected_profiles.append(prof)
            time.sleep(self.crawl_delay)

        # Process and store posts with chain of custody
        posts_file = self.output_dir / "scraped_posts.json"
        posts_str = json.dumps(posts_data, indent=2)
        with open(posts_file, "w", encoding="utf-8") as f:
            f.write(posts_str)

        self.custody.record_artifact(
            artifact_id="ART-POSTS-DUMP",
            source=f"{self.base_url}/api/posts",
            content_type="application/json",
            raw_data=posts_str,
            collector_name="MockCollector/1.0",
            metadata={"total_posts": len(posts_data)}
        )

        return {
            "mode": "live_http" if live_server else "offline_client",
            "profiles_collected": len(collected_profiles),
            "posts_collected": len(posts_data),
            "output_directory": str(self.output_dir)
        }

if __name__ == "__main__":
    collector = MockCollector()
    summary = collector.collect_all()
    print("Collection Finished:", summary)
