"""
Anna-Setu: AI Campus Food Rescue & Redistribution Network
Interactive Interface powered by IBM Granite Prompt Synthesis & RAG Compliance Pipeline
Adheres to FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam Food Service Guidelines
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

SHELTER_NAMES = pipeline.get_shelter_names()


def evaluate_surplus_flow(
    item_name,
    servings_count,
    category_label,
    time_prep,
    time_assess,
    storage_label,
    pickup_loc,
    origin_zone_label,
    shelter_label
):
    """Callback function for Gradio interface."""
    category_key = CATEGORY_MAP.get(category_label, "cooked_grains_curry")
    storage_key = STORAGE_MAP.get(storage_label, "ambient")
    origin_zone = ZONE_MAP.get(origin_zone_label, 4)

    if not time_assess or not time_assess.strip():
        time_assess = datetime.now().strftime("%H:%M")

    res = pipeline.evaluate_surplus(
        item=item_name,
        servings=int(servings_count),
        category_key=category_key,
        time_prepared=time_prep,
        assessment_time=time_assess,
        storage_condition=storage_key,
        origin_zone=origin_zone,
        shelter_display_name=shelter_label,
        pickup_location=pickup_loc
    )

    eval_data = res["evaluation"]
    timeline = eval_data["timeline"]
    status = eval_data["status"]

    # Format Status Header
    if status == "COMPLIANT_SAFE":
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"✅ **Safety Window:** Safe until **{timeline['safe_pickup_by']} IST** "
            f"({timeline['max_allowed_minutes'] - timeline['total_exposure_minutes']} mins buffer remaining).\n\n"
            f"⏱️ **Elapsed:** {timeline['elapsed_minutes']} mins | "
            f"🚚 **Estimated Transit:** {timeline['transit_minutes']} mins\n\n"
            f"ℹ️ **Summary:** {eval_data['reason']}"
        )
    elif status == "COMPLIANT_URGENT":
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"⚠️ **Attention Required:** Handover and consumption must occur before **{timeline['safe_pickup_by']} IST**.\n\n"
            f"⏱️ **Elapsed:** {timeline['elapsed_minutes']} mins | "
            f"🚚 **Transit:** {timeline['transit_minutes']} mins | "
            f"⚠️ **Remaining Window:** {timeline['max_allowed_minutes'] - timeline['total_exposure_minutes']} mins\n\n"
            f"ℹ️ **Action:** {eval_data['reason']}"
        )
    else:
        status_md = (
            f"### {eval_data['badge']}\n\n"
            f"🛑 **Redistribution Blocked:** Cannot be dispatched for human consumption.\n\n"
            f"⚠️ **Reason:** {eval_data['reason']}\n\n"
            f"♻️ **Mandatory Municipal Action:** {eval_data['lnn_action']}"
        )

    # Format Retrieved Clauses
    retrieved_md = "#### 📜 Retrieved Statutory Clauses (FSSAI 2019 & LNN By-Laws):\n\n"
    for r in eval_data.get("retrieved_rules", []):
        retrieved_md += (
            f"- **[{r.get('id')}] {r.get('clause')}** *(Relevance Score: {r.get('relevance_score', 0):.2f})*\n"
            f"  > *\"{r.get('text')}\"*\n\n"
        )

    return (
        status_md,
        res["broadcast_message"],
        retrieved_md,
        res["audit_manifest"]
    )


def regulatory_search_flow(query_text):
    """Direct QA search over FSSAI and LNN regulations."""
    if not query_text or len(query_text.strip()) < 3:
        return "Please enter a search query (e.g., 'ambient holding time', 'Lucknow dumping penalty')."

    matches = pipeline.query_regulations(query_text, top_k=3)
    if not matches:
        return "No specific regulatory clauses matched your query. Try different terms."

    result_md = f"### 🔍 Retrieved Clauses for: *\"{query_text}\"*\n\n"
    for idx, doc in enumerate(matches, 1):
        result_md += (
            f"### {idx}. [{doc.get('id')}] {doc.get('title')}\n"
            f"**Authority:** {doc.get('source_authority')} ({doc.get('source_type')})\n\n"
            f"**Clause Reference:** {doc.get('clause')}\n\n"
            f"> {doc.get('text')}\n\n"
            f"*Keywords:* `{'`, `'.join(doc.get('keywords', []))}` | *Score:* `{doc.get('relevance_score', 0):.3f}`\n\n"
            "---\n\n"
        )
    return result_md


# Launch Gradio interface if gradio is available; otherwise run fallback message
try:
    import gradio as gr

    with gr.Blocks(title="Anna-Setu: AI Campus Food Rescue & Redistribution Network", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🍽️ Anna-Setu: AI Campus Food Rescue & Redistribution Network")
        gr.Markdown(
            "### 1M1B Virtual Internship • Powered by IBM Granite Models & RAG Compliance Pipeline\n"
            "*Grounded in FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam (LNN) Food Service By-Laws*"
        )

        with gr.Tabs():
            with gr.TabItem("📋 Surplus Handoff & Compliance Evaluation"):
                with gr.Row():
                    with gr.Column(scale=5):
                        gr.Markdown("### 🍛 Cafeteria Service Handoff Logs")
                        item = gr.Textbox(
                            label="Surplus Food Item(s)",
                            value="Vegetable pulao and dal tadka"
                        )
                        servings = gr.Number(
                            label="Estimated Servings Leftover",
                            value=45,
                            precision=0
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
                        storage = gr.Dropdown(
                            label="Storage & Holding Condition",
                            choices=[label for label, _ in STORAGE_CHOICES],
                            value=STORAGE_CHOICES[0][0]
                        )
                        pickup_loc = gr.Textbox(
                            label="Campus Pickup Location",
                            value="Main Campus Dining Hall, Gate 2"
                        )
                        with gr.Row():
                            origin_zone = gr.Dropdown(
                                label="Campus Origin Zone (Lucknow)",
                                choices=[label for label, _ in ZONE_CHOICES],
                                value=ZONE_CHOICES[0][0]
                            )
                            shelter = gr.Dropdown(
                                label="Matched Shelter / Rain Basera Destination",
                                choices=SHELTER_NAMES,
                                value=SHELTER_NAMES[0]
                            )

                        btn_eval = gr.Button("🔍 Run RAG Verification & Generate IBM Granite Alert", variant="primary")

                    with gr.Column(scale=5):
                        gr.Markdown("### 🛡️ AI Compliance Assessment & RAG Output")
                        status_box = gr.Markdown(value="*Click the button to evaluate surplus food safety.*")
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

                btn_eval.click(
                    fn=evaluate_surplus_flow,
                    inputs=[item, servings, category, time_prep, time_assess, storage, pickup_loc, origin_zone, shelter],
                    outputs=[status_box, output_msg, rag_clauses_box, manifest_box]
                )

            with gr.TabItem("🔎 Regulatory Knowledge Base Explorer"):
                gr.Markdown("### 🏛️ Search Official FSSAI & Lucknow Nagar Nigam Regulations")
                gr.Markdown("Query the RAG vector index directly for specific legal clauses, holding thresholds, transit limits, and waste penalties.")
                with gr.Row():
                    query_input = gr.Textbox(
                        label="Regulatory Query",
                        placeholder="e.g. ambient holding time limit, danger zone temperature, dumping penalty in Lucknow, raw salad rules",
                        value="What is the ambient holding time limit for cooked dal and rice under FSSAI?"
                    )
                    btn_search = gr.Button("Search Regulations", variant="secondary")

                reg_results = gr.Markdown()
                btn_search.click(fn=regulatory_search_flow, inputs=query_input, outputs=reg_results)

    if __name__ == "__main__":
        demo.launch()

except ImportError:
    # If gradio is not installed in the local environment, print instructions
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
            shelter_display_name=SHELTER_NAMES[0],
            pickup_location="Main Campus Mess, Gate 2"
        )
        print(res["broadcast_message"])
