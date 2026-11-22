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

st.title("🍽️ Anna-Setu: Campus Food Rescue & Bio-Recycling Network")
st.caption("1M1B AI for Sustainability Virtual Internship · IBM SkillsBuild & AICTE · Pankhuri Govila")

# Five Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍛 Surplus Food Rescue",
    "♻️ Plate-Waste Recycler",
    "💬 Ask a Food Safety Question",
    "📊 Project Tracker",
    "📖 Food Safety Rules Guide"
])

# =============================================================================
# TAB 1: TRACK A — DEMAND ADVISOR + SURPLUS RESCUE & COMPLIANCE
# =============================================================================
with tab1:
    t1_sub1, t1_sub2 = st.tabs([
        "📋 Check if Surplus Food Can Be Donated",
        "🔮 Predict How Much Food to Cook Today"
    ])

    # -------------------------------------------------------------------------
    # SUBTAB 1: SURPLUS RESCUE & COMPLIANCE CHECK
    # -------------------------------------------------------------------------
    with t1_sub1:
        st.markdown(
            "**What this does:** Fill in the details of your leftover food below. "
            "Anna-Setu checks whether it is still safe to donate, finds the nearest shelter, "
            "and drafts a ready-to-send WhatsApp alert for the shelter team."
        )
        col_input, col_output = st.columns([1, 1], gap="large")

        with col_input:
            # STEP 1
            st.markdown("#### 📍 Step 1: Where is the food coming from?")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                facility_input = st.selectbox("Dining Facility", DINING_FACILITIES, index=0)
            with c_p2:
                origin_zone_choice = st.selectbox(
                    "City Zone (Lucknow)",
                    [o[0] for o in ZONE_OPTIONS],
                    index=0
                )

            pickup_loc_input = st.text_input(
                "Pickup Gate / Collection Point",
                value="Gate 2 Service Loading Bay (Rear Kitchen Entrance)"
            )

            # STEP 2
            st.markdown("#### 🍽️ Step 2: What food is left over?")
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
                    min_value=1,
                    max_value=2000,
                    value=preset["servings"],
                    step=5
                )

            item_input = st.text_input("Food Items (describe briefly)", value=preset["item"])
            category_choice = st.selectbox(
                "Food Type / Category",
                [o[0] for o in CATEGORY_OPTIONS],
                index=preset["category_idx"]
            )

            c_t1, c_t2 = st.columns(2)
            with c_t1:
                time_prep_input = st.text_input(
                    "Time Food Was Cooked (HH:MM)",
                    value=preset["time_prep"],
                    help="Use 24-hour format, e.g. 13:30 for 1:30 PM"
                )
            with c_t2:
                time_assess_input = st.text_input(
                    "Current Time (HH:MM)",
                    value=preset["time_assess"],
                    help="The time right now when you are checking"
                )

            c_s1, c_s2 = st.columns(2)
            with c_s1:
                storage_choice = st.selectbox(
                    "How is the food stored right now?",
                    [o[0] for o in STORAGE_OPTIONS],
                    index=preset["storage_idx"]
                )
            with c_s2:
                temp_input = st.number_input(
                    "Food Temperature (°C) — Optional",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.5,
                    help="Measure using a food thermometer or IR sensor. Leave as 0 if not measured."
                )

            # AI SYNC SECTION
            st.write("---")
            st.markdown("### 🤖 AI Safety Check (Auto-Updated)")
            st.caption("Anna-Setu automatically checks food safety rules and finds the best shelter as you fill in the form above:")

            category_key = CATEGORY_DICT[category_choice]
            storage_key = STORAGE_DICT[storage_choice]
            origin_zone_id = ZONE_DICT[origin_zone_choice]
            temp_c_val = float(temp_input) if temp_input > 0.0 else None

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

            st.text_area(
                "✅ Applicable Food Safety Rule",
                value=sync_data["retrieved_safety_rule"],
                height=70,
                key="rag_rule_box"
            )

            st.text_area(
                "🏠 Best Matching Shelter Nearby",
                value=sync_data["ai_matched_shelter"],
                height=70,
                key="shelter_dest_box"
            )

            run_button = st.button(
                "🚀 Run Safety Check & Generate Shelter Alert",
                type="primary",
                use_container_width=True
            )

        with col_output:
            st.subheader("✅ Results")

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

                # Safety verdict
                if status == "COMPLIANT_SAFE":
                    st.success(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
                elif status == "COMPLIANT_URGENT":
                    st.warning(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")
                else:
                    st.error(f"**{eval_data['badge']}**\n\n{eval_data['reason']}")

                if eval_data.get("temp_summary"):
                    st.warning(f"🌡️ **Temperature Reading:** {eval_data['temp_summary']}")

                # Time metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Time Since Cooking", f"{timeline['elapsed_minutes']} min")
                m2.metric("Delivery Time Est.", f"{timeline['transit_minutes']} min")
                m3.metric("Total Time Out", f"{timeline['total_exposure_minutes']} min")
                m4.metric("Safe Until", f"{timeline['safe_pickup_by']}")

                st.write("---")
                st.markdown("#### 📱 Ready-to-Send Shelter Alert (WhatsApp / SMS)")
                st.code(res["broadcast_message"], language="markdown")

                with st.expander("📜 Food Safety Rules That Apply (Why This Decision Was Made)", expanded=True):
                    for rule in eval_data.get("retrieved_rules", []):
                        st.markdown(f"**[{rule.get('id')}] {rule.get('clause')}**")
                        st.info(f"\"{rule.get('text')}\"")

                with st.expander("📑 Official Handover Record (FSSAI Form B)", expanded=False):
                    st.code(res["audit_manifest"], language="text")

            else:
                st.info(
                    "👈 Fill in the details on the left and click **Run Safety Check** to get the donation verdict, "
                    "shelter match, and ready-to-send alert message."
                )

    # -------------------------------------------------------------------------
    # SUBTAB 2: DEMAND ADVISOR
    # -------------------------------------------------------------------------
    with t1_sub2:
        st.subheader("🔮 How Much Food Should We Cook Today?")
        st.markdown(
            "Instead of guessing and cooking too much, Anna-Setu predicts how many students "
            "will actually show up for a meal — based on the day, weather, and exam schedule. "
            "This prevents food waste before it even happens."
        )

        col_d1, col_d2 = st.columns([1, 1], gap="large")

        with col_d1:
            st.markdown("### 📝 Tell Us About Today")
            enrolled_input = st.number_input(
                "Total Students Registered for Dining",
                min_value=100,
                max_value=5000,
                value=1200,
                step=50
            )
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                meal_input = st.selectbox("Which Meal?", ["Lunch", "Dinner", "Breakfast"])
            with c_m2:
                day_input = st.selectbox(
                    "Day of the Week",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    index=2
                )

            c_c1, c_c2 = st.columns(2)
            with c_c1:
                cal_input = st.selectbox(
                    "Academic Schedule",
                    [
                        "Regular Academic Day",
                        "Exam Week (High Attendance)",
                        "Weekend / Pre-Holiday",
                        "Post-Exam / Festival Eve"
                    ]
                )
            with c_c2:
                weather_input = st.selectbox(
                    "Today's Weather",
                    [
                        "Clear & Mild (~24°C)",
                        "Very Hot Summer (>38°C)",
                        "Monsoon / Heavy Rain",
                        "Cold Winter (~12°C)"
                    ]
                )

            base_rate_input = st.slider(
                "Usual Attendance Rate (%)",
                min_value=50,
                max_value=100,
                value=85,
                step=1,
                help="On a normal day, what percentage of registered students eat here?"
            )

            btn_demand = st.button(
                "🔮 Calculate How Much to Cook",
                type="primary",
                use_container_width=True
            )

        with col_d2:
            st.markdown("### 🎯 Today's Cooking Plan")
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
                    f"**Expected Students Today:** {d_res['predicted_turnout_students']} "
                    f"({d_res['turnout_rate_pct']:.1f}% attendance)\n\n"
                    f"**Cook This Many Portions:** **{d_res['recommended_cooking_target']}** "
                    f"(instead of the usual {d_res['traditional_unoptimized_target']} — saves waste!)"
                )

                dm1, dm2, dm3 = st.columns(3)
                dm1.metric("Meals Waste Prevented", f"{d_res['portions_prevented_from_waste']}")
                dm2.metric("Cost Saved", f"₹{d_res['cost_savings_inr']:,.2f}")
                dm3.metric("Water Saved", f"{d_res['portions_prevented_from_waste'] * 266:,.0f} L")

                st.write("---")
                st.markdown("#### 🛒 Ingredients to Buy / Prepare (kg)")
                ing = d_res["ingredient_breakdown_kg"]
                df_ing = pd.DataFrame([
                    {"Ingredient": "Rice & Grains", "Old Amount (kg)": round(ing['rice_or_grains_kg'] * 1.25, 1), "Smart Amount (kg)": ing['rice_or_grains_kg'], "You Save (kg)": round(ing['rice_or_grains_kg'] * 0.20, 1)},
                    {"Ingredient": "Lentils / Dal", "Old Amount (kg)": round(ing['dal_or_lentils_kg'] * 1.25, 1), "Smart Amount (kg)": ing['dal_or_lentils_kg'], "You Save (kg)": round(ing['dal_or_lentils_kg'] * 0.20, 1)},
                    {"Ingredient": "Vegetables", "Old Amount (kg)": round(ing['vegetables_kg'] * 1.25, 1), "Smart Amount (kg)": ing['vegetables_kg'], "You Save (kg)": round(ing['vegetables_kg'] * 0.20, 1)},
                    {"Ingredient": "Cooking Oil", "Old Amount (kg)": round(ing['cooking_oil_kg'] * 1.25, 1), "Smart Amount (kg)": ing['cooking_oil_kg'], "You Save (kg)": round(ing['cooking_oil_kg'] * 0.20, 1)},
                    {"Ingredient": "Dairy / Paneer", "Old Amount (kg)": round(ing['dairy_or_paneer_kg'] * 1.25, 1), "Smart Amount (kg)": ing['dairy_or_paneer_kg'], "You Save (kg)": round(ing['dairy_or_paneer_kg'] * 0.20, 1)},
                    {"Ingredient": "Spices & Salt", "Old Amount (kg)": round(ing['spices_kg'] * 1.25, 1), "Smart Amount (kg)": ing['spices_kg'], "You Save (kg)": round(ing['spices_kg'] * 0.20, 1)}
                ])
                st.dataframe(df_ing, use_container_width=True, hide_index=True)

                st.info(f"**Chef's Instruction:** {d_res['recommendation_summary']}")
            else:
                st.info(
                    "👈 Enter today's details on the left and click **Calculate How Much to Cook** "
                    "to get a smart portion target and ingredient list."
                )

# =============================================================================
# TAB 2: TRACK B — PLATE-WASTE INTERCEPTOR & BIO-RECYCLER SIMULATOR
# =============================================================================
with tab2:
    st.subheader("♻️ Track B: Plate-Waste Recycler")
    st.markdown(
        "When students leave food on their plates, that waste is captured by a smart kiosk at the tray-return "
        "counter. It shows diners how much water and carbon they wasted — and converts all the scraps into "
        "clean organic fertilizer within 24 hours."
    )

    col_b1, col_b2 = st.columns([1, 1], gap="large")

    with col_b1:
        st.markdown("### 🍽️ Simulate a Diner Returning Their Tray")
        st.write("Enter how much food was left uneaten on the plate:")

        sim_diner_name = st.text_input("Student / Diner ID (Optional)", value="STUDENT-2026-88")
        sim_hostel_block = st.selectbox(
            "Hostel Block",
            ["Block A (Boys)", "Block B (Girls)", "Block C (International)", "Day Scholar Dining"]
        )
        sim_waste_grams = st.slider(
            "Food Left on Plate (grams)",
            min_value=0,
            max_value=450,
            value=175,
            step=5
        )
        sim_daily_diners = st.number_input(
            "Total Diners Using This Dining Hall per Day",
            min_value=100,
            max_value=5000,
            value=850,
            step=50
        )

        # Environmental impact
        sim_water_liters = (sim_waste_grams / 1000.0) * 760.0
        sim_co2e_grams = (sim_waste_grams / 1000.0) * 2300.0

        st.write("---")
        st.markdown("### 📺 What the Kiosk Screen Shows the Diner")
        st.info(
            f"**⚠️ Hey! You left {sim_waste_grams} grams of food on your plate.**\n\n"
            f"💧 **Water wasted:** ~{sim_water_liters:.1f} Litres "
            f"(that's how much water was used to grow this food)\n\n"
            f"🌍 **Carbon footprint:** {sim_co2e_grams:.0f}g CO₂ equivalent emissions\n\n"
            f"🏆 **Your block's score:** {sim_hostel_block} is at 91% Clean Plates this week — keep it up!\n\n"
            f"*💡 Tip: Take only what you can finish. Second helpings are always available!*"
        )

    with col_b2:
        st.markdown("### 🧪 What Happens to the Plate Waste?")

        cum_daily_waste_kg = (sim_daily_diners * sim_waste_grams) / 1000.0
        compost_yield_kg = cum_daily_waste_kg * 0.15
        annual_compost_kg = compost_yield_kg * 240
        methane_avoided_kg = cum_daily_waste_kg * 1.9

        k1, k2 = st.columns(2)
        k1.metric("Total Plate Waste per Day", f"{cum_daily_waste_kg:.1f} kg")
        k2.metric("Bio-Fertilizer Made per Day", f"{compost_yield_kg:.1f} kg", delta="From this waste")

        k3, k4 = st.columns(2)
        k3.metric("Fertilizer Made per Year", f"{annual_compost_kg:,.0f} kg", delta="For campus gardens")
        k4.metric("Methane Emissions Avoided", f"{methane_avoided_kg:.1f} kg CO₂e / day", delta="Zero landfill")

        st.write("---")
        st.markdown("#### 🔄 How Plate Waste Becomes Fertilizer — 5 Steps:")
        st.markdown("""
        1. **Shred:** Food scraps are broken into tiny 3–5 mm pieces so they decompose faster.
        2. **Heat:** A heating element brings the material to 55°C–65°C, killing all harmful bacteria.
        3. **Air Flow:** A fan continuously pumps fresh air in, speeding up decomposition and removing odours.
        4. **Harvest:** Within 12–24 hours, the scraps become a dry, odourless, nutrient-rich organic fertilizer.
        5. **Zero Waste to Landfill:** Nothing goes into the city garbage system — 100% processed on-site.
        """)

# =============================================================================
# TAB 3: CONVERSATIONAL FOOD SAFETY Q&A
# =============================================================================
with tab3:
    st.subheader("💬 Ask a Food Safety Question")
    st.markdown(
        "Not sure if a certain food can be donated? Want to know the rules around food storage or transit? "
        "Ask a plain-English question below and get a clear answer backed by official FSSAI regulations "
        "and Lucknow Nagar Nigam guidelines."
    )

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
# TAB 4: PROJECT TRACKER & MILESTONES
# =============================================================================
with tab4:
    st.subheader("📊 Project Tracker — Anna-Setu (1M1B Internship)")
    st.caption("Intern: Pankhuri Govila · Mentor: Paramjeet Sir (paramjeet@onemoneb.org) · 1M1B AI for Sustainability")

    t_m1, t_m2, t_m3 = st.columns(3)
    t_m1.info("**Milestone 1:** End-November 2026\n\nBuild both Track A & B prototypes + get campus approvals")
    t_m2.info("**Milestone 2:** End-December 2026\n\nRun a 2-week live pilot on campus + submit final impact report")
    t_m3.info("**Intern:** Pankhuri Govila\n\n1M1B AI for Sustainability Virtual Internship")

    st.write("---")
    st.markdown("#### 📋 Task Log & Weekly Progress")

    try:
        df_tracker = pd.read_csv("PankhuriGovila_YIRP_Project_Tracker.csv")
        st.dataframe(df_tracker, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not load tracker file: {e}")

    st.write("---")
    st.markdown("#### 📁 Download Project Files:")
    d_c1, d_c2, d_c3 = st.columns(3)
    with d_c1:
        try:
            with open("PankhuriGovila_YIRP_Project_Tracker.xlsx", "rb") as f:
                st.download_button(
                    "📥 Project Tracker (Excel)",
                    f,
                    "PankhuriGovila_YIRP_Project_Tracker.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except FileNotFoundError:
            st.caption("Excel tracker not available.")
    with d_c2:
        try:
            with open("Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf", "rb") as f:
                st.download_button(
                    "📥 Project Brief (PDF)",
                    f,
                    "Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf",
                    "application/pdf"
                )
        except FileNotFoundError:
            st.caption("PDF brief not available.")
    with d_c3:
        try:
            with open("PankhuriGovila_YIRP_Project_Tracker.csv", "rb") as f:
                st.download_button(
                    "📥 Project Tracker (CSV)",
                    f,
                    "PankhuriGovila_YIRP_Project_Tracker.csv",
                    "text/csv"
                )
        except FileNotFoundError:
            st.caption("CSV tracker not available.")

# =============================================================================
# TAB 5: FOOD SAFETY RULES GUIDE
# =============================================================================
with tab5:
    st.subheader("📖 Food Safety Rules — Simple Guide")
    st.markdown(
        "Anna-Setu follows two sets of official rules: FSSAI national food safety regulations "
        "and Lucknow Nagar Nigam (LNN) municipal guidelines. Here's what they mean in plain language."
    )

    st.markdown("---")

    st.markdown("### 🇮🇳 FSSAI Surplus Food Regulations (2019)")
    st.markdown("""
    **What is the Danger Zone?**
    Food left between **5°C and 65°C** (roughly fridge temperature to boiling) allows bacteria to grow
    very quickly. This is called the "danger zone." Always keep food either colder than 5°C or hotter
    than 65°C if it is waiting to be eaten or donated.

    **The 2-Hour / 4-Hour Rule (Regulation 4(2)):**
    | Time Since Cooking | What You Can Do |
    |---|---|
    | Less than 2 hours | ✅ Safe to donate, chill, or reheat |
    | 2–4 hours | ⚠️ Safe only if the shelter will eat it immediately on arrival |
    | More than 4 hours | 🚫 Not safe for people — must go to compost |

    **Keeping Food Hot or Cold (Regulation 4(3)):**
    - **Hot food** must stay at **65°C or above** at all times until served.
    - **Refrigerated food** must stay at **5°C or below**.

    **What CANNOT Be Donated (Regulation 4(4)):**
    - ❌ Food left on a diner's plate (plate waste / customer leftovers)
    - ❌ Cut salads, sliced fruits, or open chutneys left at room temperature for more than 2 hours

    **Are Donors Protected by Law? (Regulation 4(5) & Section 7):**
    Yes. If a donor follows the rules above and donates in good faith, they are **legally protected**
    from being sued if something goes wrong later in the delivery chain.

    **Record Keeping (Regulation 7):**
    Every donation must be logged in an **official Form B register** — noting the food type, quantity,
    cooking time, temperature, and signatures. Records must be kept for 1 year.
    """)

    st.markdown("---")

    st.markdown("### 🏙️ Lucknow Nagar Nigam (City Council) Rules")
    st.markdown("""
    **Maximum Delivery Time (Section 14):**
    Food in transit must reach the shelter within **45 minutes** due to Lucknow traffic and summer heat (>38°C).
    For longer routes, insulated thermal containers are required.

    **No Dumping in Garbage Bins (Section 10):**
    It is **illegal** to throw commercial food waste into city dustbins or roadside dumps.
    Spot fines range from **₹5,000 to ₹25,000**.

    **Expired Food Must Be Composted (Section 18):**
    Food that is past its safe window must **never** go into mixed garbage.
    It must be sorted as green wet waste and sent to campus composting or the city's
    Kanha Upvan biomethanation facility.

    **Gate Clearance for Outgoing Food Vehicles (Section 21):**
    Campus security must verify and timestamp all food rescue vehicles leaving the premises
    with an Anna-Setu digital gate pass.
    """)
