"""
Anna-Setu: Streamlit Interface for Campus Food Rescue & Plate-Waste Bio-Recycling Network
Grounded in FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam Food Service By-Laws.
Covers Dual Tracks: Track A (Software AI & RAG Engine) + Track B (Smart Plate-Waste Interceptor & Bio-Recycler).
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from rag.pipeline import AnnaSetuRAGPipeline

st.set_page_config(
    page_title="Anna-Setu: Campus Food Rescue Network",
    page_icon="🍽️",
    layout="wide"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Font & base ── */
html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, sans-serif; }

/* ── App background ── */
.stApp { background: #f4f7f4; }

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1b5e2f 0%, #2e7d32 55%, #f9a825 100%);
    border-radius: 16px;
    padding: 32px 36px 28px;
    margin-bottom: 8px;
    color: white;
}
.hero-banner h1 { font-size: 28px; font-weight: 800; margin: 0 0 4px; color: white; }
.hero-banner p  { font-size: 14px; opacity: .88; margin: 0; color: white; }
.hero-tag {
    display: inline-block; background: rgba(255,255,255,.18);
    border-radius: 20px; padding: 3px 12px;
    font-size: 11px; font-weight: 600; margin-top: 10px; color: white;
}

/* ── Stat chips in hero ── */
.hero-stats { display: flex; gap: 20px; margin-top: 16px; flex-wrap: wrap; }
.hero-stat  {
    background: rgba(255,255,255,.15); border-radius: 10px;
    padding: 8px 16px; text-align: center;
}
.hero-stat .num  { font-size: 22px; font-weight: 800; display: block; }
.hero-stat .lbl  { font-size: 10px; opacity: .85; letter-spacing: .04em; }

/* ── Section card ── */
.section-card {
    background: white; border-radius: 14px;
    padding: 20px 22px; margin-bottom: 14px;
    border: 1px solid #e0e8e0;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
}

/* ── Step header pills ── */
.step-pill {
    display: inline-block;
    background: #e8f5e9; color: #1b5e2f;
    border-radius: 20px; padding: 4px 14px;
    font-size: 12px; font-weight: 700; margin-bottom: 10px;
}

/* ── Tab bar accent ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px 12px 0 0;
    padding: 4px 8px 0;
    gap: 4px;
    border-bottom: 2px solid #e0e8e0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 600; font-size: 13px;
    padding: 8px 16px;
    color: #555;
}
.stTabs [aria-selected="true"] {
    background: #2e7d32 !important;
    color: white !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(46,125,50,.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1b5e2f, #2e7d32) !important;
    box-shadow: 0 4px 14px rgba(46,125,50,.45) !important;
}

/* ── Secondary button ── */
.stButton > button[kind="secondary"] {
    border: 2px solid #2e7d32 !important;
    color: #2e7d32 !important; border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: white; border-radius: 12px;
    border: 1px solid #e0e8e0; padding: 12px 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

/* ── Tutorial overlay ── */
.tutorial-backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,.55);
    z-index: 999; display: flex;
    align-items: center; justify-content: center;
}
.tutorial-card {
    background: white; border-radius: 20px;
    max-width: 680px; width: 92%;
    padding: 36px 40px 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,.35);
    position: relative;
}

/* ── Progress dots ── */
.dots { display: flex; gap: 8px; justify-content: center; margin: 20px 0 0; }
.dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: #ccc; transition: background .2s;
}
.dot.active { background: #2e7d32; transform: scale(1.2); }

/* ── Expander polish ── */
.streamlit-expanderHeader {
    background: #f1f8f1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Info/success/warning box tweaks ── */
.stAlert { border-radius: 10px !important; }
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
        "icon": "🍽️",
        "title": "Welcome to Anna-Setu!",
        "subtitle": "Your AI-powered campus food rescue and bio-recycling assistant",
        "body": """
<p style="font-size:15px;line-height:1.75;color:#333;margin:0;">
  <strong>Anna-Setu</strong> means <em>"Food Bridge"</em> in Hindi.<br><br>
  Every day, campus dining halls cook more food than is eaten.
  Anna-Setu makes sure that surplus food reaches the people who need it —
  <strong>safely, legally, and in minutes.</strong><br><br>
  It also captures unavoidable plate waste and converts it into
  <strong>clean organic fertilizer</strong> within 24 hours — zero to landfill.
</p>
<div style="display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;">
  <div style="background:#e8f5e9;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#2e7d32;">6+</div>
    <div style="font-size:12px;color:#555;">Verified Shelters</div>
  </div>
  <div style="background:#fff8e1;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#f9a825;">10</div>
    <div style="font-size:12px;color:#555;">Food Safety Rules Embedded</div>
  </div>
  <div style="background:#f3e5f5;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">
    <div style="font-size:22px;font-weight:800;color:#6a1b9a;">24h</div>
    <div style="font-size:12px;color:#555;">Waste → Fertilizer</div>
  </div>
</div>
""",
    },
    # ── Slide 1: Tab guide ───────────────────────────────────────────────────
    {
        "icon": "🗂️",
        "title": "What's Inside the App?",
        "subtitle": "4 tabs — each does one clear job",
        "body": """
<table style="width:100%;border-collapse:collapse;font-size:14px;">
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;width:38px;font-size:20px;">🍛</td>
    <td style="padding:10px 8px;">
      <strong>Tab 1 · Surplus Food Rescue</strong><br>
      <span style="color:#555;font-size:13px;">
        Check if leftover food is safe to donate → get the nearest shelter matched →
        generate a WhatsApp alert. Also predicts how much to cook so waste never starts.
      </span>
    </td>
  </tr>
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;font-size:20px;">♻️</td>
    <td style="padding:10px 8px;">
      <strong>Tab 2 · Plate-Waste Recycler</strong><br>
      <span style="color:#555;font-size:13px;">
        Simulate the smart kiosk at the tray-return counter. See water & carbon impact
        of plate waste and watch it turn into fertilizer.
      </span>
    </td>
  </tr>
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:10px 8px;font-size:20px;">💬</td>
    <td style="padding:10px 8px;">
      <strong>Tab 3 · Ask a Food Safety Question</strong><br>
      <span style="color:#555;font-size:13px;">
        Type a plain-English question and get a rule-backed answer from
        official FSSAI 2019 and Lucknow city guidelines.
      </span>
    </td>
  </tr>
  <tr>
    <td style="padding:10px 8px;font-size:20px;">📖</td>
    <td style="padding:10px 8px;">
      <strong>Tab 4 · Food Safety Rules Guide</strong><br>
      <span style="color:#555;font-size:13px;">
        Plain-language reference — the 2h/4h rule, danger zone temperatures,
        donation restrictions and legal protections explained clearly.
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
        "subtitle": "Takes less than 2 minutes — no setup needed",
        "body": """
<div style="display:flex;flex-direction:column;gap:14px;">
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#2e7d32;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">1</div>
    <div>
      <strong style="font-size:14px;">Open Tab 1 → "Check if Surplus Food Can Be Donated"</strong><br>
      <span style="color:#555;font-size:13px;">
        Select your dining facility and choose <strong>Lunch</strong> as the meal type.
        The form automatically pre-fills with a sample batch — no typing needed.
      </span>
    </div>
  </div>
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#f9a825;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">2</div>
    <div>
      <strong style="font-size:14px;">Click 🚀 "Run Safety Check & Generate Shelter Alert"</strong><br>
      <span style="color:#555;font-size:13px;">
        Anna-Setu shows a <span style="color:green;font-weight:600;">🟢 Safe</span> /
        <span style="color:orange;font-weight:600;">🟡 Urgent</span> /
        <span style="color:red;font-weight:600;">🔴 Rejected</span> verdict,
        the nearest shelter with distance, and a WhatsApp message ready to copy and send.
      </span>
    </div>
  </div>
  <div style="display:flex;align-items:flex-start;gap:14px;">
    <div style="background:#1565c0;color:white;border-radius:50%;width:32px;height:32px;
                display:flex;align-items:center;justify-content:center;
                font-weight:800;font-size:15px;flex-shrink:0;">3</div>
    <div>
      <strong style="font-size:14px;">Switch to Tab 2 · Plate-Waste Recycler</strong><br>
      <span style="color:#555;font-size:13px;">
        Drag the <em>Food Left on Plate</em> slider and watch the daily bio-fertilizer
        yield and methane emissions avoided update in real time.
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
<p style="font-size:15px;line-height:1.75;color:#333;margin:0 0 20px;">
  You now know everything you need to use Anna-Setu effectively.<br><br>
  Click <strong>"Let's Go!"</strong> below to open the app.
  The <strong>📖 Food Safety Rules Guide</strong> (Tab 4) is always there
  if you need a quick reference on what food can and cannot be donated.
</p>
<div style="background:#e8f5e9;border-radius:12px;padding:16px 20px;">
  <p style="margin:0;font-size:13px;color:#2e7d32;font-weight:600;">
    💡 Quick Tips
  </p>
  <ul style="margin:8px 0 0;padding-left:18px;font-size:13px;color:#444;line-height:1.8;">
    <li>The <strong>meal type dropdown</strong> pre-fills all fields automatically — just pick Breakfast / Lunch / Dinner.</li>
    <li>The <strong>AI Safety Check section</strong> updates live as you type — you don't need to press a button to see it.</li>
    <li>All verdicts cite the exact FSSAI regulation they come from — click <em>"Food Safety Rules That Apply"</em> to read them.</li>
  </ul>
</div>
""",
    },
]

if not st.session_state.tutorial_done:
    step = st.session_state.tutorial_step
    slide = SLIDE_CONTENT[step]

    # ── render tutorial as a styled container at the top ──────────────────────
    with st.container():
        st.markdown(f"""
<div style="background:white;border-radius:20px;padding:36px 40px 28px;
            border:2px solid #e0ece0;box-shadow:0 8px 40px rgba(46,125,50,.15);
            max-width:720px;margin:0 auto 24px;">
  <div style="text-align:center;margin-bottom:20px;">
    <div style="font-size:48px;line-height:1;">{slide['icon']}</div>
    <h2 style="font-size:22px;font-weight:800;margin:10px 0 4px;color:#1b3a1f;">{slide['title']}</h2>
    <p style="font-size:13px;color:#777;margin:0;">{slide['subtitle']}</p>
  </div>
  <hr style="border:none;border-top:1px solid #eee;margin:0 0 20px;">
  {slide['body']}
  <div style="display:flex;justify-content:center;gap:8px;margin-top:24px;">
    {"".join(f'<div style="width:10px;height:10px;border-radius:50%;background:{"#2e7d32" if i == step else "#ddd"};display:inline-block;"></div>' for i in range(TUTORIAL_STEPS))}
  </div>
</div>
""", unsafe_allow_html=True)

        # ── navigation buttons ─────────────────────────────────────────────────
        btn_cols = st.columns([1, 1, 1, 1])

        with btn_cols[0]:
            if st.button("⏭️ Skip Tutorial", use_container_width=True):
                st.session_state.tutorial_done = True
                st.rerun()

        with btn_cols[1]:
            prev_disabled = step == 0
            if not prev_disabled:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.tutorial_step -= 1
                    st.rerun()
            else:
                st.markdown("<div style='height:38px'></div>", unsafe_allow_html=True)

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
st.markdown("""
<div class="hero-banner">
  <div style="display:flex;align-items:center;gap:14px;">
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="26" cy="26" r="26" fill="rgba(255,255,255,0.15)"/>
      <path d="M10 34 Q26 12 42 34" stroke="white" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <line x1="8" y1="34" x2="44" y2="34" stroke="white" stroke-width="3" stroke-linecap="round"/>
      <circle cx="17" cy="29" r="3" fill="#f9a825"/>
      <circle cx="26" cy="22" r="3" fill="#f9a825"/>
      <circle cx="35" cy="29" r="3" fill="#f9a825"/>
      <circle cx="13" cy="34" r="5" fill="rgba(255,255,255,0.3)" stroke="white" stroke-width="2"/>
      <circle cx="39" cy="34" r="5" fill="rgba(255,255,255,0.3)" stroke="white" stroke-width="2"/>
    </svg>
    <div>
      <h1>Anna-Setu</h1>
      <p>Campus Food Rescue &amp; Bio-Recycling Network</p>
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
    if st.button("📖 Restart Tutorial", help="See the step-by-step guide again"):
        st.session_state.tutorial_done = False
        st.session_state.tutorial_step = 0
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# FOUR TABS
# =============================================================================
tab1, tab2, tab3, tab5 = st.tabs([
    "🍛 Surplus Food Rescue",
    "♻️ Plate-Waste Recycler",
    "💬 Ask a Food Safety Question",
    "📖 Food Safety Rules Guide"
])

# =============================================================================
# TAB 1 — SURPLUS RESCUE + DEMAND ADVISOR
# =============================================================================
with tab1:
    t1_sub1, t1_sub2 = st.tabs([
        "📋 Check if Surplus Food Can Be Donated",
        "🔮 Predict How Much Food to Cook Today"
    ])

    # ── Subtab 1: Surplus rescue ─────────────────────────────────────────────
    with t1_sub1:
        st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  <strong>What this does:</strong> Fill in the details of your leftover food below.
  Anna-Setu checks whether it is still safe to donate, finds the nearest shelter,
  and drafts a ready-to-send WhatsApp alert for the shelter team.
</div>
""", unsafe_allow_html=True)

        col_input, col_output = st.columns([1, 1], gap="large")

        with col_input:
            st.markdown('<div class="step-pill">📍 Step 1 — Where is the food coming from?</div>', unsafe_allow_html=True)
            with st.container(border=True):
                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    facility_input = st.selectbox("Dining Facility", DINING_FACILITIES, index=0)
                with c_p2:
                    origin_zone_choice = st.selectbox("City Zone (Lucknow)", [o[0] for o in ZONE_OPTIONS], index=0)
                pickup_loc_input = st.text_input(
                    "Pickup Gate / Collection Point",
                    value="Gate 2 Service Loading Bay (Rear Kitchen Entrance)"
                )

            st.markdown('<div class="step-pill">🍽️ Step 2 — What food is left over?</div>', unsafe_allow_html=True)
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
                    "Food Type / Category",
                    [o[0] for o in CATEGORY_OPTIONS], index=preset["category_idx"]
                )
                c_t1, c_t2 = st.columns(2)
                with c_t1:
                    time_prep_input = st.text_input(
                        "Time Food Was Cooked (HH:MM)", value=preset["time_prep"],
                        help="24-hour format, e.g. 13:30 for 1:30 PM"
                    )
                with c_t2:
                    time_assess_input = st.text_input(
                        "Current Time (HH:MM)", value=preset["time_assess"],
                        help="The time right now when you are checking"
                    )
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    storage_choice = st.selectbox(
                        "How is the food stored right now?",
                        [o[0] for o in STORAGE_OPTIONS], index=preset["storage_idx"]
                    )
                with c_s2:
                    temp_input = st.number_input(
                        "Food Temperature (°C) — Optional",
                        min_value=0.0, max_value=100.0, value=0.0, step=0.5,
                        help="Use a food thermometer or IR sensor. Leave as 0 if not measured."
                    )

            # AI sync
            st.markdown('<div class="step-pill">🤖 Step 3 — AI Safety Check (Auto-Updated)</div>', unsafe_allow_html=True)
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
                st.text_area("✅ Applicable Food Safety Rule",
                             value=sync_data["retrieved_safety_rule"], height=65, key="rag_rule_box")
                st.text_area("🏠 Best Matching Shelter Nearby",
                             value=sync_data["ai_matched_shelter"], height=65, key="shelter_dest_box")

            run_button = st.button(
                "🚀 Run Safety Check & Generate Shelter Alert",
                type="primary", use_container_width=True
            )

        with col_output:
            st.markdown("### ✅ Results")
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
                    st.warning(f"🌡️ **Temperature Reading:** {eval_data['temp_summary']}")

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Time Since Cooking",   f"{timeline['elapsed_minutes']} min")
                m2.metric("Delivery Time Est.",   f"{timeline['transit_minutes']} min")
                m3.metric("Total Time Out",        f"{timeline['total_exposure_minutes']} min")
                m4.metric("Safe Until",            f"{timeline['safe_pickup_by']}")

                st.write("---")
                st.markdown("#### 📱 Ready-to-Send Shelter Alert (WhatsApp / SMS)")
                st.code(res["broadcast_message"], language="markdown")

                with st.expander("📜 Food Safety Rules That Apply", expanded=True):
                    for rule in eval_data.get("retrieved_rules", []):
                        st.markdown(f"**[{rule.get('id')}] {rule.get('clause')}**")
                        st.info(f"\"{rule.get('text')}\"")

                with st.expander("📑 Official Handover Record (FSSAI Form B)", expanded=False):
                    st.code(res["audit_manifest"], language="text")
            else:
                st.markdown("""
<div class="section-card" style="text-align:center;padding:40px 24px;color:#777;">
  <div style="font-size:40px;margin-bottom:12px;">👈</div>
  <strong>Fill in the form on the left</strong><br>
  <span style="font-size:13px;">
    Then click <strong>Run Safety Check</strong> to get the donation verdict,
    shelter match, and a ready-to-send alert message.
  </span>
</div>
""", unsafe_allow_html=True)

    # ── Subtab 2: Demand advisor ─────────────────────────────────────────────
    with t1_sub2:
        st.markdown("""
<div class="section-card" style="background:#fffde7;border-left:4px solid #f9a825;">
  <strong>What this does:</strong> Instead of guessing and cooking too much, Anna-Setu predicts
  how many students will actually show up for a meal — based on the day, weather, and exam schedule.
  This prevents food waste before it even happens.
</div>
""", unsafe_allow_html=True)

        col_d1, col_d2 = st.columns([1, 1], gap="large")

        with col_d1:
            st.markdown('<div class="step-pill">📝 Tell Us About Today</div>', unsafe_allow_html=True)
            with st.container(border=True):
                enrolled_input = st.number_input(
                    "Total Students Registered for Dining",
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
                        "Academic Schedule",
                        ["Regular Academic Day","Exam Week (High Attendance)","Weekend / Pre-Holiday","Post-Exam / Festival Eve"]
                    )
                with c_c2:
                    weather_input = st.selectbox(
                        "Today's Weather",
                        ["Clear & Mild (~24°C)","Very Hot Summer (>38°C)","Monsoon / Heavy Rain","Cold Winter (~12°C)"]
                    )
                base_rate_input = st.slider(
                    "Usual Attendance Rate (%)", min_value=50, max_value=100, value=85, step=1,
                    help="On a normal day, what % of registered students eat here?"
                )
            btn_demand = st.button("🔮 Calculate How Much to Cook", type="primary", use_container_width=True)

        with col_d2:
            st.markdown("### 🎯 Today's Cooking Plan")
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
                    f"(instead of {d_res['traditional_unoptimized_target']} — saves waste!)"
                )
                dm1, dm2, dm3 = st.columns(3)
                dm1.metric("Meals Waste Prevented", f"{d_res['portions_prevented_from_waste']}")
                dm2.metric("Cost Saved",             f"₹{d_res['cost_savings_inr']:,.2f}")
                dm3.metric("Water Saved",             f"{d_res['portions_prevented_from_waste'] * 266:,.0f} L")
                st.write("---")
                st.markdown("#### 🛒 Ingredients to Buy / Prepare (kg)")
                ing = d_res["ingredient_breakdown_kg"]
                df_ing = pd.DataFrame([
                    {"Ingredient": "Rice & Grains",  "Old (kg)": round(ing['rice_or_grains_kg']*1.25,1),   "Smart (kg)": ing['rice_or_grains_kg'],   "Saved (kg)": round(ing['rice_or_grains_kg']*0.20,1)},
                    {"Ingredient": "Lentils / Dal",  "Old (kg)": round(ing['dal_or_lentils_kg']*1.25,1),   "Smart (kg)": ing['dal_or_lentils_kg'],   "Saved (kg)": round(ing['dal_or_lentils_kg']*0.20,1)},
                    {"Ingredient": "Vegetables",      "Old (kg)": round(ing['vegetables_kg']*1.25,1),        "Smart (kg)": ing['vegetables_kg'],        "Saved (kg)": round(ing['vegetables_kg']*0.20,1)},
                    {"Ingredient": "Cooking Oil",     "Old (kg)": round(ing['cooking_oil_kg']*1.25,1),       "Smart (kg)": ing['cooking_oil_kg'],       "Saved (kg)": round(ing['cooking_oil_kg']*0.20,1)},
                    {"Ingredient": "Dairy / Paneer",  "Old (kg)": round(ing['dairy_or_paneer_kg']*1.25,1),   "Smart (kg)": ing['dairy_or_paneer_kg'],   "Saved (kg)": round(ing['dairy_or_paneer_kg']*0.20,1)},
                    {"Ingredient": "Spices & Salt",   "Old (kg)": round(ing['spices_kg']*1.25,1),            "Smart (kg)": ing['spices_kg'],            "Saved (kg)": round(ing['spices_kg']*0.20,1)},
                ])
                st.dataframe(df_ing, use_container_width=True, hide_index=True)
                st.info(f"**Chef's Instruction:** {d_res['recommendation_summary']}")
            else:
                st.markdown("""
<div class="section-card" style="text-align:center;padding:40px 24px;color:#777;">
  <div style="font-size:40px;margin-bottom:12px;">👈</div>
  <strong>Enter today's details on the left</strong><br>
  <span style="font-size:13px;">Then click <strong>Calculate How Much to Cook</strong>.</span>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TAB 2 — PLATE-WASTE RECYCLER
# =============================================================================
with tab2:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #388e3c;">
  <strong>Track B — Smart Plate-Waste Recycler:</strong> When students leave food on their plates,
  a smart kiosk at the tray-return counter weighs it, shows the diner their environmental impact,
  and converts all the scraps into clean organic fertilizer within 24 hours — zero to landfill.
</div>
""", unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([1, 1], gap="large")

    with col_b1:
        st.markdown('<div class="step-pill">🍽️ Simulate a Diner Returning Their Tray</div>', unsafe_allow_html=True)
        with st.container(border=True):
            sim_diner_name   = st.text_input("Student / Diner ID (Optional)", value="STUDENT-2026-88")
            sim_hostel_block = st.selectbox(
                "Hostel Block",
                ["Block A (Boys)", "Block B (Girls)", "Block C (International)", "Day Scholar Dining"]
            )
            sim_waste_grams  = st.slider("Food Left on Plate (grams)", min_value=0, max_value=450, value=175, step=5)
            sim_daily_diners = st.number_input(
                "Total Diners Using This Dining Hall per Day",
                min_value=100, max_value=5000, value=850, step=50
            )

        sim_water_liters = (sim_waste_grams / 1000.0) * 760.0
        sim_co2e_grams   = (sim_waste_grams / 1000.0) * 2300.0

        st.markdown('<div class="step-pill" style="margin-top:14px;">📺 Kiosk Screen — What the Diner Sees</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div style="background:#1a1f2e;border-radius:14px;padding:20px 24px;color:white;font-size:14px;line-height:1.75;">
  <div style="font-size:18px;font-weight:700;color:#ffd54f;margin-bottom:10px;">
    ⚠️ Hey! You left <strong>{sim_waste_grams}g</strong> of food on your plate.
  </div>
  💧 <strong>Water wasted:</strong> ~{sim_water_liters:.1f} Litres
  <span style="color:#90caf9;font-size:12px;">(used to grow this food)</span><br>
  🌍 <strong>Carbon footprint:</strong> {sim_co2e_grams:.0f}g CO₂ equivalent<br>
  🏆 <strong>Your block's score:</strong> {sim_hostel_block} is at 91% Clean Plates this week — keep it up!<br><br>
  <span style="color:#a5d6a7;font-size:13px;">💡 Tip: Take only what you can finish. Second helpings are always available!</span>
</div>
""", unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="step-pill">🧪 What Happens to the Plate Waste?</div>', unsafe_allow_html=True)

        cum_daily_waste_kg = (sim_daily_diners * sim_waste_grams) / 1000.0
        compost_yield_kg   = cum_daily_waste_kg * 0.15
        annual_compost_kg  = compost_yield_kg * 240
        methane_avoided_kg = cum_daily_waste_kg * 1.9

        k1, k2 = st.columns(2)
        k1.metric("Total Plate Waste / Day",     f"{cum_daily_waste_kg:.1f} kg")
        k2.metric("Bio-Fertilizer Made / Day",   f"{compost_yield_kg:.1f} kg",        delta="From this waste")
        k3, k4 = st.columns(2)
        k3.metric("Fertilizer Made / Year",      f"{annual_compost_kg:,.0f} kg",      delta="For campus gardens")
        k4.metric("Methane Emissions Avoided",   f"{methane_avoided_kg:.1f} kg CO₂e", delta="Zero landfill")

        st.write("---")
        st.markdown("#### 🔄 How Plate Waste Becomes Fertilizer — 5 Steps")
        steps_html = "".join([
            f'<div style="display:flex;gap:12px;margin-bottom:10px;">'
            f'<div style="background:#2e7d32;color:white;border-radius:50%;width:26px;height:26px;'
            f'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;flex-shrink:0;">{n}</div>'
            f'<div style="font-size:13px;color:#333;">{txt}</div></div>'
            for n, txt in [
                (1, "<strong>Shred:</strong> Food scraps are broken into 3–5 mm pieces for rapid decomposition."),
                (2, "<strong>Heat:</strong> PTC element raises temperature to 55–65°C, killing all pathogens."),
                (3, "<strong>Air Flow:</strong> Brushless fan + carbon filter supplies oxygen, removes odours."),
                (4, "<strong>Harvest:</strong> In 12–24h, scraps become dry, nutrient-rich organic fertilizer."),
                (5, "<strong>Zero Landfill:</strong> 100% processed on-site. Zero to city garbage system."),
            ]
        ])
        st.markdown(f'<div style="background:white;border-radius:12px;padding:16px 18px;border:1px solid #e0e8e0;">{steps_html}</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 3 — ASK A FOOD SAFETY QUESTION
# =============================================================================
with tab3:
    st.markdown("""
<div class="section-card" style="background:#e8eaf6;border-left:4px solid #3949ab;">
  <strong>Ask anything about food safety:</strong> Type a plain-English question and get a clear,
  rule-backed answer drawn from official FSSAI 2019 regulations and Lucknow Nagar Nigam guidelines.
</div>
""", unsafe_allow_html=True)

    c_q1, c_q2 = st.columns([3, 1])
    with c_q1:
        qa_query = st.text_input(
            "Your Question:",
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
        with st.expander("📚 Source Rules Used to Answer This Question", expanded=True):
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
# TAB 4 — FOOD SAFETY RULES GUIDE
# =============================================================================
with tab5:
    st.markdown("""
<div class="section-card" style="background:#f1f8f1;border-left:4px solid #2e7d32;">
  Anna-Setu follows two official sets of rules. Here's what they mean in plain language.
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2, gap="large")

    with col_r1:
        st.markdown("### 🇮🇳 FSSAI Surplus Food Regulations (2019)")
        with st.container(border=True):
            st.markdown("**🌡️ The Danger Zone**")
            st.markdown(
                "Food left between **5°C and 65°C** allows bacteria to grow very quickly. "
                "Always keep food colder than 5°C (fridge) or hotter than 65°C (hot-holding)."
            )
        with st.container(border=True):
            st.markdown("**⏱️ The 2-Hour / 4-Hour Rule (Regulation 4(2))**")
            st.markdown("""
| Time Since Cooking | What You Can Do |
|---|---|
| Less than 2 hours | ✅ Safe to donate, chill, or reheat |
| 2–4 hours | ⚠️ Safe only if shelter eats it immediately |
| More than 4 hours | 🚫 Not safe — must go to compost |
""")
        with st.container(border=True):
            st.markdown("**❌ What CANNOT Be Donated (Regulation 4(4))**")
            st.error("Food left on a diner's plate (plate waste / customer leftovers)", icon="🚫")
            st.error("Cut salads, sliced fruits, or open chutneys held at room temperature > 2 hours", icon="🚫")
        with st.container(border=True):
            st.markdown("**⚖️ Are Donors Protected by Law? (Regulation 4(5) & Section 7)**")
            st.success(
                "Yes. Donors who follow the rules above and donate in good faith are **legally protected** "
                "from being sued if something goes wrong later in the delivery chain.", icon="✅"
            )
        with st.container(border=True):
            st.markdown("**📋 Record Keeping (Regulation 7)**")
            st.info(
                "Every donation must be logged in an **official Form B register** — food type, quantity, "
                "cooking time, temperature, and signatures. Records kept for 1 year.", icon="📋"
            )

    with col_r2:
        st.markdown("### 🏙️ Lucknow Nagar Nigam (City Council) Rules")
        with st.container(border=True):
            st.markdown("**🚗 Maximum Delivery Time (Section 14)**")
            st.markdown(
                "Food in transit must reach the shelter within **45 minutes** due to Lucknow traffic "
                "and summer heat (>38°C). Insulated thermal containers required for longer routes."
            )
        with st.container(border=True):
            st.markdown("**🚮 No Dumping in Garbage Bins (Section 10)**")
            st.error(
                "It is **illegal** to throw commercial food waste into city dustbins or roadside dumps. "
                "Spot fines: **₹5,000 to ₹25,000**.", icon="⚠️"
            )
        with st.container(border=True):
            st.markdown("**♻️ Expired Food Must Be Composted (Section 18)**")
            st.warning(
                "Food past its safe window must **never** go into mixed garbage. "
                "It must be sorted as green wet waste and sent to campus composting or the "
                "city's Kanha Upvan biomethanation facility.", icon="🌿"
            )
        with st.container(border=True):
            st.markdown("**🏫 Gate Clearance for Food Vehicles (Section 21)**")
            st.info(
                "Campus security must verify and timestamp all food rescue vehicles leaving the premises "
                "with an Anna-Setu digital gate pass.", icon="🔖"
            )
