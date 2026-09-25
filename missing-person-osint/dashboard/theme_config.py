"""
Gradient Dashboard Design System Configuration
Inspired by the Midnight Gradient User Admin Panel (Deep Indigo / Sapphire, Glowing Neon Mint Green, Electric Royal Blue).
High-polish dark aesthetic with ambient glow, glowing horizontal accent dividers, and cohesive typography.
"""

# Foundation Colors - Gradient Midnight Dashboard Theme
BG_DEEPEST = "#0E1231"
BACKGROUND = "#141A42"
SURFACE = "#18204E"
CARD_BG = "#1A2254"
CARD_ELEVATED = "#202A66"
BORDERS = "#2C3979"
BORDERS_LIGHT = "#384994"

# Typography
PRIMARY_TEXT = "#FFFFFF"
SECONDARY_TEXT = "#98A7CE"
MUTED_TEXT = "#6D7FA8"

# Neon Mint & Electric Gradient Palette (from reference image)
COLOR_PRIMARY = "#3A6BFF"       # Electric Royal Blue
COLOR_SECONDARY = "#6C5CE7"     # Vibrant Indigo / Violet
COLOR_MINT = "#00E5A3"          # Neon Mint Green (key accent in image!)
COLOR_CYAN = "#00D2D3"          # Cyan / Locations
COLOR_SUCCESS = "#00E5A3"       # Neon Mint Green for Success / Checkmarks
COLOR_WARNING = "#F5B942"       # Warning Amber
COLOR_DANGER = "#FF4757"        # Critical / Red / Danger
COLOR_SLATE = "#7E8EB8"         # Slate Periwinkle

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
    "Photo": COLOR_MINT,           # Photographic EXIF
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

# Gradient Midnight Dashboard CSS Design System
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Gradient Midnight Dashboard Background */
    html, body, .stApp {{
        background-color: #101538 !important;
        background-image: 
            radial-gradient(circle at 18% 18%, rgba(58, 107, 255, 0.25) 0%, transparent 45%),
            radial-gradient(circle at 82% 78%, rgba(108, 92, 231, 0.22) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(0, 229, 163, 0.05) 0%, transparent 60%),
            linear-gradient(135deg, #0E1231 0%, #141A42 50%, #1A2254 100%) !important;
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

    /* REMOVE DEPLOY BUTTON AND STREAMLIT HEADER DECORATIONS */
    .stDeployButton,
    [data-testid="stAppDeployButton"],
    button[title="Deploy this app"],
    button[title="Deploy"],
    header[data-testid="stHeader"] .stDeployButton,
    div[data-testid="stToolbar"] [data-testid="stAppDeployButton"],
    header[data-testid="stHeader"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        max-height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    .stApp [data-testid="stMainBlockContainer"] {{
        background: transparent !important;
        padding-top: 0.35rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }}

    /* Top Navigation Bar styled like MyLogo header in reference */
    .dashboard-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #101438;
        border: 1px solid {BORDERS};
        padding: 0.45rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 0.65rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}

    .topbar-logo {{
        font-family: {FONT_FAMILY};
        font-weight: 800;
        font-size: 19px;
        letter-spacing: 1px;
        color: #FFFFFF;
    }}

    .topbar-right-controls {{
        display: flex;
        align-items: center;
        gap: 16px;
        color: {SECONDARY_TEXT};
        font-size: 13px;
    }}

    .topbar-badge-bell {{
        position: relative;
        cursor: pointer;
        font-size: 14px;
    }}

    .topbar-badge-count {{
        position: absolute;
        top: -6px;
        right: -8px;
        background: #FF4757;
        color: #FFFFFF;
        font-size: 9px;
        font-weight: 700;
        border-radius: 50%;
        width: 15px;
        height: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 6px rgba(255, 71, 87, 0.6);
    }}

    /* Compact Case Context Bar */
    .vui-context-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(22, 29, 72, 0.65);
        backdrop-filter: blur(14px);
        border: 1px solid {BORDERS};
        border-radius: 10px;
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

    .vui-case-id {{
        color: {PRIMARY_TEXT};
        font-weight: 700;
    }}

    .vui-case-name {{
        color: {COLOR_MINT};
        font-weight: 600;
    }}

    .vui-status-active {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        background: rgba(0, 229, 163, 0.15);
        color: {COLOR_MINT};
        border: 1px solid rgba(0, 229, 163, 0.4);
        letter-spacing: 0.5px;
    }}

    /* Top Horizontal Navigation Container (Full Viewport Width & Zero Text Break) */
    div[data-testid="stRadio"],
    div[data-testid="stRadio"] > div,
    div[data-testid="element-container"]:has(div[data-testid="stRadio"]) {{
        width: 100% !important;
        max-width: 100% !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        align-items: stretch !important;
        background: #12173D !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 10px !important;
        padding: 4px 6px !important;
        gap: 6px !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin-bottom: 0.65rem !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
    }}
    div[data-testid="stRadio"] > div[role="radiogroup"]::-webkit-scrollbar {{
        display: none !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
        flex: 1 1 auto !important;
        display: flex !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        background: transparent !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1px solid transparent !important;
        color: {SECONDARY_TEXT} !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        word-wrap: normal !important;
        overflow: visible !important;
        min-width: fit-content !important;
        box-sizing: border-box !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {{
        background: {CARD_BG} !important;
        color: #FFFFFF !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(58, 107, 255, 0.45) 0%, rgba(108, 92, 231, 0.45) 100%) !important;
        border: 1px solid {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 0 14px rgba(58, 107, 255, 0.4) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] input,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {{
        display: none !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label div,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label p,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label span {{
        white-space: nowrap !important;
        word-break: keep-all !important;
        word-wrap: normal !important;
        text-overflow: clip !important;
        overflow: visible !important;
        font-size: 13px !important;
        color: inherit !important;
        display: inline-block !important;
    }}

    @media (max-width: 1440px) {{
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
            padding: 9px 12px !important;
            font-size: 12.5px !important;
        }}
        div[data-testid="stRadio"] > div[role="radiogroup"] > label div,
        div[data-testid="stRadio"] > div[role="radiogroup"] > label p,
        div[data-testid="stRadio"] > div[role="radiogroup"] > label span {{
            font-size: 12.5px !important;
        }}
    }}

    @media (max-width: 1366px) {{
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
            padding: 8px 10px !important;
            font-size: 12px !important;
        }}
        div[data-testid="stRadio"] > div[role="radiogroup"] > label div,
        div[data-testid="stRadio"] > div[role="radiogroup"] > label p,
        div[data-testid="stRadio"] > div[role="radiogroup"] > label span {{
            font-size: 12px !important;
        }}
    }}

    /* Midnight Gradient Cards (matching the reference image cards) */
    .panel, .vui-card, .metric-card {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 14px !important;
        padding: 1.15rem 1.25rem !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 10px 28px rgba(8, 11, 30, 0.5), 0 0 1px rgba(58, 107, 255, 0.25) !important;
        position: relative;
        overflow: hidden;
    }}

    .panel:hover, .vui-card:hover {{
        border-color: {BORDERS_LIGHT} !important;
        box-shadow: 0 12px 32px rgba(8, 11, 30, 0.65), 0 0 12px rgba(58, 107, 255, 0.2) !important;
    }}

    /* Card Header Bar with Glowing Accent Line */
    .card-header-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}

    .card-title-text {{
        font-size: 13px;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: 0.2px;
        margin: 0;
    }}

    .card-close-x {{
        color: #6D7FA8;
        font-size: 12px;
        font-weight: 700;
    }}

    .card-glow-divider {{
        height: 2px;
        width: 100%;
        background: linear-gradient(90deg, #3A6BFF 0%, #6C5CE7 65%, transparent 100%);
        border-radius: 2px;
        margin-bottom: 14px;
    }}

    /* Progress Bars matching Aenean / Fermentum in image */
    .prog-container {{
        margin-bottom: 12px;
    }}

    .prog-header {{
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: {SECONDARY_TEXT};
        margin-bottom: 5px;
        font-weight: 500;
    }}

    .prog-bar-outer {{
        height: 18px;
        background: #12173D;
        border-radius: 9px;
        overflow: hidden;
        padding: 2px;
        border: 1px solid #232D63;
    }}

    .prog-bar-inner {{
        height: 100%;
        background: {COLOR_MINT};
        border-radius: 7px;
        box-shadow: 0 0 10px rgba(0, 229, 163, 0.45);
    }}

    /* Profile Avatar Ring matching Hamet faucibus */
    .avatar-ring-box {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 8px 0;
        text-align: center;
    }}

    .avatar-glowing-circle {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #FFFFFF;
        box-shadow: 0 0 18px rgba(255, 255, 255, 0.4), inset 0 0 12px rgba(58, 107, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }}

    .avatar-glowing-inner {{
        width: 86px;
        height: 86px;
        border-radius: 50%;
        background: radial-gradient(circle, #202A66 0%, #141A42 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }}

    .neon-pill-badge {{
        display: inline-block;
        padding: 4px 14px;
        background: {COLOR_MINT};
        color: #0E1231;
        font-size: 11px;
        font-weight: 700;
        border-radius: 12px;
        letter-spacing: 0.5px;
        margin-top: 6px;
        box-shadow: 0 0 10px rgba(0, 229, 163, 0.45);
    }}

    /* Checklist matching Integer ater */
    .chk-item {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(44, 57, 121, 0.4);
    }}

    .chk-item:last-child {{
        border-bottom: none;
    }}

    .chk-circle-hollow {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid #6D7FA8;
        flex-shrink: 0;
    }}

    .chk-circle-green {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: {COLOR_MINT};
        border: 2px solid {COLOR_MINT};
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0E1231;
        font-size: 11px;
        font-weight: 800;
        flex-shrink: 0;
        box-shadow: 0 0 8px rgba(0, 229, 163, 0.5);
    }}

    .chk-content {{
        flex: 1;
    }}

    .chk-title {{
        font-size: 12px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 2px;
    }}

    .chk-meta {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 10px;
        color: {SECONDARY_TEXT};
    }}

    .chk-tag-gc {{
        color: {COLOR_MINT};
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}

    /* Buttons */
    .stButton > button {{
        background: #18204E !important;
        color: #FFFFFF !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.95rem !important;
        transition: all 0.18s ease !important;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, rgba(58, 107, 255, 0.35) 0%, rgba(108, 92, 231, 0.35) 100%) !important;
        border-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 14px rgba(58, 107, 255, 0.35) !important;
        transform: translateY(-1px);
    }}

    /* Selectbox, Inputs & Multiselect */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"],
    .stTextInput > div > div > input,
    .stMultiSelect > div > div {{
        background-color: #12173D !important;
        color: #FFFFFF !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
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
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }}

    [data-baseweb="menu"] li:hover {{
        background-color: rgba(58, 107, 255, 0.2) !important;
        color: {COLOR_MINT} !important;
    }}

    [data-baseweb="tag"] {{
        background-color: {CARD_ELEVATED} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 6px !important;
        color: #FFFFFF !important;
    }}

    /* Tables & Dataframes */
    .stDataFrame, div[data-testid="stTable"] {{
        border: 1px solid {BORDERS} !important;
        border-radius: 10px !important;
        background-color: {CARD_BG} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #12173D !important;
        border-bottom: 1px solid {BORDERS} !important;
        border-radius: 10px 10px 0 0 !important;
        gap: 6px !important;
        padding: 5px 8px 0 8px !important;
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
        background: {CARD_BG} !important;
        color: {COLOR_MINT} !important;
        border-bottom: 2px solid {COLOR_MINT} !important;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDERS} !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }}

    .streamlit-expanderContent {{
        background-color: {SURFACE} !important;
        border: 1px solid {BORDERS} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }}

    /* Status Badges */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }}

    .status-active {{
        background-color: rgba(0, 229, 163, 0.15);
        color: {COLOR_MINT};
        border: 1px solid rgba(0, 229, 163, 0.4);
    }}

    .status-pending {{
        background-color: rgba(245, 185, 66, 0.15);
        color: {COLOR_WARNING};
        border: 1px solid rgba(245, 185, 66, 0.4);
    }}

    .status-critical {{
        background-color: rgba(255, 71, 87, 0.15);
        color: {COLOR_DANGER};
        border: 1px solid rgba(255, 71, 87, 0.4);
    }}

    /* Breadcrumbs */
    .breadcrumb {{
        font-size: 11px;
        font-family: {MONO_FONT};
        color: {MUTED_TEXT};
        margin-bottom: 0.35rem;
    }}

    /* Metric cards */
    .metric-label {{
        font-size: 11px;
        color: {SECONDARY_TEXT};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }}

    .metric-value {{
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0.2rem 0;
        letter-spacing: -0.5px;
    }}

    /* Scrollbars */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}

    ::-webkit-scrollbar-track {{
        background: #0E1231;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {BORDERS};
        border-radius: 3px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLOR_PRIMARY};
    }}
</style>
"""
