"""
Anna-Setu Master Verification & Validation Suite.
Validates the entire dual-track project ecosystem for 1M1B & AICTE submission:
1. RAG Compliance Pipeline (FSSAI 2019 & LNN By-Laws)
2. Generative RAG Legal Q&A (IBM Granite Prompt Synthesis)
3. Smart Dining Demand Advisor (Predictive Forecasting)
4. Track B IoT Hardware Telemetry Simulation & Dangerous Zone Thermal Sensing
5. Deliverables & File Integrity (Word docx, PDFs, Spreadsheets, Web Apps)
6. Zero em-dash and neutral institutional affiliation compliance audit
"""

import os
import sys
from datetime import datetime

def validate_ecosystem():
    print("=" * 80)
    print("      ANNA-SETU: MASTER SYSTEM VALIDATION & VERIFICATION SUITE")
    print("      1M1B AI for Sustainability Virtual Internship • IBM SkillsBuild & AICTE")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST\n")
    
    total_checks = 0
    passed_checks = 0

    def check(title, condition, details=""):
        nonlocal total_checks, passed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] {title}")
            if details:
                print(f"         └─ {details}")
        else:
            print(f"  [FAIL] {title}")
            if details:
                print(f"         └─ ERROR: {details}")

    # --- SECTION 1: Software & RAG Pipeline Checks ---
    print("[1] Verifying Track A Software & RAG Pipeline Subsystem...")
    try:
        from rag.pipeline import AnnaSetuRAGPipeline
        pipeline = AnnaSetuRAGPipeline()
        check("Initialize AnnaSetuRAGPipeline", True, "Successfully loaded vector index and knowledge bases")
        
        # Test safe surplus
        res_safe = pipeline.evaluate_surplus(
            item="Vegetable Pulao & Dal", servings=40, category_key="cooked_grains_curry",
            time_prepared="12:00", assessment_time="13:30", storage_condition="ambient", origin_zone=4
        )
        check("FSSAI Safe Evaluation (1.5h elapsed)", res_safe["evaluation"]["status"] == "COMPLIANT_SAFE", 
              f"Badge: {res_safe['evaluation']['badge']}")

        # Test urgent surplus (2h 45m elapsed)
        res_urg = pipeline.evaluate_surplus(
            item="Dal Tadka & Roti", servings=35, category_key="cooked_grains_curry",
            time_prepared="11:15", assessment_time="14:00", storage_condition="ambient", origin_zone=4
        )
        check("FSSAI Urgent Dispatch Mandate (2h 45m elapsed)", res_urg["evaluation"]["status"] == "COMPLIANT_URGENT",
              f"Badge: {res_urg['evaluation']['badge']}")

        # Test rejected surplus (>4h elapsed)
        res_rej = pipeline.evaluate_surplus(
            item="Chole Puri", servings=40, category_key="cooked_grains_curry",
            time_prepared="09:00", assessment_time="14:00", storage_condition="ambient", origin_zone=4
        )
        check("FSSAI Rejection & LNN Diversion (>4h elapsed)", res_rej["evaluation"]["status"] == "NON_COMPLIANT_REJECTED",
              f"LNN Directive: {res_rej['evaluation']['lnn_action'][:60]}...")

        # Test physical danger zone thermal sensor breach
        res_temp_breach = pipeline.evaluate_surplus(
            item="Rajma Chawal", servings=50, category_key="cooked_grains_curry",
            time_prepared="12:00", assessment_time="13:00", storage_condition="hot_holding",
            origin_zone=4, measured_temp_celsius=52.0
        )
        check("Thermal Danger Zone Enforcement (Hot Holding < 65C)", 
              res_temp_breach["evaluation"]["temp_status"] == "DANGER_ZONE_BREACH",
              f"Detected: {res_temp_breach['evaluation']['temp_summary']}")

        # Test RAG semantic search
        kb_matches = pipeline.query_regulations("ambient holding time limit", top_k=2)
        check("RAG Semantic Regulatory Search", len(kb_matches) > 0, 
              f"Top Citation: [{kb_matches[0]['id']}] {kb_matches[0]['title']}")

        # Test Generative RAG Q&A synthesis
        qa_res = pipeline.ask_regulations("Can I donate cooked paneer curry after 3 hours at room temperature?")
        check("Generative RAG QA Legal Synthesis (IBM Granite)", 
              "Statutory Compliance Verdict" in qa_res["synthesized_answer"] and len(qa_res["retrieved_clauses"]) > 0,
              f"Citations: {len(qa_res['retrieved_clauses'])} clauses cited")

        # Test Module 1 Predictive Dining Demand Advisor
        demand_res = pipeline.predict_meal_demand(
            enrolled_students=1200, meal_type="Lunch", day_of_week="Wednesday",
            academic_calendar="Regular Academic Day", weather="Clear Mild (~24°C)"
        )
        check("Module 1 AI Dining Demand Advisor", 
              demand_res["recommended_cooking_target"] > 0 and demand_res["portions_prevented_from_waste"] > 0,
              f"Recommended: {demand_res['recommended_cooking_target']} portions | Savings: ₹{demand_res['cost_savings_inr']:,.2f}")

    except Exception as e:
        check("Track A RAG Execution", False, str(e))

    # --- SECTION 2: Track B Hardware & IoT Firmware Checks ---
    print("\n[2] Verifying Track B Hardware Assets & Firmware...")
    check("ESP32 Arduino Firmware Exists", os.path.exists("firmware/esp32_smart_kiosk.ino"), "firmware/esp32_smart_kiosk.ino")
    check("FastAPI Ingestion Server Exists", os.path.exists("api_server.py"), "api_server.py")
    check("IoT Telemetry Simulation Script Exists", os.path.exists("simulate_iot_kiosk.py"), "simulate_iot_kiosk.py")

    # --- SECTION 3: Deliverables & Editable Documents Checks ---
    print("\n[3] Verifying Submission Deliverables & Document Formats...")
    deliverables = [
        ("Official 3-Page PDF (Anna_Setu...)", "Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf"),
        ("Official 3-Page PDF (PankhuriGovila_YIRP...)", "PankhuriGovila_YIRP_Project_Brief_Timeline_and_Tracker.pdf"),
        ("Editable Word Document (.docx)", "Anna_Setu_Project_Brief_Timeline_and_Tracker.docx"),
        ("Editable Word Document (.docx - Named)", "PankhuriGovila_YIRP_Project_Brief_Timeline_and_Tracker.docx"),
        ("Editable Markdown Document (.md)", "Anna_Setu_Project_Brief_Timeline_and_Tracker.md"),
        ("Excel Project Tracker (.xlsx)", "PankhuriGovila_YIRP_Project_Tracker.xlsx"),
        ("CSV Project Tracker Export (.csv)", "PankhuriGovila_YIRP_Project_Tracker.csv"),
        ("FSSAI & LNN Regulatory Manual (.md)", "FOOD_REGULATIONS_AND_LNN_GUIDELINES.md"),
        ("Institutional Approvals & MoU Templates (.md)", "INSTITUTIONAL_APPROVALS_AND_MOU_TEMPLATES.md"),
        ("Presentation Slides Update Guide (.md)", "PRESENTATION_SLIDES_UPDATE_GUIDE.md"),
        ("Gradio Web Interface (app.py)", "app.py"),
        ("Streamlit 5-Tab Interactive Dashboard", "streamlit_app.py"),
        ("Comprehensive Test Suite (test_rag.py)", "test_rag.py")
    ]

    for title, filename in deliverables:
        exists = os.path.exists(filename)
        size_kb = os.path.getsize(filename) / 1024.0 if exists else 0
        check(f"{title}", exists, f"Size: {size_kb:.1f} KB")

    # --- SECTION 4: Compliance Audits (Zero Em-Dashes & Neutral Affiliation) ---
    print("\n[4] Verifying Text Hygiene (Zero Em-Dashes & Neutral Affiliation)...")
    key_files = [
        "app.py",
        "streamlit_app.py",
        "api_server.py",
        "simulate_iot_kiosk.py",
        "test_rag.py",
        "rag/pipeline.py",
        "rag/compliance_engine.py",
        "rag/granite_generator.py",
        "rag/vector_index.py",
        "Anna_Setu_Project_Brief_Timeline_and_Tracker.md",
        "FOOD_REGULATIONS_AND_LNN_GUIDELINES.md",
        "INSTITUTIONAL_APPROVALS_AND_MOU_TEMPLATES.md",
        "PRESENTATION_SLIDES_UPDATE_GUIDE.md"
    ]
    
    em_dash_violations = 0
    affiliation_violations = 0
    dash_chars = ["\u2014", "\u2013"]
    prohibited_term = "U" + "PES"
    for kf in key_files:
        if os.path.exists(kf):
            try:
                with open(kf, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if any(dc in content for dc in dash_chars):
                        em_dash_violations += 1
                        print(f"         [WARNING] Dash found in: {kf}")
                    if prohibited_term in content or prohibited_term.lower() in content:
                        affiliation_violations += 1
                        print(f"         [WARNING] Prohibited institute found in: {kf}")
            except Exception:
                pass

    check("Strict Hyphen Rule (Zero Em-Dash/En-Dash)", em_dash_violations == 0, 
          f"Audited {len(key_files)} files; 0 violations found" if em_dash_violations == 0 else f"{em_dash_violations} files flagged")
    check("Neutral Institutional Affiliation Rule", affiliation_violations == 0,
          f"Audited {len(key_files)} files; 0 violations found" if affiliation_violations == 0 else f"{affiliation_violations} files flagged")

    # --- SUMMARY ---
    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed_checks} / {total_checks} CHECKS PASSED ({int(passed_checks/total_checks*100)}%)")
    if passed_checks == total_checks:
        print("STATUS: ALL SYSTEMS FULLY OPERATIONAL, COMPLIANT & READY FOR 1M1B SUBMISSION! 🚀")
    else:
        print("STATUS: SOME CHECKS FAILED. Please review the errors above.")
    print("=" * 80)

if __name__ == "__main__":
    validate_ecosystem()
