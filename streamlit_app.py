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
    "Breakfast": {
        "time_prep": "08:00",
        "time_assess": "09:30",
        "item": "Vegetable Poha, Idli Sambhar & Boiled Eggs",
        "servings": 35,
        "category_idx": 0,
        "storage_idx": 0
    },
    "Lunch": {
        "time_prep": "12:30",
        "time_assess": "14:00",
        "item": "Vegetable Pulao, Dal Tadka & Chapati",
        "servings": 45,
        "category_idx": 0,
        "storage_idx": 0
    },
    "Snacks / High Tea": {
        "time_prep": "16:30",
        "time_assess": "17:30",
        "item": "Vegetable Cutlets, Samosas & Tea Cake",
        "servings": 30,
        "category_idx": 3,
        "storage_idx": 0
    },
    "Dinner": {
        "time_prep": "20:00",
        "time_assess": "21:30",
        "item": "Paneer Butter Masala, Dal Makhani & Rotis",
        "servings": 50,
        "category_idx": 2,
        "storage_idx": 0
    },
    "Other": {
        "time_prep": "11:00",
        "time_assess": "12:30",
        "item": "Mixed Institutional Buffet Catering Spread",
        "servings": 60,
        "category_idx": 0,
        "storage_idx": 0
    }
}

SHELTER_LIST = ["Auto-Match Closest Verified Shelter (Recommended)"] + pipeline.get_shelter_names()

st.title("🍽️ Anna-Setu: AI Campus Food Rescue & Plate-Waste Bio-Recycling Network")
st.caption("1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE • Pankhuri Govila")

# Five Executive Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍛 Track A: Predictive Demand & Surplus RAG",
    "♻️ Track B: Plate-Waste Interceptor & Bio-Recycler",
    "💬 Conversational RAG Regulatory Assistant",
    "📊 Project Tracker & Milestones (PankhuriGovila_YIRP)",
    "📖 FSSAI & LNN Compliance Guide & SOPs"
])

# -----------------------------------------------------------------------------
# TAB 1: TRACK A (MODULE 1 DEMAND ADVISOR + MODULE 2 SURPLUS RAG COMPLIANCE)
# -----------------------------------------------------------------------------
with tab1:
    t1_sub1, t1_sub2 = st.tabs([
        "📋 Module 2: Surplus Rescue & RAG Compliance",
        "🔮 Module 1: AI Dining Demand Advisor"
    ])

    # SUBTAB 1: SURPLUS RESCUE COMPLIANCE EVALUATION
    with t1_sub1:
        col_input, col_output = st.columns([1, 1], gap="large")

        with col_input:
            st.subheader("🍛 Cafeteria Service Handoff Logs")

            # STEP 1: PLACE & LOCATION (ENTERED FIRST!)
            st.markdown("#### 📍 Step 1: Campus Dining Facility & Location (Place Details)")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                facility_input = st.selectbox("Dining Facility / Place Name", DINING_FACILITIES, index=0)
            with c_p2:
                origin_zone_choice = st.selectbox("Campus Origin Zone (Lucknow)", [o[0] for o in ZONE_OPTIONS], index=0)

            pickup_loc_input = st.text_input(
                "Specific Pickup Bay / Dispatch Gate Location",
                value="Gate 2 Service Loading Bay (Rear Kitchen Entrance)"
            )

            # STEP 2: MEAL SERVICE & FOOD DETAILS (ENTERED SECOND!)
            st.markdown("#### 🍽️ Step 2: Meal Service & Surplus Food Details")
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                meal_type_choice = st.selectbox(
                    "Meal Service Type",
                    ["Lunch", "Dinner", "Breakfast", "Snacks / High Tea", "Other"],
                    index=0
                )
            preset = MEAL_PRESETS.get(meal_type_choice, MEAL_PRESETS["Lunch"])

            with c_m2:
                servings_input = st.number_input(
                    "Estimated Servings Leftover",
                    min_value=1,
                    max_value=2000,
                    value=preset["servings"],
                    step=5
                )

            item_input = st.text_input("Surplus Food Item(s)", value=preset["item"])
            category_choice = st.selectbox(
                "Food Category (FSSAI Microbial Profile)",
                [o[0] for o in CATEGORY_OPTIONS],
                index=preset["category_idx"]
            )

            c_t1, c_t2 = st.columns(2)
            with c_t1:
                time_prep_input = st.text_input("Time Prepared (HH:MM 24h)", value=preset["time_prep"])
            with c_t2:
                time_assess_input = st.text_input("Current Evaluation Time (HH:MM)", value=preset["time_assess"])

            c_s1, c_s2 = st.columns(2)
            with c_s1:
                storage_choice = st.selectbox(
                    "Storage & Holding Condition",
                    [o[0] for o in STORAGE_OPTIONS],
                    index=preset["storage_idx"]
                )
            with c_s2:
                temp_input = st.number_input(
                    "Measured Surface Temp (°C) [Optional]",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.5,
                    help="Leave 0 if unmeasured; entering temp enables FSSAI Danger Zone verification."
                )

            # STEP 3: SIMULATED AI PIPELINE CONFIGURATIONS (MATCHING SCREENSHOT)
            st.write("---")
            st.markdown("### 🧠 Simulated AI Pipeline Configurations")
            st.caption("Fields automatically synchronized and populated from the RAG Pipeline and Shelter Directory:")

            category_key = CATEGORY_DICT[category_choice]
            storage_key = STORAGE_DICT[storage_choice]
            origin_zone_id = ZONE_DICT[origin_zone_choice]
            temp_c_val = float(temp_input) if temp_input > 0.0 else None

            # Dynamically sync configurations
            sync_data = pipeline.sync_ai_pipeline_configurations(
                origin_zone=origin_zone_id,
                item=item_input,
                servings=int(servings_input),
                category_key=category_key,
                time_prepared=time_prep_input,
                assessment_time=time_assess_input,
                storage_condition=storage_key,
                measured_temp_celsius=temp_c_val
            )

            # Pill 1: Retrieved Safety Compliance Rule (RAG)
            st.text_area(
                "Retrieved Safety Compliance Rule (RAG)",
                value=sync_data["retrieved_safety_rule"],
                height=70,
                key="rag_rule_box"
            )

            # Pill 2: AI Matched Shelter Destination
            st.text_area(
                "AI Matched Shelter Destination",
                value=sync_data["ai_matched_shelter"],
                height=70,
                key="shelter_dest_box"
            )

            run_button = st.button("Execute IBM Granite Notification Compiler", type="primary", use_container_width=True)

        with col_output:
            st.subheader("✅ Generated Output (WhatsApp / SMS Ready Format)")

            if run_button:
                res = pipeline.evaluate_surplus(
                    item=item_input,
                    servings=int(servings_input),
                    category_key=category_key,
                    time_prepared=time_prep_input,
                    assessment_time=time_assess_input,
                    storage_condition=storage_key,
                    origin_zone=origin_zone_id,
                    shelter_display_name=sync_data["ai_matched_shelter"],
                    pickup_location=pickup_loc_input,
                    facility_place=facility_input,
                    meal_type=meal_type_choice,
                    measured_temp_celsius=temp_c_val
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

                if eval_data.get("temp_summary"):
                    st.warning(f"🌡️ **Thermal Sensor Ground Truth:** {eval_data['temp_summary']}")

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
                st.info("Verify the place, meal, and surplus parameters on the left. The RAG pipeline automatically populates the compliance rule and matched shelter.")

    # SUBTAB 2: DEMAND ADVISOR
    with t1_sub2:
        st.subheader("📊 Predictive Kitchen Turnout & Procurement Optimizer")
        st.caption("Averts food waste at the source by cutting overproduction buffers from 25% to 5% using calendar and weather analytics.")

        col_d1, col_d2 = st.columns([1, 1], gap="large")

        with col_d1:
            st.markdown("### 🍳 Meal Service Parameters")
            enrolled_input = st.number_input("Enrolled Student Cohort", min_value=100, max_value=5000, value=1200, step=50)
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                meal_input = st.selectbox("Meal Service Forecast", ["Lunch", "Dinner", "Breakfast"])
            with c_m2:
                day_input = st.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=2)

            c_c1, c_c2 = st.columns(2)
            with c_c1:
                cal_input = st.selectbox("Academic Calendar", ["Regular Academic Day", "Exam Week (High Attendance)", "Weekend / Pre-Holiday", "Post-Exam / Festival Eve"])
            with c_c2:
                weather_input = st.selectbox("Weather Forecast", ["Clear Mild (~24°C)", "Extreme Hot Summer (>38°C)", "Monsoon Heavy Rain", "Cold Winter (~12°C)"])

            base_rate_input = st.slider("Historical Baseline Turnout Rate (%)", min_value=50, max_value=100, value=85, step=1)

            btn_demand = st.button("🔮 Calculate Optimized Cooking Quota", type="primary", use_container_width=True)

        with col_d2:
            st.markdown("### 🎯 Kitchen Production Directive")
            if btn_demand:
                d_res = pipeline.predict_meal_demand(
                    enrolled_students=int(enrolled_input),
                    meal_type=meal_input,
                    day_of_week=day_input,
                    academic_calendar=cal_input,
                    weather=weather_input,
                    base_turnout_rate=float(base_rate_input) / 100.0
                )

                st.success(
                    f"**Predicted Turnout:** {d_res['predicted_turnout_students']} students ({d_res['turnout_rate_pct']:.1f}%)\n\n"
                    f"**Recommended Cooking Target:** **{d_res['recommended_cooking_target']} portions** "
                    f"(vs {d_res['traditional_unoptimized_target']} traditional)"
                )

                dm1, dm2, dm3 = st.columns(3)
                dm1.metric("Wasted Meals Prevented", f"{d_res['portions_prevented_from_waste']} meals")
                dm2.metric("Procurement Savings", f"₹{d_res['cost_savings_inr']:,.2f}")
                dm3.metric("Freshwater Saved", f"{d_res['portions_prevented_from_waste'] * 266:,.0f} L")

                st.write("---")
                st.markdown("#### ⚖️ Raw Ingredient Procurement Plan (kg)")
                ing = d_res["ingredient_breakdown_kg"]
                df_ing = pd.DataFrame([
                    {"Raw Ingredient": "Rice & Grains", "Traditional Prep (kg)": round(ing['rice_or_grains_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['rice_or_grains_kg'], "Saved (kg)": round(ing['rice_or_grains_kg'] * 0.20, 1)},
                    {"Raw Ingredient": "Lentils / Dal", "Traditional Prep (kg)": round(ing['dal_or_lentils_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['dal_or_lentils_kg'], "Saved (kg)": round(ing['dal_or_lentils_kg'] * 0.20, 1)},
                    {"Raw Ingredient": "Fresh Vegetables", "Traditional Prep (kg)": round(ing['vegetables_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['vegetables_kg'], "Saved (kg)": round(ing['vegetables_kg'] * 0.20, 1)},
                    {"Raw Ingredient": "Cooking Oil", "Traditional Prep (kg)": round(ing['cooking_oil_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['cooking_oil_kg'], "Saved (kg)": round(ing['cooking_oil_kg'] * 0.20, 1)},
                    {"Raw Ingredient": "Dairy / Paneer", "Traditional Prep (kg)": round(ing['dairy_or_paneer_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['dairy_or_paneer_kg'], "Saved (kg)": round(ing['dairy_or_paneer_kg'] * 0.20, 1)},
                    {"Raw Ingredient": "Spices & Salt", "Traditional Prep (kg)": round(ing['spices_kg'] * 1.25, 1), "Optimized Prep (kg)": ing['spices_kg'], "Saved (kg)": round(ing['spices_kg'] * 0.20, 1)}
                ])
                st.dataframe(df_ing, use_container_width=True, hide_index=True)

                st.info(f"**Chef Directive Summary:** {d_res['recommendation_summary']}")
            else:
                st.info("Adjust the parameters on the left and click **Calculate Optimized Cooking Quota** to view predictive demand analytics.")

# -----------------------------------------------------------------------------
# TAB 2: TRACK B (PLATE-WASTE INTERCEPTOR & BIO-RECYCLER SIMULATOR)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("♻️ Track B: Smart Plate-Waste Interceptor & Accelerated Bio-Recycling Station")
    st.caption("Behavioral Plate Nudge Screen • Macerator Shredder • Accelerated Composter (55°C - 65°C) • Bio-Fertilizer Output")

    col_b1, col_b2 = st.columns([1, 1], gap="large")

    with col_b1:
        st.markdown("### 🍽️ Dish-Clearing Tray Return Simulator")
        st.write("Simulate a diner returning their tray with uneaten food scraps at the cafeteria dish-clearing counter:")

        sim_diner_name = st.text_input("Diner / Student ID (Optional)", value="STUDENT-2026-88")
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
            f"🌍 **Carbon Equivalent:** {sim_co2e_grams:.0f}g CO2e fugitive emissions\n\n"
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
        k3.metric("Annual Bio-Fertilizer Yield", f"{annual_compost_kg:,.0f} kg / year", delta="Campus Landscaping")
        k4.metric("Landfill Methane Avoided", f"{methane_avoided_kg:.1f} kg CO2e / day", delta="100% On-Site")

        st.write("---")
        st.markdown("#### 🔄 How the Recyclable Product is Created (The Closed Loop):")
        st.markdown("""
        1. **Pre-Processing Shredder:** Scraped plate waste is shredded to 3-5 mm particles, maximizing microbial surface contact.
        2. **Thermophilic Stage (55°C - 65°C):** PTC ceramic heating element accelerates decomposition and sterilizes pathogens (*Salmonella*, *E. coli*).
        3. **Aerobic Aeration:** Brushless fan + activated carbon filter continuously supplies oxygen, eliminating foul odors.
        4. **Recyclable Output:** In 12-24 hours, the scraps become a **dark, nutrient-rich, pathogen-free organic bio-fertilizer**.
        5. **Zero Municipal Burden:** Lucknow Nagar Nigam trucks carry **0 kg** of rotting wet waste from this mess, saving city transport fuel and avoiding dump fines!
        """)

# -----------------------------------------------------------------------------
# TAB 3: CONVERSATIONAL RAG REGULATORY ASSISTANT (GENERATIVE LEGAL QA)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("💬 Conversational RAG Regulatory Assistant")
    st.caption("Ask questions about FSSAI Surplus Regulations (2019) and Lucknow Nagar Nigam Municipal By-Laws. Generates structured legal guidance citing authoritative clauses.")

    c_q1, c_q2 = st.columns([3, 1])
    with c_q1:
        qa_query = st.text_input(
            "Enter legal or operational regulatory question:",
            value="Can I donate cooked paneer curry after 3 hours at room temperature?"
        )
    with c_q2:
        qa_filter = st.selectbox(
            "Filter Legal Source",
            ["All Authorities", "FSSAI Regulations Only", "Lucknow Nagar Nigam By-Laws Only"]
        )

    if st.button("⚖️ Synthesize Legal Guidance via RAG", type="primary"):
        filter_source = None
        if qa_filter == "FSSAI Regulations Only":
            filter_source = "FSSAI"
        elif qa_filter == "Lucknow Nagar Nigam By-Laws Only":
            filter_source = "LUCKNOW_NAGAR_NIGAM"

        qa_result = pipeline.ask_regulations(query=qa_query, top_k=3, filter_source=filter_source)

        st.markdown(qa_result.get("synthesized_answer", ""))

        st.write("---")
        with st.expander("📚 Retrieved Source Law Chunks & Similarity Scores", expanded=True):
            for idx, clause in enumerate(qa_result.get("retrieved_clauses", []), 1):
                st.markdown(f"### {idx}. [{clause.get('id')}] {clause.get('title')}")
                st.caption(f"**Authority:** {clause.get('source_authority')} | **Clause:** `{clause.get('clause')}` | **Similarity Score:** `{clause.get('relevance_score', 0):.3f}`")
                st.info(clause.get("text"))
                st.caption(f"Keywords: `{'`, `'.join(clause.get('keywords', []))}`")

# -----------------------------------------------------------------------------
# TAB 4: PROJECT TRACKER & MILESTONES (PankhuriGovila_YIRP)
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📊 1M1B Project Tracker & Mentorship Sharing Register")
    st.caption("Google Sheet Name: **PankhuriGovila_YIRP** • Mentor: **Paramjeet Sir (paramjeet@onemoneb.org)**")

    t_m1, t_m2, t_m3 = st.columns(3)
    t_m1.info("**Milestone 1 Gate:** End-Nov 2026\n\nPrototypes (Track A & B) + Campus Approvals")
    t_m2.info("**Milestone 2 Gate:** End-Dec 2026\n\nLive 2-Wk Campus Pilot + Final Impact Handover")
    t_m3.info("**Intern Details:** Pankhuri Govila\n\n1M1B AI for Sustainability Virtual Internship")

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
            st.download_button("📥 Download Official 3-Page PDF", f, "Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf", "application/pdf")
    with d_c3:
        with open("PankhuriGovila_YIRP_Project_Tracker.csv", "rb") as f:
            st.download_button("📥 Download CSV (.csv)", f, "PankhuriGovila_YIRP_Project_Tracker.csv", "text/csv")

# -----------------------------------------------------------------------------
# TAB 5: STATUTORY GUIDELINES & SOPS
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("📚 Statutory Food Regulations & Municipal Sanitation By-Laws")
    st.markdown("""
    ### 1. FSSAI Surplus Food Regulations (2019)
    - **Danger Zone:** 5°C to 65°C (41°F to 149°F). Bacteria multiply exponentially within this range.
    - **The 2-Hour / 4-Hour Rule (Reg 4(2)):**
      - **0 - 2 Hours:** Safe to redistribute, chill down to <= 5°C, or reheat to >= 74°C.
      - **2 - 4 Hours:** Safe to distribute for immediate consumption only.
      - **> 4 Hours:** **UNSAFE.** Condemned from human consumption due to heat-stable enterotoxins.
    - **Active Temperature Controls (Reg 4(3)):** Hot holding maintained continuously at >= 65°C; cold holding <= 5°C.
    - **Good Samaritan Immunity (Reg 4(5) & Sec 7):** Donors acting in good faith who comply with hygienic and thermal standards are legally indemnified against civil or criminal liability.
    - **Audit Log (Reg 7):** Mandatory **Form B Surplus Handover Register** kept for 1 year for Food Safety Officer audits.

    ### 2. Lucknow Nagar Nigam (LNN) Municipal Guidelines
    - **Corridor Transit Ceiling (Sec 14):** Maximum **45 minutes** transit across Lucknow traffic corridors (Hazratganj, Polytechnic, Charbagh) to prevent heat-spoilage in summer (>38°C). Insulated thermal cambros required for >45 mins.
    - **Dumping Ban & Penalties (Sec 10):** Illegal to discard commercial food waste into municipal dustbins (*dhalavs*); spot fines **₹5,000 to ₹25,000**.
    - **Zero-Landfill Mandate (Sec 18):** Non-compliant surplus food **must NEVER** be dumped in municipal garbage bins. It must be diverted to campus aerobic composting or LNN Kanha Upvan / Mohanlalganj biomethanation facilities.
    - **Gate Clearance (Sec 21):** Campus security must verify and timestamp all outgoing food rescue vehicles with an Anna-Setu Digital Gate Pass.
    """)
