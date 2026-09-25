"""
Streamlit Forensic Investigation Dashboard v2.0
Professional investigation workstation with dark forensic UI theme
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from pathlib import Path as PathLib
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(PathLib(__file__).resolve().parent.parent))

# Import theme configuration
from dashboard.theme_config import (
    CUSTOM_CSS, BACKGROUND, PANELS, SECONDARY_PANELS, BORDERS,
    PRIMARY_TEXT, SECONDARY_TEXT, ACCENT, POSITIVE, WARNING, CRITICAL, SUSPECTED,
    NODE_COLORS, EDGE_COLORS, TIMELINE_COLORS
)

# Set page configuration
st.set_page_config(
    page_title="ZENKEN - Investigation Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Directory paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CASE_DIR = Path(__file__).resolve().parent.parent / "case"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

# Initialize session state for cross-page navigation
if "selected_entity" not in st.session_state:
    st.session_state.selected_entity = None
if "selected_evidence" not in st.session_state:
    st.session_state.selected_evidence = None
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True

@st.cache_data
def load_all_data():
    """Load all investigation data with caching."""
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

# ==================== SIDEBAR ====================
def render_sidebar():
    """Render collapsible professional sidebar."""
    with st.sidebar:
        # Toggle sidebar expansion
        st.session_state.sidebar_expanded = st.toggle(
            "Expand Sidebar", 
            value=st.session_state.sidebar_expanded,
            key="sidebar_toggle"
        )
        
        if st.session_state.sidebar_expanded:
            # Brand section
            st.markdown("""
            <div style="margin-bottom: 2rem;">
                <h1 style="font-size: 18px; font-weight: 600; margin: 0; color: #E6EDF3;">ZENKEN</h1>
                <p style="font-size: 12px; color: #8B98A8; margin: 0;">Investigation Platform</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Case section
            st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 14px; font-weight: 500; color: #8B98A8; margin: 0 0 0.5rem 0;">CASE</h2>
                <p style="font-size: 16px; font-weight: 600; color: #E6EDF3; margin: 0;">MP-2026-0419</p>
                <p style="font-size: 13px; color: #4F8CFF; margin: 0;">Maya Lin</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            st.markdown("""
            <h2 style="font-size: 14px; font-weight: 500; color: #8B98A8; margin: 0 0 1rem 0;">NAVIGATION</h2>
            """, unsafe_allow_html=True)
            
            page = st.radio(
                "",
                ["Overview", "Evidence", "Identity Resolution", "Investigation Graph", 
                 "Geospatial", "Timeline", "Hypotheses", "Evaluation"],
                label_visibility="collapsed",
                key="main_navigation"
            )
            
            st.markdown("---")
            
            # Investigation status
            st.markdown("""
            <h2 style="font-size: 14px; font-weight: 500; color: #8B98A8; margin: 0 0 1rem 0;">INVESTIGATION STATUS</h2>
            """, unsafe_allow_html=True)
            
            if "profiles" in DATA:
                st.metric("Evidence Items", len(DATA.get("profiles", [])))
            if "resolved" in DATA:
                st.metric("Identities Resolved", len(DATA["resolved"].get("clusters", [])))
            if "movement" in DATA:
                st.metric("Locations Mapped", len(DATA["movement"].get("spatial_clusters", [])))
            if "posts" in DATA:
                st.metric("Timeline Events", len(DATA["posts"]))
            
            st.markdown("---")
            
            # Case metadata
            st.markdown("""
            <div style="margin-top: 2rem;">
                <p style="font-size: 11px; color: #64748B; margin: 0;">Synthetic Investigation</p>
                <p style="font-size: 11px; color: #64748B; margin: 0;">Last updated: Today</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Collapsed state - just show icons
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <span style="font-size: 24px;">🔍</span>
            </div>
            """, unsafe_allow_html=True)
            
            page = st.selectbox(
                "",
                ["Overview", "Evidence", "Identity Resolution", "Investigation Graph", 
                 "Geospatial", "Timeline", "Hypotheses", "Evaluation"],
                label_visibility="collapsed",
                key="collapsed_navigation"
            )
    
    return page

# ==================== PAGE HELPERS ====================
def render_breadcrumb(case_id: str, page_name: str):
    """Render breadcrumb navigation."""
    st.markdown(f"""
    <div class="breadcrumb">
        {case_id} > {page_name}
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title: str, description: str):
    """Render compact page header."""
    st.markdown(f"""
    <h1 style="font-size: 24px; font-weight: 600; color: #E6EDF3; margin: 0.5rem 0;">{title}</h1>
    <p style="font-size: 13px; color: #8B98A8; margin: 0 0 1.5rem 0;">{description}</p>
    """, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, change: Optional[str] = None, color: str = ACCENT):
    """Render compact metric card."""
    change_html = f"<span style='color: {color}; font-size: 11px;'>{change}</span>" if change else ""
    st.markdown(f"""
    <div class="panel" style="padding: 1rem; margin-bottom: 0.5rem;">
        <p style="font-size: 11px; color: #8B98A8; margin: 0;">{label}</p>
        <p style="font-size: 20px; font-weight: 600; color: #E6EDF3; margin: 0.25rem 0;">{value}</p>
        {change_html}
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE: OVERVIEW ====================
def render_overview():
    """Render case overview dashboard."""
    render_breadcrumb("MP-2026-0419", "Overview")
    render_page_header("Case Overview", "MP-2026-0419 - Missing Person Investigation")
    
    # Status indicator
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <span class="status-badge status-active">ACTIVE SIMULATION</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Metric cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        render_metric_card("Evidence Items", str(len(DATA.get("profiles", []))))
    with col2:
        render_metric_card("Social Accounts", str(len(DATA.get("profiles", []))))
    with col3:
        if "resolved" in DATA:
            render_metric_card("Resolved Identities", str(len(DATA["resolved"].get("clusters", []))))
    with col4:
        if "movement" in DATA:
            render_metric_card("Locations", str(len(DATA["movement"].get("spatial_clusters", []))))
    with col5:
        render_metric_card("Timeline Events", str(len(DATA.get("posts", []))))
    with col6:
        if "movement" in DATA:
            render_metric_card("LKL Confidence", "94%", "Whispering Pines", POSITIVE)
    
    # Main content area
    col_left, col_center, col_right = st.columns([2, 3, 2])
    
    with col_left:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Investigation Summary</h3>
            <p style="font-size: 13px; color: #8B98A8; line-height: 1.6;">
                Subject was last seen physically at Bayview Arts Fine Arts Hall on the morning of March 14. 
                Analysis of digital footprint reveals an escalating pattern of behavioral shifts beginning in early March, 
                coinciding with an inbound contact from shadow art collector @kaelen_v. 
                Three posts referencing an off-grid client dinner meeting at Pacific Horizon Diner were deleted from her primary 
                account on March 12. Digital evidence trace terminates at Whispering Pines Overlook with a final cellular sector ping at 21:45 UTC.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_center:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Activity Timeline Preview</h3>
            <p style="font-size: 13px; color: #8B98A8;">
                Timeline visualization showing key evidence events across multiple data sources.
                <a href="#" style="color: #4F8CFF;">View full timeline →</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Key Investigative Leads</h3>
            <ul style="font-size: 13px; color: #8B98A8; padding-left: 1.2rem; line-height: 1.8;">
                <li>@kaelen_v contact</li>
                <li>Burner phone activation</li>
                <li>Deleted posts pattern</li>
                <li>Whispering Pines location</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Investigation coverage
    st.markdown("""
    <div class="panel">
        <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Investigation Coverage</h3>
        <p style="font-size: 13px; color: #8B98A8;">
            Coverage across multiple evidence sources and temporal analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE: EVIDENCE ====================
def render_evidence():
    """Render evidence explorer."""
    render_breadcrumb("MP-2026-0419", "Evidence Explorer")
    render_page_header("Evidence Explorer", "Digital forensic evidence repository")
    
    # Layout: Left filters, Center table, Right details
    col_filters, col_table, col_details = st.columns([2, 4, 3])
    
    with col_filters:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Evidence Filters</h3>
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Evidence Source</p>
            evidence_types = st.multiselect(
                "",
                ["Social Media", "Photographs", "EXIF", "CDR", "Check-ins", "OSINT", "Other"],
                default=["Social Media", "Photographs", "CDR"],
                label_visibility="collapsed"
            )
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Time Range</p>
            date_range = st.date_input(
                "",
                value=(pd.to_datetime("2026-02-01"), pd.to_datetime("2026-03-15")),
                label_visibility="collapsed"
            )
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Entity Filter</p>
            entity_filter = st.text_input(
                "",
                placeholder="Filter by entity...",
                label_visibility="collapsed"
            )
        </div>
        """, unsafe_allow_html=True)
    
    with col_table:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Evidence Items</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Evidence table
        if "posts" in DATA:
            df = DATA["posts"][["post_id", "account", "timestamp_raw", "text", "location_tag", "deleted"]]
            df.columns = ["ID", "Source", "Timestamp", "Entity", "Location", "Status"]
            st.dataframe(df, height=400, use_container_width=True)
    
    with col_details:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Evidence Details</h3>
            <p style="font-size: 13px; color: #8B98A8;">
                Select an evidence item to view detailed information.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE: IDENTITY RESOLUTION ====================
def render_identity_resolution():
    """Render identity resolution page."""
    render_breadcrumb("MP-2026-0419", "Identity Resolution")
    render_page_header("Identity Resolution", "Multi-factor entity correlation and clustering")
    
    if "resolved" in DATA:
        # Resolved clusters
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Canonical Identity Clusters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        clusters_df = pd.DataFrame(DATA["resolved"]["clusters"])
        st.dataframe(
            clusters_df[["canonical_id", "canonical_name", "account_count", "accounts", "linked_emails", "linked_phones", "is_multi_account"]],
            height=300,
            use_container_width=True
        )
        
        # Identity comparison interface
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Identity Match Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("""
            <div class="panel">
                <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Maya Lin</h3>
                <p style="font-size: 13px; color: #8B98A8; margin: 0.5rem 0;">@mayalin_art</p>
                <p style="font-size: 13px; color: #8B98A8; margin: 0.5rem 0;">@pixel_maya</p>
                <p style="font-size: 13px; color: #8B98A8; margin: 0.5rem 0;">m_lin99</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
            <div class="panel">
                <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Match Confidence: 94%</h3>
                <ul style="font-size: 13px; color: #8B98A8; padding-left: 1.2rem; line-height: 1.8;">
                    <li>Username similarity</li>
                    <li>Shared location patterns</li>
                    <li>Shared photograph metadata</li>
                    <li>Temporal correlation</li>
                    <li>Device metadata match</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==================== PAGE: INVESTIGATION GRAPH ====================
def render_investigation_graph():
    """Render investigation graph with proper controls."""
    render_breadcrumb("MP-2026-0419", "Investigation Graph")
    render_page_header("Investigation Graph", "Multi-modal entity relationship network")
    
    # Graph controls toolbar
    col_search, col_filter, col_layout, col_actions = st.columns([2, 2, 2, 3])
    
    with col_search:
        search_entity = st.text_input(
            "Search Entity",
            placeholder="Search nodes...",
            label_visibility="visible"
        )
    
    with col_filter:
        node_filter = st.multiselect(
            "Filter Node Types",
            ["Person", "Account", "Phone", "Location", "Post", "Photo", "Device"],
            default=["Person", "Account", "Location"],
            label_visibility="visible"
        )
    
    with col_layout:
        layout_type = st.selectbox(
            "Layout",
            ["Organic", "Hierarchical", "Circular", "Orthogonal"],
            label_visibility="visible"
        )
    
    with col_actions:
        col_actions1, col_actions2, col_actions3 = st.columns(3)
        with col_actions1:
            if st.button("Fit Graph", use_container_width=True):
                pass
        with col_actions2:
            if st.button("Focus Selected", use_container_width=True):
                pass
        with col_actions3:
            if st.button("Reset", use_container_width=True):
                pass
    
    # Right-side controls
    col_graph, col_controls = st.columns([4, 1])
    
    with col_controls:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Graph Controls</h3>
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Node Labels</p>
            label_mode = st.radio(
                "",
                ["None", "Important only", "Selected only", "All"],
                label_visibility="collapsed"
            )
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Edge Labels</p>
            edge_label_mode = st.radio(
                "",
                ["Hidden", "Important", "All"],
                label_visibility="collapsed"
            )
            
            <p style="font-size: 11px; color: #8B98A8; margin: 0.5rem 0;">Density</p>
            density = st.select_slider(
                "",
                options=["Low", "Medium", "High"],
                label_visibility="collapsed"
            )
        </div>
        """, unsafe_allow_html=True)
        
        # Legend
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Legend</h3>
        """, unsafe_allow_html=True)
        
        for node_type, color in NODE_COLORS.items():
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <div style="width: 12px; height: 12px; background-color: {color}; border-radius: 2px; margin-right: 0.5rem;"></div>
                <span style="font-size: 12px; color: #8B98A8;">{node_type}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_graph:
        # Graph workspace
        pyvis_html_path = DATA_DIR / "investigation_graph.html"
        if pyvis_html_path.exists():
            with open(pyvis_html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            components.html(html_content, height=700, scrolling=False)
        else:
            st.warning("Graph visualization not found. Run graph generation first.")

# ==================== PAGE: GEOSPATIAL ====================
def render_geospatial():
    """Render geospatial map with controls."""
    render_breadcrumb("MP-2026-0419", "Geospatial")
    render_page_header("Geospatial Analysis", "Location intelligence and movement patterns")
    
    # Map layout
    col_controls, col_map, col_details = st.columns([2, 5, 3])
    
    with col_controls:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Map Layers</h3>
            
            <div style="margin: 0.5rem 0;">
                <input type="checkbox" checked> <span style="font-size: 12px; color: #8B98A8;">Locations</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <input type="checkbox" checked> <span style="font-size: 12px; color: #8B98A8;">Movement</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <input type="checkbox"> <span style="font-size: 12px; color: #8B98A8;">Social Activity</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <input type="checkbox"> <span style="font-size: 12px; color: #8B98A8;">Phone Activity</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <input type="checkbox"> <span style="font-size: 12px; color: #8B98A8;">Photo EXIF</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <input type="checkbox"> <span style="font-size: 12px; color: #8B98A8;">Check-ins</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Timeline slider
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Timeline Slider</h3>
            <p style="font-size: 13px; color: #8B98A8;">
                Drag slider to move through investigation timeline
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_map:
        map_html_path = DATA_DIR / "investigation_map.html"
        if map_html_path.exists():
            with open(map_html_path, "r", encoding="utf-8") as f:
                map_html = f.read()
            components.html(map_html, height=700, scrolling=False)
        else:
            st.warning("Map visualization not found. Run map generation first.")
    
    with col_details:
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Location Details</h3>
            <p style="font-size: 13px; color: #8B98A8;">
                Select a location to view detailed information
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE: TIMELINE ====================
def render_timeline():
    """Render forensic timeline with proper layout."""
    render_breadcrumb("MP-2026-0419", "Timeline")
    render_page_header("Forensic Timeline", "Chronological evidence reconstruction")
    
    # Timeline controls
    col_filters, col_zoom, col_view = st.columns([3, 2, 2])
    
    with col_filters:
        event_filter = st.multiselect(
            "Event Types",
            ["All", "Social", "Telecommunications", "Check-ins", "Photos", "OSINT"],
            default=["All"],
            label_visibility="visible"
        )
    
    with col_zoom:
        zoom_level = st.selectbox(
            "Zoom",
            ["1D", "3D", "7D", "All"],
            label_visibility="visible"
        )
    
    with col_view:
        view_mode = st.selectbox(
            "View",
            ["Compact", "Detailed", "Clusters"],
            label_visibility="visible"
        )
    
    # Timeline workspace
    st.markdown("""
    <div class="panel">
        <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Maya Lin • 17 Aug 2026 → 21 Aug 2026</h3>
    </div>
    """, unsafe_allow_html=True)
    
    timeline_html_path = DATA_DIR / "investigation_timeline.html"
    if timeline_html_path.exists():
        with open(timeline_html_path, "r", encoding="utf-8") as f:
            tl_html = f.read()
        components.html(tl_html, height=600, scrolling=False)
    else:
        st.warning("Timeline visualization not found. Run timeline generation first.")
    
    # Timeline highlights
    st.markdown("""
    <div class="panel">
        <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Investigative Milestones</h3>
        <ul style="font-size: 13px; color: #8B98A8; padding-left: 1.2rem; line-height: 1.8;">
            <li><span style="color: #F05D5E;">Day 20 (Feb 18):</span> Breakup with Lucas Reed; hostile public comment thread</li>
            <li><span style="color: #4F8CFF;">Day 31 (Mar 01):</span> Inbound invitation from @kaelen_v proposing private off-grid shoot</li>
            <li><span style="color: #F5B942;">Day 33 (Mar 03):</span> Behavioral inflection point; sentiment shifts negative with paranoia mentions</li>
            <li><span style="color: #A77BFF;">Day 36 (Mar 06):</span> Covert alias @m.shadow_7 activated</li>
            <li><span style="color: #F05D5E;">Day 40 (Mar 10):</span> Primary phone (+1-555-0144) disconnected; Burner phone (+1-555-0199) activated</li>
            <li><span style="color: #F05D5E;">Day 42 (Mar 12):</span> Deletion of 3 posts mentioning client meeting</li>
            <li><span style="color: #F05D5E;">Day 44 (Mar 14, 21:45 UTC):</span> Final cell ping at Whispering Pines Overlook before handset goes dark</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE: HYPOTHESES ====================
def render_hypotheses():
    """Render hypotheses evaluation."""
    render_breadcrumb("MP-2026-0419", "Hypotheses")
    render_page_header("Investigative Hypotheses", "Competing theory evaluation")
    
    if "hypotheses" in DATA:
        for hyp in DATA["hypotheses"]:
            status_color = POSITIVE if hyp["status"] == "MOST_PROBABLE" else (CRITICAL if "DISPROVEN" in hyp["status"] else WARNING)
            status_icon = "●" if hyp["status"] == "MOST_PROBABLE" else ("✗" if "DISPROVEN" in hyp["status"] else "?")
            
            st.markdown(f"""
            <div class="panel">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0;">
                        <span style="color: {status_color}; margin-right: 0.5rem;">{status_icon}</span>
                        {hyp['title']}
                    </h3>
                    <span style="font-size: 12px; color: #8B98A8;">Confidence: {hyp['confidence_score']*100:.0f}%</span>
                </div>
                
                <p style="font-size: 13px; color: #8B98A8; margin: 0 0 1rem 0;">{hyp['summary']}</p>
                
                <div style="display: flex; gap: 2rem;">
                    <div>
                        <p style="font-size: 11px; color: #8B98A8; margin: 0 0 0.5rem 0;">Supporting Evidence ({len(hyp['supporting_evidence'])})</p>
                        <ul style="font-size: 12px; color: #8B98A8; padding-left: 1rem; margin: 0;">
                            {"".join([f"<li>{s['item']}: {s['detail']}</li>" for s in hyp['supporting_evidence'][:3]])}
                        </ul>
                    </div>
                    <div>
                        <p style="font-size: 11px; color: #8B98A8; margin: 0 0 0.5rem 0;">Contradicting Evidence ({len(hyp['contradicting_evidence'])})</p>
                        <ul style="font-size: 12px; color: #8B98A8; padding-left: 1rem; margin: 0;">
                            {"".join([f"<li>{c['item']}: {c['detail']}</li>" for c in hyp['contradicting_evidence'][:3]])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PAGE: EVALUATION ====================
def render_evaluation():
    """Render evaluation metrics."""
    render_breadcrumb("MP-2026-0419", "Evaluation")
    render_page_header("Academic Evaluation", "Ground truth benchmark validation")
    
    st.markdown("""
    <div class="panel">
        <p style="font-size: 13px; color: #8B98A8;">
            Verification against isolated ground_truth.json (evaluation purposes only)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if "evaluation" in DATA:
        ev = DATA["evaluation"]
        m = ev["metrics"]
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Entity Resolution F1", f"{m['entity_resolution']['f1_score']*100:.1f}%")
        with col2:
            render_metric_card("Target Clustered", f"{m['entity_resolution']['target_persona_cluster_accuracy']*100:.0f}%")
        with col3:
            render_metric_card("LKL Distance Error", f"{m['last_known_location']['distance_error_meters']:.1f} m")
        with col4:
            render_metric_card("Red Herrings Avoided", f"{m['red_herring_audit']['traps_avoided_count']} of 2")
        
        # Detailed metrics
        st.markdown("""
        <div class="panel">
            <h3 style="font-size: 14px; font-weight: 500; color: #E6EDF3; margin: 0 0 1rem 0;">Detailed Metrics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.json(ev)

# ==================== MAIN APP ====================
def main():
    """Main application entry point."""
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "Overview":
        render_overview()
    elif page == "Evidence":
        render_evidence()
    elif page == "Identity Resolution":
        render_identity_resolution()
    elif page == "Investigation Graph":
        render_investigation_graph()
    elif page == "Geospatial":
        render_geospatial()
    elif page == "Timeline":
        render_timeline()
    elif page == "Hypotheses":
        render_hypotheses()
    elif page == "Evaluation":
        render_evaluation()

if __name__ == "__main__":
    main()
