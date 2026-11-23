"""
Anna-Setu: Streamlit Interface for Campus Food Rescue & Plate-Waste Bio-Recycling Network
Grounded in FSSAI Food Safety and Standards (Recovery and Distribution of Surplus Food) Regulations, 2019.
Covers Dual Tracks: Track A (Rule-based safety engine + keyword retriever) + Track B (IoT plate-waste simulator).
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
/* ── Font & base ── */
html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, sans-serif; }

/* ── Force light color-scheme so browser never applies dark-mode UA styles ── */
:root { color-scheme: light !important; }
html { color-scheme: light !important; }

/* ── App background ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stAppViewBlockContainer"] {
    background: radial-gradient(circle at 50% 0%, #ebf7ee 0%, #f4f9f5 55%, #edf6ef 100%) !important;
}

/* ── Streamlit Top-Right Header & Toolbar: transparent, let Streamlit handle icons ── */
[data-testid="stHeader"],
header[data-testid="stHeader"],
.stAppHeader {
    background: transparent !important;
}

/* ── All layout blocks transparent so app bg shows through ── */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stColumn"],
div[data-testid="stForm"],
div[data-testid="stForm"] > div {
    background-color: transparent !important;
}

/* ── Bordered containers - polished white card ── */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div,
[data-testid="stVerticalBlockBorderWrapper"] > div > div,
[data-testid="stVerticalBlockBorderWrapper"] > div > div > div {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1.5px solid #d0ebd6 !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 20px rgba(13,74,34,.06), 0 1px 3px rgba(0,0,0,.02) !important;
    padding: 22px 24px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

/* ── Widget labels dark ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stSlider label, .stTextArea label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong {
    color: #1a1a1a !important;
}

/* ── ELIMINATE ALL BLACK BOXES ACROSS THE ENTIRE APP ── */
/* Force light appearance on every BaseUI/Streamlit input control */
div[data-baseweb],
div[data-baseweb] * {
    color-scheme: light !important;
}
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] [data-testid="stMarkdownContainer"],
div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] div,
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] div,
div[data-testid="stNumberInput"],
div[data-testid="stNumberInput"] div,
div[data-testid="stTextArea"],
div[data-testid="stTextArea"] div {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
div[data-baseweb="select"] > div {
    border: 1.5px solid #a8cfb0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 4px rgba(13,74,34,.06) !important;
    min-height: 42px !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: #1a7a3c !important;
    box-shadow: 0 0 0 3px rgba(26,122,60,.18) !important;
}
div[data-baseweb="select"] svg,
div[data-baseweb="select"] svg path {
    fill: #1a7a3c !important;
    color: #1a7a3c !important;
}

/* ── RESTART TUTORIAL BUTTON: white bg, green text, pill shape ── */
.restart-tutorial-container button,
.restart-tutorial-container button[kind="secondary"],
.restart-tutorial-container button[data-testid="baseButton-secondary"] {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 2px solid #1a7a3c !important;
    color: #0d4a22 !important;
    border-radius: 999px !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 10px rgba(26,122,60,.2) !important;
}
.restart-tutorial-container button p,
.restart-tutorial-container button span,
.restart-tutorial-container button div {
    color: #0d4a22 !important;
    background: transparent !important;
    background-color: transparent !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    opacity: 1 !important;
    visibility: visible !important;
}
.restart-tutorial-container button:hover {
    background-color: #e8f5e9 !important;
    background: #e8f5e9 !important;
    border-color: #0d4a22 !important;
    color: #0d4a22 !important;
}
.restart-tutorial-container button:hover p,
.restart-tutorial-container button:hover span {
    color: #0d4a22 !important;
}

/* Dropdown popover list items */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] div,
div[data-baseweb="menu"],
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] li,
li[role="option"] {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
ul[data-baseweb="menu"] {
    border: 1.5px solid #a8cfb0 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.12) !important;
}
li[role="option"] {
    color: #1a1a1a !important;
    padding: 10px 14px !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #e8f5e9 !important;
    background: #e8f5e9 !important;
    color: #1a7a3c !important;
}
li[role="option"] *,
li[role="option"] p,
li[role="option"] span,
li[role="option"] div {
    color: inherit !important;
    background: transparent !important;
}
li[role="option"]:hover *,
li[role="option"][aria-selected="true"] * {
    color: #1a7a3c !important;
    font-weight: 700 !important;
}

/* ── TEXT INPUTS & TEXTAREA: PLAIN WHITE CONTAINERS ── */
[data-testid="stTextInput"],
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"],
[data-testid="stTextInput"] input,
.stTextInput,
.stTextInput input,
[data-testid="stTextArea"],
[data-testid="stTextArea"] > div,
[data-testid="stTextArea"] div[data-baseweb="textarea"],
[data-testid="stTextArea"] div[data-baseweb="base-input"],
[data-testid="stTextArea"] textarea,
.stTextArea,
.stTextArea textarea {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
.stTextInput input,
.stTextArea textarea {
    border: 1.5px solid #a8cfb0 !important;
    border-radius: 12px !important;
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
    padding: 10px 14px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #1a7a3c !important;
    box-shadow: 0 0 0 3px rgba(26,122,60,.18) !important;
}

/* ── NUMBER INPUT: PLAIN WHITE CONTAINER ── */
[data-testid="stNumberInput"],
[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stNumberInput"] div[data-baseweb="base-input"],
[data-testid="stNumberInput"] input,
.stNumberInput,
.stNumberInput input {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
[data-testid="stNumberInput"] input,
.stNumberInput input {
    border: 1.5px solid #a8cfb0 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
}
[data-testid="stNumberInput"] button,
.stNumberInput button {
    background-color: #f0f7f2 !important;
    color: #1a7a3c !important;
    border-color: #a8cfb0 !important;
}

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
.hero-banner h1, .hero-banner h1 *, div.hero-banner h1,
div.hero-banner p, div.hero-banner span { color: #ffffff !important; }

/* ── Student Kiosk Screen (Tab 3): Strictly White & High-Contrast Accents ── */
.kiosk-screen,
.kiosk-screen *,
.kiosk-screen p,
.kiosk-screen span,
.kiosk-screen strong,
.kiosk-screen div,
div.kiosk-screen,
div.kiosk-screen * {
    color: #ffffff !important;
}
.kiosk-screen .kiosk-gold,
div.kiosk-screen .kiosk-gold {
    color: #ffd54f !important;
    font-weight: 800 !important;
}
.kiosk-screen .kiosk-highlight,
div.kiosk-screen .kiosk-highlight {
    color: #a3e635 !important;
    font-weight: 700 !important;
}
.kiosk-screen .kiosk-subtext,
div.kiosk-screen .kiosk-subtext {
    color: #d1e7dd !important;
    font-size: 12.5px !important;
}

/* ── Hero stat chips ── */
.hero-stats { display: flex; gap: 14px; margin-top: 16px; flex-wrap: wrap; }
.hero-stat {
    background: rgba(255,255,255,.18); border-radius: 16px;
    padding: 10px 18px; text-align: center;
    border: 1px solid rgba(255,255,255,.25);
}
.hero-stat .num { font-size: 22px; font-weight: 800; display: block; color: #ffffff !important; }
.hero-stat .lbl { font-size: 10px; opacity: .88; letter-spacing: .05em; color: #ffffff !important; }

/* ── Section card ── */
.section-card {
    background: #ffffff !important;
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 14px;
    border: 1px solid rgba(26,122,60,.18);
    box-shadow: 0 2px 10px rgba(13,74,34,.10);
    color: #1a1a1a !important;
}
.section-card * { color: #1a1a1a !important; }

/* ── Step pills ── */
.step-pill {
    display: inline-block;
    background: linear-gradient(135deg, #13602f 0%, #1a7a3c 50%, #2a9d50 100%);
    color: #ffffff !important;
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 12.5px;
    font-weight: 700;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(26,122,60,.28);
    letter-spacing: 0.2px;
}

/* ── Modern Pill Navigation Tabs with Rounded Active Tab Edges ── */
.stTabs {
    margin-top: 10px !important;
    margin-bottom: 24px !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-radius: 999px !important;
    padding: 6px 8px !important;
    gap: 6px !important;
    border: 1.5px solid #cce5d2 !important;
    box-shadow: 0 4px 16px rgba(13,74,34,.07) !important;
    display: inline-flex !important;
    flex-wrap: wrap !important;
    align-items: center !important;
}
.stTabs [data-baseweb="tab"],
.stTabs [role="tab"],
.stTabs button[role="tab"],
.stTabs div[role="tab"] {
    border-radius: 999px !important;
    -webkit-border-radius: 999px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 8px 18px !important;
    color: #235431 !important;
    background: transparent !important;
    border: none !important;
    outline: none !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}
.stTabs [data-baseweb="tab"]::after,
.stTabs [data-baseweb="tab"]::before,
.stTabs button[role="tab"]::after,
.stTabs button[role="tab"]::before {
    display: none !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Active Tab: Smooth rounded pill with emerald green gradient and bold orange text */
.stTabs [aria-selected="true"],
.stTabs [data-baseweb="tab"][aria-selected="true"],
.stTabs button[role="tab"][aria-selected="true"],
.stTabs div[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #1a7a3c 0%, #2a9d50 100%) !important;
    color: #f5a623 !important;
    font-weight: 800 !important;
    border-radius: 999px !important;
    -webkit-border-radius: 999px !important;
    box-shadow: 0 4px 14px rgba(26,122,60,.35) !important;
    padding: 8px 20px !important;
    border: none !important;
}
.stTabs [aria-selected="false"],
.stTabs [data-baseweb="tab"][aria-selected="false"],
.stTabs button[role="tab"][aria-selected="false"] {
    color: #235431 !important;
    background: transparent !important;
    border-radius: 999px !important;
}
.stTabs [aria-selected="false"]:hover,
.stTabs [data-baseweb="tab"][aria-selected="false"]:hover,
.stTabs button[role="tab"][aria-selected="false"]:hover {
    background: #e8f5e9 !important;
    color: #1a7a3c !important;
    border-radius: 999px !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div,
.stTabs button[role="tab"] p,
.stTabs button[role="tab"] span,
.stTabs button[role="tab"] div {
    color: inherit !important;
    font-size: inherit !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
    color: #f5a623 !important;
    font-weight: 800 !important;
}

/* ── Buttons - secondary / default (Restart Tutorial and all secondary buttons) ── */
div[data-testid="stButton"] button,
div[data-testid="stButton"] button[kind="secondary"],
.stButton button,
.stButton > button,
button[data-testid="baseButton-secondary"],
button[kind="secondary"],
.restart-tutorial-container button {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 2px solid #1a7a3c !important;
    color: #0d4a22 !important;
    border-radius: 999px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    padding: 6px 18px !important;
    box-shadow: 0 2px 8px rgba(26,122,60,.16) !important;
    cursor: pointer !important;
}
/* Explicitly target the inner <p> that Streamlit renders inside every button */
div[data-testid="stButton"] button p,
div[data-testid="stButton"] button span,
div[data-testid="stButton"] button div,
.stButton > button p,
.stButton > button span,
.stButton > button div,
button[data-testid="baseButton-secondary"] p,
button[data-testid="baseButton-secondary"] span,
.restart-tutorial-container button p,
.restart-tutorial-container button span,
.restart-tutorial-container button div {
    color: #0d4a22 !important;
    background: transparent !important;
    background-color: transparent !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    opacity: 1 !important;
    visibility: visible !important;
}
div[data-testid="stButton"] button:hover,
button[data-testid="baseButton-secondary"]:hover,
button[kind="secondary"]:hover,
.stButton > button:hover,
.restart-tutorial-container button:hover {
    background-color: #e8f5e9 !important;
    background: #e8f5e9 !important;
    border-color: #0d4a22 !important;
    color: #0d4a22 !important;
}
div[data-testid="stButton"] button:hover p,
div[data-testid="stButton"] button:hover span,
button[data-testid="baseButton-secondary"]:hover p,
button[data-testid="baseButton-secondary"]:hover span,
.restart-tutorial-container button:hover p,
.restart-tutorial-container button:hover span {
    color: #0d4a22 !important;
}

/* ── Buttons - primary: green gradient, white text ── */
button[data-testid="baseButton-primary"],
button[kind="primary"],
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"],
div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stButton"] button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #1a7a3c, #2a9d50) !important;
    background-color: #1a7a3c !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    box-shadow: 0 3px 12px rgba(26,122,60,.35) !important;
    border-radius: 999px !important;
}
button[data-testid="baseButton-primary"] *,
button[kind="primary"] *,
.stButton > button[kind="primary"] *,
.stButton > button[data-testid="baseButton-primary"] *,
div[data-testid="stButton"] button[kind="primary"] *,
div[data-testid="stButton"] button[data-testid="baseButton-primary"] *,
button[data-testid="baseButton-primary"] p,
button[kind="primary"] p {
    color: #ffffff !important;
    background: transparent !important;
    font-weight: 700 !important;
}
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0d4a22, #1a7a3c) !important;
    background-color: #0d4a22 !important;
    box-shadow: 0 5px 18px rgba(26,122,60,.45) !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 20px !important;
    border: 1px solid rgba(26,122,60,.18) !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 8px rgba(13,74,34,.08) !important;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"] p,
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #1a1a1a !important; }

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border-radius: 16px !important;
    border: 1px solid rgba(26,122,60,.18) !important;
}
[data-testid="stExpander"] summary { color: #1a7a3c !important; font-weight: 600 !important; }

/* ── Alerts ── */
.stAlert { border-radius: 16px !important; }
.stAlert p { color: inherit !important; }

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: #1a7a3c !important;
}

/* ── Tables ── */
.dataframe thead th {
    background: linear-gradient(135deg, #1a7a3c, #2a9d50) !important;
    color: #ffffff !important;
}
.dataframe tbody td { color: #1a1a1a !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: rgba(13,74,34,.92) !important; }
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
    ("Raw Cut Salads, Sliced Fruits - Cannot be donated ⚠️", "raw_salads_cut_fruits"),
    ("Plate Waste / Leftover from Diners' Plates - Strictly Prohibited ⚠️", "plate_waste")
]
CATEGORY_DICT = {label: key for label, key in CATEGORY_OPTIONS}

STORAGE_OPTIONS = [
    ("Kept at Room Temperature (~25°C - 35°C)", "ambient"),
    ("Kept Hot - maintained at 65°C or above", "hot_holding"),
    ("Kept in Fridge / Cold Storage - 5°C or below", "refrigerated")
]
STORAGE_DICT = {label: key for label, key in STORAGE_OPTIONS}

ZONE_OPTIONS = [
    ("Zone 4 - Gomti Nagar, Extension, Indira Nagar", 4),
    ("Zone 1 - Hazratganj, Chowk, Charbagh, Qaiserbagh", 1),
    ("Zone 2 - Aishbagh, Rajajipuram", 2),
    ("Zone 3 - Aliganj, Jankipuram, Vikas Nagar", 3),
    ("Zone 5 - Alambagh, Singar Nagar, Krishna Nagar", 5),
    ("Zone 6 - Hardoi Road, Dubagga, Kakori", 6),
    ("Zone 7 - Chinhat, Faizabad Road, BBD Corridor", 7),
    ("Zone 8 - Sarojini Nagar, Transport Nagar, Airport", 8)
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

# Demo scenarios for the 3 quick-load buttons
DEMO_SCENARIOS = {
    "red": {
        "label": "🔴 Plate Waste (Rejected)",
        "meal": "Lunch",
        "category_idx": 5,   # plate_waste - prohibited
        "storage_idx": 0,
        "time_prep": "12:00", "time_assess": "13:00",
        "item": "Mixed plate scraps from diners' trays",
        "servings": 20,
        "help": "Plate waste - always rejected regardless of time.",
    },
    "yellow": {
        "label": "🟡 Urgent Window (Act Now)",
        "meal": "Lunch",
        "category_idx": 0,   # cooked_grains_curry — urgent when elapsed+transit > 150 min
        "storage_idx": 0,
        "time_prep": "12:00", "time_assess": "14:15",  # 135 min elapsed + 20 transit = 155 > 150 urgent threshold
        "item": "Vegetable Pulao, Dal Tadka",
        "servings": 40,
        "help": "High-moisture food cooked ~2h 15m ago at room temperature - in the urgent dispatch window (elapsed+transit > 2.5h).",
    },
    "green": {
        "label": "🟢 Safe to Donate",
        "meal": "Dinner",
        "category_idx": 1,   # dry_staples_roti
        "storage_idx": 0,
        "time_prep": "19:30", "time_assess": "20:15",
        "item": "Rotis and Dry Sabzi",
        "servings": 60,
        "help": "Dry staples, only 45 min old - well within safe window.",
    },
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
  Anna-Setu helps your team donate that leftover food to nearby shelters -
  <strong>safely and quickly.</strong><br><br>
  Food that cannot be donated is turned into
  <strong>dry soil conditioner</strong> in 24 hours via a PTC bio-recycler - nothing goes to landfill.
</p>
<div style="display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;">
  <div style="background:#e8f5e9;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#2e7d32;">6+</div>
    <div style="font-size:12px;color:#555;">Sample Shelters</div>
  </div>
  <div style="background:#fff8e1;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#f9a825;">10</div>
    <div style="font-size:12px;color:#555;">Safety Rules Built-In</div>
  </div>
  <div style="background:#f3e5f5;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#6a1b9a;">24h</div>
    <div style="font-size:12px;color:#555;">Waste to Soil Conditioner</div>
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
        Watch how the kiosk turns those scraps into dry soil conditioner.
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
        Move the <em>Food Left on Plate</em> slider and see the dry biomass output
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
    # The page background CSS already shows the green gradient - the card
    # sits centred on that gradient as a white pop-up panel.
    _modal_html = (
        '<div style="max-width:680px;margin:40px auto 0;'
        'background:#ffffff;border-radius:28px;padding:40px 44px 24px;'
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

    # ── Navigation buttons: narrow centred columns matching card width ─────
    # Use a 3-col layout with dead margins so buttons stay clustered below card
    _gap, _btn_area, _gap2 = st.columns([1, 4, 1])
    with _btn_area:
        btn_cols = st.columns([2, 1, 1, 2])

        with btn_cols[0]:
            if st.button("⏭️ Skip Tutorial", use_container_width=True):
                st.session_state.tutorial_done = True
                st.rerun()

        with btn_cols[1]:
            if step > 0:
                if st.button("← Prev", use_container_width=True):
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
    <div class="hero-stat"><span class="num">6+</span><span class="lbl">SAMPLE SHELTERS</span></div>
    <div class="hero-stat"><span class="num">10</span><span class="lbl">FSSAI RULES EMBEDDED</span></div>
    <div class="hero-stat"><span class="num">45 min</span><span class="lbl">MAX DELIVERY TIME</span></div>
    <div class="hero-stat"><span class="num">24h</span><span class="lbl">WASTE → SOIL CONDITIONER</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# small "restart tutorial" link
restart_col, helper_col = st.columns([2.2, 3.8])
with restart_col:
    st.markdown('<div class="restart-tutorial-container">', unsafe_allow_html=True)
    if st.button("📖 Restart Interactive Tutorial", key="btn_restart_tutorial", help="See the step-by-step interactive walkthrough again", type="secondary"):
        st.session_state.tutorial_done = False
        st.session_state.tutorial_step = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with helper_col:
    st.markdown("""
<div style="display:flex;align-items:center;height:100%;padding-top:6px;font-size:12.5px;color:#2e5939;">
  <span>💡 <strong>Quick Tip:</strong> Select a meal type below to auto-fill details or query safety rules in real time.</span>
</div>
""", unsafe_allow_html=True)

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
# TAB 1 - DONATE SURPLUS FOOD
# =============================================================================
with tab1:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  <strong>How to use:</strong> Fill in the details of what food is left over, or tap a demo scenario below.
  The app applies FSSAI safety rules, matches the nearest sample shelter, and generates a WhatsApp advance notice.
</div>
""", unsafe_allow_html=True)

    # ── Demo scenario loader ──────────────────────────────────────────────────
    if "demo_key" not in st.session_state:
        st.session_state.demo_key = None

    st.markdown('<div class="step-pill" style="background:linear-gradient(90deg,#555,#777);">🎬 Load a Demo Scenario</div>', unsafe_allow_html=True)
    demo_cols = st.columns(3)
    for idx, (key, sc) in enumerate(DEMO_SCENARIOS.items()):
        with demo_cols[idx]:
            if st.button(sc["label"], key=f"demo_{key}", help=sc["help"], use_container_width=True):
                st.session_state.demo_key = key

    active = DEMO_SCENARIOS.get(st.session_state.demo_key)

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
                _meal_options = ["Lunch", "Dinner", "Breakfast", "Snacks / High Tea", "Other"]
                _meal_default = active["meal"] if active else "Lunch"
                meal_type_choice = st.selectbox(
                    "Meal Type", _meal_options,
                    index=_meal_options.index(_meal_default)
                )
            preset = MEAL_PRESETS.get(meal_type_choice, MEAL_PRESETS["Lunch"])
            _servings_default = active["servings"] if active else preset["servings"]
            with c_m2:
                servings_input = st.number_input(
                    "Number of Servings Left",
                    min_value=1, max_value=2000, value=_servings_default, step=5
                )
            item_input = st.text_input(
                "Food Items (describe briefly)",
                value=active["item"] if active else preset["item"]
            )
            category_choice = st.selectbox(
                "Food Type",
                [o[0] for o in CATEGORY_OPTIONS],
                index=active["category_idx"] if active else preset["category_idx"]
            )
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                time_prep_input = st.text_input(
                    "Time Food Was Cooked (HH:MM)",
                    value=active["time_prep"] if active else preset["time_prep"],
                    help="24-hour format, e.g. 13:30 means 1:30 PM"
                )
            with c_t2:
                time_assess_input = st.text_input(
                    "Current Time (HH:MM)",
                    value=active["time_assess"] if active else preset["time_assess"],
                    help="What time is it right now?"
                )
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                storage_choice = st.selectbox(
                    "How is the food stored right now?",
                    [o[0] for o in STORAGE_OPTIONS],
                    index=active["storage_idx"] if active else preset["storage_idx"]
                )
            with c_s2:
                temp_input = st.number_input(
                    "Food Temperature (°C) - Optional",
                    min_value=0.0, max_value=100.0, value=None, step=0.5,
                    placeholder="Leave blank if not measured",
                    help="Measure with a thermometer. Leave blank if you have not measured."
                )
            # Input validation
            _time_error = None
            _temp_warning = None
            try:
                _tp = datetime.strptime(time_prep_input.strip(), "%H:%M")
                _ta = datetime.strptime(time_assess_input.strip(), "%H:%M")
                if _ta < _tp:
                    _time_error = (
                        "Current time is earlier than cooking time. "
                        "If the food was cooked yesterday, that case is not yet supported - "
                        "enter today's times only."
                    )
            except ValueError:
                _time_error = "Enter times in HH:MM format, e.g. 13:30 for 1:30 PM."
            storage_key_check = STORAGE_DICT[storage_choice]
            if storage_key_check in ("hot_holding", "refrigerated") and (temp_input is None or temp_input == 0.0):
                _temp_warning = (
                    f"You selected {'hot-holding' if storage_key_check == 'hot_holding' else 'refrigerated'} storage. "
                    "Please measure and enter the actual food temperature for an accurate verdict."
                )
            if _time_error:
                st.error(f"⏰ {_time_error}", icon="⚠️")
            if _temp_warning:
                st.warning(f"🌡️ {_temp_warning}", icon="🌡️")

        # Live safety preview
        st.markdown('<div class="step-pill">🔍 Step 3 - Live Safety Preview</div>', unsafe_allow_html=True)
        category_key   = CATEGORY_DICT[category_choice]
        storage_key    = STORAGE_DICT[storage_choice]
        origin_zone_id = ZONE_DICT[origin_zone_choice]
        temp_c_val     = float(temp_input) if (temp_input is not None) else None

        sync_data = pipeline.sync_ai_pipeline_configurations(
            origin_zone=origin_zone_id, item=item_input,
            servings=int(servings_input), category_key=category_key,
            time_prepared=time_prep_input, assessment_time=time_assess_input,
            storage_condition=storage_key, measured_temp_celsius=temp_c_val
        )
        with st.container(border=True):
            _rule_text = sync_data["retrieved_safety_rule"]
            _shelter_text = sync_data["ai_matched_shelter"]
            st.markdown(
                f'<div style="background:#f0f7f2;border:1.5px solid #a8cfb0;border-radius:10px;'
                f'padding:10px 14px;font-size:13px;color:#1a1a1a;margin-bottom:10px;">'
                f'<strong style="color:#1a7a3c;">📜 Safety Rule:</strong> {_rule_text}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div style="background:#f0f7f2;border:1.5px solid #a8cfb0;border-radius:10px;'
                f'padding:10px 14px;font-size:13px;color:#1a1a1a;">'
                f'<strong style="color:#1a7a3c;">🏠 Nearest Shelter (illustrative sample data):</strong> {_shelter_text}</div>',
                unsafe_allow_html=True
            )
            st.caption(
                "⚠️ Preview does not include transit time. "
                "The final verdict (below) adds estimated delivery time and may differ."
            )

        run_button = st.button(
            "✅ Check if This Food Can Be Donated",
            type="primary", use_container_width=True
        )

    with col_output:
        st.markdown("### Results")
        if run_button:
            # Block submission if time inputs are invalid
            if _time_error:
                st.error("Fix the time inputs on the left before running the check.", icon="⚠️")
            else:
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

                # ── Verdict banner (badge already contains emoji — no separate icon) ──
                safe_until = timeline.get("safe_pickup_by", "N/A")
                _remaining = timeline.get("max_allowed_minutes", 240) - timeline.get("total_exposure_minutes", 0)
                if status == "COMPLIANT_SAFE":
                    st.markdown(f"""
<div style="background:#1b5e20;border-radius:16px;padding:20px 24px;margin-bottom:16px;text-align:center;">
  <div style="font-size:22px;font-weight:800;color:#ffffff;">{eval_data['badge']}</div>
  <div style="font-size:14px;color:#a5d6a7;margin-top:6px;">Safe until <strong style="color:#ffffff;">{safe_until}</strong> &nbsp;·&nbsp; <strong style="color:#ffffff;">{_remaining} min remaining</strong></div>
  <div style="font-size:13px;color:#c8e6c9;margin-top:8px;">{eval_data['reason']}</div>
</div>""", unsafe_allow_html=True)
                elif status == "COMPLIANT_URGENT":
                    st.markdown(f"""
<div style="background:#e65100;border-radius:16px;padding:20px 24px;margin-bottom:16px;text-align:center;">
  <div style="font-size:22px;font-weight:800;color:#ffffff;">{eval_data['badge']}</div>
  <div style="font-size:14px;color:#ffe0b2;margin-top:6px;">Act now — safe until <strong style="color:#ffffff;">{safe_until}</strong> &nbsp;·&nbsp; <strong style="color:#ffffff;">{_remaining} min remaining</strong></div>
  <div style="font-size:13px;color:#ffccbc;margin-top:8px;">{eval_data['reason']}</div>
</div>""", unsafe_allow_html=True)
                else:
                    _reject_shelter = "No shelter match — food cannot be donated"
                    st.markdown(f"""
<div style="background:#b71c1c;border-radius:16px;padding:20px 24px;margin-bottom:16px;text-align:center;">
  <div style="font-size:22px;font-weight:800;color:#ffffff;">{eval_data['badge']}</div>
  <div style="font-size:14px;color:#ffcdd2;margin-top:6px;">{_reject_shelter}</div>
  <div style="font-size:13px;color:#ef9a9a;margin-top:8px;">{eval_data['reason']}</div>
</div>""", unsafe_allow_html=True)

                if eval_data.get("temp_summary"):
                    st.warning(f"🌡️ **Temperature:** {eval_data['temp_summary']}")

                # ── Time metrics ───────────────────────────────────────────
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Time Since Cooking",  f"{timeline['elapsed_minutes']} min")
                m2.metric("Delivery Time",       f"{timeline['transit_minutes']} min")
                m3.metric("Total Time Out",      f"{timeline['total_exposure_minutes']} min")
                m4.metric("Remaining Window",    f"{_remaining} min",
                          help=f"Limit {timeline.get('max_allowed_minutes',240)} min − {timeline['total_exposure_minutes']} min used = {_remaining} min left")

                # ── WhatsApp alert in expander ─────────────────────────────
                with st.expander("📱 WhatsApp Advance Notice - tap to copy", expanded=True):
                    st.caption(
                        "Copy this message and send via WhatsApp to give the shelter advance notice "
                        "as required by FSSAI Surplus Food Regulations 2019."
                    )
                    st.code(res["broadcast_message"], language="markdown")

                # ── Rules ──────────────────────────────────────────────────
                with st.expander("📜 Food Safety Rules That Apply", expanded=False):
                    for rule in eval_data.get("retrieved_rules", []):
                        st.markdown(f"**[{rule.get('id')}] {rule.get('clause')}**")
                        st.info(f"\"{rule.get('text')}\"")

                # ── Manifest ───────────────────────────────────────────────
                with st.expander("📑 Handover Record (FSSAI Schedule II fields)", expanded=False):
                    st.markdown(
                        "_Decision-support tool only. Mess manager remains accountable as FBO. "
                        "Add batch number, best-before date and recipient FSSAI registration before filing._"
                    )
                    st.code(res["audit_manifest"], language="text")
        else:
            st.markdown("""
<div class="section-card" style="padding:22px 24px;border:1.5px solid #cce5d2;border-radius:20px;background:#ffffff;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
    <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#1a7a3c,#2a9d50);display:flex;align-items:center;justify-content:center;color:#ffffff;font-size:20px;">🛡️</div>
    <div>
      <h4 style="margin:0;font-size:15px;font-weight:800;color:#0d4a22;">Rule-Based Safety Engine</h4>
      <p style="margin:0;font-size:12px;color:#4a6b51;">FSSAI Surplus Food Regulations 2019 - deterministic rules, keyword-matched clause retrieval</p>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;">
    <div style="background:#f4f9f5;border:1px solid #d8ebd9;border-radius:12px;padding:12px 14px;">
      <div style="font-size:12px;font-weight:700;color:#1a7a3c;margin-bottom:3px;">🟢🟡🔴 Verdict Banner</div>
      <div style="font-size:11px;color:#333;line-height:1.5;">Large coloured banner with "Safe until HH:MM" shown first.</div>
    </div>
    <div style="background:#f4f9f5;border:1px solid #d8ebd9;border-radius:12px;padding:12px 14px;">
      <div style="font-size:12px;font-weight:700;color:#1a7a3c;margin-bottom:3px;">📍 Sample Shelter Match</div>
      <div style="font-size:11px;color:#333;line-height:1.5;">Nearest sample shelter matched by zone. Confirm availability before dispatch.</div>
    </div>
    <div style="background:#f4f9f5;border:1px solid #d8ebd9;border-radius:12px;padding:12px 14px;">
      <div style="font-size:12px;font-weight:700;color:#1a7a3c;margin-bottom:3px;">📱 WhatsApp Advance Notice</div>
      <div style="font-size:11px;color:#333;line-height:1.5;">Ready-to-copy advance notice message per FSSAI requirements.</div>
    </div>
    <div style="background:#f4f9f5;border:1px solid #d8ebd9;border-radius:12px;padding:12px 14px;">
      <div style="font-size:12px;font-weight:700;color:#1a7a3c;margin-bottom:3px;">📑 Schedule II Record</div>
      <div style="font-size:11px;color:#333;line-height:1.5;">Draft FSSAI Schedule II handover record - add batch/best-before before filing.</div>
    </div>
  </div>
  <div style="background:#eaf6ec;border:1.5px dashed #a8cfb0;border-radius:12px;padding:14px;text-align:center;">
    <div style="font-size:22px;margin-bottom:4px;">👈</div>
    <div style="font-weight:700;color:#0d4a22;font-size:13px;margin-bottom:2px;">Fill the form or tap a demo scenario above</div>
    <div style="font-size:11px;color:#55785c;">Then click <strong>"Check if This Food Can Be Donated"</strong></div>
  </div>
  <div style="margin-top:12px;padding:10px 14px;background:#fff8e1;border-radius:10px;border-left:3px solid #f9a825;">
    <div style="font-size:11px;color:#5d4037;line-height:1.6;">
      <strong>About shelter data:</strong> Shelters shown are sample/illustrative data.
      Confirm FSSAI registration, live capacity and acceptance before dispatching food.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 2 - PLAN HOW MUCH TO COOK
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
                help="Set this from your dining hall swipe logs or registration data."
            )
            st.caption("Attendance rate hint: check your canteen swipe-card log for the last 4 weeks.")
            baseline_buffer_pct = st.slider(
                "Your Kitchen's Current Overproduction Buffer (%)",
                min_value=0, max_value=50, value=25, step=5,
                help="How much extra do you currently cook beyond expected attendance? Default 25% is a common campus mess buffer."
            )
        btn_demand = st.button("🔮 Show Me How Much to Cook", type="primary", use_container_width=True)

    with col_d2:
        st.markdown("### Today's Cooking Plan")
        if btn_demand:
            _buf = baseline_buffer_pct / 100.0
            d_res = pipeline.predict_meal_demand(
                enrolled_students=int(enrolled_input), meal_type=meal_input,
                day_of_week=day_input, academic_calendar=cal_input,
                weather=weather_input, base_turnout_rate=float(base_rate_input) / 100.0
            )
            _traditional = int(d_res['predicted_turnout_students'] * (1 + _buf))
            _prevented = max(0, _traditional - d_res['recommended_cooking_target'])
            st.success(
                f"**Expected Students Today:** {d_res['predicted_turnout_students']} "
                f"({d_res['turnout_rate_pct']:.1f}% attendance)\n\n"
                f"**Cook This Many Portions:** **{d_res['recommended_cooking_target']}** "
                f"(instead of {_traditional} using your {baseline_buffer_pct}% buffer)"
            )
            st.caption(
                f"Modelled estimate. 'Without App' baseline = expected students × (1 + {baseline_buffer_pct}%). "
                "Attendance uses fixed day-of-week and weather multipliers, not regression-trained data. "
                "Actual savings depend on your kitchen's real baseline — adjust the buffer slider above."
            )
            dm1, dm2, dm3 = st.columns(3)
            dm1.metric("Meals of Waste Prevented",
                       f"{_prevented}",
                       help=f"vs. your {baseline_buffer_pct}% buffer baseline")
            dm2.metric("Money Saved",               f"Rs.{d_res['cost_savings_inr']:,.2f}")
            dm3.metric("Water Saved",               f"{_prevented * 266:,.0f} L")
            st.caption(
                "Water factor: 266 L per meal = 0.35 kg/meal × 760 L/kg (Mekonnen & Hoekstra 2011). "
                "Track B uses the same 760 L/kg applied to kg of food waste — same factor, different input unit."
            )
            st.info(
                "ℹ️ **Note:** 'Meals prevented' counts overproduction avoided at the cooking stage. "
                "'Meals rescued' (Track A) counts already-cooked surplus redirected to shelters. "
                "These are measured at different points in the food chain — no double counting."
            )
            st.write("---")
            st.markdown("#### Ingredients to Buy / Prepare (kg)")
            ing = d_res["ingredient_breakdown_kg"]
            _buf_factor = 1 + _buf
            # Saved = buffer overhead removed = With App × buf (not buf/buf_factor)
            rows = [
                {"Ingredient": "Rice & Grains",  "Without App (kg)": round(ing['rice_or_grains_kg']*_buf_factor,1),   "With App (kg)": round(ing['rice_or_grains_kg'],1),   "Saved (kg)": round(ing['rice_or_grains_kg']*_buf,1)},
                {"Ingredient": "Lentils / Dal",  "Without App (kg)": round(ing['dal_or_lentils_kg']*_buf_factor,1),   "With App (kg)": round(ing['dal_or_lentils_kg'],1),   "Saved (kg)": round(ing['dal_or_lentils_kg']*_buf,1)},
                {"Ingredient": "Vegetables",      "Without App (kg)": round(ing['vegetables_kg']*_buf_factor,1),        "With App (kg)": round(ing['vegetables_kg'],1),        "Saved (kg)": round(ing['vegetables_kg']*_buf,1)},
                {"Ingredient": "Cooking Oil",     "Without App (kg)": round(ing['cooking_oil_kg']*_buf_factor,1),       "With App (kg)": round(ing['cooking_oil_kg'],1),       "Saved (kg)": round(ing['cooking_oil_kg']*_buf,1)},
                {"Ingredient": "Dairy / Paneer",  "Without App (kg)": round(ing['dairy_or_paneer_kg']*_buf_factor,1),   "With App (kg)": round(ing['dairy_or_paneer_kg'],1),   "Saved (kg)": round(ing['dairy_or_paneer_kg']*_buf,1)},
                {"Ingredient": "Spices & Salt",   "Without App (kg)": round(ing['spices_kg']*_buf_factor,1),            "With App (kg)": round(ing['spices_kg'],1),            "Saved (kg)": round(ing['spices_kg']*_buf,1)},
            ]
            # Totals row — no markdown in dataframe cells
            rows.append({
                "Ingredient": "TOTAL",
                "Without App (kg)": round(sum(r["Without App (kg)"] for r in rows), 1),
                "With App (kg)":    round(sum(r["With App (kg)"]    for r in rows), 1),
                "Saved (kg)":       round(sum(r["Saved (kg)"]       for r in rows), 1),
            })
            df_ing = pd.DataFrame(rows)
            st.dataframe(df_ing, use_container_width=True, hide_index=True)
            st.caption(
                f"'Without App' assumes your {baseline_buffer_pct}% overproduction buffer. "
                "'Saved' = Without App minus With App. Modelled estimates only."
            )
            # Prominent kitchen instruction card
            st.markdown(f"""
<div style="background:#1b5e20;border-radius:14px;padding:18px 22px;margin-top:12px;">
  <div style="font-size:13px;font-weight:700;color:#a5d6a7;margin-bottom:4px;">
    👨‍🍳 KITCHEN INSTRUCTION FOR TODAY
  </div>
  <div style="font-size:17px;font-weight:800;color:#ffffff;line-height:1.5;">
    {d_res['recommendation_summary']}
  </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="section-card" style="padding:26px 24px;border:1.5px solid #f0dfb4;border-radius:20px;box-shadow:0 6px 24px rgba(249,168,37,.06);background:#ffffff;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;">
    <div style="width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#f59e0b,#d97706);display:flex;align-items:center;justify-content:center;color:#ffffff;font-size:22px;box-shadow:0 3px 8px rgba(217,119,6,.3);">🔮</div>
    <div>
      <h4 style="margin:0;font-size:16px;font-weight:800;color:#92400e;">Meal Demand Estimator</h4>
      <p style="margin:0;font-size:12px;color:#78350f;">Attendance multipliers for day, weather &amp; academic calendar - modelled, not regression-trained</p>
    </div>
  </div>
  
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;">
    <div style="background:#fefce8;border:1px solid #fef08a;border-radius:14px;padding:14px 16px;">
      <div style="font-size:13px;font-weight:700;color:#854d0e;margin-bottom:4px;">👥 Attendance Estimate</div>
      <div style="font-size:12px;color:#333;line-height:1.5;">Estimates dining hall turnout using fixed multipliers for exams, weather, and day of week.</div>
    </div>
    <div style="background:#fefce8;border:1px solid #fef08a;border-radius:14px;padding:14px 16px;">
      <div style="font-size:13px;font-weight:700;color:#854d0e;margin-bottom:4px;">🍲 Portions Target</div>
      <div style="font-size:12px;color:#333;line-height:1.5;">Calculates exact portions to cook to prevent overproduction surplus.</div>
    </div>
    <div style="background:#fefce8;border:1px solid #fef08a;border-radius:14px;padding:14px 16px;">
      <div style="font-size:13px;font-weight:700;color:#854d0e;margin-bottom:4px;">💰 Cost &amp; Water Savings</div>
      <div style="font-size:12px;color:#333;line-height:1.5;">Computes rupee budget savings and agricultural water saved.</div>
    </div>
    <div style="background:#fefce8;border:1px solid #fef08a;border-radius:14px;padding:14px 16px;">
      <div style="font-size:13px;font-weight:700;color:#854d0e;margin-bottom:4px;">📊 Ingredient Breakdown</div>
      <div style="font-size:12px;color:#333;line-height:1.5;">Generates precise kg procurement requisitions across 6 food categories.</div>
    </div>
  </div>

  <div style="background:linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);border:1.5px dashed #ca8a04;border-radius:14px;padding:16px;text-align:center;">
    <div style="font-size:24px;margin-bottom:6px;">👈</div>
    <div style="font-weight:700;color:#713f12;font-size:13.5px;margin-bottom:2px;">Enter dining parameters on the left</div>
    <div style="font-size:12px;color:#854d0e;">Click <strong>"Show Me How Much to Cook"</strong> to run predictive analytics.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 3 - PLATE-WASTE RECYCLER
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
<div class="kiosk-screen" style="background:linear-gradient(135deg, #0d4a22 0%, #155724 100%);border-radius:18px;padding:22px 26px;color:#ffffff !important;font-size:14.5px;line-height:1.8;box-shadow:0 6px 20px rgba(13,74,34,.35);border:1.5px solid rgba(255,255,255,.18);">
  <div style="font-size:19px;font-weight:800;color:#ffd54f !important;margin-bottom:12px;">
    Hey! You left <strong class="kiosk-gold" style="color:#ffd54f !important;font-weight:800;">{sim_waste_grams}g</strong> <span style="color:#ffd54f !important;">of food on your plate.</span>
  </div>
  <div style="color:#ffffff !important;margin-bottom:6px;">
    💧 <strong style="color:#ffffff !important;">Water wasted:</strong> <span style="color:#ffffff !important;">~{sim_water_liters:.1f} litres</span>
    <span class="kiosk-subtext" style="color:#d1e7dd !important;font-size:12.5px;">(water used to grow this food)</span>
  </div>
  <div style="color:#ffffff !important;margin-bottom:6px;">
    🌍 <strong style="color:#ffffff !important;">Carbon footprint:</strong> <span style="color:#ffffff !important;">{sim_co2e_grams:.0f}g CO2 equivalent</span>
  </div>
  <div style="color:#ffffff !important;margin-bottom:12px;">
    🏆 <strong style="color:#ffffff !important;">Your block ({sim_hostel_block}):</strong> <span class="kiosk-highlight" style="color:#a3e635 !important;font-weight:700;">[sample message]</span>
  </div>
  <div style="background:rgba(255,255,255,.12);border-radius:10px;padding:12px 16px;color:#ffffff !important;font-size:13px;border-left:3px solid #ffd54f;">
    💡 <strong style="color:#ffffff !important;">Tip:</strong> <span style="color:#ffffff !important;">Take only what you can finish. Second helpings are always available!</span>
  </div>
</div>
""", unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="step-pill">What Happens to the Plate Waste?</div>', unsafe_allow_html=True)

        # Assumptions: 15% dry-weight yield from PTC dehydrator (pre-compost biomass,
        # pending curing and NPK testing before use as soil conditioner);
        # GHG factor 1.9 kg CO2e/kg food waste to landfill (IPCC AR5 Tier 1);
        # water embedded 760 L/kg (avg Indian staple crop, Mekonnen & Hoekstra 2011).
        # All figures are modelled for a single campus - label as estimates.
        cum_daily_waste_kg = (sim_daily_diners * sim_waste_grams) / 1000.0
        compost_yield_kg   = cum_daily_waste_kg * 0.15   # 15% dry-weight yield
        annual_compost_kg  = compost_yield_kg * 240       # 240 operating days/yr
        methane_avoided_kg = cum_daily_waste_kg * 1.9    # IPCC Tier 1 landfill factor

        k1, k2 = st.columns(2)
        k1.metric("Plate Waste Per Day",               f"{cum_daily_waste_kg:.1f} kg")
        k2.metric("Dry Biomass Made Per Day",          f"{compost_yield_kg:.1f} kg",        delta="From this waste")
        k3, k4 = st.columns(2)
        k3.metric("Dry Biomass Per Year (Modelled)",   f"{annual_compost_kg:,.0f} kg",      delta="Pending NPK testing")
        k4.metric("Emissions Avoided (Modelled)",      f"{methane_avoided_kg:.1f} kg CO2e", delta="Zero landfill")

        st.write("---")
        st.caption(
            f"Modelled estimates - {int(sim_daily_diners)}-diner hall, 240 operating days/year. "
            "Output is dry pre-compost biomass from PTC dehydrator; "
            "NPK values and suitability as soil conditioner require curing and lab testing. "
            "GHG factor: 1.9 kg CO2e/kg food waste avoided to landfill (IPCC AR5 Tier 1). "
            "Water factor: 760 L/kg embedded water (Mekonnen & Hoekstra 2011). "
            "Kiosk screen uses 2.3 kg CO2e/kg (lifecycle production estimate, different boundary)."
        )
        st.markdown("#### How Plate Waste Becomes Soil Conditioner - 5 Steps")
        steps_html = "".join([
            f'<div style="display:flex;gap:12px;margin-bottom:10px;">'
            f'<div style="background:#2e7d32;color:white;border-radius:50%;width:26px;height:26px;'
            f'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;flex-shrink:0;">{n}</div>'
            f'<div style="font-size:13px;color:#333;">{txt}</div></div>'
            for n, txt in [
                (1, "<strong>Shred:</strong> Scraps are broken into small pieces for fast decomposition."),
                (2, "<strong>Heat:</strong> Temperature rises to 55-65°C, reducing pathogens significantly."),
                (3, "<strong>Airflow:</strong> A fan and carbon filter keep oxygen flowing and remove odours."),
                (4, "<strong>Harvest:</strong> In 12-24 hours, scraps become dry pre-compost biomass (pending curing and NPK lab testing before use as soil conditioner)."),
                (5, "<strong>Zero Landfill:</strong> 100% processed on-site. Nothing sent to city garbage."),
            ]
        ])
        st.markdown(f'<div style="background:white;border-radius:12px;padding:16px 18px;border:1px solid #e0e8e0;">{steps_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="step-pill" style="margin-top:18px;">📡 Simulate an ESP32 Kiosk Weigh-In</div>', unsafe_allow_html=True)
        st.caption("This shows the JSON payload an ESP32-based kiosk would send to the server when a student places their tray.")
        if st.button("🔌 Generate Sample ESP32 Payload", key="btn_esp32"):
            import json as _json
            _ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            _payload = {
                "kiosk_id": f"KIOSK-{sim_hostel_block.replace(' ', '-').upper()[:8]}",
                "timestamp": _ts,
                "weight_grams": sim_waste_grams,
                "hostel_block": sim_hostel_block,
                "event": "tray_return",
                "metrics": {
                    "water_litres": round(sim_water_liters, 1),
                    "co2e_grams": round(sim_co2e_grams, 0),
                    "dry_biomass_grams": round(sim_waste_grams * 0.15, 1)
                }
            }
            st.code(_json.dumps(_payload, indent=2), language="json")
            st.caption("In a live deployment, this payload would be sent via HTTPS POST to the Anna-Setu API server (api_server.py).")

# =============================================================================
# TAB 4 - ASK A FOOD SAFETY QUESTION
# =============================================================================
with tab4:
    st.markdown("""
<div class="section-card" style="background:#e8eaf6;border-left:4px solid #3949ab;">
  <strong>How to use:</strong> Type any question about food safety in plain English.
  Answers are assembled from keyword-matched clauses in the embedded rule base - not generated by an LLM.
  Safety verdicts always come from the deterministic rule engine, not this Q&amp;A module.
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
# TAB 5 - FOOD SAFETY RULES GUIDE
# =============================================================================
with tab5:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  Anna-Setu draws on two sets of rules. Here is what they mean in plain language.
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2, gap="large")

    with col_r1:
        st.markdown("### 🇮🇳 National Food Safety Rules")
        st.caption("Source: FSSAI Food Safety and Standards (Recovery and Distribution of Surplus Food) Regulations, 2019")
        with st.container(border=True):
            st.markdown("**🌡️ The Danger Zone**")
            st.markdown(
                "Food left between **5°C and 65°C** allows bacteria to grow very quickly. "
                "Always keep food colder than 5°C (fridge) or hotter than 65°C (hot-holding equipment)."
            )
        with st.container(border=True):
            st.markdown("**⏱️ Time Limits (Engineering Estimates)**")
            st.caption("Category time limits in this app are engineering safety estimates derived from FSSAI Regulation 4 principles. Verify against the gazette text for your specific food type.")
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
                "The FSSAI Surplus Food Regulations 2019 aim to protect donors acting in good faith. "
                "Confirm the exact protection with the published gazette text before relying on it legally. "
                "The mess manager remains accountable as the FBO under their own Food Safety Management System.", icon="✅"
            )
        with st.container(border=True):
            st.markdown("**📋 Record Keeping (Schedule II fields)**")
            st.info(
                "Every donation must be logged per Schedule II: donor name, distribution org, "
                "donation date, product, batch number, manufacture date, best-before date, "
                "quantity, food temperature, distribution area, and distribution date. "
                "Also add recipient FSSAI registration. Records kept for 1 year.", icon="📋"
            )

    with col_r2:
        st.markdown("### 🏙️ Lucknow Nagar Nigam (LNN) Guidelines")
        st.caption("Note: LNN clauses below are engineering assumptions based on municipal solid-waste bye-laws and standard food-safety transit practice. Verify exact section numbers and penalty ranges against published LNN gazette text before citing in official filings.")
        with st.container(border=True):
            st.markdown("**🚗 Maximum Delivery Time (Engineering Estimate)**")
            st.markdown(
                "Food in transit should reach the shelter within **45 minutes** given Lucknow "
                "traffic and summer temperatures. Insulated containers required for longer routes. "
                "_Source: engineering estimate based on FSSAI ambient time limits and local conditions._"
            )
        with st.container(border=True):
            st.markdown("**🚮 No Dumping in Garbage Bins**")
            st.error(
                "Municipal solid-waste rules prohibit dumping commercial organic waste in city bins. "
                "Penalty ranges cited are illustrative - confirm current amounts from LNN notifications.", icon="⚠️"
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
