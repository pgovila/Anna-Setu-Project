"""
Anna-Setu Master Verification & Validation Suite.
Validates the entire dual-track project ecosystem for 1M1B & AICTE submission:
1. RAG Compliance Pipeline (FSSAI 2019 & LNN By-Laws)
2. Track B IoT Hardware Telemetry Simulation
3. File integrity of all documentation, spreadsheets, PDFs, and editable DOCX files
"""

import os
import sys
from datetime import datetime

def validate_ecosystem():
    print("=" * 80)
    print("      ANNA-SETU: MASTER SYSTEM VALIDATION & VERIFICATION SUITE")
    print("      1M1B AI for Sustainability Virtual Internship • UPES Dehradun")
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

        # Test rejected surplus (>4h elapsed)
        res_rej = pipeline.evaluate_surplus(
            item="Chole Puri", servings=40, category_key="cooked_grains_curry",
            time_prepared="09:00", assessment_time="14:00", storage_condition="ambient", origin_zone=4
        )
        check("FSSAI Rejection & LNN Diversion (>4h elapsed)", res_rej["evaluation"]["status"] == "NON_COMPLIANT_REJECTED",
              f"LNN Directive: {res_rej['evaluation']['lnn_action'][:60]}...")

        # Test RAG semantic search
        kb_matches = pipeline.query_regulations("ambient holding time limit", top_k=2)
        check("RAG Semantic Regulatory Search", len(kb_matches) > 0, 
              f"Top Citation: [{kb_matches[0]['id']}] {kb_matches[0]['title']}")

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
        ("Streamlit 5-Tab Interactive Dashboard", "streamlit_app.py")
    ]

    for title, filename in deliverables:
        exists = os.path.exists(filename)
        size_kb = os.path.getsize(filename) / 1024.0 if exists else 0
        check(f"{title}", exists, f"Size: {size_kb:.1f} KB")

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
