"""
Vision UI Forensic Design System Configuration
Inspired by Vision UI Dashboard PRO React (Creative Tim / Simmmple), Maltego, Neo4j Bloom, and Kaseware.
High-polish dark aesthetic with glassmorphic cards, restrained gradients, and cohesive typography.
"""

# Foundation Colors
BG_DEEPEST = "#05070B"
BACKGROUND = "#080C12"
SURFACE = "#0B1017"
CARD_BG = "#10151D"
CARD_ELEVATED = "#141A23"
BORDERS = "#222B38"
BORDERS_LIGHT = "#2E3A4B"

# Typography
PRIMARY_TEXT = "#F1F5F9"
SECONDARY_TEXT = "#8B98A8"
MUTED_TEXT = "#5F6B7A"

# Vision UI Semantic Accent Palette
COLOR_PRIMARY = "#4F7CFF"       # Primary Accent Blue
COLOR_SECONDARY = "#7C5CFF"     # Secondary Purple Gradient
COLOR_CYAN = "#27C6D9"          # Geographic / Locations
COLOR_SUCCESS = "#19C37D"       # Confirmed / Positive Green
COLOR_WARNING = "#F5B942"       # Transmissions / Warning Amber
COLOR_DANGER = "#FF4D5D"        # Critical / Red / Subject LKL
COLOR_SLATE = "#64748B"         # Hardware / Devices / Muted

# Backwards Compatibility Aliases
PANELS = CARD_BG
SECONDARY_PANELS = CARD_ELEVATED
ACCENT = COLOR_PRIMARY
POSITIVE = COLOR_SUCCESS
WARNING = COLOR_WARNING
CRITICAL = COLOR_DANGER
SUSPECTED = COLOR_SECONDARY
COLOR_BLUE = COLOR_PRIMARY
COLOR_PURPLE = COLOR_SECONDARY
COLOR_GREEN = COLOR_SUCCESS
COLOR_RED = COLOR_DANGER
COLOR_ORANGE = COLOR_WARNING

# Node Colors for Network Graph
NODE_COLORS = {
    "Person": COLOR_DANGER,        # Critical subject/leads
    "Account": COLOR_SECONDARY,    # Digital identity handles
    "Phone": COLOR_SUCCESS,        # Telecommunications & handsets
    "Location": COLOR_CYAN,        # Physical venues / coordinates
    "Post": COLOR_WARNING,         # Microblog transmissions
    "Photo": COLOR_CYAN,           # Photographic EXIF
    "Device": COLOR_SLATE          # Hardware signatures
}

# Graph Edge Colors
EDGE_COLORS = {
    "OWNS": COLOR_SUCCESS,
    "FOLLOWS": COLOR_PRIMARY,
    "POSTED": COLOR_WARNING,
    "MENTIONS": COLOR_SECONDARY,
    "CHECKED_IN_AT": COLOR_CYAN,
    "CONTACTED": COLOR_SUCCESS,
    "SAME_AS": COLOR_PRIMARY,
    "APPEARS_IN": COLOR_SECONDARY,
    "TAKEN_AT": COLOR_CYAN,
    "COMMENTED": COLOR_WARNING
}

# Timeline Event Colors
TIMELINE_COLORS = {
    "Deleted Post": COLOR_DANGER,
    "Public Post": COLOR_PRIMARY,
    "Burner Handset Ping": COLOR_DANGER,
    "Voice Call": COLOR_SUCCESS,
    "Venue Check-in": COLOR_CYAN,
    "Red Herring Photo": COLOR_WARNING,
    "Captured Photo": COLOR_SECONDARY,
    "OSINT / Behavioral": COLOR_WARNING
}

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
MONO_FONT = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"

# Vision UI CSS Design System
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Dark Reset & Background */
    html, body, .stApp {{
        background-color: {BG_DEEPEST} !important;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(79, 124, 255, 0.07) 0%, transparent 60%),
            radial-gradient(circle at 100% 50%, rgba(124, 92, 255, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 0% 100%, rgba(39, 198, 217, 0.04) 0%, transparent 50%) !important;
        background-attachment: fixed !important;
        color: {PRIMARY_TEXT} !important;
        font-family: {FONT_FAMILY};
        font-size: 13px;
        letter-spacing: -0.01em;
    }}

    /* COMPLETELY HIDE PERMANENT SIDEBAR & STREAMLIT DECORATIONS */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
    }}

    .stApp [data-testid="stMainBlockContainer"] {{
        background: transparent !important;
        padding-top: 0.35rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }}

    /* Top Sticky Workstation Navigation Bar */
    .vui-topbar {{
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(8, 12, 18, 0.88);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid {BORDERS};
        padding: 0.5rem 0.5rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65);
    }}

    .vui-topbar-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(34, 43, 56, 0.5);
        margin-bottom: 0.45rem;
    }}

    .vui-brand {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .vui-logo {{
        font-family: {FONT_FAMILY};
        font-weight: 800;
        font-size: 17px;
        letter-spacing: 1.8px;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .vui-badge-pill {{
        font-family: {MONO_FONT};
        font-size: 9px;
        font-weight: 600;
        padding: 2px 7px;
        background: linear-gradient(135deg, rgba(79, 124, 255, 0.2) 0%, rgba(124, 92, 255, 0.2) 100%);
        border: 1px solid rgba(79, 124, 255, 0.4);
        color: {COLOR_PRIMARY};
        border-radius: 4px;
        letter-spacing: 0.6px;
    }}

    .vui-case-tag {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: {MONO_FONT};
        font-size: 11px;
    }}

    .vui-case-id {{
        color: {PRIMARY_TEXT};
        font-weight: 600;
    }}

    .vui-case-name {{
        color: {COLOR_PRIMARY};
        font-weight: 500;
    }}

    .vui-status-active {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        background: rgba(25, 195, 125, 0.12);
        color: {COLOR_SUCCESS};
        border: 1px solid rgba(25, 195, 125, 0.3);
        letter-spacing: 0.5px;
    }}

    /* Compact Case Context Bar */
    .vui-context-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(16, 21, 29, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid {BORDERS};
        border-radius: 8px;
        padding: 6px 14px;
        margin-bottom: 0.85rem;
        font-size: 11px;
    }}

    .vui-context-left {{
        display: flex;
        align-items: center;
        gap: 12px;
        color: {SECONDARY_TEXT};
    }}

    .vui-context-right {{
        display: flex;
        align-items: center;
        gap: 16px;
        font-family: {MONO_FONT};
        color: {SECONDARY_TEXT};
    }}

    .vui-stat-item {{
        display: flex;
        align-items: center;
        gap: 5px;
    }}

    .vui-stat-num {{
        color: {PRIMARY_TEXT};
        font-weight: 600;
    }}

    /* Top Horizontal Navigation Strip (Styled Radio) */
    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        background: {CARD_BG} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
        padding: 3px !important;
        gap: 3px !important;
        width: 100% !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
        flex: 1 !important;
        display: flex !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        background: transparent !important;
        border-radius: 6px !important;
        padding: 7px 12px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1px solid transparent !important;
        color: {SECONDARY_TEXT} !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {{
        background: {CARD_ELEVATED} !important;
        color: {PRIMARY_TEXT} !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(79, 124, 255, 0.18) 0%, rgba(124, 92, 255, 0.18) 100%) !important;
        border: 1px solid rgba(79, 124, 255, 0.5) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 10px rgba(79, 124, 255, 0.25) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] input,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {{
        display: none !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] span {{
        font-size: 12px !important;
        color: inherit !important;
    }}

    /* Vision UI Rounded Glass Cards */
    .vui-card {{
        background: rgba(16, 21, 29, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid {BORDERS};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .vui-card:hover {{
        border-color: {BORDERS_LIGHT};
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.6);
    }}

    .vui-card-glow {{
        border-color: rgba(79, 124, 255, 0.35);
        box-shadow: 0 0 20px rgba(79, 124, 255, 0.15);
    }}

    .vui-card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.65rem;
    }}

    .vui-card-title {{
        font-size: 11px;
        font-weight: 600;
        color: {MUTED_TEXT};
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin: 0;
    }}

    .vui-card-value {{
        font-family: {FONT_FAMILY};
        font-size: 22px;
        font-weight: 700;
        color: {PRIMARY_TEXT};
        margin: 0.15rem 0;
    }}

    .vui-card-sub {{
        font-size: 11px;
        color: {SECONDARY_TEXT};
        margin-top: 0.2rem;
    }}

    /* Buttons */
    .stButton > button {{
        background: rgba(20, 26, 35, 0.85) !important;
        color: {PRIMARY_TEXT} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 0.4rem 0.85rem !important;
        transition: all 0.18s ease !important;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, rgba(79, 124, 255, 0.25) 0%, rgba(124, 92, 255, 0.25) 100%) !important;
        border-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 12px rgba(79, 124, 255, 0.3) !important;
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* Selectbox, Inputs & Multiselect */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"],
    .stTextInput > div > div > input,
    .stMultiSelect > div > div {{
        background-color: {CARD_BG} !important;
        color: {PRIMARY_TEXT} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 6px !important;
        font-size: 12px !important;
    }}

    .stTextInput > div > div > input:focus,
    .stSelectbox [data-baseweb="select"]:focus-within {{
        border-color: {COLOR_PRIMARY} !important;
        box-shadow: 0 0 0 1px {COLOR_PRIMARY} !important;
    }}

    /* Dropdown Menus */
    [data-baseweb="popover"], [data-baseweb="menu"], [data-baseweb="select-dropdown"] {{
        background-color: {CARD_ELEVATED} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
        color: {PRIMARY_TEXT} !important;
    }}

    [data-baseweb="menu"] li:hover {{
        background-color: rgba(79, 124, 255, 0.15) !important;
        color: {COLOR_PRIMARY} !important;
    }}

    [data-baseweb="tag"] {{
        background-color: {CARD_ELEVATED} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 4px !important;
        color: {PRIMARY_TEXT} !important;
    }}

    /* Tables & Dataframes */
    .stDataFrame, div[data-testid="stTable"] {{
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
        background-color: {CARD_BG} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {CARD_BG} !important;
        border-bottom: 1px solid {BORDERS} !important;
        border-radius: 8px 8px 0 0 !important;
        gap: 4px !important;
        padding: 4px 6px 0 6px !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: {SECONDARY_TEXT} !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 8px 14px !important;
        border-radius: 6px 6px 0 0 !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {CARD_ELEVATED} !important;
        color: {COLOR_PRIMARY} !important;
        border-bottom: 2px solid {COLOR_PRIMARY} !important;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 6px !important;
        color: {PRIMARY_TEXT} !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }}

    .streamlit-expanderContent {{
        background-color: {SURFACE} !important;
        border: 1px solid {BORDERS} !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }}

    /* Status Badges */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        font-family: {MONO_FONT};
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    .status-active {{
        background-color: rgba(25, 195, 125, 0.12);
        color: {COLOR_SUCCESS};
        border: 1px solid rgba(25, 195, 125, 0.3);
    }}

    .status-critical {{
        background-color: rgba(255, 77, 93, 0.12);
        color: {COLOR_DANGER};
        border: 1px solid rgba(255, 77, 93, 0.3);
    }}

    .status-pending {{
        background-color: rgba(245, 185, 66, 0.12);
        color: {COLOR_WARNING};
        border: 1px solid rgba(245, 185, 66, 0.3);
    }}

    .status-info {{
        background-color: rgba(79, 124, 255, 0.12);
        color: {COLOR_PRIMARY};
        border: 1px solid rgba(79, 124, 255, 0.3);
    }}

    .breadcrumb {{
        color: {MUTED_TEXT};
        font-family: {MONO_FONT};
        font-size: 10px;
        margin-bottom: 0.25rem;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }}

    /* Iframe Responsiveness */
    iframe {{
        border: none !important;
        border-radius: 10px;
        width: 100% !important;
        background-color: {BG_DEEPEST} !important;
    }}

    /* Sleek Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {BG_DEEPEST};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {BORDERS};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {BORDERS_LIGHT};
    }}
</style>
"""
