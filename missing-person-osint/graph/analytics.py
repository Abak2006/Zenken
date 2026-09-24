"""
Graph Analytics and Network Forensics Engine.
Calculates centrality metrics, detects communities, extracts critical temporal subgraphs,
and detects anomalous communication spikes.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List
import networkx as nx
import pandas as pd

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph.build_networkx import build_investigation_graph

def run_graph_analytics(
    G: nx.MultiDiGraph,
    output_dir: Path | None = None
) -> Dict[str, Any]:
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "data"

    # Convert to simple undirected graph for standard centrality & community algorithms
    U = nx.Graph()
    for n, d in G.nodes(data=True):
        U.add_node(n, **d)
    for u, v, k, d in G.edges(keys=True, data=True):
        w = d.get("confidence", d.get("weight", 1.0))
        if U.has_edge(u, v):
            U[u][v]["weight"] = U[u][v].get("weight", 1.0) + w
        else:
            U.add_edge(u, v, weight=w, edge_type=d.get("edge_type", "RELATED"))

    # 1. Centrality metrics
    deg_centrality = nx.degree_centrality(U)
    betweenness = nx.betweenness_centrality(U, weight="weight")
    closeness = nx.closeness_centrality(U)

    top_degree = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

    # 2. Community Detection (Greedy modularity communities / Louvain equivalent)
    communities_generator = nx.community.greedy_modularity_communities(U, weight="weight")
    communities = []
    for idx, c in enumerate(communities_generator):
        node_list = list(c)
        # Identify key labels
        labels = [G.nodes[n].get("label", n) for n in node_list]
        communities.append({
            "community_id": idx,
            "size": len(node_list),
            "members": node_list,
            "sample_labels": labels[:6]
        })

    # 3. Critical Last 72-Hour Subgraph Extraction
    # Case anchor disappearance: 2026-03-14T21:45:00Z
    cutoff_end = datetime(2026, 3, 15, 0, 0, 0, tzinfo=timezone.utc)
    cutoff_start = cutoff_end - timedelta(hours=72) # 2026-03-12T00:00:00Z

    subgraph_edges = []
    subgraph_nodes = set()

    for u, v, k, d in G.edges(keys=True, data=True):
        ts_str = d.get("timestamp")
        is_in_window = False
        if ts_str:
            try:
                # Basic ISO parse
                ts_clean = str(ts_str).replace("Z", "+00:00")
                dt = datetime.fromisoformat(ts_clean)
                if cutoff_start <= dt <= cutoff_end:
                    is_in_window = True
            except Exception:
                pass

        # Also retain core identity and phone ownership edges
        if d.get("edge_type") in ["OWNS", "SAME_AS"]:
            is_in_window = True

        if is_in_window:
            subgraph_edges.append((u, v, d))
            subgraph_nodes.add(u)
            subgraph_nodes.add(v)

    last_72h_graph = G.subgraph(subgraph_nodes).copy()

    # 4. Contact Frequency Anomaly Detection
    # Detect sudden spikes in calls or interactions in the final days vs routine baseline
    cdrs_path = output_dir / "call_records.csv"
    anomalies = []
    if cdrs_path.exists():
        cdr_df = pd.read_csv(cdrs_path)
        cdr_df["dt"] = pd.to_datetime(cdr_df["timestamp_utc"])
        cdr_df["day"] = cdr_df["dt"].dt.date

        # Look for new caller numbers not seen in the first 30 days
        day_30_date = cdr_df["day"].min() + pd.Timedelta(days=30)
        early_callers = set(cdr_df[cdr_df["day"] < day_30_date]["caller_number"]).union(
            set(cdr_df[cdr_df["day"] < day_30_date]["receiver_number"])
        )
        late_calls = cdr_df[cdr_df["day"] >= day_30_date]
        
        for _, r in late_calls.iterrows():
            caller = r["caller_number"]
            receiver = r["receiver_number"]
            if caller not in early_callers or receiver not in early_callers:
                anomalies.append({
                    "type": "NEW_COMMUNICATION_LINK",
                    "timestamp": r["timestamp_utc"],
                    "caller": caller,
                    "receiver": receiver,
                    "cell_tower": r["cell_tower_sector"],
                    "duration_sec": r["duration_sec"],
                    "notes": "Unprecedented communication partner detected after routine baseline period"
                })

    analytics_summary = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "density": round(nx.density(U), 4),
        "top_degree_centrality": [{"node": n, "score": round(s, 4), "label": G.nodes[n].get("label", n)} for n, s in top_degree],
        "top_betweenness_centrality": [{"node": n, "score": round(s, 4), "label": G.nodes[n].get("label", n)} for n, s in top_betweenness],
        "communities_count": len(communities),
        "communities": communities,
        "last_72h_subgraph": {
            "node_count": last_72h_graph.number_of_nodes(),
            "edge_count": last_72h_graph.number_of_edges(),
            "nodes": list(last_72h_graph.nodes())
        },
        "detected_communication_anomalies": anomalies
    }

    with open(output_dir / "graph_analytics.json", "w", encoding="utf-8") as f:
        json.dump(analytics_summary, f, indent=2)

    return analytics_summary

if __name__ == "__main__":
    from graph.build_networkx import build_investigation_graph
    g = build_investigation_graph()
    res = run_graph_analytics(g)
    print("Graph Analytics Completed:")
    print(f"  Nodes: {res['total_nodes']}, Edges: {res['total_edges']}")
    print(f"  Communities: {res['communities_count']}")
    print(f"  72-hour Subgraph Nodes: {res['last_72h_subgraph']['node_count']}")
    print(f"  Communication Anomalies Detected: {len(res['detected_communication_anomalies'])}")
