# Anna-Setu: AI Campus Food Rescue & Plate-Waste Bio-Recycling Network 🍽️♻️

### 1M1B AI for Sustainability Virtual Internship Project Submission
*In Collaboration with IBM SkillsBuild & AICTE*  
**Author / Student Lead:** Pankhuri Govila  
**Institution:** University of Petroleum and Energy Studies (UPES)  
**1M1B Mentor:** Paramjeet Sir (`paramjeet@onemoneb.org`)  
**Project Tracker Identifier:** `PankhuriGovila_YIRP`

---

## 🚀 Live System Deployments & Prototype Links
* **Interactive Web App (Gradio):** [Launch on Hugging Face Spaces](https://huggingface.co/spaces/pgovila/Anna-Setu-Demo)
* **Local Interactive Dashboard (Streamlit):** Run `streamlit run streamlit_app.py`
* **Google Drive Assets (Videos, Deck & Docs):** [Access 1M1B Project Folder](https://drive.google.com/drive/folders/1089iQX6AttZPXIuL8e6_bv6nGzkhyZW3?usp=sharing)
* **Official Executive Brief & Timeline (PDF):** [`Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf`](Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf)
* **Editable Word Document (.docx):** [`Anna_Setu_Project_Brief_Timeline_and_Tracker.docx`](Anna_Setu_Project_Brief_Timeline_and_Tracker.docx)
* **Google Sheets Master Tracker (.xlsx):** [`PankhuriGovila_YIRP_Project_Tracker.xlsx`](PankhuriGovila_YIRP_Project_Tracker.xlsx)

---

## 📌 Project Overview: The Closed-Loop Campus Food Framework
**Anna-Setu** (*"Anna"* meaning sustenance and *"Setu"* meaning bridge) is a closed-loop socio-technical framework engineered for higher education dining facilities. It tackles food waste across two structural friction points:
1. **At the Kitchen Level:** Blind, unforecasted overcooking creating 10%–30% buffer surplus.
2. **At the Diner Plate Level:** Students taking extra food onto their plates and dumping leftovers into general waste bins.

By coupling an AI predictive software platform (**Track A**) with an on-site smart plate-waste interceptor and bio-recycling instrument (**Track B**), Anna-Setu creates a **Zero-Waste Circular Campus Loop**: untouched kitchen surplus is legally redistributed to local shelters, while unconsumed plate scraps are intercepted and transformed on-site into a **recyclable element (organic bio-fertilizer)**, eliminating the waste burden on municipal authorities (Lucknow Nagar Nigam) and our planet Earth.

---

## 🎯 UN Sustainable Development Goal (SDG) Alignment
* **Primary SDG: SDG 12 — Responsible Consumption and Production**
  * *Target 12.3:* Halving per-capita global food waste at retail and consumer levels by 2030.
  * *Target 12.5:* Substantially reducing waste generation through prevention, reduction, recycling, and reuse.
* **Secondary SDG: SDG 2 — Zero Hunger**
  * *Target 2.1 & 2.2:* End hunger by redirecting wholesome, safety-verified meals to local night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar) and food banks.
* **Tertiary SDG: SDG 11 — Sustainable Cities and Communities**
  * *Target 11.6:* Relieves urban sanitation collection trucks and avoids ₹5,000–₹25,000 penalties under Lucknow Nagar Nigam Solid Waste By-Laws.
* **Quaternary SDG: SDG 13 — Climate Action**
  * Halts anaerobic landfill decomposition of organic waste, directly reducing fugitive methane ($CH_4$) emissions.

---

## 🤖 The Dual-Track Solution Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ANNA-SETU CIRCULAR CAMPUS FOOD LOOP                      │
└─────────────────────────────────────────────────────────────────────────────┘

    [Campus Kitchen Preparation]  ─────────>  [Student Dining / Plate Return]
               │                                                │
       (Untouched Surplus)                             (Uneaten Plate Scraps)
               │                                                │
               ▼                                                ▼
 ┌───────────────────────────┐                    ┌───────────────────────────┐
 │ TRACK A: ANNA-SETU APP    │                    │ TRACK B: BIO-CYCLE STATION│
 │ (AI Forecasting & RAG)    │                    │ (Behavioral Nudge & Bio-  │
 │ Grounded in FSSAI & LNN   │                    │  Recycling into Fertilizer│
 └─────────────┬─────────────┘                    └─────────────┬─────────────┘
               │                                                │
               ▼                                                ▼
  [Safe Redistribution to Rain                     [Recyclable Organic Bio-    │
   Basera Shelters & Food Banks]                    Fertilizer for Campus/Soil]│
```

### Track A: The Anna-Setu AI Software Platform
* **Module 1 — Smart Campus Dining Advisor (Predictive Forecasting):** Machine learning regression trained on historical swipe logs, academic calendars (exams, holidays), and weather to forecast next-day cooking quantities.
* **Module 2 — Statutory RAG Compliance Pipeline:**
  * Grounded in **FSSAI Surplus Regulations (2019)**: Microbial danger zone ($5^\circ\text{C}-65^\circ\text{C}$), ambient 2h/4h rule, prohibited food categories, and Good Samaritan legal immunity (Section 7).
  * Grounded in **Lucknow Nagar Nigam (LNN) By-Laws**: 45-minute municipal transit corridor ceiling across Lucknow Zones 1–8 and mandatory bio-compost diversion for non-compliant food (Section 18).
* **IBM Granite Model Compiler:** Generates WhatsApp/SMS alerts (<60w) and official **FSSAI Form B & LNN Gate Pass manifests**.

### Track B: Smart Plate-Waste Interceptor & Bio-Recycling Converter (Hardware)
* **Behavioral Nudge Front-End:** Precision plate scale (0–20 kg) at the dish-clearing counter + 7-inch display showing wasted grams, water footprint, and hostel leaderboards to stop diners from taking extra food.
* **Pre-Processing Shredder:** Reduces uneaten plate scraps to 3–5 mm particles.
* **Accelerated Bio-Composting Chamber ($55^\circ\text{C}-65^\circ\text{C}$):** Thermophilic heating + active aerobic aeration + microbial enzymes achieve an **85% to 90% volume reduction in 12–24 hours**.
* **Recyclable Output:** Converts waste into high-grade **Organic Bio-Fertilizer / Soil Conditioner** for campus greening and local farmers, eliminating municipal collection truck transport and landfill dumping.
* **Affordable Student BOM:** Built with off-the-shelf maker electronics for **₹4,670 (~$55 USD)**.

---

## 📁 Repository Structure
```text
├── app.py                                              # Gradio Interface (Hugging Face Spaces Deploy)
├── streamlit_app.py                                    # Streamlit 5-Tab Interactive Live Dashboard
├── api_server.py                                       # FastAPI Gateway connecting IoT Kiosks to Cloud RAG
├── simulate_iot_kiosk.py                               # Hardware Telemetry Simulation & Scenarios
├── test_rag.py                                         # Automated RAG Regulatory Verification Test Suite
├── validate_all.py                                     # Master Ecosystem Validation Script (19/19 Checks)
├── requirements.txt                                    # Python dependencies
│
├── Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf    # Official 3-Page Executive PDF Submission
├── Anna_Setu_Project_Brief_Timeline_and_Tracker.docx   # Editable Word Document (.docx)
├── Anna_Setu_Project_Brief_Timeline_and_Tracker.md     # Editable Markdown Document (.md)
├── PankhuriGovila_YIRP_Project_Tracker.xlsx            # Master Google Sheets Tracker (Excel Format)
├── PankhuriGovila_YIRP_Project_Tracker.csv             # Activity Tracker CSV Export
│
├── FOOD_REGULATIONS_AND_LNN_GUIDELINES.md              # In-Depth FSSAI (2019) & LNN Regulatory Manual
├── PROJECT_BRIEF_TIMELINE_AND_TRACKER.md               # Master Project Blueprint & Dual-Track Specs
├── INSTITUTIONAL_APPROVALS_AND_MOU_TEMPLATES.md        # Campus Permission Letters & Shelter MoU Dossier
├── PRESENTATION_SLIDES_UPDATE_GUIDE.md                 # 10-Slide Deck Presentation Guide
│
├── firmware/                                           # Track B Embedded Firmware
│   └── esp32_smart_kiosk.ino                           # ESP32 C++/Arduino Telemetry Firmware
│
└── rag/                                                # Anna-Setu RAG Regulatory Subsystem
    ├── __init__.py                                     # Package exports
    ├── retriever.py                                    # TF-IDF & Cosine Similarity Regulatory Vector Engine
    ├── compliance_engine.py                            # FSSAI Holding Time & LNN Transit Protocol Evaluator
    ├── granite_generator.py                            # IBM Granite Prompt Synthesis & Notification Compiler
    ├── pipeline.py                                     # Unified AnnaSetuRAGPipeline Interface
    └── knowledge_base/                                 # Regulatory Corpora
        ├── fssai_guidelines.json                       # FSSAI Surplus Food Regulations (2019) Clauses
        ├── lnn_guidelines.json                         # Lucknow Nagar Nigam Food Service & SWM By-Laws
        └── shelters_lucknow.json                       # Verified Lucknow Shelter Directory (Zones 1-8)
```

---

## 💻 Quick Start & Execution Commands

### 1. Run Automated Test Suites
```bash
# Verify RAG compliance engine across 5 real-world scenarios
python test_rag.py

# Simulate Track B IoT hardware telemetry events
python simulate_iot_kiosk.py

# Run master ecosystem validation
python validate_all.py
```

### 2. Launch Local Interactive Dashboard (Streamlit)
```bash
streamlit run streamlit_app.py
```

### 3. Start IoT Telemetry Gateway Server
```bash
python api_server.py
```

---

## 📅 Phased Execution Timeline (Nov – Dec 2026)
* **Phase 1 & 2 (Nov 1 – Nov 10, 2026) — [COMPLETED]:** Grounded RAG compliance pipeline in FSSAI (2019) & Lucknow Nagar Nigam by-laws; deployed Gradio and Streamlit interfaces; verified test cases.
* **Sprint 3A (Nov 11 – Nov 20, 2026) — [IN PROGRESS]:** Procure hardware components (ESP32, HX711, MLX90614); assemble bench breadboard; test firmware telemetry.
* **Sprint 3B (Nov 21 – Nov 30, 2026) — [MILESTONE 1 GATE]:** Secure campus mess permissions from Dean of Student Welfare / Mess Committee (UPES); establish coordination agreement with Rain Basera Charbagh; Milestone 1 review with 1M1B mentor.
* **Phase 4 (Dec 1 – Dec 21, 2026):** Install IP65 enclosure at tray return; execute 14-day live campus pilot in central mess; log plate-waste reduction via nudge screen; harvest bio-fertilizer.
* **Phase 5 (Dec 22 – Dec 31, 2026) — [MILESTONE 2 GATE]:** Retrain Module 1 demand model; compile quantified impact report; final project handover.

---

## 🛡️ Responsible AI Framework

| Pillar | Applied Implementation Logic |
| :--- | :--- |
| **Fairness** | Demand forecasting uses aggregate mess logs stripped of student demographics; demand predictions are audited across dietary preferences (vegetarian, non-vegetarian, Jain) to ensure balanced portioning. |
| **Transparency** | Explains every forecast with top 3 driver factors (e.g. "Predicted 15% reduction due to end-semester exam schedule"). |
| **Ethics** | Embedded verification blocks completely halt donation if a batch's holding time exceeds FSSAI 4-hour limits; non-compliant batches are strictly diverted to on-site composting. |
| **Privacy** | Student registration numbers are anonymized before log ingestion; no individual dietary data is shared externally. |
