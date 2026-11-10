"""
Generates the comprehensive PankhuriGovila_YIRP_Project_Tracker.xlsx
for the 1M1B AI for Sustainability Virtual Internship.
Updated with Track B: Smart Plate-Waste Interceptor & Bio-Recycling Converter.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_project_tracker():
    wb = openpyxl.Workbook()
    
    header_fill = PatternFill(start_color="1B4D3E", end_color="1B4D3E", fill_type="solid") # Dark Forest Green
    sub_fill = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")    # Soft Mint Green
    completed_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid") # Soft Green
    in_progress_fill = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid") # Soft Yellow
    planned_fill = PatternFill(start_color="E2E3E5", end_color="E2E3E5", fill_type="solid") # Soft Gray
    
    white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=16, bold=True, color="1B4D3E")
    bold_font = Font(name="Calibri", size=11, bold=True)
    regular_font = Font(name="Calibri", size=11)
    
    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )
    
    # -------------------------------------------------------------
    # TAB 1: Project Overview & Meta Info
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Project Overview"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "ANNA-SETU: 1M1B YIRP PROJECT TRACKER & OVERVIEW"
    ws1["A1"].font = title_font
    ws1["A1"].alignment = Alignment(horizontal="left", vertical="center")
    
    meta_info = [
        ("Project Title:", "Anna-Setu: AI Campus Food Rescue & Plate-Waste Bio-Recycling Network"),
        ("Student / Intern Name:", "Pankhuri Govila"),
        ("Institution:", "University of Petroleum and Energy Studies (UPES)"),
        ("Internship Program:", "1M1B AI for Sustainability Virtual Internship (In Collab with IBM SkillsBuild & AICTE)"),
        ("1M1B Mentor / Lead:", "Paramjeet Sir (paramjeet@onemoneb.org)"),
        ("Target Completion:", "Prototype & Approvals: End Nov 2026 | Full Campus Deployment: End Dec 2026"),
        ("Primary SDG:", "SDG 12: Responsible Consumption and Production (Target 12.3 - Halving Food Waste)"),
        ("Secondary SDGs:", "SDG 2: Zero Hunger, SDG 11: Sustainable Cities & SDG 13: Climate Action"),
        ("Dual-Track Model:", "Track A: AI Software Platform + Track B: Plate-Waste Upcycling Hardware Station"),
        ("Track A (Software):", "Campus Dining Demand Advisor + FSSAI/LNN RAG Regulatory Compliance Engine + IBM Granite Compiler"),
        ("Track B (Hardware):", "Smart Plate-Waste Interceptor & Bio-Recycling Converter (Behavioral Nudge Screen + Upcycling to Fertilizer)"),
        ("GitHub Repository:", "https://github.com/pgovila/Anna-Setu-Project"),
        ("Live Web App (Gradio):", "https://huggingface.co/spaces/pgovila/Anna-Setu-Demo"),
        ("Project Assets Drive:", "https://drive.google.com/drive/folders/1089iQX6AttZPXIuL8e6_bv6nGzkhyZW3?usp=sharing"),
        ("Statutory Document:", "FOOD_REGULATIONS_AND_LNN_GUIDELINES.md (FSSAI 2019 & Lucknow SWM By-Laws)")
    ]
    
    for r_idx, (k, v) in enumerate(meta_info, start=3):
        ws1[f"A{r_idx}"] = k
        ws1[f"A{r_idx}"].font = bold_font
        ws1[f"B{r_idx}"] = v
        ws1[f"B{r_idx}"].font = regular_font
        ws1.merge_cells(f"B{r_idx}:F{r_idx}")

    # -------------------------------------------------------------
    # TAB 2: Work Activity & Progress Tracker
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Activity Tracker")
    ws2.views.sheetView[0].showGridLines = True
    
    headers = [
        "Task ID", "Track", "Milestone / Phase", "Task / Activity Description", 
        "Detailed Work Done & Deliverables", "Start Date", "Target Date", 
        "Actual Date", "Status", "% Complete", "Links / Artifacts", "Any help from 1M1B"
    ]
    
    for col_idx, h in enumerate(headers, start=1):
        cell = ws2.cell(row=1, column=col_idx, value=h)
        cell.font = white_bold
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    tasks = [
        # Track A: Software & RAG
        ("TSK-01", "Track A (Software)", "Phase 1: Foundation", "Project Scoping & SDG Problem Statement Framing",
         "Defined core problem: 10-30% buffer overcooking in cafeterias and post-consumer plate waste; mapped to SDG 12.3 & SDG 2. Published report & slides.",
         "2026-09-01", "2026-09-20", "2026-09-20", "Completed", 1.0,
         "https://drive.google.com/drive/folders/1089iQX6AttZPXIuL8e6_bv6nGzkhyZW3?usp=sharing",
         "None at this stage; completed standard internship framing."),
         
        ("TSK-02", "Track A (Software)", "Phase 1: Foundation", "Initial Gradio UI Prototype & Hugging Face Deploy",
         "Engineered interactive web demo with input fields for food item, portions, prep time, and simulated Granite compiler. Deployed live on Hugging Face Spaces.",
         "2026-09-15", "2026-09-25", "2026-09-25", "Completed", 1.0,
         "https://huggingface.co/spaces/pgovila/Anna-Setu-Demo",
         "Guidance on integrating IBM Granite model weights or direct API endpoints."),
         
        ("TSK-03", "Track A (Software)", "Phase 2: RAG Subsystem", "Codify FSSAI & Lucknow Nagar Nigam Regulations",
         "Constructed structured knowledge bases: fssai_guidelines.json (holding times, danger zone 5-65C, 2h/4h rule) and lnn_guidelines.json (45m transit, Rain Basera network, biomethanation diversion).",
         "2026-10-15", "2026-11-05", "2026-11-08", "Completed", 1.0,
         "FOOD_REGULATIONS_AND_LNN_GUIDELINES.md",
         "Validation of legal templates for FSSAI Good Samaritan protection."),
         
        ("TSK-04", "Track A (Software)", "Phase 2: RAG Subsystem", "RAG Semantic Vector Retriever & Engine Build",
         "Built TF-IDF n-gram vector retriever, deterministic compliance calculator across Lucknow municipal zones, and Granite notification compiler with Form B audit manifests.",
         "2026-11-01", "2026-11-10", "2026-11-10", "Completed", 1.0,
         "test_rag.py",
         "Feedback on enterprise scaling of vector indexing."),
         
        ("TSK-05", "Track A (Software)", "Phase 2: RAG Subsystem", "Dual UI Implementation (Gradio + Streamlit)",
         "Upgraded app.py for Hugging Face Spaces and built streamlit_app.py for local interactive testing with live metric cards, zone transit calculators, and regulatory search.",
         "2026-11-08", "2026-11-10", "2026-11-10", "Completed", 1.0,
         "streamlit_app.py",
         "Assistance with server hosting if deploying full multi-tenant instance."),
         
        # Track B: Hardware Instrument (Plate Waste Interceptor & Recycler)
        ("TSK-06", "Track B (Hardware)", "Phase 2: HW Conceptualization", "Smart Plate-Waste Interceptor & Bio-Recycler Architecture",
         "Engineered architecture for tray-return station: plate-waste weighing scale (0-20 kg) + behavioral nudge screen (displaying wasted grams & water footprint) + thermal accelerated aerobic composting chamber to convert scraps into organic bio-fertilizer.",
         "2026-11-05", "2026-11-15", "2026-11-10", "Completed", 1.0,
         "PROJECT_BRIEF_TIMELINE_AND_TRACKER.md",
         "1M1B technical mentor review of IoT schematic and composting mechanical design."),
         
        ("TSK-07", "Track B (Hardware)", "Phase 3: HW Breadboard", "Procure Components & Build Bench Breadboard Prototype",
         "Sourcing ESP32 micro-controller, HX711 load cell amp, LCD/OLED behavioral display, heating element/fan relay, and assembling bench test circuit.",
         "2026-11-11", "2026-11-20", "", "In Progress", 0.45,
         "firmware/esp32_smart_kiosk.ino",
         "Support or recommendation for student hardware lab grants / maker-space access."),
         
        ("TSK-08", "Track B (Hardware)", "Phase 3: HW Breadboard", "Firmware Development & Cloud Telemetry API Bridge",
         "Written Arduino/C++ firmware (esp32_smart_kiosk.ino) to read plate waste, calculate student impact metrics, and post telemetry to Anna-Setu API over Wi-Fi.",
         "2026-11-15", "2026-11-23", "2026-11-10", "Completed", 1.0,
         "api_server.py & firmware/esp32_smart_kiosk.ino",
         "Feedback on optimal data sync frequency for low-power edge nodes."),
         
        # Approvals & Milestone 1 (End November 2026)
        ("TSK-09", "Approvals & Gov", "Phase 3: Approvals", "Draft Institutional MoU & Campus Mess Permission Letter",
         "Draft formal pilot request letter to University Mess Committee, Chief Warden, and Dean of Student Welfare (UPES) for permission to install the interceptor in the dining hall and pilot composting.",
         "2026-11-18", "2026-11-27", "", "Planned", 0.20,
         "Draft Permission Letter to Campus Administration",
         "Official 1M1B / IBM SkillsBuild Internship Endorsement Letter to College Principal/Dean."),
         
        ("TSK-10", "Approvals & Gov", "Phase 3: Approvals", "Lucknow Shelter Coordination & Handoff Agreement",
         "Establish formal contact with Rain Basera Charbagh / Lucknow Roti Bank coordinators to align on daily pickup time window and volunteer dispatch protocol.",
         "2026-11-20", "2026-11-28", "", "Planned", 0.15,
         "Partner NGO Acknowledgement / Consent Slip",
         "Introduction or network referral to verified hunger-relief NGO partners in UP."),
         
        ("TSK-11", "Integrated", "Milestone 1 Gate", "Milestone 1 Gate Review: Integrated Prototype & Approvals",
         "Demonstrate bench prototype of Track B hardware talking to Track A app; present signed campus pilot approval. Formal checkpoint with 1M1B mentor.",
         "2026-11-25", "2026-11-30", "", "Planned", 0.10,
         "Milestone 1 Prototype Demo Video & Approval Dossier",
         "Review and evaluation session with Paramjeet Sir (paramjeet@onemoneb.org)."),
         
        # Phase 4 & 5: Live Pilot Deployment (December 2026)
        ("TSK-12", "Integrated", "Phase 4: Field Pilot", "Enclosure Fabrication & Station Installation at Tray Return",
         "Install splash-proof stainless steel enclosure at cafeteria tray return; mount load cell deck, behavioral display, and connect bio-composting shredder module.",
         "2026-12-01", "2026-12-07", "", "Planned", 0.0,
         "On-site Installation Photographs & Calibration Logs",
         "Guidance on food-grade sanitary enclosure compliance."),
         
        ("TSK-13", "Integrated", "Phase 4: Field Pilot", "Live 2-Week Campus Pilot Run (Central Dining Hall)",
         "Run end-to-end operational pilot: measure reduction in student plate waste via nudge screen, evaluate kitchen surplus through RAG, dispatch meals, and convert plate waste into organic fertilizer on-site.",
         "2026-12-08", "2026-12-21", "", "Planned", 0.0,
         "Daily Pilot Logs (Meals Saved, Kg Diverted, Compost Produced)",
         "Mid-pilot troubleshooting check-in."),
         
        ("TSK-14", "Track A (Software)", "Phase 5: Evaluation", "Module 1 Demand Forecast Retraining on Real Waste Data",
         "Feed real plate-waste logs captured by Track B hardware back into Module 1 forecasting model to validate reduction in overproduction margins.",
         "2026-12-20", "2026-12-26", "", "Planned", 0.0,
         "Model Evaluation Metric Graphs (RMSE, % Waste Reduced)",
         "Advice on time-series feature weighting for academic calendars."),
         
        ("TSK-15", "Integrated", "Milestone 2 Gate", "Final Project Deployment, Impact Report & Video Submission",
         "Final project compilation: quantified impact statement (meals rescued, kg converted to bio-fertilizer, methane avoided, ₹ saved), full demo video, updated PPT, and submission to 1M1B.",
         "2026-12-24", "2026-12-31", "", "Planned", 0.0,
         "Final Project Report (PDF), PPT, Video Walkthrough",
         "Final evaluation, certification endorsement, and nomination for showcase.")
    ]
    
    for row_idx, t in enumerate(tasks, start=2):
        for col_idx, val in enumerate(t, start=1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if col_idx in (1, 6, 7, 8):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 9:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if val == "Completed":
                    cell.fill = completed_fill
                    cell.font = Font(name="Calibri", size=11, bold=True, color="155724")
                elif val == "In Progress":
                    cell.fill = in_progress_fill
                    cell.font = Font(name="Calibri", size=11, bold=True, color="856404")
                else:
                    cell.fill = planned_fill
                    cell.font = Font(name="Calibri", size=11, color="383D41")
            elif col_idx == 10:
                cell.number_format = '0%'
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 12:
                cell.fill = sub_fill
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------
    # TAB 3: Track B Hardware Specifications (Bio-Recycling Station)
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Track B Hardware Specs")
    ws3.views.sheetView[0].showGridLines = True
    
    hw_headers = ["Module / Subsystem", "Component / Sensor", "Technical Specification", "Estimated Cost (INR)", "Primary Functional Role in Anna-Setu"]
    for col_idx, h in enumerate(hw_headers, start=1):
        cell = ws3.cell(row=1, column=col_idx, value=h)
        cell.font = white_bold
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    bom_data = [
        ("Core Compute & IoT", "ESP32 Dev Module (WROOM-32)", "Dual-Core 240MHz, Wi-Fi & Bluetooth BLE, 4MB Flash", 450, "Coordinates load cells, updates behavioral display, posts JSON telemetry to Track A"),
        ("Plate Waste Scale", "Load Cell (0-20 kg) + HX711", "Precision bar load cell, 24-bit ADC amplifier", 550, "Measures exact plate waste left on individual student tray at return counter"),
        ("Behavioral Nudge Screen", "7-inch HDMI/I2C Display / OLED", "1024x600 IPS LCD or 0.96 OLED Nudge Display", 850, "Displays instantaneous wasted grams, embedded water footprint, & green dining points"),
        ("Surplus Thermal Probe", "MLX90614 Contactless IR Probe", "Non-contact Infrared Sensor (-70C to 380C)", 750, "Checks kitchen batch temperature to verify if food is held safely >=65C before donation"),
        ("Composting Aeration Fan", "12V Brushless Exhaust Fan", "High-airflow 12V DC fan with carbon filter", 250, "Provides active aerobic aeration in composting vessel, preventing foul odors"),
        ("Thermo-Heater Strip", "100W PTC Ceramic Heating Strip", "55C - 65C Thermostatically controlled heating element", 450, "Maintains thermophilic stage (55-65C) to accelerate microbial decomposition & kill pathogens"),
        ("Power & Relay Controller", "12V 5A Power Adapter + 4-Ch Relay", "Regulated multi-channel isolated relay module", 420, "Powers MCU, heater, exhaust fan, and optical indicators"),
        ("Sanitary Station Enclosure", "Stainless Steel / Food-Grade Acrylic", "Waterproof IP65 tray counter housing with drop chute", 950, "Durable, cleanable cafeteria housing with chute directly into composting container"),
        ("TOTAL HARDWARE BOM", "Bio-Recycling Station Prototype", "Integrated Behavioral Interceptor & Rapid Composter", 4670, "Affordable, high-impact student innovation under INR 4,700 (~USD 55)")
    ]
    
    for row_idx, item in enumerate(bom_data, start=2):
        for col_idx, val in enumerate(item, start=1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            cell.font = bold_font if row_idx == len(bom_data) + 1 else regular_font
            cell.border = thin_border
            if col_idx == 4:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '₹#,##0'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Column dimensions
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)
            
    ws2.column_dimensions['A'].width = 10
    ws2.column_dimensions['B'].width = 18
    ws2.column_dimensions['C'].width = 18
    ws2.column_dimensions['D'].width = 34
    ws2.column_dimensions['E'].width = 48
    ws2.column_dimensions['F'].width = 13
    ws2.column_dimensions['G'].width = 13
    ws2.column_dimensions['H'].width = 13
    ws2.column_dimensions['I'].width = 14
    ws2.column_dimensions['J'].width = 12
    ws2.column_dimensions['K'].width = 32
    ws2.column_dimensions['L'].width = 38

    file_path = "PankhuriGovila_YIRP_Project_Tracker.xlsx"
    wb.save(file_path)
    print(f"Project Tracker Excel successfully updated at: {file_path}")

if __name__ == "__main__":
    create_project_tracker()
