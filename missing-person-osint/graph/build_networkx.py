"""
Multi-Modal Investigation Graph Builder using NetworkX.
Creates typed nodes (Person, Account, Phone, Location, Post, Photo, Device)
and typed edges (OWNS, FOLLOWS, POSTED, MENTIONS, CHECKED_IN_AT, CONTACTED, SAME_AS).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Optional
import networkx as nx
import pandas as pd

def build_investigation_graph(
    data_dir: Path | None = None,
    include_low_confidence: bool = True
) -> nx.MultiDiGraph:
    """
    Constructs an evidentiary NetworkX MultiDiGraph from all generated & correlated datasets.
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"

    G = nx.MultiDiGraph()

    # 1. Load profiles and resolved identity clusters
    with open(data_dir / "profiles.json", "r", encoding="utf-8") as f:
        profiles = json.load(f)

    resolved_clusters = []
    cluster_file = data_dir / "resolved_identities.json"
    if cluster_file.exists():
        with open(cluster_file, "r", encoding="utf-8") as f:
            res_data = json.load(f)
            resolved_clusters = res_data.get("clusters", [])

    # Map account to Person canonical entity
    account_to_person = {}
    for cluster in resolved_clusters:
        p_id = cluster["canonical_id"]
        is_target_node = bool(
            "MAYA_LIN" in p_id or 
            "ANANYA_NAIR" in p_id or 
            cluster.get("is_target", False) or 
            cluster.get("is_primary_subject", False)
        )
        G.add_node(
            p_id,
            node_type="Person",
            label=cluster["canonical_name"],
            name=cluster["canonical_name"],
            is_target=is_target_node,
            accounts=cluster.get("accounts", []),
            phones=cluster.get("linked_phones", []),
            emails=cluster.get("linked_emails", [])
        )
        for acc in cluster.get("accounts", []):
            account_to_person[acc.lower()] = p_id

    # Add Account nodes
    for p in profiles:
        acc_handle = p["handle"]
        acc_node_id = f"ACC_{acc_handle.lower()}"
        G.add_node(
            acc_node_id,
            node_type="Account",
            label=f"@{acc_handle}",
            handle=acc_handle,
            platform=p.get("platform", "Unknown"),
            email=p.get("email"),
            phone=p.get("phone"),
            is_private=p.get("is_private", False),
            followers=p.get("followers_count", 0)
        )

        # Link Person -> OWNS -> Account
        person_id = account_to_person.get(acc_handle.lower())
        if person_id:
            G.add_edge(person_id, acc_node_id, edge_type="OWNS", confidence=1.0)

    # 2. Add Phone nodes & OWNS / CONTACTED edges
    phones_path = data_dir / "phones.csv"
    if phones_path.exists():
        phones_df = pd.read_csv(phones_path)
        for _, row in phones_df.iterrows():
            ph_num = str(row["phone_number"])
            ph_node_id = f"PHONE_{ph_num.replace('+', '').replace('-', '')}"
            G.add_node(
                ph_node_id,
                node_type="Phone",
                label=ph_num,
                number=ph_num,
                carrier=row.get("carrier"),
                plan_type=row.get("plan_type"),
                status=row.get("status")
            )
            # Check owner hint or match to person
            for cluster in resolved_clusters:
                if ph_num in cluster.get("linked_phones", []):
                    G.add_edge(cluster["canonical_id"], ph_node_id, edge_type="OWNS", confidence=0.95)

    # Add CDR edges (CONTACTED)
    cdrs_path = data_dir / "call_records.csv"
    if cdrs_path.exists():
        cdrs_df = pd.read_csv(cdrs_path)
        for _, row in cdrs_df.iterrows():
            caller_id = f"PHONE_{str(row['caller_number']).replace('+', '').replace('-', '')}"
            receiver_id = f"PHONE_{str(row['receiver_number']).replace('+', '').replace('-', '')}"
            if not G.has_node(caller_id):
                G.add_node(caller_id, node_type="Phone", label=str(row['caller_number']), number=str(row['caller_number']))
            if not G.has_node(receiver_id):
                G.add_node(receiver_id, node_type="Phone", label=str(row['receiver_number']), number=str(row['receiver_number']))
            G.add_edge(
                caller_id,
                receiver_id,
                edge_type="CONTACTED",
                call_id=row.get("call_id"),
                timestamp=row.get("timestamp_utc"),
                duration_sec=row.get("duration_sec"),
                cell_tower=row.get("cell_tower_sector"),
                confidence=1.0
            )

    # 3. Add Location / Venue nodes
    venues = []
    if (data_dir / "venues.json").exists():
        with open(data_dir / "venues.json", "r", encoding="utf-8") as f:
            venues = json.load(f)
    elif (data_dir / "case_bible.json").exists():
        with open(data_dir / "case_bible.json", "r", encoding="utf-8") as f:
            cb_json = json.load(f)
            venues = cb_json.get("venues", [])
    elif (data_dir.parent / "case" / "case_bible.yaml").exists():
        import yaml
        with open(data_dir.parent / "case" / "case_bible.yaml", "r", encoding="utf-8") as f:
            cb = yaml.safe_load(f)
            venues = cb.get("venues", [])

    for v in venues:
        loc_id = f"LOC_{v['id']}"
        G.add_node(
            loc_id,
            node_type="Location",
            label=v.get("name", loc_id),
            venue_id=v.get("id"),
            name=v.get("name", loc_id),
            category=v.get("category", "General"),
            latitude=v.get("latitude"),
            longitude=v.get("longitude"),
            address=v.get("address")
        )

    # 4. Add Check-in edges
    checkins_path = data_dir / "checkins.csv"
    if checkins_path.exists():
        checkins_df = pd.read_csv(checkins_path)
        for _, row in checkins_df.iterrows():
            acc_id = f"ACC_{str(row['account']).lower()}"
            v_id = row.get("venue_id")
            if pd.isna(v_id) or not v_id:
                v_name = str(row.get("venue_name", "unknown"))
                v_id = v_name.lower().replace(" ", "_")[:24]
            loc_id = f"LOC_{v_id}"
            if not G.has_node(loc_id):
                G.add_node(
                    loc_id,
                    node_type="Location",
                    label=str(row.get("venue_name", loc_id)),
                    name=str(row.get("venue_name", loc_id)),
                    latitude=row.get("latitude"),
                    longitude=row.get("longitude")
                )
            if G.has_node(acc_id):
                G.add_edge(
                    acc_id,
                    loc_id,
                    edge_type="CHECKED_IN_AT",
                    checkin_id=row.get("checkin_id"),
                    timestamp=row.get("timestamp_utc"),
                    confidence=0.9
                )

    # 5. Add Post and Photo nodes & edges
    posts_path = data_dir / "posts.csv"
    if posts_path.exists():
        posts_df = pd.read_csv(posts_path)
        for _, row in posts_df.iterrows():
            p_id = f"POST_{row['post_id']}"
            ts = row.get("timestamp_utc_iso") or row.get("timestamp_raw") or row.get("timestamp_utc") or ""
            G.add_node(
                p_id,
                node_type="Post",
                label=f"Post {row['post_id']}",
                post_id=row["post_id"],
                timestamp=ts,
                text=row.get("text", ""),
                deleted=bool(row.get("deleted", False)),
                sentiment=row.get("sentiment_label")
            )
            # Edge: Account -> POSTED -> Post
            acc_id = f"ACC_{str(row['account']).lower()}"
            if G.has_node(acc_id):
                G.add_edge(acc_id, p_id, edge_type="POSTED", timestamp=ts)

            # Mentions edge
            mentions = str(row.get("mentions", "")).split(";") if pd.notna(row.get("mentions")) else []
            for m in mentions:
                clean_m = m.strip().lstrip("@").lower()
                m_node = f"ACC_{clean_m}"
                if G.has_node(m_node):
                    G.add_edge(p_id, m_node, edge_type="MENTIONS", context="post_mention")

    # Photo nodes
    photos_meta_path = data_dir / "photos_metadata.json"
    if photos_meta_path.exists():
        with open(photos_meta_path, "r", encoding="utf-8") as f:
            photos_list = json.load(f)
            for ph in photos_list:
                ph_node_id = f"PHOTO_{ph['photo_id']}"
                G.add_node(
                    ph_node_id,
                    node_type="Photo",
                    label=ph["photo_id"],
                    photo_id=ph["photo_id"],
                    filename=ph["filename"],
                    phash=ph.get("phash"),
                    latitude=ph.get("latitude"),
                    longitude=ph.get("longitude"),
                    camera_model=ph.get("camera_model"),
                    is_stripped=ph.get("exif_stripped", False)
                )
                # Link Account -> POSTED/APPEARS_IN -> Photo
                acc_id = f"ACC_{ph['account'].lower()}"
                if G.has_node(acc_id):
                    G.add_edge(acc_id, ph_node_id, edge_type="APPEARS_IN", timestamp=ph["timestamp_utc"])

                # Link Photo -> Location if geo is present
                if ph.get("venue_id"):
                    loc_id = f"LOC_{ph['venue_id']}"
                    if G.has_node(loc_id):
                        G.add_edge(ph_node_id, loc_id, edge_type="TAKEN_AT", latitude=ph.get("latitude"), longitude=ph.get("longitude"))

    # 6. Add Social Connections (FOLLOWS)
    conns_path = data_dir / "connections.csv"
    if conns_path.exists():
        conns_df = pd.read_csv(conns_path)
        for _, row in conns_df.iterrows():
            src = f"ACC_{str(row['source']).lower()}"
            tgt = f"ACC_{str(row['target']).lower()}"
            if G.has_node(src) and G.has_node(tgt):
                G.add_edge(
                    src,
                    tgt,
                    edge_type=row.get("relationship_type", "FOLLOWS"),
                    weight=row.get("weight", 1.0),
                    context=row.get("context")
                )

    # 7. Add SAME_AS identity resolution edges
    if cluster_file.exists():
        with open(cluster_file, "r", encoding="utf-8") as f:
            confirmed_links = json.load(f).get("confirmed_links", [])
            for link in confirmed_links:
                acc_a = f"ACC_{link['account_a'].lower()}"
                acc_b = f"ACC_{link['account_b'].lower()}"
                if G.has_node(acc_a) and G.has_node(acc_b):
                    G.add_edge(
                        acc_a,
                        acc_b,
                        edge_type="SAME_AS",
                        confidence=link["confidence"],
                        rationale=link["rationale"]
                    )

    # 8. Add Git Repos & Commits
    git_path = data_dir / "git_commits.json"
    if git_path.exists():
        with open(git_path, "r", encoding="utf-8") as f:
            commits = json.load(f)
            for c in commits:
                c_id = f"COMMIT_{c['commit_id']}"
                G.add_node(
                    c_id,
                    node_type="GitCommit",
                    label=f"Commit: {c['commit_id']}",
                    commit_sha=c.get("commit_sha"),
                    repo=c.get("repo"),
                    branch=c.get("branch"),
                    message=c.get("message"),
                    timestamp=c.get("timestamp_utc"),
                    pgp_valid=c.get("pgp_signature_valid", False)
                )
                acc_handle = c.get("author_account")
                if acc_handle:
                    acc_id = f"ACC_{acc_handle.lower()}"
                    if G.has_node(acc_id):
                        G.add_edge(acc_id, c_id, edge_type="COMMITTED", timestamp=c.get("timestamp_utc"))

    # 9. Add Transit & Infrastructure Sensors
    sensor_path = data_dir / "transit_sensors.json"
    if sensor_path.exists():
        with open(sensor_path, "r", encoding="utf-8") as f:
            sensors = json.load(f)
            for s in sensors:
                s_id = f"SENSOR_{s['sensor_event_id']}"
                G.add_node(
                    s_id,
                    node_type="SensorEvent",
                    label=f"{s.get('event_type')}: {s['sensor_event_id']}",
                    sensor_type=s.get("event_type"),
                    location=s.get("sensor_location"),
                    latitude=s.get("latitude"),
                    longitude=s.get("longitude"),
                    timestamp=s.get("timestamp_utc")
                )

    # 10. Add Crypto Escrow Nodes
    escrow_path = data_dir / "crypto_escrow.json"
    if escrow_path.exists():
        with open(escrow_path, "r", encoding="utf-8") as f:
            escrows = json.load(f)
            for esc in escrows:
                tx_node_id = f"TX_{esc['tx_id']}"
                G.add_node(
                    tx_node_id,
                    node_type="FinancialTransaction",
                    label=f"{esc.get('tx_type')}: {esc['tx_id']}",
                    network=esc.get("network"),
                    amount=esc.get("amount"),
                    timestamp=esc.get("timestamp_utc")
                )

    # 11. Add Device Artifact Nodes
    devices_path = data_dir / "devices.json"
    if devices_path.exists():
        with open(devices_path, "r", encoding="utf-8") as f:
            devices = json.load(f)
            for d in devices:
                d_id = f"DEV_{d['device_id']}"
                G.add_node(
                    d_id,
                    node_type="Device",
                    label=f"Device: {d.get('device_name', d['device_id'])}",
                    device_id=d["device_id"],
                    device_type=d.get("device_type"),
                    platform=d.get("platform"),
                    imei_mac=d.get("imei_or_mac"),
                    status=d.get("status")
                )
                owner = d.get("associated_account") or d.get("owner_entity")
                if owner:
                    owner_node = f"ACC_{owner.lstrip('@').lower()}"
                    if G.has_node(owner_node):
                        G.add_edge(owner_node, d_id, edge_type="OPERATES", timestamp=d.get("timestamp_utc", ""))
                # If tied to target person
                for cluster in resolved_clusters:
                    if d["device_id"] in cluster.get("linked_devices", []):
                        G.add_edge(cluster["canonical_id"], d_id, edge_type="OWNS", confidence=1.0)

    # 12. Add OSINT Correlation Nodes & Edges
    osint_path = data_dir / "osint_links.json"
    if osint_path.exists():
        with open(osint_path, "r", encoding="utf-8") as f:
            links = json.load(f)
            for lk in links:
                lk_id = f"OSINT_{lk['link_id']}"
                G.add_node(
                    lk_id,
                    node_type="OSINTCorrelation",
                    label=f"OSINT: {lk['link_id']}",
                    platform=lk.get("platform"),
                    basis=lk.get("basis"),
                    confidence=lk.get("confidence")
                )
                src = lk.get("source_account")
                tgt = lk.get("target_account")
                if src:
                    src_node = f"ACC_{src.lstrip('@').lower()}"
                    if G.has_node(src_node):
                        G.add_edge(src_node, lk_id, edge_type="CORRELATES_TO", confidence=lk.get("confidence", 0.9))
                if tgt:
                    tgt_node = f"ACC_{tgt.lstrip('@').lower()}"
                    if G.has_node(tgt_node):
                        G.add_edge(lk_id, tgt_node, edge_type="RESOLVES_AS", confidence=lk.get("confidence", 0.9))

    return G

if __name__ == "__main__":
    g = build_investigation_graph()
    print("Investigation Graph Constructed Successfully:")
    print(f"  Nodes: {g.number_of_nodes()}")
    print(f"  Edges: {g.number_of_edges()}")
