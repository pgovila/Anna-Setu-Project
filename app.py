import gradio as gr

def anna_setu_workflow(item, servings, time_prepared, location, compliance, shelter):
    safe_pickup = "15:30" 
    
    alert_msg = (
        f"🍽️ *Surplus Food Alert — Anna-Setu*\n\n"
        f"Hi {shelter} team, we have {int(servings)} servings of {item} ready for pickup, "
        f"prepared at {time_prepared} and safe until {safe_pickup} ({compliance}).\n\n"
        f"📍 *Pickup point:* {location}.\n\n"
        f"Please reply *YES* to confirm pickup, or call the manager directly to adjust the arrival window. Thank you for partnering with us!"
    )
    return alert_msg

# Custom UI layout styling matching the project report specifications
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍽️ Anna-Setu: AI Campus Food Rescue & Redistribution Network")
    gr.Markdown("### 1M1B Virtual Internship • Powered by IBM Granite Models & RAG Simulation")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📋 Cafeteria Service Handoff Logs")
            item = gr.Textbox(label="Surplus Food Item(s)", value="Vegetable pulao and dal")
            servings = gr.Number(label="Estimated Servings Leftover", value=45)
            time_prepared = gr.Textbox(label="Time Prepared (HH:MM)", value="13:05")
            location = gr.Textbox(label="Pickup Point Location", value="Main Campus Mess, Gate 2")
            
            gr.Markdown("### 🧠 Simulated AI Pipeline Configurations")
            compliance = gr.Textbox(label="Retrieved Safety Compliance Rule (RAG)", value="Within 3-hour ambient holding limit per municipal food hygiene standard Sec-4.")
            shelter = gr.Textbox(label="AI Matched Shelter Destination", value="Asha Community Shelter (2.1 km away)")
            
            btn = gr.Button("Execute IBM Granite Notification Compiler", variant="primary")
            
        with gr.Column():
            gr.Markdown("### ✅ Generated Output (WhatsApp / SMS Ready Format)")
            output = gr.TextArea(label="AI-Drafted Broadcast Message", interactive=False, lines=10)
            gr.Markdown("*Note: In production, this output is validated via a Human-in-the-Loop admin verification step before dispatching to the Twilio/WhatsApp API provider.*")

    btn.click(fn=anna_setu_workflow, inputs=[item, servings, time_prepared, location, compliance, shelter], outputs=output)

demo.launch()
