"""
Graph Exporters:
1. Maltego-compatible entity and link CSVs for visual link-analysis tools.
2. PyVis interactive standalone HTML visualization with colored node taxonomies.
3. Standard GraphML format for Gephi and Cytoscape.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from typing import Dict, Any
import networkx as nx
import pandas as pd
from pyvis.network import Network

NODE_COLOR_MAP = {
    "Person": "#ef4444",    # Crimson Red
    "Account": "#3b82f6",   # Royal Blue
    "Phone": "#10b981",     # Emerald Green
    "Location": "#f59e0b",  # Amber / Gold
    "Post": "#8b5cf6",      # Purple
    "Photo": "#06b6d4",     # Cyan
    "Device": "#64748b"     # Slate Gray
}

def export_all_formats(
    G: nx.MultiDiGraph,
    output_dir: Path | None = None
) -> Dict[str, str]:
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "data"

    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = {}

    # 1. Maltego Entities CSV
    entities_rows = []
    for node_id, data in G.nodes(data=True):
        ntype = data.get("node_type", "Unknown")
        # Maltego entity type mapping
        maltego_type = {
            "Person": "maltego.Person",
            "Account": "maltego.Alias",
            "Phone": "maltego.PhoneNumber",
            "Location": "maltego.Location",
            "Post": "maltego.Phrase",
            "Photo": "maltego.Image",
            "Device": "maltego.Device"
        }.get(ntype, "maltego.Entity")

        entities_rows.append({
            "Entity_ID": node_id,
            "Maltego_Type": maltego_type,
            "Value": data.get("label", node_id),
            "Original_Type": ntype,
            "Properties": json.dumps({k: v for k, v in data.items() if k not in ["label", "node_type"]})
        })

    entities_df = pd.DataFrame(entities_rows)
    maltego_ent_path = output_dir / "maltego_entities.csv"
    entities_df.to_csv(maltego_ent_path, index=False)
    generated_files["maltego_entities"] = str(maltego_ent_path)

    # Maltego Links CSV
    links_rows = []
    for u, v, k, data in G.edges(keys=True, data=True):
        links_rows.append({
            "Source_ID": u,
            "Target_ID": v,
            "Relationship": data.get("edge_type", "RELATED_TO"),
            "Weight": data.get("weight", data.get("confidence", 1.0)),
            "Timestamp": data.get("timestamp", ""),
            "Context": data.get("context", data.get("rationale", ""))
        })

    links_df = pd.DataFrame(links_rows)
    maltego_link_path = output_dir / "maltego_links.csv"
    links_df.to_csv(maltego_link_path, index=False)
    generated_files["maltego_links"] = str(maltego_link_path)

    # 2. GraphML Export
    # GraphML requires primitive attributes (convert lists/dicts to strings)
    G_clean = nx.MultiDiGraph()
    for n, d in G.nodes(data=True):
        clean_d = {}
        for k, v in d.items():
            clean_d[k] = json.dumps(v) if isinstance(v, (list, dict)) else str(v)
        G_clean.add_node(n, **clean_d)
    for u, v, k, d in G.edges(keys=True, data=True):
        clean_d = {}
        for ek, ev in d.items():
            clean_d[ek] = json.dumps(ev) if isinstance(ev, (list, dict)) else str(ev)
        G_clean.add_edge(u, v, key=k, **clean_d)

    graphml_path = output_dir / "investigation_graph.graphml"
    nx.write_graphml(G_clean, str(graphml_path))
    generated_files["graphml"] = str(graphml_path)

    # 3. PyVis Interactive HTML - Use improved graph export
    from graph.improved_graph_export import create_improved_pyvis_graph
    pyvis_path = output_dir / "investigation_graph.html"
    create_improved_pyvis_graph(G, pyvis_path, layout="organic")
    generated_files["pyvis_html"] = str(pyvis_path)

    return generated_files

if __name__ == "__main__":
    from graph.build_networkx import build_investigation_graph
    g = build_investigation_graph()
    outs = export_all_formats(g)
    print("Graph Exports Complete:")
    for k, p in outs.items():
        print(f"  {k}: {p}")
