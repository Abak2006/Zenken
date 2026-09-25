"""
Streamlit Forensic Investigation Dashboard.
8-Tab interactive digital forensics and OSINT intelligence workstation:
1. Case Overview
2. Evidence Explorer
3. Identity Resolution
4. Investigation Graph
5. Geospatial Map
6. Forensic Timeline
7. Investigative Hypotheses
8. Academic Evaluation
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from pathlib import Path as PathLib
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Add parent directory to path for imports
sys.path.insert(0, str(PathLib(__file__).resolve().parent.parent))

# Set page configuration
st.set_page_config(
    page_title="Forensic OSINT: Missing Person Investigation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CASE_DIR = Path(__file__).resolve().parent.parent / "case"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

@st.cache_data
def load_all_data():
    data = {}
    
    # Case bible
    case_path = CASE_DIR / "case_bible.yaml"
    if case_path.exists():
        import yaml
        with open(case_path, "r", encoding="utf-8") as f:
            data["case_bible"] = yaml.safe_load(f)

    # Profiles
    p_path = DATA_DIR / "profiles.json"
    if p_path.exists():
        with open(p_path, "r", encoding="utf-8") as f:
            data["profiles"] = json.load(f)

    # Posts
    posts_path = DATA_DIR / "posts.csv"
    if posts_path.exists():
        data["posts"] = pd.read_csv(posts_path)

    # Calls
    calls_path = DATA_DIR / "call_records.csv"
    if calls_path.exists():
        data["calls"] = pd.read_csv(calls_path)

    # Checkins
    chk_path = DATA_DIR / "checkins.csv"
    if chk_path.exists():
        data["checkins"] = pd.read_csv(chk_path)

    # Photos
    ph_path = DATA_DIR / "photos_metadata.json"
    if ph_path.exists():
        with open(ph_path, "r", encoding="utf-8") as f:
            data["photos"] = json.load(f)

    # Resolved identities
    res_path = DATA_DIR / "resolved_identities.json"
    if res_path.exists():
        with open(res_path, "r", encoding="utf-8") as f:
            data["resolved"] = json.load(f)

    # Ambiguous links
    amb_path = DATA_DIR / "ambiguous_links.json"
    if amb_path.exists():
        with open(amb_path, "r", encoding="utf-8") as f:
            data["ambiguous"] = json.load(f)

    # Movement
    mov_path = DATA_DIR / "movement_analysis.json"
    if mov_path.exists():
        with open(mov_path, "r", encoding="utf-8") as f:
            data["movement"] = json.load(f)

    # Hypotheses
    hyp_path = DATA_DIR / "hypotheses_evaluation.json"
    if hyp_path.exists():
        with open(hyp_path, "r", encoding="utf-8") as f:
            data["hypotheses"] = json.load(f)

    # Evaluation
    eval_path = REPORTS_DIR / "evaluation.json"
    if eval_path.exists():
        with open(eval_path, "r", encoding="utf-8") as f:
            data["evaluation"] = json.load(f)

    # Graph Analytics
    ga_path = DATA_DIR / "graph_analytics.json"
    if ga_path.exists():
        with open(ga_path, "r", encoding="utf-8") as f:
            data["graph_analytics"] = json.load(f)

    return data

DATA = load_all_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://img.icons8.com/color/96/detective.png", width=64)
st.sidebar.title("Forensic OSINT Lab")
st.sidebar.caption("Case #MP-2026-0419: Disappearance of Maya Lin")

st.sidebar.markdown("---")
st.sidebar.subheader("Filter & Triage Controls")

# Confidence threshold slider
conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.05,
    help="Filter ambiguous links and evidentiary correlation weights"
)

# Account filter
available_handles = []
if "profiles" in DATA:
    available_handles = sorted([p["handle"] for p in DATA["profiles"]])
selected_accounts = st.sidebar.multiselect(
    "Filter by Accounts",
    options=available_handles,
    default=[]
)

st.sidebar.markdown("---")
st.sidebar.info("🔒 100% Synthetic Academic Simulation Dataset. No real individuals, real faces, or production social platforms are used.")

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📋 Case Overview",
    "🔎 Evidence Explorer",
    "🧬 Identity Resolution",
    "🕸️ Investigation Graph",
    "🗺️ Geospatial Map",
    "⏱️ Forensic Timeline",
    "💡 Hypotheses",
    "📊 Evaluation"
])

# ----------------- TAB 1: CASE OVERVIEW -----------------
with tab1:
    st.header("Case File: Disappearance of Maya Lin")
    st.caption("Case ID: MP-2026-0419 | Status: OPEN | Assigned: Academic Digital Forensics Unit")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Profiles Tracked", len(DATA.get("profiles", [])))
    col2.metric("Posts Extracted", len(DATA.get("posts", [])))
    col3.metric("CDR Pings Analyzed", len(DATA.get("calls", [])))
    col4.metric("Candidate LKL Conf.", "94.0%", "Whispering Pines")

    st.markdown("### Subject Dossier")
    c_left, c_right = st.columns([2, 3])
    with c_left:
        st.markdown("""
        - **Name:** Maya Lin (Age: 21, pronouns: she/her)
        - **Status:** Missing since March 14, 2026, ~21:45 UTC
        - **Affiliation:** Senior BFA Student & Photographer, Bayview Arts Institute
        - **Primary Known Device:** Sony Alpha a7 IV / Google Pixel 7
        - **Primary Cellular Number:** `+1-555-0144` (Inactive after March 10)
        - **Burner Cellular Number:** `+1-555-0199` (Active until final tower ping)
        - **Reporting Party:** Roommate Chloe Simmons
        """)
    with c_right:
        st.markdown("""
        **Investigative Incident Synopsis:**
        Subject was last seen physically at Bayview Arts Fine Arts Hall on the morning of March 14. 
        Analysis of digital footprint reveals an escalating pattern of behavioral shifts beginning in early March, 
        coinciding with an inbound contact from shadow art collector `@kaelen_v`. 
        Three posts referencing an off-grid client dinner meeting at Pacific Horizon Diner were deleted from her primary 
        account on March 12. Digital evidence trace terminates at Whispering Pines Overlook with a final cellular sector ping at 21:45 UTC.
        """)

# ----------------- TAB 2: EVIDENCE EXPLORER -----------------
with tab2:
    st.header("Evidence Repository Explorer")
    ev_type = st.radio("Select Evidence Modality", ["Microblog Posts", "Call Detail Records (CDR)", "Physical Check-ins", "Photo Metadata (EXIF)"], horizontal=True)

    if ev_type == "Microblog Posts" and "posts" in DATA:
        df = DATA["posts"]
        if selected_accounts:
            df = df[df["account"].isin(selected_accounts)]
        st.dataframe(
            df[["post_id", "account", "timestamp_raw", "text", "location_tag", "deleted", "sentiment_label"]],
            width='stretch'
        )
        st.caption("🚨 Red rows indicate deleted posts recovered from web archive forensic snapshots.")

    elif ev_type == "Call Detail Records (CDR)" and "calls" in DATA:
        st.dataframe(DATA["calls"], width='stretch')

    elif ev_type == "Physical Check-ins" and "checkins" in DATA:
        st.dataframe(DATA["checkins"], width='stretch')

    elif ev_type == "Photo Metadata (EXIF)" and "photos" in DATA:
        ph_df = pd.DataFrame(DATA["photos"])
        st.dataframe(ph_df[["photo_id", "account", "timestamp_utc", "camera_make", "camera_model", "latitude", "longitude", "exif_stripped", "is_red_herring"]], width='stretch')

# ----------------- TAB 3: IDENTITY RESOLUTION -----------------
with tab3:
    st.header("Multi-Factor Identity Correlation & Resolution")
    st.markdown("Algorithmic clustering matches fragmented digital accounts into canonical Person entities using string distance, shared identifiers, bio tokens, and perceptual image hashing.")

    if "resolved" in DATA:
        st.subheader("Canonical Resolved Person Clusters")
        clusters_df = pd.DataFrame(DATA["resolved"]["clusters"])
        st.dataframe(clusters_df[["canonical_id", "canonical_name", "account_count", "accounts", "linked_emails", "linked_phones", "is_multi_account"]], width='stretch')

        st.subheader("Confirmed Identity Links (Confidence >= 0.75)")
        links_df = pd.DataFrame(DATA["resolved"]["confirmed_links"])
        st.dataframe(links_df[["account_a", "account_b", "confidence", "rationale"]], width='stretch')

    if "ambiguous" in DATA:
        st.subheader("⚠️ Ambiguous Links Requiring Manual Analyst Review")
        amb_df = pd.DataFrame(DATA["ambiguous"]["ambiguous_links"])
        if not amb_df.empty:
            filtered_amb = amb_df[amb_df["confidence"] >= conf_threshold]
            st.dataframe(filtered_amb[["account_a", "account_b", "confidence", "rationale"]], width='stretch')

# ----------------- TAB 4: INVESTIGATION GRAPH -----------------
with tab4:
    st.header("Multi-Modal Investigation Graph")
    pyvis_html_path = DATA_DIR / "investigation_graph.html"

    if pyvis_html_path.exists():
        with open(pyvis_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=650, scrolling=True)

    if "graph_analytics" in DATA:
        ga = DATA["graph_analytics"]
        st.subheader("Network Forensic Centrality Metrics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Top Degree Centrality (Most Connected Hubs):**")
            st.dataframe(pd.DataFrame(ga["top_degree_centrality"]), width='stretch')
        with col_b:
            st.markdown("**Top Betweenness Centrality (Key Informational Bridges):**")
            st.dataframe(pd.DataFrame(ga["top_betweenness_centrality"]), width='stretch')

    st.subheader("Catalogue of Forensic Cypher Queries (Neo4j)")
    from graph.cypher_queries import CYPHER_QUERIES as cypher_queries
    for q in cypher_queries[:4]:
        with st.expander(f"{q['query_id']}: {q['title']}"):
            st.write(f"**Objective:** {q['objective']}")
            st.code(q["cypher"], language="cypher")

# ----------------- TAB 5: GEOSPATIAL MAP -----------------
with tab5:
    st.header("Geospatial Forensics & Movement Analysis")
    map_html_path = DATA_DIR / "investigation_map.html"

    if map_html_path.exists():
        with open(map_html_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=650, scrolling=True)

    if "movement" in DATA:
        mov = DATA["movement"]
        st.subheader("Candidate Last Known Location (LKL) Rankings")
        lkl_df = pd.DataFrame(mov["ranked_candidate_lkl"])
        st.dataframe(lkl_df[["rank", "candidate_name", "confidence", "latitude", "longitude", "timestamp", "rationale"]], width='stretch')

        st.subheader("DBSCAN Dwell-Time Clusters")
        st.dataframe(pd.DataFrame(mov["spatial_clusters"]), width='stretch')

# ----------------- TAB 6: FORENSIC TIMELINE -----------------
with tab6:
    st.header("Chronological Multi-Lane Timeline")
    timeline_html_path = DATA_DIR / "investigation_timeline.html"

    if timeline_html_path.exists():
        with open(timeline_html_path, "r", encoding="utf-8") as f:
            tl_html = f.read()
        components.html(tl_html, height=680, scrolling=True)

    st.markdown("""
    **Timeline Forensic Highlights:**
    - **Day 20 (Feb 18):** Breakup with Lucas Reed; hostile public comment thread.
    - **Day 31 (Mar 01):** Inbound invitation from @kaelen_v proposing private off-grid shoot.
    - **Day 33 (Mar 03):** Behavioral inflection point; sentiment shifts negative with paranoia mentions.
    - **Day 36 (Mar 06):** Covert alias `@m.shadow_7` activated.
    - **Day 40 (Mar 10):** Primary phone (`+1-555-0144`) disconnected; Burner phone (`+1-555-0199`) activated.
    - **Day 42 (Mar 12):** Deletion of 3 posts mentioning client meeting.
    - **Day 44 (Mar 14, 21:45 UTC):** Final cell ping at Whispering Pines Overlook before handset goes dark.
    """)

# ----------------- TAB 7: HYPOTHESES -----------------
with tab7:
    st.header("Investigative Hypotheses Evaluation")

    if "hypotheses" in DATA:
        for hyp in DATA["hypotheses"]:
            status_color = "🟢" if hyp["status"] == "MOST_PROBABLE" else ("🔴" if "DISPROVEN" in hyp["status"] else "🟠")
            with st.expander(f"{status_color} {hyp['title']} (Confidence: {hyp['confidence_score']*100:.0f}%)", expanded=(hyp["status"]=="MOST_PROBABLE")):
                st.write(f"**Status:** `{hyp['status']}`")
                st.write(f"**Summary:** {hyp['summary']}")

                h_left, h_right = st.columns(2)
                with h_left:
                    st.markdown("**Supporting Evidence:**")
                    for s in hyp["supporting_evidence"]:
                        st.markdown(f"- **{s['item']}:** {s['detail']} (w={s['weight']})")
                with h_right:
                    st.markdown("**Contradicting Evidence & Alibis:**")
                    for c in hyp["contradicting_evidence"]:
                        st.markdown(f"- **{c['item']}:** {c['detail']}")

                st.markdown("**Recommended Investigative Actions:**")
                for act in hyp["recommended_actions"]:
                    st.markdown(f"1. {act}")

# ----------------- TAB 8: EVALUATION -----------------
with tab8:
    st.header("Academic Evaluation & Ground Truth Benchmark")
    st.caption("Verification against isolated ground_truth.json (evaluation purposes only)")

    metric_img_path = REPORTS_DIR / "evaluation_metrics.png"
    if metric_img_path.exists():
        st.image(str(metric_img_path), width='stretch')

    if "evaluation" in DATA:
        ev = DATA["evaluation"]
        m = ev["metrics"]

        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Entity Resolution F1", f"{m['entity_resolution']['f1_score']*100:.1f}%")
        e2.metric("Target Clustered", f"{m['entity_resolution']['target_persona_cluster_accuracy']*100:.0f}%")
        e3.metric("LKL Distance Error", f"{m['last_known_location']['distance_error_meters']:.1f} m")
        e4.metric("Red Herrings Avoided", f"{m['red_herring_audit']['traps_avoided_count']} of 2")

        st.json(ev)
