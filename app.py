"""
Anna-Setu: AI Campus Food Rescue & Redistribution Network
Interactive Interface powered by IBM Granite Prompt Synthesis & RAG Compliance Pipeline
Adheres to FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam Food Service Guidelines
Covers Dual Tracks: Track A (Software AI & RAG Engine) + Track B (Smart Plate-Waste Interceptor & Bio-Recycler)
"""

import sys
from datetime import datetime
from rag.pipeline import AnnaSetuRAGPipeline

# Initialize RAG Pipeline
pipeline = AnnaSetuRAGPipeline()

# Category mapping
CATEGORY_CHOICES = [
    ("Cooked Grains, Rice, Dal & Gravies (High Moisture)", "cooked_grains_curry"),
    ("Dry Cooked Staples (Rotis, Chapatis, Dry Sabzi)", "dry_staples_roti"),
    ("Dairy, Paneer Curries, Milk Sweets & Kheer", "dairy_sweets"),
    ("Dry Fried Snacks (Samosas, Cutlets, Pakoras)", "fried_snacks"),
    ("Raw Cut Salads, Sliced Fruits (Prohibited Ambient)", "raw_salads_cut_fruits"),
    ("Plate Waste / Post-Consumer Leftovers (Strictly Prohibited)", "plate_waste")
]
CATEGORY_MAP = {label: key for label, key in CATEGORY_CHOICES}

STORAGE_CHOICES = [
    ("Ambient Room Temperature (~25°C - 35°C)", "ambient"),
    ("Active Hot-Holding (Maintained >= 65°C)", "hot_holding"),
    ("Active Refrigerated / Cold-Chain (Maintained <= 5°C)", "refrigerated")
]
STORAGE_MAP = {label: key for label, key in STORAGE_CHOICES}

ZONE_CHOICES = [
    ("Zone 4 - Gomti Nagar, Extension, Indira Nagar", 4),
    ("Zone 1 - Hazratganj, Chowk, Charbagh, Qaiserbagh", 1),
    ("Zone 2 - Aishbagh, Rajajipuram", 2),
    ("Zone 3 - Aliganj, Jankipuram, Vikas Nagar", 3),
    ("Zone 5 - Alambagh, Singar Nagar, Krishna Nagar", 5),
    ("Zone 6 - Hardoi Road, Dubagga, Kakori", 6),
    ("Zone 7 - Chinhat, Faizabad Road, BBD Corridor", 7),
    ("Zone 8 - Sarojini Nagar, Transport Nagar, Airport", 8)
]
ZONE_MAP = {label: zone_id for label, zone_id in ZONE_CHOICES}

DINING_PLACES = [
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
        "category": "Cooked Grains, Rice, Dal & Gravies (High Moisture)",
        "storage": "Ambient Room Temperature (~25°C - 35°C)"
    },
    "Lunch": {
        "time_prep": "12:30",
        "time_assess": "14:00",
        "item": "Vegetable Pulao, Dal Tadka & Chapati",
        "servings": 45,
        "category": "Cooked Grains, Rice, Dal & Gravies (High Moisture)",
        "storage": "Ambient Room Temperature (~25°C - 35°C)"
    },
    "Snacks / High Tea": {
        "time_prep": "16:30",
        "time_assess": "17:30",
        "item": "Vegetable Cutlets, Samosas & Tea Cake",
        "servings": 30,
        "category": "Dry Fried Snacks (Samosas, Cutlets, Pakoras)",
        "storage": "Ambient Room Temperature (~25°C - 35°C)"
    },
    "Dinner": {
        "time_prep": "20:00",
        "time_assess": "21:30",
        "item": "Paneer Butter Masala, Dal Makhani & Rotis",
        "servings": 50,
        "category": "Dairy, Paneer Curries, Milk Sweets & Kheer",
        "storage": "Ambient Room Temperature (~25°C - 35°C)"
    },
    "Other": {
        "time_prep": "11:00",
        "time_assess": "12:30",
        "item": "Mixed Institutional Buffet Catering Spread",
        "servings": 60,
        "category": "Cooked Grains, Rice, Dal & Gravies (High Moisture)",
        "storage": "Ambient Room Temperature (~25°C - 35°C)"
    }
}

SHELTER_NAMES = ["Auto-Match Closest Verified Shelter (Recommended)"] + pipeline.get_shelter_names()


def on_meal_change(selected_meal):
    """Dynamically updates preparation time, evaluation time, items, and servings when meal type changes."""
    preset = MEAL_PRESETS.get(selected_meal, MEAL_PRESETS["Lunch"])
    return (
        preset["time_prep"],
        preset["time_assess"],
        preset["item"],
        preset["servings"],
        preset["category"],
        preset["storage"]
    )


def sync_pipeline_fields(
    place_facility,
    pickup_loc,
    origin_zone_label,
    meal_type,
    item_name,
    servings_count,
    category_label,
    time_prep,
    time_assess,
    storage_label,
    measured_temp
):
    """
    Syncs with RAG Pipeline to populate:
    1. Retrieved Safety Compliance Rule (RAG)
    2. AI Matched Shelter Destination
    """
    category_key = CATEGORY_MAP.get(category_label, "cooked_grains_curry")
    storage_key = STORAGE_MAP.get(storage_label, "ambient")
    origin_zone = ZONE_MAP.get(origin_zone_label, 4)

    temp_val = None
    if measured_temp is not None and str(measured_temp).strip():
        try:
            temp_val = float(measured_temp)
        except (ValueError, TypeError):
            temp_val = None

    sync_res = pipeline.sync_ai_pipeline_configurations(
        origin_zone=origin_zone,
        item=item_name,
        servings=int(servings_count) if servings_count else 40,
        category_key=category_key,
        time_prepared=time_prep,
        assessment_time=time_assess,
        storage_condition=storage_key,
        measured_temp_celsius=temp_val
    )

    return (
        sync_res["retrieved_safety_rule"],
        sync_res["ai_matched_shelter"]
    )


def demand_advisor_flow(
    enrolled_students,
    meal_type,
    day_of_week,
    academic_calendar,
    weather_condition,
    base_turnout_pct
):
    """Predicts daily dining hall turnout and optimizes prep quotas (Module 1)."""
    try:
        enrolled = int(enrolled_students)
    except (ValueError, TypeError):
        enrolled = 1200

    try:
        base_rate = float(base_turnout_pct) / 100.0
    except (ValueError, TypeError):
        base_rate = 0.85

    res = pipeline.predict_meal_demand(
        enrolled_students=enrolled,
        meal_type=meal_type,
        day_of_week=day_of_week,
        academic_calendar=academic_calendar,
        weather=weather_condition,
        base_turnout_rate=base_rate
    )

    metrics_md = (
        f"### 🎯 Dining Turnout & Production Target Optimization\n\n"
        f"- **Enrolled Dining Cohort:** `{res['enrolled_students']}` students\n"
        f"- **Predicted Turnout Rate:** `{res['turnout_rate_pct']:.1f}%` ({res['predicted_turnout_students']} students)\n"
        f"- **Recommended Cooking Target:** **{res['recommended_cooking_target']} portions** "
        f"*(5% safety buffer vs traditional 25% overproduction buffer)*\n"
        f"- **Traditional Static Buffer Target:** `{res['traditional_unoptimized_target']}` portions\n"
        f"- **Portions Saved from Waste:** **{res['portions_prevented_from_waste']} meals**\n"
        f"- **Estimated Kitchen Procurement Savings:** **₹{res['cost_savings_inr']:,.2f}** per meal service!\n"
    )

    ing = res["ingredient_breakdown_kg"]
    ingredients_md = (
        f"### ⚖️ Optimized Raw Ingredient Procurement Requirements:\n\n"
        f"| Raw Ingredient | Traditional Prep (kg) | Optimized Prep (kg) | Quantity Saved (kg) |\n"
        f"| :--- | :--- | :--- | :--- |\n"
        f"| **Rice & Grains** | {ing['rice_or_grains_kg'] * 1.25:.1f} kg | **{ing['rice_or_grains_kg']:.1f} kg** | {ing['rice_or_grains_kg'] * 0.20:.1f} kg |\n"
        f"| **Lentils / Dal** | {ing['dal_or_lentils_kg'] * 1.25:.1f} kg | **{ing['dal_or_lentils_kg']:.1f} kg** | {ing['dal_or_lentils_kg'] * 0.20:.1f} kg |\n"
        f"| **Fresh Vegetables** | {ing['vegetables_kg'] * 1.25:.1f} kg | **{ing['vegetables_kg']:.1f} kg** | {ing['vegetables_kg'] * 0.20:.1f} kg |\n"
        f"| **Cooking Oil** | {ing['cooking_oil_kg'] * 1.25:.1f} kg | **{ing['cooking_oil_kg']:.1f} kg** | {ing['cooking_oil_kg'] * 0.20:.1f} kg |\n"
        f"| **Dairy / Paneer** | {ing['dairy_or_paneer_kg'] * 1.25:.1f} kg | **{ing['dairy_or_paneer_kg']:.1f} kg** | {ing['dairy_or_paneer_kg'] * 0.20:.1f} kg |\n"
        f"| **Spices & Condiments** | {ing['spices_kg'] * 1.25:.1f} kg | **{ing['spices_kg']:.1f} kg** | {ing['spices_kg'] * 0.20:.1f} kg |\n\n"
        f"*Calculations assume ~350g cooked meal portion size with standard institutional cafeteria recipe ratios.*"
    )

    guidance_md = (
        f"### 📋 Head Chef Morning Kitchen Directive\n\n"
        f"```text\n{res['recommendation_summary']}\n```\n\n"
        f"**Environmental Impact:** Preventing {res['portions_prevented_from_waste']} wasted meals conserves "
        f"~`{res['portions_prevented_from_waste'] * 266:.0f} Liters` of embedded freshwater and avoids "
        f"~`{res['portions_prevented_from_waste'] * 0.8:.1f} kg CO2e` in life-cycle emissions."
    )

    return metrics_md, ingredients_md, guidance_md


def evaluate_surplus_flow(
    place_facility,
    pickup_loc,
    origin_zone_label,
    meal_type,
    item_name,
    servings_count,
    category_label,
    time_prep,
    time_assess,
    storage_label,
    measured_temp,
    compliance_rule_in,
    shelter_label_in
):
    """Callback function executing end-to-end RAG compliance and IBM Granite compiler."""
    category_key = CATEGORY_MAP.get(category_label, "cooked_grains_curry")
    storage_key = STORAGE_MAP.get(storage_label, "ambient")
    origin_zone = ZONE_MAP.get(origin_zone_label, 4)

    if not time_assess or not time_assess.strip():
        time_assess = datetime.now().strftime("%H:%M")

    temp_val = None
    if measured_temp is not None and str(measured_temp).strip():
        try:
            temp_val = float(measured_temp)
        except (ValueError, TypeError):
            temp_val = None

    res = pipeline.evaluate_surplus(
        item=item_name,
        servings=int(servings_count),
        category_key=category_key,
        time_prepared=time_prep,
        assessment_time=time_assess,
        storage_condition=storage_key,
        origin_zone=origin_zone,
        shelter_display_name=shelter_label_in,
        pickup_location=pickup_loc,
        facility_place=place_facility,
        meal_type=meal_type,
        measured_temp_celsius=temp_val
    )

    eval_data = res["evaluation"]
    timeline = eval_data["timeline"]
    status = eval_data["status"]

    temp_note = ""
    if eval_data.get("temp_summary"):
        temp_note = f"\n\n🌡️ **Thermal Sensor Ground Truth:** `{eval_data['temp_summary']}`"

    # Format Status Header
    if status == "COMPLIANT_SAFE":
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"✅ **Safety Window:** Safe until **{timeline['safe_pickup_by']} IST** "
            f"({timeline['max_allowed_minutes'] - timeline['total_exposure_minutes']} mins buffer remaining).\n\n"
            f"📍 **Origin Facility:** {place_facility} ({pickup_loc}) | **Meal Service:** {meal_type}\n\n"
            f"⏱️ **Elapsed:** {timeline['elapsed_minutes']} mins | "
            f"🚚 **Estimated Transit:** {timeline['transit_minutes']} mins\n\n"
            f"ℹ️ **Summary:** {eval_data['reason']}{temp_note}"
        )
    elif status == "COMPLIANT_URGENT":
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"⚠️ **Attention Required:** Handover and consumption must occur before **{timeline['safe_pickup_by']} IST**.\n\n"
            f"📍 **Origin Facility:** {place_facility} ({pickup_loc}) | **Meal Service:** {meal_type}\n\n"
            f"⏱️ **Elapsed:** {timeline['elapsed_minutes']} mins | "
            f"🚚 **Transit:** {timeline['transit_minutes']} mins | "
            f"⚠️ **Remaining Window:** {timeline['max_allowed_minutes'] - timeline['total_exposure_minutes']} mins\n\n"
            f"ℹ️ **Action:** {eval_data['reason']}{temp_note}"
        )
    else:
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"🛑 **Redistribution Blocked:** Cannot be dispatched for human consumption.\n\n"
            f"📍 **Origin Facility:** {place_facility} ({pickup_loc}) | **Meal Service:** {meal_type}\n\n"
            f"⚠️ **Reason:** {eval_data['reason']}\n\n"
            f"♻️ **Mandatory Municipal Action:** {eval_data['lnn_action']}{temp_note}"
        )

    # Format Retrieved Clauses
    retrieved_md = "#### 📜 Retrieved Statutory Clauses (FSSAI 2019 & LNN By-Laws):\n\n"
    for r in eval_data.get("retrieved_rules", []):
        retrieved_md += (
            f"- **[{r.get('id')}] {r.get('clause')}** *(Relevance Score: {r.get('relevance_score', 0):.2f})*\n"
            f"  > *\"{r.get('text')}\"*\n\n"
        )

    # Update synced fields
    updated_rule = res.get("retrieved_safety_rule", compliance_rule_in)
    updated_shelter = res.get("ai_matched_shelter", shelter_label_in)

    return (
        status_md,
        res["broadcast_message"],
        retrieved_md,
        res["audit_manifest"],
        updated_rule,
        updated_shelter
    )


def regulatory_qa_flow(query_text, authority_filter):
    """Generative RAG QA synthesized by IBM Granite citing legal clauses."""
    if not query_text or len(query_text.strip()) < 3:
        return "Please enter a specific question about FSSAI or Lucknow Nagar Nigam regulations.", ""

    filter_val = None
    if authority_filter == "FSSAI Regulations Only":
        filter_val = "FSSAI"
    elif authority_filter == "Lucknow Nagar Nigam By-Laws Only":
        filter_val = "LUCKNOW_NAGAR_NIGAM"

    qa_res = pipeline.ask_regulations(query=query_text, top_k=3, filter_source=filter_val)
    answer_md = qa_res.get("synthesized_answer", "No answer generated.")

    citations_md = "#### 📚 Retrieved Statutory Grounding Chunks:\n\n"
    for idx, clause in enumerate(qa_res.get("retrieved_clauses", []), 1):
        citations_md += (
            f"**{idx}. [{clause.get('id')}] {clause.get('title')}**\n"
            f"- **Authority:** {clause.get('source_authority')}\n"
            f"- **Clause Reference:** `{clause.get('clause')}` | *Similarity Score:* `{clause.get('relevance_score', 0):.3f}`\n"
            f"> *\"{clause.get('text')}\"*\n\n"
        )

    return answer_md, citations_md


def plate_waste_sim_flow(student_id, hostel_block, waste_grams, daily_diners):
    """Calculates student plate waste, behavioral nudges, and on-site bio-recycler yield."""
    try:
        w_grams = float(waste_grams)
    except (ValueError, TypeError):
        w_grams = 175.0

    try:
        diners = int(daily_diners)
    except (ValueError, TypeError):
        diners = 850

    water_l = (w_grams / 1000.0) * 760.0
    co2e_g = (w_grams / 1000.0) * 2300.0

    daily_waste_kg = (diners * w_grams) / 1000.0
    compost_daily_kg = daily_waste_kg * 0.15
    annual_compost_kg = compost_daily_kg * 240
    methane_avoided_kg = daily_waste_kg * 1.9

    nudge_md = (
        f"### 📺 Dynamic Student Tray Nudge Screen\n\n"
        f"```text\n"
        f"+-------------------------------------------------------------------------+\n"
        f"|  ⚠️ ATTENTION DINER: You left {w_grams:.0f}g of uneaten food on your plate!      |\n"
        f"|  💧 Embedded Freshwater Lost: ~{water_l:.1f} Liters (Grain & pulse cultivation) |\n"
        f"|  🌍 Carbon Equivalent: {co2e_g:.0f}g CO2e fugitive footprint                    |\n"
        f"|  🏆 HOSTEL LEADERBOARD: {hostel_block} is at 91% Clean Plates this week! |\n"
        f"|  💡 Action: Take only what you finish. Second helpings are unlimited!    |\n"
        f"+-------------------------------------------------------------------------+\n"
        f"```\n\n"
        f"**Behavioral Psychology Insight:** Providing instant visual feedback on resource loss "
        f"reduces individual diner plate scrap waste by 25-38% within 14 days of campus deployment."
    )

    yield_md = (
        f"### 🧪 Campus-Wide Bio-Recycling Output (Track B Kiosk)\n\n"
        f"- **Cumulative Daily Plate Waste:** **{daily_waste_kg:.1f} kg/day** (from {diners} daily diners)\n"
        f"- **High-Grade Organic Bio-Fertilizer Harvested:** **{compost_daily_kg:.1f} kg/day** *(15% dry yield after 85% moisture reduction)*\n"
        f"- **Projected Annual Campus Fertilizer Yield:** **{annual_compost_kg:,.0f} kg/year** *(Replaces synthetic chemical fertilizer on campus grounds)*\n"
        f"- **Landfill Methane Emissions Avoided:** **{methane_avoided_kg:.1f} kg CO2e/day**\n"
        f"- **Municipal Sanitation Burden on Lucknow Nagar Nigam:** **0.0 kg** *(100% on-site closed-loop valorization)*\n\n"
        f"#### 🔄 The 5-Step Closed Loop Transformation Process:\n"
        f"1. **Pre-Processing Shredder:** Scraped plate waste is macerated to 3-5 mm particles for rapid microbial contact.\n"
        f"2. **Thermophilic Stage (55°C - 65°C):** PTC ceramic heating element accelerates decomposition and eliminates pathogens (*Salmonella*, *E. coli*).\n"
        f"3. **Aerobic Aeration:** Continuous airflow + activated carbon filtration eliminates odors without synthetic chemicals.\n"
        f"4. **Recyclable Harvest:** In 12-24 hours, scraps turn into rich, dry, odourless organic soil conditioner.\n"
        f"5. **Zero Municipal Burden:** Eliminates municipal dhalav disposal, completely avoiding LNN Section 10 penalties (₹5,000-₹25,000)."
    )

    return nudge_md, yield_md


# Launch Gradio interface if gradio is available; otherwise run fallback message
try:
    import gradio as gr

    with gr.Blocks(title="Anna-Setu: AI Campus Food Rescue & Bio-Recycling Network", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🍽️ Anna-Setu: AI Campus Food Rescue & Bio-Recycling Network")
        gr.Markdown(
            "### 1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE • Pankhuri Govila\n"
            "*Powered by IBM Granite Models & Dual-Track Architecture: Track A (AI Platform & RAG Compliance) + Track B (IoT Plate-Waste Interceptor)*"
        )

        with gr.Tabs():
            # TAB 1: SURPLUS RESCUE & RAG COMPLIANCE (WITH PLACE, MEAL, AND SIMULATED AI CONFIGS)
            with gr.TabItem("📋 Surplus Handoff & RAG Compliance Evaluation"):
                gr.Markdown("### 🍛 Cafeteria Service Handoff Logs & Statutory FSSAI Verification")
                gr.Markdown(
                    "Enter the dining facility location and meal details below. The RAG pipeline automatically retrieves the governing "
                    "safety rules and matches the optimal destination shelter, populating the AI configurations in real time."
                )

                with gr.Row():
                    # LEFT COLUMN: INPUTS & AI PIPELINE CONFIGURATIONS
                    with gr.Column(scale=5):
                        # SECTION 1: PLACE & LOCATION DETAILS (ENTERED FIRST!)
                        gr.Markdown("#### 📍 Step 1: Campus Dining Facility & Location (Place Details)")
                        with gr.Row():
                            place_facility = gr.Dropdown(
                                label="Dining Facility / Place Name",
                                choices=DINING_PLACES,
                                value=DINING_PLACES[0]
                            )
                            origin_zone = gr.Dropdown(
                                label="Campus Origin Zone (Lucknow)",
                                choices=[label for label, _ in ZONE_CHOICES],
                                value=ZONE_CHOICES[0][0]
                            )
                        pickup_loc = gr.Textbox(
                            label="Specific Pickup Bay / Dispatch Gate Location",
                            value="Gate 2 Service Loading Bay (Rear Kitchen Entrance)"
                        )

                        # SECTION 2: MEAL SERVICE & FOOD DETAILS (ENTERED SECOND!)
                        gr.Markdown("#### 🍽️ Step 2: Meal Service & Surplus Food Details")
                        with gr.Row():
                            meal_type = gr.Dropdown(
                                label="Meal Service Type",
                                choices=["Breakfast", "Lunch", "Snacks / High Tea", "Dinner", "Other"],
                                value="Lunch"
                            )
                            servings = gr.Number(
                                label="Estimated Servings Leftover",
                                value=45,
                                precision=0
                            )

                        item = gr.Textbox(
                            label="Surplus Food Item(s)",
                            value="Vegetable Pulao, Dal Tadka & Chapati"
                        )
                        category = gr.Dropdown(
                            label="Food Category (FSSAI Microbial Profile)",
                            choices=[label for label, _ in CATEGORY_CHOICES],
                            value=CATEGORY_CHOICES[0][0]
                        )

                        with gr.Row():
                            time_prep = gr.Textbox(
                                label="Time Prepared (HH:MM 24h)",
                                value="12:30"
                            )
                            time_assess = gr.Textbox(
                                label="Current Assessment Time (HH:MM 24h)",
                                value="14:00"
                            )

                        with gr.Row():
                            storage = gr.Dropdown(
                                label="Storage & Holding Condition",
                                choices=[label for label, _ in STORAGE_CHOICES],
                                value=STORAGE_CHOICES[0][0]
                            )
                            measured_temp = gr.Number(
                                label="Measured Surface Temp (°C) [Optional Contactless IR Sensor]",
                                value=None
                            )

                        # SECTION 3: SIMULATED AI PIPELINE CONFIGURATIONS (MATCHING SCREENSHOT!)
                        gr.Markdown("### 🧠 Simulated AI Pipeline Configurations")
                        gr.Markdown("*These fields are automatically synchronized and populated from the RAG Pipeline and Shelter Directory:*")

                        compliance_rule_box = gr.Textbox(
                            label="Retrieved Safety Compliance Rule (RAG)",
                            value="[FSSAI-REG-4-2] Within 4-hour ambient holding limit per FSSAI Reg 4(2) & LNN Sec 14. Safe redistribution active until 16:30 IST.",
                            lines=2,
                            interactive=True
                        )

                        shelter_box = gr.Textbox(
                            label="AI Matched Shelter Destination",
                            value="Rain Basera Gomti Nagar (Zone 4 (Gomti Nagar) - 2.1 km away | Route Transit: 15 mins | Bed Capacity: 100)",
                            lines=2,
                            interactive=True
                        )

                        with gr.Row():
                            btn_sync = gr.Button("🔄 Sync AI Pipeline Configurations (RAG)", variant="secondary")
                            btn_eval = gr.Button("Execute IBM Granite Notification Compiler", variant="primary")

                    # RIGHT COLUMN: GENERATED OUTPUTS
                    with gr.Column(scale=5):
                        gr.Markdown("### ✅ Generated Output (WhatsApp / SMS Ready Format)")
                        status_box = gr.Markdown(value="*Click 'Execute IBM Granite Notification Compiler' to evaluate surplus food safety and generate alert.*")
                        output_msg = gr.TextArea(
                            label="AI-Drafted Broadcast Message (WhatsApp / SMS Ready)",
                            lines=8,
                            interactive=False
                        )
                        with gr.Accordion("📜 Retrieved FSSAI & LNN Regulatory Grounding (RAG)", open=True):
                            rag_clauses_box = gr.Markdown(value="*Retrieved regulatory clauses will appear here.*")
                        with gr.Accordion("📑 Official FSSAI Form B & LNN Gate Pass Manifest", open=False):
                            manifest_box = gr.TextArea(
                                label="Digital Compliance Audit Manifest",
                                lines=12,
                                interactive=False
                            )

                # Meal preset change event listener
                meal_type.change(
                    fn=on_meal_change,
                    inputs=[meal_type],
                    outputs=[time_prep, time_assess, item, servings, category, storage]
                )

                # Sync button click listener
                btn_sync.click(
                    fn=sync_pipeline_fields,
                    inputs=[
                        place_facility, pickup_loc, origin_zone, meal_type,
                        item, servings, category, time_prep, time_assess, storage, measured_temp
                    ],
                    outputs=[compliance_rule_box, shelter_box]
                )

                # Primary evaluation click listener
                btn_eval.click(
                    fn=evaluate_surplus_flow,
                    inputs=[
                        place_facility, pickup_loc, origin_zone, meal_type,
                        item, servings, category, time_prep, time_assess, storage, measured_temp,
                        compliance_rule_box, shelter_box
                    ],
                    outputs=[status_box, output_msg, rag_clauses_box, manifest_box, compliance_rule_box, shelter_box]
                )

            # TAB 2: AI DINING DEMAND ADVISOR (MODULE 1)
            with gr.TabItem("🔮 Module 1: AI Dining Demand Advisor"):
                gr.Markdown("### 📊 Predictive Kitchen Demand & Procurement Optimization")
                gr.Markdown(
                    "Predicts actual student meal turnout using historical calendar, weather, and exam schedules. "
                    "Replaces arbitrary 25% cooking buffers with a lean 5% safety buffer to eliminate food waste at the source."
                )
                with gr.Row():
                    with gr.Column(scale=5):
                        enrolled_input = gr.Number(label="Total Enrolled Students in Dining Hall", value=1200, precision=0)
                        meal_choice = gr.Dropdown(
                            label="Meal Service Type",
                            choices=["Lunch", "Dinner", "Breakfast"],
                            value="Lunch"
                        )
                        day_choice = gr.Dropdown(
                            label="Day of the Week",
                            choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                            value="Wednesday"
                        )
                        calendar_choice = gr.Dropdown(
                            label="Academic Calendar Status",
                            choices=["Regular Academic Day", "Exam Week (High Attendance)", "Weekend / Pre-Holiday", "Post-Exam / Festival Eve"],
                            value="Regular Academic Day"
                        )
                        weather_choice = gr.Dropdown(
                            label="Weather Forecast",
                            choices=["Clear Mild (~24°C)", "Extreme Hot Summer (>38°C)", "Monsoon Heavy Rain", "Cold Winter (~12°C)"],
                            value="Clear Mild (~24°C)"
                        )
                        base_turnout_input = gr.Slider(
                            label="Historical Baseline Turnout Rate (%)",
                            minimum=50,
                            maximum=100,
                            value=85,
                            step=1
                        )
                        btn_predict = gr.Button("🔮 Run Predictive Demand Optimization", variant="primary")

                    with gr.Column(scale=5):
                        demand_metrics_box = gr.Markdown(value="*Click 'Run Predictive Demand Optimization' to calculate targets.*")
                        demand_ing_box = gr.Markdown()
                        demand_guidance_box = gr.Markdown()

                btn_predict.click(
                    fn=demand_advisor_flow,
                    inputs=[enrolled_input, meal_choice, day_choice, calendar_choice, weather_choice, base_turnout_input],
                    outputs=[demand_metrics_box, demand_ing_box, demand_guidance_box]
                )

            # TAB 3: CONVERSATIONAL RAG REGULATORY ASSISTANT
            with gr.TabItem("💬 Conversational RAG Regulatory Assistant"):
                gr.Markdown("### 🏛️ Generative Legal QA on FSSAI Regulations & Lucknow Municipal By-Laws")
                gr.Markdown(
                    "Ask free-form legal and operational questions. The RAG pipeline retrieves authoritative statutory clauses and uses "
                    "IBM Granite prompt synthesis to provide structured legal guidance with exact citations, safety boundaries, and liability protections."
                )
                with gr.Row():
                    with gr.Column(scale=8):
                        qa_input = gr.Textbox(
                            label="Ask a Regulatory Question",
                            placeholder="e.g., Can I donate cooked paneer curry after 3 hours at room temperature?",
                            value="Can I donate cooked paneer curry after 3 hours at room temperature?"
                        )
                    with gr.Column(scale=2):
                        authority_filter = gr.Dropdown(
                            label="Filter Legal Authority",
                            choices=["All Authorities", "FSSAI Regulations Only", "Lucknow Nagar Nigam By-Laws Only"],
                            value="All Authorities"
                        )
                btn_qa = gr.Button("⚖️ Synthesize Legal Guidance via RAG", variant="secondary")

                qa_answer_box = gr.Markdown(value="*Enter a question above and click to synthesize grounded legal guidance.*")
                with gr.Accordion("📜 Source Law Citations & Chunks", open=True):
                    qa_citations_box = gr.Markdown()

                btn_qa.click(
                    fn=regulatory_qa_flow,
                    inputs=[qa_input, authority_filter],
                    outputs=[qa_answer_box, qa_citations_box]
                )

            # TAB 4: TRACK B SMART PLATE-WASTE INTERCEPTOR
            with gr.TabItem("♻️ Track B: Plate-Waste Interceptor & Bio-Recycler"):
                gr.Markdown("### 🍽️ Dish-Clearing Tray Return Simulator & Accelerated Bio-Recycling Station")
                gr.Markdown(
                    "Track B deploys an IoT-enabled dish-clearing kiosk (load cell, thermal sensor, display) that nudges diners "
                    "and transforms scraped food scraps into nutrient-rich organic bio-fertilizer within 12-24 hours."
                )
                with gr.Row():
                    with gr.Column(scale=5):
                        st_id = gr.Textbox(label="Diner / Student ID (Optional)", value="STUDENT-2026-88")
                        hostel = gr.Dropdown(
                            label="Hostel Dining Hall Block",
                            choices=["Block A (Boys)", "Block B (Girls)", "Block C (International)", "Day Scholar Dining"],
                            value="Block B (Girls)"
                        )
                        waste_slider = gr.Slider(
                            label="Scraped Plate Waste (Grams)",
                            minimum=0,
                            maximum=450,
                            value=175,
                            step=5
                        )
                        diners_input = gr.Number(
                            label="Total Daily Diners in Dining Hall",
                            value=850,
                            precision=0
                        )
                        btn_sim = gr.Button("♻️ Simulate Tray Scrape & Bio-Recycle Yield", variant="primary")

                    with gr.Column(scale=5):
                        nudge_output = gr.Markdown(value="*Click to simulate tray return.*")
                        yield_output = gr.Markdown()

                btn_sim.click(
                    fn=plate_waste_sim_flow,
                    inputs=[st_id, hostel, waste_slider, diners_input],
                    outputs=[nudge_output, yield_output]
                )

            # TAB 5: PROJECT TRACKER & MILESTONES (PankhuriGovila_YIRP)
            with gr.TabItem("📊 Project Tracker & Statutory SOPs"):
                gr.Markdown("### 📊 1M1B Project Tracker & Mentorship Sharing Register")
                gr.Markdown(
                    "**Project Tracker:** `PankhuriGovila_YIRP` | **Shared With:** `paramjeet@onemoneb.org` | "
                    "**Intern:** Pankhuri Govila (1M1B AI for Sustainability Virtual Internship)\n\n"
                    "---"
                )
                with gr.Row():
                    with gr.Column():
                        gr.Markdown(
                            "#### 🚩 Key Project Milestones & Gates\n\n"
                            "- **Milestone 1 (End-November 2026):** Project Prototype Completion & Institutional Approvals.\n"
                            "  - Complete functional Anna-Setu Track A RAG software platform.\n"
                            "  - Assemble Track B IoT hardware prototype with load cell and thermal sensor.\n"
                            "  - Secure signed MoU with Campus Dining Administration and 2 local Lucknow shelter partners.\n\n"
                            "- **Milestone 2 (End-December 2026):** Live Campus Pilot & Full Deployment.\n"
                            "  - Deploy 2-week continuous pilot in campus cafeteria dining hall.\n"
                            "  - Track meals rescued, plate waste diverted, and bio-fertilizer produced.\n"
                            "  - Deliver comprehensive impact report and presentation for 1M1B evaluation."
                        )
                    with gr.Column():
                        gr.Markdown(
                            "#### 📚 Statutory Food Regulations Summary (FSSAI 2019)\n\n"
                            "- **Bacterial Danger Zone:** 5°C to 65°C. Rapid exponential microbial proliferation.\n"
                            "- **The 2h / 4h Rule (Reg 4(2)):**\n"
                            "  - `< 2 hours:` Safe to redistribute, refrigerate (<=5°C), or reheat (>=74°C).\n"
                            "  - `2 - 4 hours:` Safe for immediate consumption only.\n"
                            "  - `> 4 hours:` Condemned from human consumption due to heat-stable toxins.\n"
                            "- **Lucknow Nagar Nigam By-Laws:**\n"
                            "  - Max 45-minute corridor transit ceiling across city traffic.\n"
                            "  - Commercial food waste dumping in municipal bins carries ₹5,000 to ₹25,000 fine (Sec 10).\n"
                            "  - Mandatory diversion of non-compliant food to decentralized composting (Sec 18)."
                        )

    if __name__ == "__main__":
        demo.launch()

except ImportError:
    if __name__ == "__main__":
        print("Note: Gradio is not installed locally. Gradio is configured for Hugging Face Spaces.")
        print("To run locally with Streamlit, execute: streamlit run streamlit_app.py")
        print("Running CLI simulation...")
        res = pipeline.evaluate_surplus(
            item="Vegetable pulao and dal",
            servings=45,
            category_key="cooked_grains_curry",
            time_prepared="12:30",
            assessment_time="14:00",
            storage_condition="ambient",
            origin_zone=4,
            shelter_display_name="AUTO_MATCH",
            pickup_location="Gate 2 Service Loading Bay",
            facility_place="Central Campus Dining Complex",
            meal_type="Lunch"
        )
        print(res["broadcast_message"])
