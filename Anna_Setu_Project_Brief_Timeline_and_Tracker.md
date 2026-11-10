# 🍽️ ANNA-SETU: PROJECT BRIEF & PHASED TIMELINE
### 1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE

---

| **Field** | **Details** |
| :--- | :--- |
| **Intern / Author** | Pankhuri Govila |
| **Program** | 1M1B AI for Sustainability Virtual Internship |
| **1M1B Mentor** | Paramjeet Sir (`paramjeet@onemoneb.org`) |
| **Primary SDG** | SDG 12: Responsible Consumption & Production (Target 12.3 & 12.5) |
| **Dual-Track Model** | Track A (AI Software Platform) + Track B (Smart Bio-Recycler Hardware) |
| **Anchor Milestones** | Prototype & Approvals: End-Nov 2026 \| Campus Deployment: End-Dec 2026 |

---

## 1. Executive Project Brief, Problem & SDG Alignment

**Anna-Setu** (from Sanskrit: *"Anna"* meaning sustenance and *"Setu"* meaning bridge) is a closed-loop socio-technical framework designed for institutional campus dining ecosystems. It attacks food waste at two interconnected points:
1. **At the kitchen level**, where unforecasted safety margins create 10%-30% surplus buffers, and
2. **At the diner plate level**, where students routinely take excessive portions onto their plates and dump uneaten leftovers into garbage bins.

By coupling an AI predictive software engine (**Track A**) with an on-site smart plate-waste interceptor and accelerated bio-recycling converter (**Track B**), Anna-Setu creates a zero-waste circular campus economy: untouched kitchen food is safely redistributed to verified night shelters, while plate scraps are converted on-site into high-grade organic bio-fertilizer, relieving municipal authorities (Lucknow Nagar Nigam) and preventing fugitive methane emissions in landfills.

### Table 1.1: Sustainable Development Goal (SDG) Alignment Matrix

| UN SDG | Specific Target | Anna-Setu Implementation & Impact |
| :--- | :--- | :--- |
| **SDG 12: Responsible Consumption** *(Primary)* | **Target 12.3:** Halve food waste by 2030.<br/>**Target 12.5:** Substantially reduce waste via recycling. | **Track A** reduces kitchen overcooking by 15-25% via predictive ML; **Track B** deters over-serving with behavioral plate nudges and upcycles plate waste into organic fertilizer. |
| **SDG 2: Zero Hunger** *(Secondary)* | **Target 2.1 & 2.2:** End hunger; ensure access to safe, nutritious food. | Untouched surplus is checked through FSSAI statutory holding algorithms and safely dispatched to local night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar). |
| **SDG 11: Sustainable Cities** | **Target 11.6:** Reduce urban municipal per-capita environmental impact. | Eliminates organic wet-waste burden on municipal collection trucks and avoids ₹5,000-₹25,000 penalties under Lucknow Nagar Nigam Solid Waste By-Laws. |
| **SDG 13: Climate Action** | **Target 13.3:** Climate mitigation and institutional awareness. | Diverts organic matter from anaerobic landfill decomposition, eliminating methane ($CH_4$) emissions. Real-time displays show diners their carbon and water footprints. |

**Target Beneficiaries:**
* **Students:** Dynamic nudges build mindful eating habits.
* **Mess Management:** Cuts procurement bills by 15-25%.
* **Lucknow Nagar Nigam:** Zero waste burden hauled to landfills.
* **Local Shelters:** Reliable access to verified nutritious meals.
* **Campus Grounds:** Free high-grade bio-fertilizer.

---

## 2. Dual-Track Integrated Solution Architecture

Anna-Setu operates two synchronized operational tracks bridging the physical dining floor with digital cloud intelligence:

| **TRACK A: ANNA-SETU AI SOFTWARE PLATFORM**<br/>*(Status: In Progress / Working Prototype Deployed)* | **TRACK B: SMART PLATE-WASTE BIO-RECYCLER**<br/>*(Status: In Ideation / Hardware Prototype in Progress)* |
| :--- | :--- |
| • **Module 1 (Dining Demand Advisor):** Time-series forecasting model predicting next-day cooking volumes based on turnstiles, exams, and weather.<br/>• **Module 2 (RAG Compliance Engine):** Grounded in **FSSAI Surplus Regulations (2019)** (danger zone 5°C-65°C, 2h/4h ambient rule) and **Lucknow Nagar Nigam By-Laws** (45m transit buffer across 8 zones).<br/>• **IBM Granite Model Compiler:** Generates WhatsApp/SMS alerts (<60w) and official **FSSAI Form B & LNN Gate Pass manifests**.<br/>• **Live Assets:** Deployed on Hugging Face Spaces (Gradio) and local Streamlit app with 5 automated test cases. | • **Behavioral Nudge Front-End:** Precision plate scale (0-20kg) at tray return counter + 7-inch display showing wasted grams, water footprint, and hostel leaderboards to stop diners from taking extra food.<br/>• **Pre-Processing Shredder:** Reduces uneaten food scrap size to 3-5mm.<br/>• **Accelerated Bio-Composting Chamber:** Thermophilic heating (55°C-65°C) + active aerobic aeration + microbial enzymes achieve **85%-90% volume reduction in 12-24h**.<br/>• **Recyclable Resource Output:** High-grade **Organic Bio-Fertilizer / Soil Conditioner** for campus greenery and local farmers.<br/>• **IoT Cloud Bridge:** ESP32 streams daily plate waste logs back to Track A AI. |

### Table 2.1: Track B Hardware Bill of Materials (BOM) & Cost Feasibility

| Subsystem | Component | Technical Role in Station | Est. Cost (INR) |
| :--- | :--- | :--- | :---: |
| **Compute / IoT** | ESP32 WROOM-32 MCU | Wi-Fi telemetry, sensor polling, cloud API bridge | ₹450 |
| **Plate Waste Scale** | 0-20 kg Load Cell + HX711 | Measures individual student plate waste left on tray | ₹550 |
| **Nudge Display** | 7-inch IPS / OLED Screen | Displays wasted grams, water footprint & leaderboard | ₹850 |
| **Thermal Sensing** | MLX90614 Contactless IR | Verifies kitchen surplus food is held safe $\ge 65^\circ\text{C}$ | ₹750 |
| **Aerobic Aeration** | 12V Brushless Fan + Carbon | Supplies oxygen to composting chamber; stops odors | ₹250 |
| **Thermophilic Heat** | 100W PTC Ceramic Strip | Maintains 55°C-65°C to accelerate microbial breakdown | ₹450 |
| **Power & Housing** | 12V SMPS + SS Kiosk | Regulated power and IP65 sanitary stainless housing | ₹1,370 |
| **TOTAL BOM** | **Complete Integrated Kiosk** | **Affordable, student-built IoT bio-recycler prototype** | **₹4,670 (~$55)** |

---

## 3. Project Timeline & Phased Execution Roadmap

The project follows a structured two-month Agile delivery plan anchored to program milestones:
* **Milestone 1 (End of November 2026):** Working prototypes of Track A and Track B integrated, with campus administration approvals;
* **Milestone 2 (End of December 2026):** Live on-campus 2-week pilot deployment, AI model retraining on real waste data, and final impact handover.

### Table 3.1: Phased Execution Timeline

| Phase / Sprint | Date Range | Key Work Deliverables & Activities | Gate Status |
| :--- | :---: | :--- | :---: |
| **Phase 1 & 2:**<br/>RAG Engine & UI | Nov 1 - Nov 10, 2026 | Codified FSSAI 2019 and LNN by-laws into JSON KB; built TF-IDF vector retriever, compliance calculator, and IBM Granite notification compiler. Deployed Gradio demo on Hugging Face and local Streamlit app. Verified 5 automated test cases. | **COMPLETED** |
| **Sprint 3A:**<br/>HW Breadboard & IoT | Nov 11 - Nov 20, 2026 | Procure ESP32, load cell, MLX90614 IR sensor, and display; assemble bench breadboard; flash C++/MicroPython firmware (`esp32_smart_kiosk.ino`); bridge telemetry to `api_server.py`. | **IN PROGRESS** |
| **Sprint 3B:**<br/>Approvals & Gate 1 | Nov 21 - Nov 30, 2026 | Draft permission letter to Dean of Student Welfare / Campus Mess Committee; establish coordination agreement with Rain Basera Charbagh; **Milestone 1 Gate Review with 1M1B mentor**. | **MILESTONE 1 GATE**<br/>*(End-Nov 2026)* |
| **Phase 4:**<br/>Enclosure & Pilot | Dec 1 - Dec 21, 2026 | Assemble IP65 stainless enclosure at tray return; conduct 14-day live campus pilot in student mess; log plate-waste reduction via nudge screen; dispatch compliant kitchen surplus; produce first batch of bio-fertilizer. | **PLANNED PILOT**<br/>*(Central Mess)* |
| **Phase 5:**<br/>Impact & Closeout | Dec 22 - Dec 31, 2026 | Retrain Module 1 demand model on real pilot plate-waste logs; compute total kg rescued, kg bio-fertilizer harvested, methane avoided, and procurement ₹ saved. Submit final PDF report, PPT, and demo video. | **MILESTONE 2 GATE**<br/>*(End-Dec 2026)* |

---

> **Summary Note:** The project tracker and activity task breakdown are maintained dynamically in the collaborative Google Sheets register: **`PankhuriGovila_YIRP`**, shared with **`paramjeet@onemoneb.org`**. The offline master spreadsheet is available at `PankhuriGovila_YIRP_Project_Tracker.xlsx`.

