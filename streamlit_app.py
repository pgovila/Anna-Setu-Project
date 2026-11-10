"""
Anna-Setu: Streamlit Interface for Campus Food Rescue & Plate-Waste Bio-Recycling Network
Grounded in FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam Food Service By-Laws.
Covers Dual Tracks: Track A (Software AI & RAG) + Track B (Smart Plate-Waste Interceptor & Bio-Recycler).
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from rag.pipeline import AnnaSetuRAGPipeline

st.set_page_config(
    page_title="Anna-Setu: AI Campus Food Rescue & Bio-Recycling Network",
    page_icon="🍽️",
    layout="wide"
)

# Initialize RAG Pipeline (cached)
@st.cache_resource
def get_pipeline():
    return AnnaSetuRAGPipeline()

pipeline = get_pipeline()

CATEGORY_OPTIONS = [
    ("Cooked Grains, Rice, Dal & Gravies (High Moisture)", "cooked_grains_curry"),
    ("Dry Cooked Staples (Rotis, Chapatis, Dry Sabzi)", "dry_staples_roti"),
    ("Dairy, Paneer Curries, Milk Sweets & Kheer", "dairy_sweets"),
    ("Dry Fried Snacks (Samosas, Cutlets, Pakoras)", "fried_snacks"),
    ("Raw Cut Salads, Sliced Fruits (Prohibited Ambient)", "raw_salads_cut_fruits"),
    ("Plate Waste / Post-Consumer Leftovers (Strictly Prohibited)", "plate_waste")
]
CATEGORY_DICT = {label: key for label, key in CATEGORY_OPTIONS}

STORAGE_OPTIONS = [
    ("Ambient Room Temperature (~25°C - 35°C)", "ambient"),
    ("Active Hot-Holding (Maintained >= 65°C)", "hot_holding"),
    ("Active Refrigerated / Cold-Chain (Maintained <= 5°C)", "refrigerated")
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

SHELTER_LIST = pipeline.get_shelter_names()

st.title("🍽️ Anna-Setu: AI Campus Food Rescue & Plate-Waste Bio-Recycling Network")
st.caption("1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE • Pankhuri Govila (UPES)")

# Five Executive Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍛 Track A: Surplus Rescue & RAG Compliance",
    "♻️ Track B: Plate-Waste Interceptor & Bio-Recycler",
    "🏛️ Regulatory Vector Search (RAG QA)",
    "📊 Project Tracker & Milestones (PankhuriGovila_YIRP)",
    "📖 FSSAI & LNN Compliance Guide & SOPs"
])

# -----------------------------------------------------------------------------
# TAB 1: TRACK A (SURPLUS RESCUE & RAG COMPLIANCE)
# -----------------------------------------------------------------------------
with tab1:
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("🍛 Cafeteria Kitchen Surplus Handoff Logs")
        item_input = st.text_input("Surplus Food Item(s)", value="Vegetable pulao and dal tadka")
        servings_input = st.number_input("Estimated Servings Leftover", min_value=1, max_value=2000, value=45, step=5)
        category_choice = st.selectbox("Food Category (FSSAI Microbial Profile)", [o[0] for o in CATEGORY_OPTIONS])
        
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            time_prep_input = st.text_input("Time Prepared (HH:MM 24h)", value="12:30")
        with c_t2:
            time_assess_input = st.text_input("Current Evaluation Time (HH:MM)", value="14:00")
            
        storage_choice = st.selectbox("Storage & Holding Condition", [o[0] for o in STORAGE_OPTIONS])
        pickup_loc_input = st.text_input("Campus Pickup Location", value="Main Campus Dining Hall, Gate 2")
        
        c_z1, c_z2 = st.columns(2)
        with c_z1:
            origin_zone_choice = st.selectbox("Campus Origin Zone", [o[0] for o in ZONE_OPTIONS])
        with c_z2:
            shelter_choice = st.selectbox("Matched Destination Shelter", SHELTER_LIST)

        run_button = st.button("🔍 Run RAG Verification & Generate Alert", type="primary", use_container_width=True)

    with col_output:
        st.subheader("🛡️ AI Compliance Assessment & RAG Output")
        
        if run_button:
            category_key = CATEGORY_DICT[category_choice]
            storage_key = STORAGE_DICT[storage_choice]
            origin_zone = ZONE_DICT[origin_zone_choice]

            res = pipeline.evaluate_surplus(
                item=item_input,
                servings=int(servings_input),
                category_key=category_key,
                time_prepared=time_prep_input,
                assessment_time=time_assess_input,
                storage_condition=storage_key,
                origin_zone=origin_zone,
                shelter_display_name=shelter_choice,
                pickup_location=pickup_loc_input
            )

            eval_data = res["evaluation"]
            timeline = eval_data["timeline"]
            status = eval_data["status"]

            # Visual Badge
            if status == "COMPLIANT_SAFE":
                st.success(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
            elif status == "COMPLIANT_URGENT":
                st.warning(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
            else:
                st.error(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")

            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Elapsed", f"{timeline['elapsed_minutes']} m")
            m2.metric("Transit Est.", f"{timeline['transit_minutes']} m")
            m3.metric("Total Exposure", f"{timeline['total_exposure_minutes']} m")
            m4.metric("Safe Until", f"{timeline['safe_pickup_by']}")

            st.write("---")
            st.markdown("#### 📱 AI-Drafted Broadcast Message (IBM Granite)")
            st.code(res["broadcast_message"], language="markdown")

            with st.expander("📜 Retrieved FSSAI & LNN Statutory Grounding (RAG)", expanded=True):
                for rule in eval_data.get("retrieved_rules", []):
                    st.markdown(f"**[{rule.get('id')}] {rule.get('clause')}** *(Relevance Score: {rule.get('relevance_score', 0):.2f})*")
                    st.info(f"\"{rule.get('text')}\"")

            with st.expander("📑 Official FSSAI Form B & LNN Gate Pass Manifest", expanded=False):
                st.code(res["audit_manifest"], language="text")

        else:
            st.info("Fill out the Cafeteria Kitchen Surplus Handoff Logs on the left and click **Run RAG Verification** to evaluate safety parameters.")

# -----------------------------------------------------------------------------
# TAB 2: TRACK B (PLATE-WASTE INTERCEPTOR & BIO-RECYCLER SIMULATOR)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("♻️ Track B: Smart Plate-Waste Interceptor & Accelerated Bio-Recycling Station")
    st.caption("Behavioral Plate Nudge Screen • Macerator Shredder • Accelerated Composter ($55°C - 65°C) • Bio-Fertilizer Output")

    col_b1, col_b2 = st.columns([1, 1], gap="large")

    with col_b1:
        st.markdown("### 🍽️ Dish-Clearing Tray Return Simulator")
        st.write("Simulate a diner returning their tray with uneaten food scraps at the cafeteria dish-clearing counter:")
        
        sim_diner_name = st.text_input("Diner / Student ID (Optional)", value="STUDENT-UPES-2026-88")
        sim_hostel_block = st.selectbox("Hostel Block", ["Block A (Boys)", "Block B (Girls)", "Block C (International)", "Day Scholar Dining"])
        sim_waste_grams = st.slider("Plate Waste Leftover (Grams)", min_value=0, max_value=450, value=175, step=5)
        sim_daily_diners = st.number_input("Total Cafeteria Diners per Day", min_value=100, max_value=5000, value=850, step=50)

        # Environmental Footprint calculations
        sim_water_liters = (sim_waste_grams / 1000.0) * 760.0 # ~760L embedded water per kg of grain/pulse meal
        sim_co2e_grams = (sim_waste_grams / 1000.0) * 2300.0  # ~2.3kg CO2e per kg food

        st.write("---")
        st.markdown("### 📺 Live Behavioral Nudge Screen Output")
        st.info(
            f"**⚠️ ATTENTION DINER:** You left **{sim_waste_grams} grams** of uneaten food on your plate!\n\n"
            f"💧 **Embedded Water Wasted:** ~{sim_water_liters:.1f} Liters of freshwater\n\n"
            f"🌍 **Carbon Equivalent:** {sim_co2e_grams:.0f}g $CO_2e$ fugitive emissions\n\n"
            f"🏆 **Hostel Leaderboard:** {sim_hostel_block} is currently averaging 91% Clean Plates this week!\n\n"
            f"*💡 Mindful Eating Nudge: Take only what you finish. You can always take second helpings!*"
        )

    with col_b2:
        st.markdown("### 🧪 On-Site Bio-Recycling Yield & Impact")
        
        # Campus aggregated metrics
        cum_daily_waste_kg = (sim_daily_diners * sim_waste_grams) / 1000.0
        compost_yield_kg = cum_daily_waste_kg * 0.15 # 85% volume/moisture reduction -> 15% dry bio-fertilizer
        annual_compost_kg = compost_yield_kg * 240   # 240 academic days
        methane_avoided_kg = cum_daily_waste_kg * 1.9

        k1, k2 = st.columns(2)
        k1.metric("Daily Campus Plate Waste", f"{cum_daily_waste_kg:.1f} kg / day")
        k2.metric("Organic Bio-Fertilizer Harvested", f"{compost_yield_kg:.1f} kg / day", delta="15% Dry Yield")

        k3, k4 = st.columns(2)
        k3.metric("Annual Bio-Fertilizer Yield", f"{annual_compost_kg:.0f} kg / year", delta="Campus Landscaping")
        k4.metric("Landfill Methane Avoided", f"{methane_avoided_kg:.1f} kg CO2e / day", delta="100% On-Site")

        st.write("---")
        st.markdown("#### 🔄 How the Recyclable Product is Created (The Closed Loop):")
        st.markdown(r"""
        1. **Pre-Processing Shredder:** Scraped plate waste is shredded to 3–5 mm particles, maximizing microbial surface contact.
        2. **Thermophilic Stage ($55^\circ\text{C} - 65^\circ\text{C}$):** PTC ceramic heating element accelerates decomposition and sterilizes pathogens (*Salmonella*, *E. coli*).
        3. **Aerobic Aeration:** Brushless fan + activated carbon filter continuously supplies oxygen, eliminating foul odors.
        4. **Recyclable Output:** In 12–24 hours, the scraps become a **dark, nutrient-rich, pathogen-free organic bio-fertilizer**.
        5. **Zero Municipal Burden:** Lucknow Nagar Nigam trucks carry **0 kg** of rotting wet waste from this mess, saving city transport fuel and avoiding dump fines!
        """)

# -----------------------------------------------------------------------------
# TAB 3: REGULATORY VECTOR SEARCH (RAG QA)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("🏛️ Interactive Regulatory Knowledge Base Explorer (RAG Search)")
    st.write("Query statutory provisions from the Food Safety and Standards Authority of India (FSSAI) and Lucknow Nagar Nigam (LNN) Municipal By-Laws.")
    
    query = st.text_input(
        "Enter statutory keyword or question:",
        value="What is the ambient holding time limit for cooked dal and rice under FSSAI?"
    )
    if st.button("Search Knowledge Base"):
        results = pipeline.query_regulations(query, top_k=4)
        if not results:
            st.warning("No direct matches found.")
        else:
            for r in results:
                st.markdown(f"### [{r.get('id')}] {r.get('title')}")
                st.caption(f"**Authority:** {r.get('source_authority')} | **Clause:** {r.get('clause')} | **Score:** {r.get('relevance_score', 0):.3f}")
                st.write(r.get("text"))
                st.write(f"*Keywords:* `{'`, `'.join(r.get('keywords', []))}`")
                st.write("---")

# -----------------------------------------------------------------------------
# TAB 4: PROJECT TRACKER & MILESTONES (PankhuriGovila_YIRP)
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📊 1M1B Project Tracker & Mentorship Sharing Register")
    st.caption("Google Sheet Name: **PankhuriGovila_YIRP** • Mentor: **Paramjeet Sir (paramjeet@onemoneb.org)**")

    t_m1, t_m2, t_m3 = st.columns(3)
    t_m1.info("**Milestone 1 Gate:** End-Nov 2026\n\nPrototypes (Track A & B) + Campus Approvals")
    t_m2.info("**Milestone 2 Gate:** End-Dec 2026\n\nLive 2-Wk Campus Pilot + Final Impact Handover")
    t_m3.info("**Intern Details:** Pankhuri Govila\n\nUniversity of Petroleum & Energy Studies (UPES)")

    st.write("---")
    st.markdown("#### 📋 Activity Tracker Logbook (WBS Tasks & 1M1B Support Column)")
    
    # Load and display tracker CSV
    try:
        df_tracker = pd.read_csv("PankhuriGovila_YIRP_Project_Tracker.csv")
        st.dataframe(df_tracker, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not load CSV: {e}")

    st.write("---")
    st.markdown("#### 📁 Downloadable Project Artifacts:")
    d_c1, d_c2, d_c3 = st.columns(3)
    with d_c1:
        with open("PankhuriGovila_YIRP_Project_Tracker.xlsx", "rb") as f:
            st.download_button("📥 Download Excel Tracker (.xlsx)", f, "PankhuriGovila_YIRP_Project_Tracker.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with d_c2:
        with open("Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf", "rb") as f:
            st.download_button("📥 Download Official 5-Page PDF", f, "Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf", "application/pdf")
    with d_c3:
        with open("PankhuriGovila_YIRP_Project_Tracker.csv", "rb") as f:
            st.download_button("📥 Download CSV (.csv)", f, "PankhuriGovila_YIRP_Project_Tracker.csv", "text/csv")

# -----------------------------------------------------------------------------
# TAB 5: STATUTORY GUIDELINES & SOPS
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("📚 Statutory Food Regulations & Municipal Sanitation By-Laws")
    st.markdown(r"""
    ### 1. FSSAI Surplus Food Regulations (2019)
    - **Danger Zone:** 5°C to 65°C (41°F to 149°F). Bacteria multiply exponentially within this range.
    - **The 2-Hour / 4-Hour Rule (Reg 4(2)):**
      - **0 - 2 Hours:** Safe to redistribute, chill down to $\le 5^\circ\text{C}$, or reheat to $\ge 74^\circ\text{C}$.
      - **2 - 4 Hours:** Safe to distribute for immediate consumption only.
      - **> 4 Hours:** **UNSAFE.** Condemned from human consumption due to heat-stable enterotoxins.
    - **Active Temperature Controls (Reg 4(3)):** Hot holding maintained continuously at $\ge 65^\circ\text{C}$; cold holding $\le 5^\circ\text{C}$.
    - **Good Samaritan Immunity (Reg 4(5) & Sec 7):** Donors acting in good faith who comply with hygienic and thermal standards are legally indemnified against civil or criminal liability.
    - **Audit Log (Reg 7):** Mandatory **Form B Surplus Handover Register** kept for 1 year for Food Safety Officer audits.

    ### 2. Lucknow Nagar Nigam (LNN) Municipal Guidelines
    - **Corridor Transit Ceiling (Sec 14):** Maximum **45 minutes** transit across Lucknow traffic corridors (Hazratganj, Polytechnic, Charbagh) to prevent heat-spoilage in summer ($>38^\circ\text{C}$). Insulated thermal cambros required for $>45$ mins.
    - **Dumping Ban & Penalties (Sec 10):** Illegal to discard commercial food waste into municipal dustbins (*dhalavs*); spot fines **₹5,000 to ₹25,000**.
    - **Zero-Landfill Mandate (Sec 18):** Non-compliant surplus food **must NEVER** be dumped in municipal garbage bins. It must be diverted to campus aerobic composting or LNN Kanha Upvan / Mohanlalganj biomethanation facilities.
    - **Gate Clearance (Sec 21):** Campus security must verify and timestamp all outgoing food rescue vehicles with an Anna-Setu Digital Gate Pass.
    """)
