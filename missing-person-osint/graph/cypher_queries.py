"""
Catalogue of 10+ Analytical and Forensic Cypher Queries for Neo4j.
Each query addresses a specific investigative hypothesis or evidentiary link.
"""
from __future__ import annotations
from typing import Dict, Any, List

CYPHER_QUERIES: List[Dict[str, Any]] = [
    {
        "query_id": "CYPHER-01",
        "title": "Shortest Path from Missing Person to Covert / Suspicious Contact",
        "objective": "Identify intermediaries or communication vectors connecting Maya Lin to Kaelen Vance.",
        "cypher": """
MATCH (p1:Person {name: 'Maya Lin'}), (p2:Person {name: 'Kaelen Vance'})
MATCH path = shortestPath((p1)-[*..6]-(p2))
RETURN path, length(path) AS hops;
        """.strip()
    },
    {
        "query_id": "CYPHER-02",
        "title": "All Telecommunications & Interactions in the Critical 72-Hour Window",
        "objective": "Isolate calls and posts that took place between 2026-03-12T00:00:00Z and 2026-03-15T00:00:00Z.",
        "cypher": """
MATCH (n)-[r:CONTACTED|POSTED|CHECKED_IN_AT]->(m)
WHERE r.timestamp >= '2026-03-12T00:00:00Z' AND r.timestamp <= '2026-03-15T00:00:00Z'
RETURN n.label, type(r), r.timestamp, m.label
ORDER BY r.timestamp DESC;
        """.strip()
    },
    {
        "query_id": "CYPHER-03",
        "title": "Co-Located Accounts at Specific Venues (Spatiotemporal Overlap)",
        "objective": "Find distinct accounts that checked in or photographed the same physical venue.",
        "cypher": """
MATCH (a1:Account)-[:CHECKED_IN_AT]->(loc:Location)<-[:CHECKED_IN_AT]-(a2:Account)
WHERE a1 <> a2
RETURN loc.name AS Venue, a1.handle AS Account1, a2.handle AS Account2;
        """.strip()
    },
    {
        "query_id": "CYPHER-04",
        "title": "Phone Numbers Linked to Multiple Person Identities or Handsets",
        "objective": "Detect burner usage or shared hardware across multiple aliases.",
        "cypher": """
MATCH (p:Person)-[:OWNS]->(ph:Phone)
WITH ph, collect(p.name) AS Owners, count(p) AS OwnerCount
WHERE OwnerCount > 1
RETURN ph.number AS PhoneNumber, Owners, OwnerCount;
        """.strip()
    },
    {
        "query_id": "CYPHER-05",
        "title": "High-Frequency Call Partners for Target Handsets",
        "objective": "Rank incoming and outgoing call frequency to surface key contacts.",
        "cypher": """
MATCH (ph1:Phone)-[c:CONTACTED]->(ph2:Phone)
RETURN ph1.number AS Caller, ph2.number AS Receiver, count(c) AS CallCount, sum(c.duration_sec) AS TotalDuration
ORDER BY CallCount DESC;
        """.strip()
    },
    {
        "query_id": "CYPHER-06",
        "title": "Accounts Connected by SAME_AS High-Confidence Resolvers",
        "objective": "View resolved identity clusters with confidence >= 0.75.",
        "cypher": """
MATCH (a1:Account)-[s:SAME_AS]->(a2:Account)
RETURN a1.handle AS IdentityA, a2.handle AS IdentityB, s.confidence AS Confidence, s.rationale AS Evidence
ORDER BY s.confidence DESC;
        """.strip()
    },
    {
        "query_id": "CYPHER-07",
        "title": "Deleted Content and Associated Accounts & Mentions",
        "objective": "Locate sanitized evidence (posts with deleted=true) and who was tagged in them.",
        "cypher": """
MATCH (a:Account)-[:POSTED]->(p:Post {deleted: true})
OPTIONAL MATCH (p)-[:MENTIONS]->(m:Account)
RETURN a.handle AS Author, p.post_id AS PostID, p.timestamp AS Timestamp, p.text AS ScrubbedText, m.handle AS Mentioned;
        """.strip()
    },
    {
        "query_id": "CYPHER-08",
        "title": "Photos Captured with Known Target Camera Models",
        "objective": "Identify all photos captured using Maya's primary camera signature (Sony ILCE-7M4).",
        "cypher": """
MATCH (ph:Photo {camera_model: 'ILCE-7M4'})<-[:APPEARS_IN]-(a:Account)
OPTIONAL MATCH (ph)-[:TAKEN_AT]->(loc:Location)
RETURN ph.filename AS PhotoFile, a.handle AS Uploader, loc.name AS Venue, ph.latitude AS Lat, ph.longitude AS Lon;
        """.strip()
    },
    {
        "query_id": "CYPHER-09",
        "title": "Direct Circle of Associates Surrounding the Target",
        "objective": "Extract all accounts with 1-degree social follow or mention edges to Maya Lin.",
        "cypher": """
MATCH (target:Account {handle: 'mayalin_art'})-[r:FOLLOWS|MENTIONS]-(associate:Account)
RETURN associate.handle AS Associate, type(r) AS InteractionType, r.context AS Context;
        """.strip()
    },
    {
        "query_id": "CYPHER-10",
        "title": "Last Recorded Cell Tower Pings Prior to Disappearance",
        "objective": "Trace the geographical movement of cellular handset pings ordered by timestamp.",
        "cypher": """
MATCH (ph:Phone)-[c:CONTACTED]->()
WHERE c.cell_tower IS NOT NULL
RETURN c.timestamp AS Timestamp, ph.number AS Handset, c.cell_tower AS TowerSector
ORDER BY c.timestamp ASC;
        """.strip()
    }
]

def get_query(query_id: str) -> Dict[str, Any] | None:
    return next((q for q in CYPHER_QUERIES if q["query_id"] == query_id), None)
