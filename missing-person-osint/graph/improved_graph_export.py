"""
Professional Investigation Workstation Graph Export Engine
Produces stable, high-performance, dark-themed digital intelligence network visualization.
Inspired by Palantir Gotham, Maltego, Neo4j Bloom, and IBM i2 Analyst's Notebook.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import networkx as nx
import pandas as pd
import pyvis

# Palette definition matching theme_config.py
NODE_COLOR_MAP = {
    "Person": "#EF4444",       # Critical Red
    "Account": "#8B5CF6",      # Purple (Digital Identities)
    "Phone": "#10B981",        # Positive Green (Telecom)
    "Location": "#06B6D4",     # Cyan (Geographic)
    "Post": "#F59E0B",         # Amber/Orange (Transmissions)
    "Photo": "#06B6D4",        # Cyan (Photographic EXIF)
    "Device": "#64748B"        # Slate (Hardware)
}

EDGE_COLOR_MAP = {
    "OWNS": "#10B981",
    "FOLLOWS": "#3B82F6",
    "POSTED": "#F59E0B",
    "MENTIONS": "#8B5CF6",
    "CHECKED_IN_AT": "#06B6D4",
    "CONTACTED": "#10B981",
    "SAME_AS": "#3B82F6",
    "APPEARS_IN": "#8B5CF6",
    "TAKEN_AT": "#06B6D4",
    "COMMENTED": "#F59E0B"
}

def get_local_vis_js() -> str:
    """Read local vis-network.min.js from pyvis installation for offline stability."""
    try:
        pyvis_path = Path(pyvis.__file__).parent / "templates" / "lib" / "vis-9.1.2" / "vis-network.min.js"
        if pyvis_path.exists():
            with open(pyvis_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass
    return ""

def create_improved_pyvis_graph(
    G: nx.MultiDiGraph,
    output_path: Path,
    focus_entity: Optional[str] = None,
    show_all_labels: bool = False,
    layout: str = "organic"
) -> str:
    """Compatibility wrapper for generate_workstation_graph_html."""
    init_filter = "target" if focus_entity else ("full" if show_all_labels else "core")
    return generate_workstation_graph_html(
        G=G,
        output_path=output_path,
        default_focus_target=focus_entity or "PERSON_MAYA_LIN",
        initial_layout=layout,
        initial_filter=init_filter
    )

def generate_workstation_graph_html(
    G: nx.MultiDiGraph,
    output_path: Path,
    default_focus_target: Optional[str] = "PERSON_MAYA_LIN",
    initial_layout: str = "organic",
    initial_filter: str = "core"
) -> str:
    """
    Generate professional cyber investigation network visualization with:
    - Guaranteed stationary nodes after initial stabilization (NO continuous vibration/movement)
    - Integrated secondary toolbar (search, filters, layout, fit, reset, labels, export)
    - In-graph search with instant focus and auto-centering
    - Multi-tier focus mode (Selected 100%, 1-Hop 85%, 2-Hop 40%, Unrelated 12%)
    - Sliding right-side entity dossier panel
    - Subtle ambient dark intelligence backdrop (zero impact on graph physics)
    """
    nodes_data = []
    edges_data = []
    
    # Identify target person and primary aliases
    target_person_id = "PERSON_MAYA_LIN"
    target_accounts = {"acc_mayalin_art", "acc_m_lin99", "acc_m.shadow_7"}
    target_phones = {"phone_15550144", "phone_15550199"}
    critical_locations = {"loc_v01", "loc_v02", "loc_v03"} # Whispering Pines, Pacific Horizon Diner, Bayview Arts

    # Process Nodes
    for node_id, data in G.nodes(data=True):
        ntype = data.get("node_type", "Unknown")
        label = data.get("label", node_id)
        name = data.get("name", label)
        
        # Check target association
        is_target = (
            node_id == target_person_id or 
            data.get("is_target", False) or 
            node_id.lower() in target_accounts or 
            node_id.lower() in target_phones
        )
        
        # Determine importance tier:
        # Tier 1: Target subject & covert alias
        # Tier 2: Key Persons, Phones, Primary Accounts, Key Locations
        # Tier 3: Secondary Accounts, Venues
        # Tier 4: Posts, Photos, Generic transmissions
        if is_target:
            importance = 1
        elif ntype in ["Person", "Phone"] or (ntype == "Location" and node_id.lower() in critical_locations):
            importance = 2
        elif ntype in ["Account", "Location"]:
            importance = 3
        else:
            importance = 4

        # Is this node part of the default "Core Investigation" view?
        # Core view includes Persons, Accounts, Phones, Locations, and deleted/critical posts
        is_core = (importance <= 3) or data.get("deleted", False) or data.get("is_red_herring", False)

        # Base node sizing
        if importance == 1:
            size = 32
        elif importance == 2:
            size = 24
        elif importance == 3:
            size = 18
        else:
            size = 11

        color = NODE_COLOR_MAP.get(ntype, "#64748B")
        if is_target and ntype == "Person":
            color = "#EF4444" # Primary Subject Red
        elif is_target and ntype == "Account":
            color = "#8B5CF6" # Target Account Purple

        # Hierarchical Level assignment (UD: Level 0 -> Level 4)
        if node_id == target_person_id:
            level = 0
        elif is_target and ntype in ["Account", "Phone"]:
            level = 1
        elif ntype == "Person":
            level = 1
        elif ntype in ["Account", "Phone"]:
            level = 2
        elif ntype in ["Post", "Photo"]:
            level = 3
        elif ntype == "Location":
            level = 4
        else:
            level = 3

        # Prepare rich metadata attributes for inspector panel
        meta_dict = {
            "ID": node_id,
            "Type": ntype,
            "Label": label,
            "Importance Tier": f"Tier {importance}"
        }
        for k, v in data.items():
            if k not in ["label", "node_type", "is_target"] and v is not None and not isinstance(v, (dict, list)):
                meta_dict[k.replace("_", " ").title()] = str(v)

        # Build clean tooltip HTML
        tooltip_lines = [
            f"<div style='font-family:Inter,sans-serif;font-size:12px;color:#E6EDF3;'>",
            f"<b style='color:#3B82F6;'>{label}</b> <span style='font-size:10px;color:#7D8998;'>({ntype})</span>",
            f"<hr style='border:none;border-top:1px solid #202833;margin:4px 0;'/>"
        ]
        for mk, mv in list(meta_dict.items())[:6]:
            if mk not in ["ID", "Label"]:
                tooltip_lines.append(f"<span style='color:#7D8998;'>{mk}:</span> <b>{mv}</b><br/>")
        tooltip_lines.append("</div>")

        # Determine default label visibility (Important nodes show label, secondary hide until hover/focus)
        show_label_default = (importance <= 2)

        nodes_data.append({
            "id": node_id,
            "label": label if show_label_default else "",
            "full_label": label,
            "title": "".join(tooltip_lines),
            "group": ntype,
            "node_type": ntype,
            "size": size,
            "color": {
                "background": color,
                "border": "#202833",
                "highlight": {
                    "background": color,
                    "border": "#3B82F6"
                }
            },
            "borderWidth": 2 if is_target else 1.2,
            "borderWidthSelected": 3,
            "font": {
                "color": "#E6EDF3",
                "size": 12 if importance <= 2 else 10,
                "face": "Inter, -apple-system, sans-serif",
                "strokeWidth": 2,
                "strokeColor": "#05070A"
            },
            "level": level,
            "importance": importance,
            "is_core": is_core,
            "is_target": is_target,
            "metadata": meta_dict
        })

    # Process Edges
    for u, v, k, data in G.edges(keys=True, data=True):
        rel = data.get("edge_type", "RELATED_TO")
        color = EDGE_COLOR_MAP.get(rel, "#64748B")
        
        # Edge width based on relationship criticality
        width = 2.5 if rel in ["SAME_AS", "OWNS"] else (1.8 if rel in ["FOLLOWS", "CONTACTED"] else 1.2)
        
        # Tooltip
        edge_tip = f"<div style='font-family:Inter,sans-serif;font-size:11px;color:#E6EDF3;'><b>{rel}</b>"
        if "confidence" in data:
            edge_tip += f"<br/><span style='color:#7D8998;'>Confidence:</span> {data['confidence']}"
        if "timestamp" in data:
            edge_tip += f"<br/><span style='color:#7D8998;'>Time:</span> {data['timestamp']}"
        edge_tip += "</div>"

        edges_data.append({
            "id": f"{u}__{v}__{rel}__{k}",
            "from": u,
            "to": v,
            "rel": rel,
            "title": edge_tip,
            "color": {
                "color": color,
                "opacity": 0.35,
                "highlight": "#3B82F6",
                "hover": "#60A5FA"
            },
            "width": width,
            "arrows": {
                "to": {"enabled": True, "scaleFactor": 0.5}
            },
            "smooth": {
                "type": "continuous",
                "roundness": 0.15
            }
        })

    # Read local vis-network JS or fallback
    vis_js_content = get_local_vis_js()
    if vis_js_content:
        script_tag = f"<script>{vis_js_content}</script>"
    else:
        script_tag = '<script src="https://unpkg.com/vis-network@9.1.2/standalone/umd/vis-network.min.js"></script>'

    nodes_json = json.dumps(nodes_data, ensure_ascii=False)
    edges_json = json.dumps(edges_data, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZENKEN - Investigation Network</title>
    {script_tag}
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }}
        html, body {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #05070A;
            color: #E6EDF3;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}

        /* Subtle Investigative Ambient Backdrop (Zero CPU Impact on Nodes) */
        #network-wrapper {{
            position: relative;
            width: 100%;
            height: 100vh;
            background-color: #05070A;
            background-image: 
                radial-gradient(circle at 50% 45%, rgba(13, 17, 23, 0.85) 0%, #05070A 100%),
                linear-gradient(rgba(32, 40, 51, 0.18) 1px, transparent 1px),
                linear-gradient(90deg, rgba(32, 40, 51, 0.18) 1px, transparent 1px);
            background-size: 100% 100%, 32px 32px, 32px 32px;
        }}

        #network-canvas {{
            width: 100%;
            height: 100%;
        }}

        /* Secondary Graph Toolbar (Compact, Professional Maltego/Gotham Style) */
        .graph-toolbar {{
            position: absolute;
            top: 12px;
            left: 12px;
            z-index: 50;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 21, 28, 0.88);
            backdrop-filter: blur(10px);
            border: 1px solid #202833;
            border-radius: 6px;
            padding: 6px 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        }}

        .search-box {{
            position: relative;
            display: flex;
            align-items: center;
        }}

        .search-input {{
            background: #0D1117;
            border: 1px solid #202833;
            border-radius: 4px;
            color: #E6EDF3;
            font-size: 11px;
            padding: 5px 8px 5px 24px;
            width: 190px;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-input:focus {{
            border-color: #3B82F6;
            width: 230px;
            box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
        }}

        .search-icon {{
            position: absolute;
            left: 7px;
            color: #7D8998;
            font-size: 11px;
            pointer-events: none;
        }}

        .toolbar-select {{
            background: #0D1117;
            border: 1px solid #202833;
            border-radius: 4px;
            color: #E6EDF3;
            font-size: 11px;
            padding: 4px 6px;
            outline: none;
            cursor: pointer;
        }}

        .toolbar-select:focus {{
            border-color: #3B82F6;
        }}

        .toolbar-btn {{
            background: #151B23;
            border: 1px solid #202833;
            border-radius: 4px;
            color: #E6EDF3;
            font-size: 11px;
            font-weight: 500;
            padding: 5px 9px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s ease;
        }}

        .toolbar-btn:hover {{
            background: #1B222D;
            border-color: #3B82F6;
            color: #3B82F6;
        }}

        .toolbar-btn:active {{
            transform: translateY(1px);
        }}

        .divider {{
            width: 1px;
            height: 18px;
            background: #202833;
            margin: 0 2px;
        }}

        /* Status & Telemetry Pill */
        .status-pill {{
            position: absolute;
            bottom: 12px;
            left: 12px;
            z-index: 50;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 21, 28, 0.85);
            backdrop-filter: blur(8px);
            border: 1px solid #202833;
            border-radius: 4px;
            padding: 4px 10px;
            font-size: 10px;
            color: #7D8998;
            font-family: 'JetBrains Mono', monospace;
        }}

        .status-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #10B981;
            box-shadow: 0 0 6px #10B981;
        }}

        /* Floating Right-Side Entity Dossier Panel */
        #detail-panel {{
            position: absolute;
            top: 12px;
            right: 12px;
            bottom: 12px;
            width: 320px;
            background: rgba(16, 21, 28, 0.94);
            backdrop-filter: blur(14px);
            border: 1px solid #202833;
            border-radius: 6px;
            z-index: 100;
            display: none;
            flex-direction: column;
            box-shadow: -8px 0 32px rgba(0, 0, 0, 0.7);
            overflow: hidden;
            animation: slideIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(30px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}

        .panel-header {{
            padding: 12px 14px;
            background: #151B23;
            border-bottom: 1px solid #202833;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .panel-title {{
            font-size: 13px;
            font-weight: 600;
            color: #E6EDF3;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .panel-close {{
            background: transparent;
            border: none;
            color: #7D8998;
            font-size: 16px;
            cursor: pointer;
            padding: 0 4px;
            line-height: 1;
        }}

        .panel-close:hover {{
            color: #EF4444;
        }}

        .panel-body {{
            padding: 14px;
            overflow-y: auto;
            flex: 1;
        }}

        .entity-badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 3px;
            font-size: 9px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            border: 1px solid transparent;
        }}

        .meta-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid rgba(32, 40, 51, 0.5);
            font-size: 11px;
        }}

        .meta-label {{
            color: #7D8998;
        }}

        .meta-val {{
            color: #E6EDF3;
            font-weight: 500;
            text-align: right;
            max-width: 170px;
            word-break: break-all;
        }}

        .rel-section-title {{
            font-size: 10px;
            font-weight: 700;
            color: #7D8998;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 14px 0 8px 0;
        }}

        .rel-chip {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #0D1117;
            border: 1px solid #202833;
            border-radius: 3px;
            padding: 3px 7px;
            font-size: 10px;
            color: #E6EDF3;
            margin: 2px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .rel-chip:hover {{
            border-color: #3B82F6;
            color: #3B82F6;
            background: #151B23;
        }}

        .panel-footer {{
            padding: 10px 14px;
            background: #151B23;
            border-top: 1px solid #202833;
            display: flex;
            gap: 8px;
        }}

        .panel-footer button {{
            flex: 1;
            padding: 6px;
            font-size: 11px;
            font-weight: 600;
            border-radius: 4px;
            border: 1px solid #202833;
            background: #0D1117;
            color: #E6EDF3;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .panel-footer button.primary {{
            background: #3B82F6;
            border-color: #3B82F6;
            color: #FFFFFF;
        }}

        .panel-footer button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        /* Initial Loading Splash */
        #loading-overlay {{
            position: absolute;
            inset: 0;
            background: #05070A;
            z-index: 200;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
            transition: opacity 0.3s ease;
        }}

        .spinner {{
            width: 28px;
            height: 28px;
            border: 2px solid #202833;
            border-top-color: #3B82F6;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .loading-text {{
            font-size: 11px;
            color: #7D8998;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
    <div id="network-wrapper">
        <!-- Secondary Investigation Toolbar -->
        <div class="graph-toolbar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input 
                    type="text" 
                    id="search-input" 
                    class="search-input" 
                    placeholder="Search entity (e.g. Maya Lin, kaelen_v)..." 
                    list="entities-datalist"
                    autocomplete="off"
                />
                <datalist id="entities-datalist"></datalist>
            </div>

            <div class="divider"></div>

            <select id="filter-select" class="toolbar-select" title="Filter Investigation Subgraph">
                <option value="core">Core Investigation (Default)</option>
                <option value="full">Full Evidentiary Network</option>
                <option value="target">Target Dossier Only</option>
                <option value="identities">Identities & Persons Only</option>
            </select>

            <select id="layout-select" class="toolbar-select" title="Network Topology Layout">
                <option value="organic">Organic (Stationary)</option>
                <option value="hierarchical">Hierarchical (UD)</option>
            </select>

            <div class="divider"></div>

            <button id="btn-focus-target" class="toolbar-btn" title="Focus Maya Lin (Target)">
                🎯 Target
            </button>

            <button id="btn-fit" class="toolbar-btn" title="Fit Network to Viewport">
                ⛶ Fit
            </button>

            <button id="btn-reset" class="toolbar-btn" title="Reset Camera & Focus">
                🔄 Reset
            </button>

            <button id="btn-labels" class="toolbar-btn" title="Toggle Node Labels">
                🏷️ Labels
            </button>

            <div class="divider"></div>

            <button id="btn-export" class="toolbar-btn" title="Export High-Resolution Canvas">
                💾 Export
            </button>
        </div>

        <!-- Telemetry Status Bar -->
        <div class="status-pill">
            <span class="status-dot" id="status-dot"></span>
            <span id="status-text">STABILIZING NETWORK...</span>
            <span>|</span>
            <span id="node-count-display">0 Nodes</span>
            <span>|</span>
            <span id="edge-count-display">0 Edges</span>
        </div>

        <!-- Floating Entity Dossier Panel -->
        <div id="detail-panel">
            <div class="panel-header">
                <div class="panel-title">
                    <span id="panel-icon">👤</span>
                    <span id="panel-name">Entity Dossier</span>
                </div>
                <button class="panel-close" id="panel-close-btn">&times;</button>
            </div>
            <div class="panel-body">
                <div id="panel-badge-container"></div>
                <div id="panel-meta-container"></div>
                <div class="rel-section-title">Direct Connected Relationships</div>
                <div id="panel-rel-container"></div>
            </div>
            <div class="panel-footer">
                <button id="btn-panel-hop" class="primary">Focus 1-Hop</button>
                <button id="btn-panel-center">Center</button>
            </div>
        </div>

        <!-- Loading Overlay -->
        <div id="loading-overlay">
            <div class="spinner"></div>
            <div class="loading-text">CALCULATING INITIAL TOPOLOGY...</div>
        </div>

        <!-- Vis Canvas -->
        <div id="network-canvas"></div>
    </div>

    <script>
        // Raw Evidentiary Graph Data
        const ALL_NODES = {nodes_json};
        const ALL_EDGES = {edges_json};

        // Populate search autocomplete datalist
        const datalist = document.getElementById("entities-datalist");
        ALL_NODES.forEach(n => {{
            const opt = document.createElement("option");
            opt.value = n.full_label;
            opt.dataset.id = n.id;
            datalist.appendChild(opt);
        }});

        let currentFilter = "{initial_filter}";
        let currentLayout = "{initial_layout}";
        let labelMode = "important"; // "important" | "all" | "none"
        let activeSelectedNodeId = null;

        // Filter nodes based on active view mode
        function getFilteredDataset(filterType) {{
            let filteredNodes = [];
            if (filterType === "core") {{
                filteredNodes = ALL_NODES.filter(n => n.is_core);
            }} else if (filterType === "target") {{
                filteredNodes = ALL_NODES.filter(n => n.is_target || n.importance <= 2);
            }} else if (filterType === "identities") {{
                filteredNodes = ALL_NODES.filter(n => n.node_type === "Person" || n.node_type === "Account");
            }} else {{
                filteredNodes = ALL_NODES; // full
            }}

            const allowedIds = new Set(filteredNodes.map(n => n.id));
            const filteredEdges = ALL_EDGES.filter(e => allowedIds.has(e.from) && allowedIds.has(e.to));

            // Format labels according to labelMode
            const preparedNodes = filteredNodes.map(n => {{
                let lbl = "";
                if (labelMode === "all") {{
                    lbl = n.full_label;
                }} else if (labelMode === "important") {{
                    lbl = (n.importance <= 2) ? n.full_label : "";
                }}
                return Object.assign({{}}, n, {{ label: lbl }});
            }});

            return {{
                nodes: new vis.DataSet(preparedNodes),
                edges: new vis.DataSet(filteredEdges)
            }};
        }}

        let data = getFilteredDataset(currentFilter);
        const container = document.getElementById("network-canvas");

        // Rigorous Physics Configuration:
        // Stabilize ONCE on load, then completely FREEZE.
        const baseOptions = {{
            nodes: {{
                shape: "dot",
                borderWidth: 1.5,
                borderWidthSelected: 3,
                font: {{
                    color: "#E6EDF3",
                    face: "Inter, -apple-system, sans-serif",
                    size: 11
                }}
            }},
            edges: {{
                width: 1.2,
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }},
                smooth: {{ type: "continuous", roundness: 0.15 }},
                color: {{ inherit: false, opacity: 0.35 }},
                hoverWidth: 2.0
            }},
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -4000,
                    centralGravity: 0.25,
                    springLength: 130,
                    springConstant: 0.04,
                    damping: 0.85,
                    avoidOverlap: 0.75
                }},
                minVelocity: 0.75,
                stabilization: {{
                    enabled: true,
                    iterations: 120,
                    updateInterval: 25,
                    fit: true
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 120,
                hideEdgesOnDrag: false,
                hideNodesOnDrag: false,
                dragNodes: true,
                dragView: true,
                zoomView: true,
                selectConnectedEdges: true
            }}
        }};

        // Initialize Vis Network
        let network = new vis.Network(container, data, baseOptions);

        function updateTelemetry() {{
            document.getElementById("node-count-display").innerText = data.nodes.length + " Nodes";
            document.getElementById("edge-count-display").innerText = data.edges.length + " Edges";
        }}
        updateTelemetry();

        // CRITICAL: FREEZE SIMULATION AFTER STABILIZATION
        function freezeSimulation() {{
            network.setOptions({{ physics: {{ enabled: false }} }});
            network.stopSimulation();
            const overlay = document.getElementById("loading-overlay");
            if (overlay) overlay.style.display = "none";
            document.getElementById("status-text").innerText = "STATIONARY (PHYSICS LOCKED)";
            document.getElementById("status-dot").style.backgroundColor = "#3B82F6";
            document.getElementById("status-dot").style.boxShadow = "0 0 6px #3B82F6";
        }}

        network.once("stabilizationIterationsDone", function() {{
            freezeSimulation();
            network.fit({{ animation: {{ duration: 400, easingFunction: "easeInOutQuad" }} }});
        }});

        network.once("stabilized", function() {{
            freezeSimulation();
        }});

        // Multi-Tier Focus Mode Implementation
        function focusNode(nodeId) {{
            if (!nodeId || !data.nodes.get(nodeId)) return;
            activeSelectedNodeId = nodeId;

            const firstDegree = network.getConnectedNodes(nodeId);
            const connectedEdges = network.getConnectedEdges(nodeId);
            const secondDegreeSet = new Set();

            firstDegree.forEach(nbrId => {{
                network.getConnectedNodes(nbrId).forEach(nbr2Id => {{
                    if (nbr2Id !== nodeId && !firstDegree.includes(nbr2Id)) {{
                        secondDegreeSet.add(nbr2Id);
                    }}
                }});
            }});

            const nodeUpdates = [];
            data.nodes.getIds().forEach(id => {{
                const n = data.nodes.get(id);
                if (id === nodeId) {{
                    // Selected: 100% opacity, glow outline
                    nodeUpdates.push({{
                        id: id,
                        opacity: 1.0,
                        label: n.full_label,
                        font: {{ color: "#E6EDF3", size: 13, strokeWidth: 2, strokeColor: "#05070A" }},
                        shadow: {{ enabled: true, color: "#3B82F6", size: 16 }}
                    }});
                }} else if (firstDegree.includes(id)) {{
                    // 1st Degree: 85% opacity, full label
                    nodeUpdates.push({{
                        id: id,
                        opacity: 0.85,
                        label: n.full_label,
                        font: {{ color: "#E6EDF3", size: 11, strokeWidth: 1, strokeColor: "#05070A" }},
                        shadow: {{ enabled: false }}
                    }});
                }} else if (secondDegreeSet.has(id)) {{
                    // 2nd Degree: 40% opacity
                    nodeUpdates.push({{
                        id: id,
                        opacity: 0.40,
                        label: (labelMode === "all" || n.importance <= 2) ? n.full_label : "",
                        font: {{ color: "#7D8998", size: 10 }},
                        shadow: {{ enabled: false }}
                    }});
                }} else {{
                    // Unrelated: Dimmed to 12%
                    nodeUpdates.push({{
                        id: id,
                        opacity: 0.12,
                        label: "",
                        shadow: {{ enabled: false }}
                    }});
                }}
            }});
            data.nodes.update(nodeUpdates);

            // Edge Opacities
            const edgeUpdates = [];
            data.edges.getIds().forEach(eid => {{
                const e = data.edges.get(eid);
                if (connectedEdges.includes(eid)) {{
                    edgeUpdates.push({{ id: eid, width: 2.6, color: {{ opacity: 0.85 }} }});
                }} else {{
                    edgeUpdates.push({{ id: eid, width: 1.0, color: {{ opacity: 0.08 }} }});
                }}
            }});
            data.edges.update(edgeUpdates);

            // Populate & show floating dossier panel
            openDossierPanel(data.nodes.get(nodeId), firstDegree);

            // Center camera smoothly
            network.focus(nodeId, {{
                scale: 1.15,
                animation: {{ duration: 500, easingFunction: "easeInOutQuad" }}
            }});
        }}

        // Reset Focus to Default
        function resetFocus() {{
            activeSelectedNodeId = null;
            const nodeUpdates = [];
            data.nodes.getIds().forEach(id => {{
                const n = data.nodes.get(id);
                let lbl = "";
                if (labelMode === "all") lbl = n.full_label;
                else if (labelMode === "important") lbl = (n.importance <= 2) ? n.full_label : "";
                
                nodeUpdates.push({{
                    id: id,
                    opacity: 1.0,
                    label: lbl,
                    font: {{ color: "#E6EDF3", size: (n.importance <= 2) ? 12 : 10 }},
                    shadow: {{ enabled: false }}
                }});
            }});
            data.nodes.update(nodeUpdates);

            const edgeUpdates = [];
            data.edges.getIds().forEach(eid => {{
                edgeUpdates.push({{ id: eid, width: 1.2, color: {{ opacity: 0.35 }} }});
            }});
            data.edges.update(edgeUpdates);

            closeDossierPanel();
            network.unselectAll();
        }}

        // Floating Dossier Panel Controls
        function openDossierPanel(nodeObj, connectedIds) {{
            const panel = document.getElementById("detail-panel");
            document.getElementById("panel-name").innerText = nodeObj.full_label;

            const iconMap = {{
                "Person": "👤",
                "Account": "🔗",
                "Phone": "📱",
                "Location": "📍",
                "Post": "💬",
                "Photo": "📷",
                "Device": "💻"
            }};
            document.getElementById("panel-icon").innerText = iconMap[nodeObj.node_type] || "🔹";

            // Badge
            const badgeContainer = document.getElementById("panel-badge-container");
            const typeColor = nodeObj.color.background || "#3B82F6";
            badgeContainer.innerHTML = `<span class="entity-badge" style="background: ${{typeColor}}22; color: ${{typeColor}}; border-color: ${{typeColor}}66;">${{nodeObj.node_type}} · ${{nodeObj.is_target ? 'PRIMARY SUBJECT' : 'ENTITY'}}</span>`;

            // Metadata rows
            const metaContainer = document.getElementById("panel-meta-container");
            let metaHtml = "";
            for (let [k, v] of Object.entries(nodeObj.metadata || {{}})) {{
                metaHtml += `<div class="meta-row"><span class="meta-label">${{k}}</span><span class="meta-val">${{v}}</span></div>`;
            }}
            metaContainer.innerHTML = metaHtml;

            // Relationship chips
            const relContainer = document.getElementById("panel-rel-container");
            let chipsHtml = "";
            (connectedIds || []).forEach(nbrId => {{
                const nbr = data.nodes.get(nbrId);
                if (nbr) {{
                    chipsHtml += `<span class="rel-chip" onclick="focusNode('${{nbrId}}')">${{iconMap[nbr.node_type] || '🔹'}} ${{nbr.full_label}}</span>`;
                }}
            }});
            relContainer.innerHTML = chipsHtml || "<span style='font-size:11px;color:#7D8998;'>No direct links mapped.</span>";

            panel.style.display = "flex";
        }}

        function closeDossierPanel() {{
            document.getElementById("detail-panel").style.display = "none";
        }}

        document.getElementById("panel-close-btn").addEventListener("click", closeDossierPanel);
        document.getElementById("btn-panel-center").addEventListener("click", () => {{
            if (activeSelectedNodeId) {{
                network.focus(activeSelectedNodeId, {{ scale: 1.2, animation: {{ duration: 400 }} }});
            }}
        }});
        document.getElementById("btn-panel-hop").addEventListener("click", () => {{
            if (activeSelectedNodeId) {{
                focusNode(activeSelectedNodeId);
            }}
        }});

        // Network Interaction Events
        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                focusNode(params.nodes[0]);
            }} else {{
                resetFocus();
            }}
        }});

        // Search Input Handler
        const searchInput = document.getElementById("search-input");
        searchInput.addEventListener("change", function(e) {{
            const val = e.target.value.trim().toLowerCase();
            if (!val) return;
            const match = ALL_NODES.find(n => 
                n.full_label.toLowerCase() === val || 
                n.id.toLowerCase() === val ||
                (n.metadata && n.metadata.Handle && n.metadata.Handle.toLowerCase() === val)
            );
            if (match) {{
                if (!data.nodes.get(match.id)) {{
                    // Switch filter to full if not currently visible
                    document.getElementById("filter-select").value = "full";
                    applyFilter("full");
                }}
                focusNode(match.id);
            }}
        }});

        // Filter Switcher
        function applyFilter(filterType) {{
            currentFilter = filterType;
            data = getFilteredDataset(filterType);
            network.setData(data);
            updateTelemetry();
            freezeSimulation();
            network.fit({{ animation: {{ duration: 500 }} }});
        }}

        document.getElementById("filter-select").addEventListener("change", function(e) {{
            applyFilter(e.target.value);
        }});

        // Layout Switcher
        document.getElementById("layout-select").addEventListener("change", function(e) {{
            const mode = e.target.value;
            currentLayout = mode;
            if (mode === "hierarchical") {{
                network.setOptions({{
                    layout: {{
                        hierarchical: {{
                            enabled: true,
                            direction: "UD",
                            sortMethod: "directed",
                            levelSeparation: 130,
                            nodeSpacing: 110,
                            treeSpacing: 160
                        }}
                    }},
                    physics: {{ enabled: false }}
                }});
            }} else {{
                network.setOptions({{
                    layout: {{ hierarchical: {{ enabled: false }} }},
                    physics: {{ enabled: false }}
                }});
            }}
            network.fit({{ animation: {{ duration: 500 }} }});
        }});

        // Toolbar Button Handlers
        document.getElementById("btn-focus-target").addEventListener("click", function() {{
            focusNode("PERSON_MAYA_LIN");
        }});

        document.getElementById("btn-fit").addEventListener("click", function() {{
            network.fit({{ animation: {{ duration: 400, easingFunction: "easeInOutQuad" }} }});
        }});

        document.getElementById("btn-reset").addEventListener("click", function() {{
            resetFocus();
            network.fit({{ animation: {{ duration: 400, easingFunction: "easeInOutQuad" }} }});
        }});

        document.getElementById("btn-labels").addEventListener("click", function() {{
            if (labelMode === "important") labelMode = "all";
            else if (labelMode === "all") labelMode = "none";
            else labelMode = "important";

            const updates = [];
            data.nodes.getIds().forEach(id => {{
                const n = data.nodes.get(id);
                let lbl = "";
                if (labelMode === "all") lbl = n.full_label;
                else if (labelMode === "important") lbl = (n.importance <= 2) ? n.full_label : "";
                updates.push({{ id: id, label: lbl }});
            }});
            data.nodes.update(updates);
        }});

        document.getElementById("btn-export").addEventListener("click", function() {{
            const canvas = container.querySelector("canvas");
            if (canvas) {{
                const link = document.createElement("a");
                link.download = "zenken_investigation_network.png";
                link.href = canvas.toDataURL("image/png");
                link.click();
            }}
        }});
    </script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    return str(output_path)

def export_investigation_graph(
    G: nx.MultiDiGraph,
    output_dir: Path,
    variations: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Export all investigation graph variations required by Zenken workstation.
    """
    if variations is None:
        variations = ["default", "focus_maya", "no_labels", "hierarchical"]

    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    for var in variations:
        if var == "default":
            p = output_dir / "investigation_graph.html"
            generate_workstation_graph_html(G, p, initial_layout="organic", initial_filter="core")
            results["default"] = str(p)
        elif var == "focus_maya":
            p = output_dir / "investigation_graph_focus.html"
            generate_workstation_graph_html(G, p, default_focus_target="PERSON_MAYA_LIN", initial_filter="target")
            results["focus_maya"] = str(p)
        elif var == "no_labels":
            p = output_dir / "investigation_graph_clean.html"
            generate_workstation_graph_html(G, p, initial_filter="core")
            results["no_labels"] = str(p)
        elif var == "hierarchical":
            p = output_dir / "investigation_graph_hierarchical.html"
            generate_workstation_graph_html(G, p, initial_layout="hierarchical", initial_filter="core")
            results["hierarchical"] = str(p)

    return results

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from graph.build_networkx import build_investigation_graph

    print("Building evidentiary NetworkX graph...")
    G = build_investigation_graph()
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    out_dir = Path(__file__).resolve().parent.parent / "data"
    exported = export_investigation_graph(G, out_dir)
    print("Graph variations exported successfully:")
    for k, v in exported.items():
        print(f"  {k} -> {v}")
