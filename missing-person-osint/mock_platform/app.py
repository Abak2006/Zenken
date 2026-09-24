"""
Flask mock social media platform server.
Serves synthetic profiles, posts, media files, and JSON endpoints.
Includes rate limiting simulation and private profile protections to test collectors realistically.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, List
from flask import Flask, jsonify, request, render_template, send_from_directory, Response
import pandas as pd

app = Flask(__name__, template_folder="templates")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Simulated rate limiter state
REQUEST_LOG: Dict[str, List[float]] = {}
RATE_LIMIT_MAX = 40  # Max requests per window
RATE_LIMIT_WINDOW = 30  # Window in seconds

def check_rate_limit(client_ip: str) -> bool:
    """Returns True if request is within rate limit, False if exceeded."""
    if request.headers.get("X-Forensic-Bypass") == "true":
        return True
    now = time.time()
    timestamps = REQUEST_LOG.get(client_ip, [])
    # Evict timestamps outside the sliding window
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    timestamps.append(now)
    REQUEST_LOG[client_ip] = timestamps
    return len(timestamps) <= RATE_LIMIT_MAX

def load_data():
    profiles_path = DATA_DIR / "profiles.json"
    posts_path = DATA_DIR / "posts.csv"

    profiles = []
    if profiles_path.exists():
        with open(profiles_path, "r", encoding="utf-8") as f:
            profiles = json.load(f)

    posts_df = pd.DataFrame()
    if posts_path.exists():
        posts_df = pd.read_csv(posts_path)

    return profiles, posts_df

@app.before_request
def apply_rate_limit():
    client_ip = request.remote_addr or "127.0.0.1"
    if request.path.startswith(("/api", "/u/")):
        if not check_rate_limit(client_ip):
            return jsonify({
                "error": "Too Many Requests",
                "message": "Simulated rate limit exceeded. Please back off.",
                "retry_after_seconds": 2
            }), 429

@app.route("/")
def index():
    profiles, posts_df = load_data()
    return jsonify({
        "status": "online",
        "service": "Simulated Social Network (Mock OSINT Target Platform)",
        "available_profiles_count": len(profiles),
        "available_posts_count": len(posts_df),
        "endpoints": {
            "robots": "/robots.txt",
            "profiles_list": "/api/profiles",
            "profile_detail": "/api/profiles/<handle>",
            "profile_html": "/u/<handle>",
            "posts_list": "/api/posts",
            "photos": "/photos/<filename>"
        }
    })

@app.route("/robots.txt")
def robots_txt():
    content = "User-agent: *\nDisallow: /private/\nDisallow: /api/internal/\nCrawl-delay: 1\n"
    return Response(content, mimetype="text/plain")

@app.route("/api/profiles", methods=["GET"])
def api_profiles():
    profiles, _ = load_data()
    # Filter public profiles by default unless all requested
    include_private = request.args.get("all", "false").lower() == "true"
    result = [p for p in profiles if include_private or not p.get("is_private", False)]
    return jsonify({"count": len(result), "profiles": result})

@app.route("/api/profiles/<handle>", methods=["GET"])
def api_profile_detail(handle: str):
    profiles, _ = load_data()
    match = next((p for p in profiles if p["handle"].lower() == handle.lower()), None)
    if not match:
        return jsonify({"error": "Profile not found", "handle": handle}), 404

    if match.get("is_private", False) and request.headers.get("X-Auth-Token") != "secret_investigator_token":
        return jsonify({
            "error": "Account is private",
            "handle": match["handle"],
            "display_name": match["display_name"],
            "platform": match["platform"],
            "is_private": True,
            "message": "Full profile details and posts are restricted."
        }), 403

    return jsonify(match)

@app.route("/api/posts", methods=["GET"])
def api_posts():
    _, posts_df = load_data()
    if posts_df.empty:
        return jsonify({"count": 0, "posts": []})

    account = request.args.get("account")
    include_deleted = request.args.get("include_deleted", "false").lower() == "true"

    df = posts_df
    if not include_deleted and "deleted" in df.columns:
        df = df[df["deleted"] == False]
    if account:
        df = df[df["account"].str.lower() == account.lower()]

    limit = int(request.args.get("limit", 100))
    posts_list = df.head(limit).to_dict(orient="records")
    return jsonify({"count": len(posts_list), "posts": posts_list})

@app.route("/u/<handle>")
def html_profile(handle: str):
    profiles, posts_df = load_data()
    match = next((p for p in profiles if p["handle"].lower() == handle.lower()), None)
    if not match:
        return f"<h2>User @{handle} not found</h2>", 404

    account_posts = []
    if not match.get("is_private", False) and not posts_df.empty:
        # Public posts only
        df = posts_df[(posts_df["account"].str.lower() == handle.lower()) & (posts_df["deleted"] == False)]
        account_posts = df.to_dict(orient="records")

    return render_template("profile.html", profile=match, posts=account_posts)

@app.route("/photos/<path:filename>")
def serve_photo(filename: str):
    photos_dir = DATA_DIR / "photos"
    return send_from_directory(photos_dir, filename)

def create_app():
    return app

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mock Platform Server")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    args = parser.parse_args()
    print(f"Starting Mock Social Media Platform on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)
