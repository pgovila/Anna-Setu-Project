"""
Anna-Setu: Streamlit Interface for Campus Food Rescue & Plate-Waste Bio-Recycling Network
Grounded in FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam Food Service By-Laws.
Covers Dual Tracks: Track A (Software AI & RAG Engine) + Track B (Smart Plate-Waste Interceptor & Bio-Recycler).
"""

import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime
from rag.pipeline import AnnaSetuRAGPipeline

def _img_to_b64(path: str) -> str:
    """Return a base64 data URI for an image file, for use in HTML."""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    return f"data:{mime};base64,{data}"

LOGO_B64 = _img_to_b64("Anna Setu Transparent.png") or _img_to_b64("Anna Setu.png")

st.set_page_config(
    page_title="Anna-Setu: Campus Food Rescue Network",
    page_icon="Anna Setu Transparent.png" if os.path.exists("Anna Setu Transparent.png") else "Anna Setu.png",
    layout="wide"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════
   ANNA-SETU BRAND PALETTE
   Deep Green #1a7a3c · Mid Green #2a9d50 · Gold #f5a623
   BG: clean off-white · Surface: white · Text: #1a1a1a
   ═══════════════════════════════════════════════════════ */

/* ── Font & base ── */
html, body { font-family: 'Segoe UI', system-ui, sans-serif; }

/* ── App background — clean off-white (not gradient) ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #f4f9f5 !important;
}

/* ── All text dark by default — targeted, NOT .stApp * (too broad) ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stSlider label, .stTextArea label,
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
.stMarkdown p, .stMarkdown li, .stMarkdown strong {
    color: #1a1a1a !important;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* ── Hero text — explicit white, highest specificity ── */
.hero-banner h1,
.hero-banner h1 *,
div.hero-banner h1 { color: #ffffff !important; }
div.hero-banner p,
div.hero-banner span { color: #ffffff !important; }

/* ── Fix text boxes — white bg, dark text, fully rounded ── */
.stTextArea textarea,
.stTextInput input,
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    border: 1.5px solid #a8cfb0 !important;
    border-radius: 16px !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #1a7a3c !important;
    box-shadow: 0 0 0 3px rgba(26,122,60,.18) !important;
}

/* ── Selectbox — all parts: trigger, value, dropdown menu, items ── */
/* Trigger container + value text */
.stSelectbox div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    border-color: #a8cfb0 !important;
    border-radius: 12px !important;
}
/* Selected value text */
.stSelectbox [data-baseweb="select"] [data-testid="stMarkdownContainer"],
.stSelectbox div[class*="ValueContainer"] *,
.stSelectbox div[class*="singleValue"],
.stSelectbox div[class*="placeholder"] {
    color: #1a1a1a !important;
    background: transparent !important;
}
/* Dropdown popup list */
ul[data-baseweb="menu"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid #a8cfb0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(26,122,60,.15) !important;
}
/* Dropdown items */
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"],
ul[data-baseweb="menu"] li {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
}
/* Dropdown item hover → orange highlight with black text */
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #f5a623 !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
}
/* Number input */
.stNumberInput input {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    border-color: #a8cfb0 !important;
    border-radius: 12px !important;
}
/* Dropdown arrow icon */
.stSelectbox svg { color: #1a7a3c !important; fill: #1a7a3c !important; }

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0d4a22 0%, #1a7a3c 45%, #2a9d50 75%, #f5a623 100%);
    border-radius: 24px;
    padding: 32px 36px 28px;
    margin-bottom: 10px;
    box-shadow: 0 4px 24px rgba(13,74,34,.40);
}
.hero-banner h1 { font-size: 28px; font-weight: 800; margin: 0 0 4px; color: #ffffff !important; }
.hero-banner p  { font-size: 14px; opacity: .92; margin: 0; color: #ffffff !important; }
.hero-tag {
    display: inline-block; background: rgba(255,255,255,.22);
    border-radius: 999px; padding: 4px 16px;
    font-size: 11px; font-weight: 600; margin-top: 10px; color: #ffffff !important;
}

/* ── Stat chips in hero ── */
.hero-stats { display: flex; gap: 14px; margin-top: 16px; flex-wrap: wrap; }
.hero-stat {
    background: rgba(255,255,255,.18); border-radius: 16px;
    padding: 10px 18px; text-align: center;
    border: 1px solid rgba(255,255,255,.25);
}
.hero-stat .num { font-size: 22px; font-weight: 800; display: block; color: #ffffff !important; }
.hero-stat .lbl { font-size: 10px; opacity: .88; letter-spacing: .05em; color: #ffffff !important; }

/* ── Section card — rounded rectangle, white surface ── */
.section-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 14px;
    border: 1px solid rgba(26,122,60,.18);
    box-shadow: 0 2px 10px rgba(13,74,34,.10);
    color: #1a1a1a !important;
}
.section-card *, .section-card strong, .section-card span,
.section-card p, .section-card b { color: #1a1a1a !important; }

/* ── Step header pills — fully rounded, gold accent ── */
.step-pill {
    display: inline-block;
    background: linear-gradient(90deg, #1a7a3c, #2a9d50);
    color: #ffffff !important;
    border-radius: 999px; padding: 5px 18px;
    font-size: 12px; font-weight: 700; margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(26,122,60,.30);
}

/* ── Bordered containers — rounded rectangles on white ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(26,122,60,.22) !important;
    border-radius: 20px !important;
    background: #ffffff !important;
    box-shadow: 0 2px 8px rgba(13,74,34,.08) !important;
}

/* ── Tabs — pill-style on white tray ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 6px 8px;
    gap: 4px;
    border: 1px solid #d4e8d8;
    box-shadow: 0 2px 10px rgba(26,122,60,.10);
    display: flex;
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600; font-size: 13px;
    padding: 7px 16px;
    color: #1a1a1a !important;
    background: transparent;
    border: none !important;
    outline: none !important;
}
/* Remove red/default underline Streamlit adds */
.stTabs [data-baseweb="tab"]::after,
.stTabs [data-baseweb="tab"]::before { display: none !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }
/* Active tab: green box, bold orange text */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a7a3c, #2a9d50) !important;
    color: #f5a623 !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 10px rgba(26,122,60,.35) !important;
}
.stTabs [aria-selected="false"] { color: #2a2a2a !important; font-weight: 600 !important; }
.stTabs [aria-selected="false"]:hover {
    background: #e8f5e9 !important; color: #1a7a3c !important;
}
/* Propagate colour to all children of tab button */
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div { color: inherit !important; }
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div { color: #f5a623 !important; font-weight: 800 !important; }

/* ── Primary button — green gradient, rounded ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1a7a3c, #2a9d50) !important;
    border: none !important; border-radius: 999px !important;
    color: #ffffff !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 3px 12px rgba(26,122,60,.35) !important;
    transition: all .2s;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0d4a22, #1a7a3c) !important;
    box-shadow: 0 5px 18px rgba(26,122,60,.45) !important;
    transform: translateY(-1px);
}

/* ── Secondary / default button ── */
.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: #ffffff !important;
    border: 2px solid #1a7a3c !important;
    color: #1a7a3c !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(26,122,60,.15) !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover {
    background: #e8f5e9 !important;
    transform: translateY(-1px);
}

/* ── Metric cards — white rounded rectangles ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 20px !important;
    border: 1px solid rgba(26,122,60,.18) !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 8px rgba(13,74,34,.08) !important;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] p,
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1a1a1a !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,.92) !important;
    border-radius: 16px !important;
    font-weight: 600 !important;
    color: #1a7a3c !important;
}

/* ── Alerts — rounded ── */
.stAlert { border-radius: 16px !important; }
.stAlert p { color: inherit !important; }

/* ── Slider track — green ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: #1a7a3c !important;
}

/* ── Dataframe / table ── */
.dataframe thead th {
    background: linear-gradient(135deg, #1a7a3c, #2a9d50) !important;
    color: #ffffff !important;
    border-radius: 8px 8px 0 0;
}
.dataframe tbody td { color: #1a1a1a !important; }

/* ── Sidebar (if shown) ── */
[data-testid="stSidebar"] {
    background: rgba(13,74,34,.92) !important;
    border-radius: 0 20px 20px 0;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Pipeline ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_pipeline():
    return AnnaSetuRAGPipeline()

pipeline = get_pipeline()

# ── Option lists ─────────────────────────────────────────────────────────────
CATEGORY_OPTIONS = [
    ("Cooked Grains, Rice, Dal & Gravies (High Moisture)", "cooked_grains_curry"),
    ("Dry Cooked Staples (Rotis, Chapatis, Dry Sabzi)", "dry_staples_roti"),
    ("Dairy, Paneer Curries, Milk Sweets & Kheer", "dairy_sweets"),
    ("Dry Fried Snacks (Samosas, Cutlets, Pakoras)", "fried_snacks"),
    ("Raw Cut Salads, Sliced Fruits — ⚠️ Cannot be donated", "raw_salads_cut_fruits"),
    ("Plate Waste / Leftover from Diners' Plates — ⚠️ Strictly Prohibited", "plate_waste")
]
CATEGORY_DICT = {label: key for label, key in CATEGORY_OPTIONS}

STORAGE_OPTIONS = [
    ("Kept at Room Temperature (~25°C – 35°C)", "ambient"),
    ("Kept Hot — maintained at 65°C or above", "hot_holding"),
    ("Kept in Fridge / Cold Storage — 5°C or below", "refrigerated")
]
STORAGE_DICT = {label: key for label, key in STORAGE_OPTIONS}

ZONE_OPTIONS = [
    ("Zone 4 – Gomti Nagar, Extension, Indira Nagar", 4),
    ("Zone 1 – Hazratganj, Chowk, Charbagh, Qaiserbagh", 1),
    ("Zone 2 – Aishbagh, Rajajipuram", 2),
    ("Zone 3 – Aliganj, Jankipuram, Vikas Nagar", 3),
    ("Zone 5 – Alambagh, Singar Nagar, Krishna Nagar", 5),
    ("Zone 6 – Hardoi Road, Dubagga, Kakori", 6),
    ("Zone 7 – Chinhat, Faizabad Road, BBD Corridor", 7),
    ("Zone 8 – Sarojini Nagar, Transport Nagar, Airport", 8)
]
ZONE_DICT = {label: zone_id for label, zone_id in ZONE_OPTIONS}

DINING_FACILITIES = [
    "Central Campus Dining Complex (Main Mess)",
    "North Campus Cafeteria (Block A Dining)",
    "Girls Hostel Dining Hall (Block B)",
    "International Scholars Mess (Block C)",
    "Faculty & Executive Dining Hall",
    "Student Activity Centre Food Court",
    "Auditorium & Banquet Catering Hub",
    "Other / Custom Facility"
]

MEAL_PRESETS = {
    "Breakfast":        {"time_prep": "08:00", "time_assess": "09:30", "item": "Vegetable Poha, Idli Sambhar & Boiled Eggs",    "servings": 35, "category_idx": 0, "storage_idx": 0},
    "Lunch":            {"time_prep": "12:30", "time_assess": "14:00", "item": "Vegetable Pulao, Dal Tadka & Chapati",           "servings": 45, "category_idx": 0, "storage_idx": 0},
    "Snacks / High Tea":{"time_prep": "16:30", "time_assess": "17:30", "item": "Vegetable Cutlets, Samosas & Tea Cake",          "servings": 30, "category_idx": 3, "storage_idx": 0},
    "Dinner":           {"time_prep": "20:00", "time_assess": "21:30", "item": "Paneer Butter Masala, Dal Makhani & Rotis",      "servings": 50, "category_idx": 2, "storage_idx": 0},
    "Other":            {"time_prep": "11:00", "time_assess": "12:30", "item": "Mixed Institutional Buffet Catering Spread",     "servings": 60, "category_idx": 0, "storage_idx": 0},
}

SHELTER_LIST = ["Auto-Match Closest Verified Shelter (Recommended)"] + pipeline.get_shelter_names()

# =============================================================================
# MULTI-STEP POP-UP TUTORIAL
# =============================================================================
TUTORIAL_STEPS = 4   # slide 0 → 3

if "tutorial_done"  not in st.session_state: st.session_state.tutorial_done  = False
if "tutorial_step"  not in st.session_state: st.session_state.tutorial_step  = 0

SLIDE_CONTENT = [
    # ── Slide 0: Welcome ─────────────────────────────────────────────────────
    {
        "icon": f'<img src="{LOGO_B64}" style="width:72px;height:72px;border-radius:18px;object-fit:cover;" alt="Anna-Setu"/>' if LOGO_B64 else "🍽️",
        "title": "Welcome to Anna-Setu!",
        "subtitle": "Your campus food rescue and waste-recycling helper",
        "body": """
<p style="font-size:15px;line-height:1.75;color:#333;margin:0;">
  <strong>Anna-Setu</strong> means <em>"Food Bridge"</em> in Hindi.<br><br>
  Every day, campus dining halls cook more food than students can eat.
  Anna-Setu helps your team donate that leftover food to nearby shelters —
  <strong>safely and quickly.</strong><br><br>
  Food that cannot be donated is turned into
  <strong>clean compost fertilizer</strong> in 24 hours — nothing goes to landfill.
</p>
<div style="display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;">
  <div style="background:#e8f5e9;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#2e7d32;">6+</div>
    <div style="font-size:12px;color:#555;">Shelters Nearby</div>
  </div>
  <div style="background:#fff8e1;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#f9a825;">10</div>
    <div style="font-size:12px;color:#555;">Safety Rules Built-In</div>
  </div>
  <div style="background:#f3e5f5;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#6a1b9a;">24h</div>
    <div style="font-size:12px;color:#555;">Waste Becomes Fertilizer</div>
  </div>
</div>
""",
    },
    # ── Slide 1: Tab guide ───────────────────────────────────────────────────
    {
        "icon": "🗂️",
        "title": "What's Inside the App?",
        "subtitle": "5 tabs - each one does a simple, clear job",
        "body": """
<table style="width:100%;border-collapse:collapse;font-size:14px;">
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;width:38px;font-size:20px;">🍛</td>
    <td style="padding:10px 8px;">
      <strong style="color:#1a1a1a;font-size:14px;">Tab 1 - Donate Surplus Food</strong><br>
      <span style="color:#333;font-size:13px;">
        Fill in what food is left over. The app tells you if it is safe to donate,
        finds the nearest shelter, and writes a WhatsApp message you can send in one tap.
      </span>
    </td>
  </tr>
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;font-size:20px;">🔮</td>
    <td style="padding:10px 8px;">
      <strong style="color:#1a1a1a;font-size:14px;">Tab 2 - Plan How Much to Cook</strong><br>
      <span style="color:#333;font-size:13px;">
        Tell the app today's day, weather, and exam schedule.
        It tells you exactly how many portions to make so you don't over-cook.
      </span>
    </td>
  </tr>
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;font-size:20px;">♻️</td>
    <td style="padding:10px 8px;">
      <strong style="color:#1a1a1a;font-size:14px;">Tab 3 - Plate-Waste Recycler</strong><br>
      <span style="color:#333;font-size:13px;">
        See how much water and carbon is wasted when students leave food on their plates.
        Watch how the kiosk turns those scraps into fertilizer.
      </span>
    </td>
  </tr>
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;font-size:20px;">💬</td>
    <td style="padding:10px 8px;">
      <strong style="color:#1a1a1a;font-size:14px;">Tab 4 - Ask a Food Safety Question</strong><br>
      <span style="color:#333;font-size:13px;">
        Type any question in plain English.
        Get a simple answer backed by official food safety rules.
      </span>
    </td>
  </tr>
  <tr>
    <td style="padding:10px 8px;font-size:20px;">📖</td>
    <td style="padding:10px 8px;">
      <strong style="color:#1a1a1a;font-size:14px;">Tab 5 - Food Safety Rules</strong><br>
      <span style="color:#333;font-size:13px;">
        A simple guide: the 2-hour rule, what food cannot be donated,
        and how donors are protected by law.
      </span>
    </td>
  </tr>
</table>
""",
    },
    # ── Slide 2: 3-step quick start ──────────────────────────────────────────
    {
        "icon": "🚀",
        "title": "Try It in 3 Steps",
        "subtitle": "Takes less than 2 minutes - no setup needed",
        "body": """
<div style="display:flex;flex-direction:column;gap:14px;">
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#2e7d32;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">1</div>
    <div>
      <strong style="font-size:14px;color:#1a1a1a;">Go to Tab 1 - Donate Surplus Food</strong><br>
      <span style="color:#333;font-size:13px;">
        Pick your dining facility and choose <strong style="color:#1a1a1a;">Lunch</strong> as the meal.
        All fields fill in automatically - no typing needed.
      </span>
    </div>
  </div>
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#f9a825;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">2</div>
    <div>
      <strong style="font-size:14px;color:#1a1a1a;">Click "Check if This Food Can Be Donated"</strong><br>
      <span style="color:#333;font-size:13px;">
        You get a clear verdict:
        <span style="color:#2e7d32;font-weight:600;">🟢 Safe to donate</span>,
        <span style="color:#e65100;font-weight:600;">🟡 Donate urgently</span>, or
        <span style="color:#c62828;font-weight:600;">🔴 Cannot donate</span>.
        Plus the nearest shelter and a WhatsApp message, ready to copy and send.
      </span>
    </div>
  </div>
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#1565c0;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">3</div>
    <div>
      <strong style="font-size:14px;color:#1a1a1a;">Switch to Tab 3 - Plate-Waste Recycler</strong><br>
      <span style="color:#333;font-size:13px;">
        Move the <em>Food Left on Plate</em> slider and see the fertilizer output
        and water savings update instantly.
      </span>
    </div>
  </div>
</div>
""",
    },
    # ── Slide 3: Ready ───────────────────────────────────────────────────────
    {
        "icon": "✅",
        "title": "You're All Set!",
        "subtitle": "Anna-Setu is ready to help rescue food and reduce waste",
        "body": """
<p style="font-size:15px;line-height:1.75;color:#1a1a1a;margin:0 0 20px;">
  You know everything you need. Click <strong style="color:#1a1a1a;">"Let's Go!"</strong> below to open the app.<br><br>
  The <strong style="color:#1a1a1a;">Food Safety Rules tab</strong> (Tab 5) is always available
  if you need a quick reference on what food can or cannot be donated.
</p>
<div style="background:#e8f5e9;border-radius:12px;padding:16px 20px;">
  <p style="margin:0;font-size:13px;color:#1a7a3c;font-weight:700;">
    Helpful Tips
  </p>
  <ul style="margin:8px 0 0;padding-left:18px;font-size:13px;color:#1a1a1a;line-height:1.8;">
    <li>Choosing a <strong style="color:#1a1a1a;">meal type</strong> (Breakfast / Lunch / Dinner) fills all fields in automatically.</li>
    <li>The safety preview below the form updates as you type - you don't need to click anything.</li>
    <li>Every result shows the exact rule that applies - tap "Food Safety Rules That Apply" to read it.</li>
  </ul>
</div>
""",
    },
]

if not st.session_state.tutorial_done:
    step = st.session_state.tutorial_step
    slide = SLIDE_CONTENT[step]

    # ── render tutorial as full-screen overlay pop-up ─────────────────────────
    # Build every part as plain Python strings to avoid Streamlit's markdown
    # parser treating injected <div> fragments as fenced code blocks.
    _icon_html = (
        slide['icon']
        if isinstance(slide['icon'], str) and slide['icon'].startswith('<')
        else '<div style="font-size:52px;line-height:1;">' + str(slide['icon']) + '</div>'
    )
    _dot_parts = []
    for i in range(TUTORIAL_STEPS):
        if i == step:
            _dot_parts.append(
                '<span style="display:inline-block;width:12px;height:12px;'
                'border-radius:50%;background:#1a7a3c;margin:0 3px;"></span>'
            )
        else:
            _dot_parts.append(
                '<span style="display:inline-block;width:10px;height:10px;'
                'border-radius:50%;background:#dce8dc;'
                'border:1.5px solid #a8cfb0;margin:0 3px;"></span>'
            )
    _dots_html = "".join(_dot_parts)

    # Assemble the modal card as a normal page element (NOT position:fixed).
    # Using fixed positioning hides Streamlit buttons behind the overlay.
    # The page background CSS already shows the green gradient — the card
    # sits centred on that gradient as a white pop-up panel.
    _modal_html = (
        '<div style="max-width:680px;margin:40px auto 0;'
        'background:#ffffff;border-radius:28px;padding:40px 44px 28px;'
        'box-shadow:0 24px 80px rgba(0,0,0,.35);position:relative;">'
        '<div style="position:absolute;top:0;left:0;right:0;height:7px;'
        'background:linear-gradient(90deg,#0d4a22,#1a7a3c,#2a9d50,#f5a623);'
        'border-radius:28px 28px 0 0;"></div>'
        '<div style="text-align:center;margin-bottom:22px;">'
        + _icon_html
        + '<h2 style="font-size:22px;font-weight:800;margin:12px 0 4px;color:#0d4a22;">'
        + slide['title']
        + '</h2>'
        '<p style="font-size:13px;color:#666;margin:0;">'
        + slide['subtitle']
        + '</p>'
        '</div>'
        '<hr style="border:none;border-top:1px solid #e8f0e8;margin:0 0 20px;">'
        + slide['body']
        + '<div style="display:flex;justify-content:center;gap:6px;margin-top:20px;align-items:center;">'
        + _dots_html
        + '</div>'
        '</div>'
    )
    st.markdown(_modal_html, unsafe_allow_html=True)

    # ── Spacer so buttons don't sit flush against card ─────────────────────
    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

    # ── Navigation buttons — rendered in normal page flow below the card ───
    btn_cols = st.columns([1, 1, 1, 1])

    with btn_cols[0]:
        if st.button("⏭️ Skip Tutorial", use_container_width=True):
            st.session_state.tutorial_done = True
            st.rerun()

    with btn_cols[1]:
        if step > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.tutorial_step -= 1
                st.rerun()

    with btn_cols[2]:
        if step < TUTORIAL_STEPS - 1:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.tutorial_step += 1
                st.rerun()

    with btn_cols[3]:
        if step == TUTORIAL_STEPS - 1:
            if st.button("✅ Let's Go!", type="primary", use_container_width=True):
                st.session_state.tutorial_done = True
                st.rerun()

    st.stop()   # don't render app tabs while tutorial is showing

# =============================================================================
# HERO BANNER
# =============================================================================
st.markdown(f"""
<div class="hero-banner">
  <div style="display:flex;align-items:center;gap:16px;">
    <img src="{LOGO_B64}"
         style="width:62px;height:62px;border-radius:14px;object-fit:cover;
                box-shadow:0 2px 10px rgba(0,0,0,.25);"
         alt="Anna-Setu Logo"/>
    <div>
      <h1 style="color:#ffffff !important;font-size:28px;font-weight:800;margin:0 0 4px;">Anna-Setu</h1>
      <p style="color:#ffffff !important;font-size:14px;opacity:.92;margin:0;">Campus Food Rescue &amp; Bio-Recycling Network</p>
      <span class="hero-tag">🌿 1M1B · IBM SkillsBuild · AICTE · Pankhuri Govila</span>
    </div>
  </div>
  <div class="hero-stats">
    <div class="hero-stat"><span class="num">6+</span><span class="lbl">VERIFIED SHELTERS</span></div>
    <div class="hero-stat"><span class="num">10</span><span class="lbl">FSSAI RULES EMBEDDED</span></div>
    <div class="hero-stat"><span class="num">45 min</span><span class="lbl">MAX DELIVERY TIME</span></div>
    <div class="hero-stat"><span class="num">24h</span><span class="lbl">WASTE → FERTILIZER</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# small "restart tutorial" link
restart_col, _ = st.columns([1, 5])
with restart_col:
    if st.button("📖 Restart Tutorial", help="See the step-by-step guide again", type="secondary"):
        st.session_state.tutorial_done = False
        st.session_state.tutorial_step = 0
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# FOUR TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍛 Donate Surplus Food",
    "🔮 Plan How Much to Cook",
    "♻️ Plate-Waste Recycler",
    "💬 Ask a Question",
    "📖 Food Safety Rules"
])

# =============================================================================
# TAB 1 — DONATE SURPLUS FOOD
# =============================================================================
with tab1:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  <strong>How to use:</strong> Fill in the details of what food is left over below.
  The app tells you if it is safe to donate, finds the nearest shelter,
  and writes a WhatsApp message you can send in one tap.
</div>
""", unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown('<div class="step-pill">📍 Step 1 - Where is the food coming from?</div>', unsafe_allow_html=True)
        with st.container(border=True):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                facility_input = st.selectbox("Dining Facility", DINING_FACILITIES, index=0)
            with c_p2:
                origin_zone_choice = st.selectbox("City Zone (Lucknow)", [o[0] for o in ZONE_OPTIONS], index=0)
            pickup_loc_input = st.text_input(
                "Pickup Point (gate or entrance)",
                value="Gate 2 - Rear Kitchen Entrance"
            )

        st.markdown('<div class="step-pill">🍽️ Step 2 - What food is left over?</div>', unsafe_allow_html=True)
        with st.container(border=True):
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                meal_type_choice = st.selectbox(
                    "Meal Type",
                    ["Lunch", "Dinner", "Breakfast", "Snacks / High Tea", "Other"],
                    index=0
                )
            preset = MEAL_PRESETS.get(meal_type_choice, MEAL_PRESETS["Lunch"])
            with c_m2:
                servings_input = st.number_input(
                    "Number of Servings Left",
                    min_value=1, max_value=2000, value=preset["servings"], step=5
                )
            item_input = st.text_input("Food Items (describe briefly)", value=preset["item"])
            category_choice = st.selectbox(
                "Food Type",
                [o[0] for o in CATEGORY_OPTIONS], index=preset["category_idx"]
            )
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                time_prep_input = st.text_input(
                    "Time Food Was Cooked (HH:MM)", value=preset["time_prep"],
                    help="24-hour format, e.g. 13:30 means 1:30 PM"
                )
            with c_t2:
                time_assess_input = st.text_input(
                    "Current Time (HH:MM)", value=preset["time_assess"],
                    help="What time is it right now?"
                )
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                storage_choice = st.selectbox(
                    "How is the food stored right now?",
                    [o[0] for o in STORAGE_OPTIONS], index=preset["storage_idx"]
                )
            with c_s2:
                temp_input = st.number_input(
                    "Food Temperature (°C) - Optional",
                    min_value=0.0, max_value=100.0, value=0.0, step=0.5,
                    help="Measure with a thermometer. Leave as 0 if you haven't measured."
                )

        # Live safety preview
        st.markdown('<div class="step-pill">🔍 Step 3 - Live Safety Preview</div>', unsafe_allow_html=True)
        category_key   = CATEGORY_DICT[category_choice]
        storage_key    = STORAGE_DICT[storage_choice]
        origin_zone_id = ZONE_DICT[origin_zone_choice]
        temp_c_val     = float(temp_input) if temp_input > 0.0 else None

        sync_data = pipeline.sync_ai_pipeline_configurations(
            origin_zone=origin_zone_id, item=item_input,
            servings=int(servings_input), category_key=category_key,
            time_prepared=time_prep_input, assessment_time=time_assess_input,
            storage_condition=storage_key, measured_temp_celsius=temp_c_val
        )
        with st.container(border=True):
            st.text_area("Food Safety Rule That Applies",
                         value=sync_data["retrieved_safety_rule"], height=65, key="rag_rule_box")
            st.text_area("Nearest Shelter Match",
                         value=sync_data["ai_matched_shelter"], height=65, key="shelter_dest_box")

        run_button = st.button(
            "✅ Check if This Food Can Be Donated",
            type="primary", use_container_width=True
        )

    with col_output:
        st.markdown("### Results")
        if run_button:
            res = pipeline.evaluate_surplus(
                item=item_input, servings=int(servings_input), category_key=category_key,
                time_prepared=time_prep_input, assessment_time=time_assess_input,
                storage_condition=storage_key, origin_zone=origin_zone_id,
                shelter_display_name=sync_data["ai_matched_shelter"],
                pickup_location=pickup_loc_input, facility_place=facility_input,
                meal_type=meal_type_choice, measured_temp_celsius=temp_c_val
            )
            eval_data = res["evaluation"]
            timeline  = eval_data["timeline"]
            status    = eval_data["status"]

            if status == "COMPLIANT_SAFE":
                st.success(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
            elif status == "COMPLIANT_URGENT":
                st.warning(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
            else:
                st.error(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")

            if eval_data.get("temp_summary"):
                st.warning(f"🌡️ **Temperature:** {eval_data['temp_summary']}")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Time Since Cooking",  f"{timeline['elapsed_minutes']} min")
            m2.metric("Delivery Time",       f"{timeline['transit_minutes']} min")
            m3.metric("Total Time Out",      f"{timeline['total_exposure_minutes']} min")
            m4.metric("Safe Until",          f"{timeline['safe_pickup_by']}")

            st.write("---")
            st.markdown("#### 📱 WhatsApp Alert - Ready to Copy and Send")
            st.code(res["broadcast_message"], language="markdown")

            with st.expander("📜 Food Safety Rules That Apply", expanded=True):
                for rule in eval_data.get("retrieved_rules", []):
                    st.markdown(f"**[{rule.get('id')}] {rule.get('clause')}**")
                    st.info(f"\"{rule.get('text')}\"")

            with st.expander("📑 Handover Record (FSSAI Form B)", expanded=False):
                st.code(res["audit_manifest"], language="text")
        else:
            st.markdown("""
<div class="section-card" style="text-align:center;padding:40px 24px;color:#777;">
  <div style="font-size:40px;margin-bottom:12px;">👈</div>
  <strong>Fill in the form on the left</strong><br>
  <span style="font-size:13px;">
    Then click <strong>Check if This Food Can Be Donated</strong>
    to get the verdict, shelter match, and alert message.
  </span>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 2 — PLAN HOW MUCH TO COOK
# =============================================================================
with tab2:
    st.markdown("""
<div class="section-card" style="background:#fffde7;border-left:4px solid #f9a825;">
  <strong>How to use:</strong> Tell the app about today - the day of the week, weather, and exam schedule.
  It predicts how many students will actually eat, so you cook the right amount
  and avoid waste before it starts.
</div>
""", unsafe_allow_html=True)

    col_d1, col_d2 = st.columns([1, 1], gap="large")

    with col_d1:
        st.markdown('<div class="step-pill">📝 Tell Us About Today</div>', unsafe_allow_html=True)
        with st.container(border=True):
            enrolled_input = st.number_input(
                "Total Students Signed Up for Dining",
                min_value=100, max_value=5000, value=1200, step=50
            )
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                meal_input = st.selectbox("Which Meal?", ["Lunch", "Dinner", "Breakfast"])
            with c_m2:
                day_input = st.selectbox(
                    "Day of the Week",
                    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], index=2
                )
            c_c1, c_c2 = st.columns(2)
            with c_c1:
                cal_input = st.selectbox(
                    "What's Happening on Campus?",
                    ["Regular Academic Day","Exam Week (High Attendance)","Weekend / Pre-Holiday","Post-Exam / Festival Eve"]
                )
            with c_c2:
                weather_input = st.selectbox(
                    "Today's Weather",
                    ["Clear & Mild (~24°C)","Very Hot Summer (>38°C)","Monsoon / Heavy Rain","Cold Winter (~12°C)"]
                )
            base_rate_input = st.slider(
                "Usual Attendance Rate (%)", min_value=50, max_value=100, value=85, step=1,
                help="On a normal day, what % of registered students come to eat?"
            )
        btn_demand = st.button("🔮 Show Me How Much to Cook", type="primary", use_container_width=True)

    with col_d2:
        st.markdown("### Today's Cooking Plan")
        if btn_demand:
            d_res = pipeline.predict_meal_demand(
                enrolled_students=int(enrolled_input), meal_type=meal_input,
                day_of_week=day_input, academic_calendar=cal_input,
                weather=weather_input, base_turnout_rate=float(base_rate_input) / 100.0
            )
            st.success(
                f"**Expected Students Today:** {d_res['predicted_turnout_students']} "
                f"({d_res['turnout_rate_pct']:.1f}% attendance)\n\n"
                f"**Cook This Many Portions:** **{d_res['recommended_cooking_target']}** "
                f"(instead of {d_res['traditional_unoptimized_target']} - saves waste!)"
            )
            dm1, dm2, dm3 = st.columns(3)
            dm1.metric("Meals of Waste Prevented", f"{d_res['portions_prevented_from_waste']}")
            dm2.metric("Money Saved",               f"Rs.{d_res['cost_savings_inr']:,.2f}")
            dm3.metric("Water Saved",               f"{d_res['portions_prevented_from_waste'] * 266:,.0f} L")
            st.write("---")
            st.markdown("#### Ingredients to Buy / Prepare (kg)")
            ing = d_res["ingredient_breakdown_kg"]
            df_ing = pd.DataFrame([
                {"Ingredient": "Rice & Grains",  "Without App (kg)": round(ing['rice_or_grains_kg']*1.25,1),   "With App (kg)": ing['rice_or_grains_kg'],   "Saved (kg)": round(ing['rice_or_grains_kg']*0.20,1)},
                {"Ingredient": "Lentils / Dal",  "Without App (kg)": round(ing['dal_or_lentils_kg']*1.25,1),   "With App (kg)": ing['dal_or_lentils_kg'],   "Saved (kg)": round(ing['dal_or_lentils_kg']*0.20,1)},
                {"Ingredient": "Vegetables",      "Without App (kg)": round(ing['vegetables_kg']*1.25,1),        "With App (kg)": ing['vegetables_kg'],        "Saved (kg)": round(ing['vegetables_kg']*0.20,1)},
                {"Ingredient": "Cooking Oil",     "Without App (kg)": round(ing['cooking_oil_kg']*1.25,1),       "With App (kg)": ing['cooking_oil_kg'],       "Saved (kg)": round(ing['cooking_oil_kg']*0.20,1)},
                {"Ingredient": "Dairy / Paneer",  "Without App (kg)": round(ing['dairy_or_paneer_kg']*1.25,1),   "With App (kg)": ing['dairy_or_paneer_kg'],   "Saved (kg)": round(ing['dairy_or_paneer_kg']*0.20,1)},
                {"Ingredient": "Spices & Salt",   "Without App (kg)": round(ing['spices_kg']*1.25,1),            "With App (kg)": ing['spices_kg'],            "Saved (kg)": round(ing['spices_kg']*0.20,1)},
            ])
            st.dataframe(df_ing, use_container_width=True, hide_index=True)
            st.info(f"**Kitchen Instruction:** {d_res['recommendation_summary']}")
        else:
            st.markdown("""
<div class="section-card" style="text-align:center;padding:40px 24px;color:#777;">
  <div style="font-size:40px;margin-bottom:12px;">👈</div>
  <strong>Enter today's details on the left</strong><br>
  <span style="font-size:13px;">Then click <strong>Show Me How Much to Cook</strong>.</span>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 3 — PLATE-WASTE RECYCLER
# =============================================================================
with tab3:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #388e3c;">
  <strong>How to use:</strong> Enter how much food a student left on their plate.
  See the environmental impact and how the kiosk converts those scraps into fertilizer -
  nothing goes to landfill.
</div>
""", unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([1, 1], gap="large")

    with col_b1:
        st.markdown('<div class="step-pill">🍽️ Simulate a Student Returning Their Tray</div>', unsafe_allow_html=True)
        with st.container(border=True):
            sim_diner_name   = st.text_input("Student ID (Optional)", value="STUDENT-2026-88")
            sim_hostel_block = st.selectbox(
                "Hostel Block",
                ["Block A (Boys)", "Block B (Girls)", "Block C (International)", "Day Scholar Dining"]
            )
            sim_waste_grams  = st.slider("Food Left on Plate (grams)", min_value=0, max_value=450, value=175, step=5)
            sim_daily_diners = st.number_input(
                "Total Diners in This Dining Hall Per Day",
                min_value=100, max_value=5000, value=850, step=50
            )

        sim_water_liters = (sim_waste_grams / 1000.0) * 760.0
        sim_co2e_grams   = (sim_waste_grams / 1000.0) * 2300.0

        st.markdown('<div class="step-pill" style="margin-top:14px;">📺 What the Student Sees on the Kiosk Screen</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div style="background:#0d4a22;border-radius:14px;padding:20px 24px;color:white;font-size:14px;line-height:1.75;">
  <div style="font-size:18px;font-weight:700;color:#ffd54f;margin-bottom:10px;">
    Hey! You left <strong>{sim_waste_grams}g</strong> of food on your plate.
  </div>
  💧 <strong>Water wasted:</strong> ~{sim_water_liters:.1f} litres
  <span style="color:#90caf9;font-size:12px;">(water used to grow this food)</span><br>
  🌍 <strong>Carbon footprint:</strong> {sim_co2e_grams:.0f}g CO2 equivalent<br>
  🏆 <strong>Your block ({sim_hostel_block}):</strong> 91% clean plates this week - great job!<br><br>
  <span style="color:#a5d6a7;font-size:13px;">Tip: Take only what you can finish. Second helpings are always available!</span>
</div>
""", unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="step-pill">What Happens to the Plate Waste?</div>', unsafe_allow_html=True)

        cum_daily_waste_kg = (sim_daily_diners * sim_waste_grams) / 1000.0
        compost_yield_kg   = cum_daily_waste_kg * 0.15
        annual_compost_kg  = compost_yield_kg * 240
        methane_avoided_kg = cum_daily_waste_kg * 1.9

        k1, k2 = st.columns(2)
        k1.metric("Plate Waste Per Day",     f"{cum_daily_waste_kg:.1f} kg")
        k2.metric("Fertilizer Made Per Day", f"{compost_yield_kg:.1f} kg",        delta="From this waste")
        k3, k4 = st.columns(2)
        k3.metric("Fertilizer Per Year",     f"{annual_compost_kg:,.0f} kg",      delta="For campus gardens")
        k4.metric("Emissions Avoided",       f"{methane_avoided_kg:.1f} kg CO2e", delta="Zero landfill")

        st.write("---")
        st.markdown("#### How Plate Waste Becomes Fertilizer - 5 Steps")
        steps_html = "".join([
            f'<div style="display:flex;gap:12px;margin-bottom:10px;">'
            f'<div style="background:#2e7d32;color:white;border-radius:50%;width:26px;height:26px;'
            f'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;flex-shrink:0;">{n}</div>'
            f'<div style="font-size:13px;color:#333;">{txt}</div></div>'
            for n, txt in [
                (1, "<strong>Shred:</strong> Scraps are broken into small pieces for fast decomposition."),
                (2, "<strong>Heat:</strong> Temperature rises to 55-65°C, killing all harmful bacteria."),
                (3, "<strong>Airflow:</strong> A fan and carbon filter keep oxygen flowing and remove odours."),
                (4, "<strong>Harvest:</strong> In 12-24 hours, scraps become dry, nutrient-rich fertilizer."),
                (5, "<strong>Zero Landfill:</strong> 100% processed on-site. Nothing sent to city garbage."),
            ]
        ])
        st.markdown(f'<div style="background:white;border-radius:12px;padding:16px 18px;border:1px solid #e0e8e0;">{steps_html}</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 4 — ASK A FOOD SAFETY QUESTION
# =============================================================================
with tab4:
    st.markdown("""
<div class="section-card" style="background:#e8eaf6;border-left:4px solid #3949ab;">
  <strong>How to use:</strong> Type any question about food safety in plain English.
  You get a clear answer backed by official FSSAI 2019 regulations and Lucknow city guidelines.
</div>
""", unsafe_allow_html=True)

    c_q1, c_q2 = st.columns([3, 1])
    with c_q1:
        qa_query = st.text_input(
            "Your Question",
            value="Can I donate cooked paneer curry after 3 hours at room temperature?",
            placeholder="e.g. How long can rice stay out before it becomes unsafe?"
        )
    with c_q2:
        qa_filter = st.selectbox(
            "Filter by Rule Source",
            ["All Rules", "FSSAI Regulations Only", "Lucknow Nagar Nigam Rules Only"]
        )

    if st.button("🔍 Get Answer", type="primary"):
        filter_source = None
        if qa_filter == "FSSAI Regulations Only":
            filter_source = "FSSAI"
        elif qa_filter == "Lucknow Nagar Nigam Rules Only":
            filter_source = "LUCKNOW_NAGAR_NIGAM"

        qa_result = pipeline.ask_regulations(query=qa_query, top_k=3, filter_source=filter_source)
        st.markdown(qa_result.get("synthesized_answer", ""))
        st.write("---")
        with st.expander("📚 Rules Used to Answer This Question", expanded=True):
            for idx, clause in enumerate(qa_result.get("retrieved_clauses", []), 1):
                st.markdown(f"### {idx}. [{clause.get('id')}] {clause.get('title')}")
                st.caption(
                    f"**Source:** {clause.get('source_authority')} | "
                    f"**Rule:** `{clause.get('clause')}` | "
                    f"**Match Score:** `{clause.get('relevance_score', 0):.3f}`"
                )
                st.info(clause.get("text"))
                st.caption(f"Keywords: `{'`, `'.join(clause.get('keywords', []))}`")

# =============================================================================
# TAB 5 — FOOD SAFETY RULES GUIDE
# =============================================================================
with tab5:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  Anna-Setu follows two official sets of rules. Here is what they mean in plain language.
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2, gap="large")

    with col_r1:
        st.markdown("### 🇮🇳 National Food Safety Rules (FSSAI 2019)")
        with st.container(border=True):
            st.markdown("**🌡️ The Danger Zone**")
            st.markdown(
                "Food left between **5°C and 65°C** allows bacteria to grow very quickly. "
                "Always keep food colder than 5°C (fridge) or hotter than 65°C (hot-holding equipment)."
            )
        with st.container(border=True):
            st.markdown("**⏱️ The 2-Hour / 4-Hour Rule**")
            st.markdown("""
| Time Since Cooking | What You Can Do |
|---|---|
| Less than 2 hours | ✅ Safe to donate, chill, or reheat |
| 2 to 4 hours | ⚠️ Safe only if the shelter eats it right away |
| More than 4 hours | 🚫 Not safe for people - must go to compost |
""")
        with st.container(border=True):
            st.markdown("**❌ What CANNOT Be Donated**")
            st.error("Food left on a diner's plate (plate waste / customer leftovers)", icon="🚫")
            st.error("Cut salads, sliced fruits, or open chutneys held at room temperature for more than 2 hours", icon="🚫")
        with st.container(border=True):
            st.markdown("**⚖️ Are Donors Protected by Law?**")
            st.success(
                "Yes. Donors who follow the rules above and donate in good faith are **legally protected** "
                "from being blamed if something goes wrong after the food leaves their hands.", icon="✅"
            )
        with st.container(border=True):
            st.markdown("**📋 Record Keeping**")
            st.info(
                "Every donation must be logged in an official register - food type, quantity, "
                "cooking time, temperature, and signatures. Records kept for 1 year.", icon="📋"
            )

    with col_r2:
        st.markdown("### 🏙️ Lucknow City Council Rules (LNN)")
        with st.container(border=True):
            st.markdown("**🚗 Maximum Delivery Time**")
            st.markdown(
                "Food in transit must reach the shelter within **45 minutes** because of Lucknow traffic "
                "and summer temperatures. Insulated containers are required for longer routes."
            )
        with st.container(border=True):
            st.markdown("**🚮 No Dumping in Garbage Bins**")
            st.error(
                "It is **illegal** to throw commercial food waste into city dustbins or roadside dumps. "
                "On-the-spot fines: **Rs.5,000 to Rs.25,000**.", icon="⚠️"
            )
        with st.container(border=True):
            st.markdown("**♻️ Expired Food Must Be Composted**")
            st.warning(
                "Food that is past its safe window must **never** go into mixed garbage. "
                "It must be separated as green wet waste and sent to campus composting or the "
                "city biomethanation facility.", icon="🌿"
            )
        with st.container(border=True):
            st.markdown("**🏫 Gate Clearance for Food Vehicles**")
            st.info(
                "Campus security must check and log all food rescue vehicles leaving the campus "
                "with an Anna-Setu digital gate pass.", icon="🔖"
            )
