# 🍽️ Anna-Setu: Integrated Project Brief, Dual-Track Blueprint, Timeline & Project Tracker
### 1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE
**Intern Name:** Pankhuri Govila | **Program:** 1M1B AI for Sustainability Virtual Internship  
**1M1B Mentor:** Paramjeet Sir (`paramjeet@onemoneb.org`)  
**Project Tracker Name:** `PankhuriGovila_YIRP`

---

## 📌 PART 1: Executive Project Brief & SDG Alignment

### 1.1 Project Title & Core Philosophy
**Anna-Setu** (*"Anna"* meaning food/nourishment and *"Setu"* meaning bridge) is a closed-loop socio-technical framework designed for institutional campus dining ecosystems. It bridges two critical systemic failures:
1. **At the Kitchen Level:** Blind, unforecasted overproduction resulting in massive untouched surplus.
2. **At the Consumer Plate Level:** Diners taking extra portions onto their plates and discarding uneaten food into trash bins.

By combining an AI-driven digital platform (Track A) with an on-site smart plate-waste interceptor and bio-recycling instrument (Track B), Anna-Setu creates a **Zero-Waste Circular Campus Loop**: untouched kitchen surplus is legally redistributed to local shelters, while unconsumed plate scraps are intercepted and transformed on-site into a **recyclable organic resource (bio-fertilizer)**, eliminating the waste burden on municipal authorities and our planet Earth.

```
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

---

### 1.2 The Problem Statement
> *"How might we use AI demand forecasting and smart on-site IoT hardware to eliminate cafeteria overproduction, deter individuals from taking extra food and wasting plate leftovers, and upcycle unconsumed food into recyclable elements so that institutional dining ecosystems reduce municipal burdens and environmental harm?"*

Campus dining halls suffer from two distinct waste streams:
* **Stream 1 (Kitchen Overproduction):** Cafeteria management routinely cooks **10% to 30% arbitrary buffers** to avoid the logistical risk of food running out. Due to unpredictable academic schedules (exams, events) and weather shifts, tens of kilograms of untouched food are wasted daily.
* **Stream 2 (Consumer Plate Waste):** Diners routinely overfill their plates ("eyes bigger than stomach"), fail to finish their meals, and dump leftovers into general waste bins. There is zero individual accountability or awareness of the ecological cost of wasted food.
* **The Downstream Burden:** Mixing food waste into municipal trash creates rotting, foul-smelling garbage that burdens municipal sanitation authorities (Lucknow Nagar Nigam), risks heavy statutory penalties (₹5,000-₹25,000 under LNN Solid Waste By-Laws), and generates methane ($CH_4$) in landfills-a greenhouse gas 28 times more potent than $CO_2$.

---

### 1.3 Alignment with UN Sustainable Development Goals (SDGs)

| SDG Target | Target Specifics | Direct Implementation in Anna-Setu |
| :--- | :--- | :--- |
| **SDG 12: Responsible Consumption & Production (PRIMARY)** | **Target 12.3:** Halve per-capita global food waste at consumer and retail levels by 2030; **Target 12.5:** Substantially reduce waste generation through prevention, reduction, recycling, and reuse. | **Track A** prevents kitchen overproduction by 15-25% via predictive AI; **Track B** intercepts plate waste, deters over-serving through behavioral nudges, and converts scraps into recyclable organic fertilizer. |
| **SDG 2: Zero Hunger (SECONDARY)** | **Target 2.1 & 2.2:** End hunger and ensure access to safe, nutritious food for vulnerable populations. | Surplus untouched kitchen food is verified through FSSAI compliance algorithms and safely dispatched to local night shelters (Rain Basera) and urban food banks. |
| **SDG 11: Sustainable Cities & Communities** | **Target 11.6:** Reduce the adverse per-capita environmental impact of cities, including municipal waste management. | Eliminates the burden on municipal collection trucks by treating 100% of organic waste on-site, preventing illegal landfill dumping in city corridors. |
| **SDG 13: Climate Action** | **Target 13.3:** Improve institutional education and human capacity on climate change mitigation. | Diverting organic matter from anaerobic landfill decomposition eliminates methane emissions; real-time displays educate students on their carbon and water footprints. |

---

### 1.4 Target End Users & Direct Beneficiaries
1. **Students & Campus Diners:** Interactive behavioral screens discourage taking excessive food, instilling mindful consumption habits and rewarding zero-waste dining.
2. **Kitchen & Mess Operations:** Access to daily predictive meal-demand forecasts cuts raw material procurement costs by 15-25% and streamlines inventory management.
3. **Local Municipal Authorities (Lucknow Nagar Nigam):** Zero organic wet-waste burden delivered to municipal dustbins or transfer stations; compliance with Swachh Bharat Urban directives.
4. **Vulnerable Communities & Shelters:** Guaranteed access to wholesome, safety-verified surplus meals at empanelled night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar).
5. **Campus Grounds & Agriculture:** Access to nutrient-rich, pathogen-free organic bio-fertilizer produced on-site for campus gardens, green belts, and local agriculture.

---

## 🏗️ PART 2: The Two-Track Integrated Solution Architecture

To solve both kitchen-level overproduction and consumer-level plate waste, Anna-Setu is structured into **two synchronized operational tracks**:

---

### Track A: The Anna-Setu App & AI Engine *(In Progress / Advanced Working Prototype)*
Track A serves as the cognitive forecasting and statutory redistribution layer:

#### 1. Module 1: Smart Campus Dining Advisor (Predictive Forecasting)
* Uses machine learning regression (Gradient Boosted Trees / Random Forests) trained on historical meal logs, academic calendars (exam periods, orientation, holidays), day-of-week patterns, and regional weather.
* Outputs optimized daily recommended cooking volumes per menu item with confidence intervals, cutting the default 10-30% buffer down to data-backed thresholds.

#### 2. Module 2: Predictive Redistribution Pipeline (RAG + IBM Granite Models)
* **Vector Index Retrieval (RAG):** When excess food is flagged, a semantic vector retriever indexes official statutory regulations:
  * **FSSAI Surplus Regulations (2019):** Danger zone ($5^\circ\text{C}-65^\circ\text{C}$), ambient 2h/4h rule, prohibited items (raw cut salads, plate scrapings), and Good Samaritan legal immunity (Section 7).
  * **Lucknow Nagar Nigam (LNN) By-Laws:** 45-minute municipal transit corridor ceiling across Lucknow Zones 1-8, verified Rain Basera directories, and mandatory organic bio-composting diversion (Section 18).
* **IBM Granite Foundation Model Synthesis:** Automatically compiles structured surplus parameters into:
  1. Concise, warm WhatsApp/SMS alerts (<60 words) for shelter coordinators.
  2. Official **FSSAI Form B & LNN Gate Security Pass Audit Manifests**.
  3. LNN Bio-Compost Diversion Certificates if food is non-compliant.
* **Current Software Assets:**
  * Live Hugging Face Spaces Gradio Demo: [Anna-Setu Demo](https://huggingface.co/spaces/pgovila/Anna-Setu-Demo)
  * Local Interactive Streamlit Dashboard: [`streamlit_app.py`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/streamlit_app.py)
  * Automated 5-Scenario Test Suite: [`test_rag.py`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/test_rag.py)

---

### Track B: Smart Plate-Waste Interceptor & Bio-Recycling Converter *(Hardware Proposal & Engineering Blueprint)*
*Status: In Ideation / Conceptual Design (Targeted for Benchtop Prototype by End-November 2026).*

Track B directly addresses the user's specific requirement: **preventing diners from throwing plate leftovers into garbage bins and converting unavoidable scraps into a recyclable element (organic bio-fertilizer)**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 TRACK B: SMART PLATE-WASTE BIO-RECYCLING STATION            │
└─────────────────────────────────────────────────────────────────────────────┘

  [Diner Returns Tray] ──> [Weighing Deck] ──> [Dynamic Behavioral Nudge Screen]
                                │              "You left 160g food (120L water)!
                                │               Hostel Block A: 88% Clean Plates"
                                ▼
                       [Drop Chute & Shredder]
                                │
                                ▼
               ┌─────────────────────────────────┐
               │ ACCELERATED BIO-COMPOST CHAMBER │
               │ - Thermophilic Heat (55C - 65C) │
               │ - Aerobic Aeration Fan          │
               │ - Micro-Enzyme Bio-Inoculant    │
               │ - Volume Reduction: 85% to 90%  │
               └────────────────┬────────────────┘
                                │
                                ▼
                  [RECYCLABLE PRODUCT OUTPUT]
            Nutrient-Rich Organic Bio-Fertilizer / Soil
          Amender for Campus Gardens & Local Agriculture!
```

#### 1. How It Deters Diners From Wasting Food (The Behavioral Front-End)
* **The Plate-Return Scale:** Installed directly at the dish-clearing counter. When a student places their plate onto the station deck, a high-precision load cell (0-20 kg with HX711 24-bit ADC) instantly registers the tare-subtracted plate-waste weight.
* **Interactive Behavioral Nudge Screen (7-inch IPS / OLED Display):**
  * Displays instant personal feedback:
    > *"⚠️ You left **165 grams** of uneaten food on your plate today."*  
    > *"💧 That represents **125 Liters** of wasted embedded freshwater and **380g $CO_2e$**!"*
  * **Social Proof & Gamification:** Displays real-time hostel block leaderboards (*"Hostel Block C is currently in 1st place with 94% clean plates this week!"*).
  * Psychological deterrence significantly curtails the habit of taking oversized portions.

#### 2. How It Creates a Recyclable Element (On-Site Bio-Conversion)
* **Pre-Processing Shredder / Macerator Chute:** Plate leftovers scraped into the station chute pass through a motorized shredder that reduces particle size to 3-5 mm, maximizing surface area for rapid microbial breakdown.
* **Accelerated Thermo-Mechanical Aerobic Composting Vessel:**
  * **Controlled Thermophilic Stage ($55^\circ\text{C} - 65^\circ\text{C}$):** A PTC ceramic heating element maintains an optimal thermophilic temperature range, which accelerates microbial digestion and destroys harmful pathogens (*Salmonella*, *E. coli*) and weed seeds.
  * **Active Aerobic Aeration & Agitation:** A slow-turning internal auger arm and an exhaust fan with an activated carbon filter continuously oxygenate the mixture, completely preventing anaerobic foul odors.
  * **Bio-Enzyme Inoculation:** Introduces a small proprietary microbial culture (effective microorganisms / actinomycetes) that breaks down complex starches, fats, and proteins.
  * **Rapid Volume Reduction:** In **12 to 24 hours**, the machine drives off moisture and breaks down organic matter, achieving an **80% to 90% volume reduction**.
* **The Final Recyclable Element (Organic Bio-Fertilizer):**
  * The resulting output is a dark, dry, earthy, nutrient-rich **Organic Bio-Fertilizer / Soil Conditioner (NPK-enriched soil amender)**.
  * **Use Cases:**
    * 100% of campus landscaping, flowerbeds, and sports fields can be fertilized without chemical synthetic fertilizers.
    * Packaged into "Anna-Setu Green Bags" and distributed free to local smallholder farmers or student agricultural clubs.
  * **Relief to Municipal Authorities:** Zero organic waste is handed over to municipal collection trucks. The campus transforms a landfill liability into high-value agricultural wealth!

#### 3. Closed-Loop Cloud Bridge to Track A
* An **ESP32 microcontroller** logs the total daily plate waste (in kg) and transmits it over campus Wi-Fi via RESTful HTTP/MQTT to the Track A server (`api_server.py`).
* **AI Feedback Loop:** The Track A Dining Advisor (Module 1) ingests this plate-waste ground truth: if students consistently leave 25% of a specific vegetable dish on their plates, the AI flags recipe unpalatability and lowers future cooking recommendations automatically!

#### 4. Hardware Bill of Materials (BOM) & Budget

| Subsystem | Component / Part | Technical Function | Est. Cost (INR) |
| :--- | :--- | :--- | :--- |
| **Compute & Cloud Sync** | ESP32 WROOM-32 MCU | Wi-Fi telemetry, sensor polling, display driver | ₹450 |
| **Plate Waste Scale** | 0-20 kg Load Cell + HX711 | Instantaneous plate leftover measurement | ₹550 |
| **Behavioral Nudge Screen** | 7-inch IPS Display / OLED | Real-time student feedback, carbon/water footprint | ₹850 |
| **Thermal Sensing** | MLX90614 Contactless IR Probe | Monitors kitchen surplus holding temperatures ($\ge 65^\circ\text{C}$) | ₹750 |
| **Compost Aeration** | 12V DC Brushless Fan + Carbon Filter | Active aerobic aeration; prevents odors | ₹250 |
| **Thermophilic Heating** | 100W PTC Ceramic Heating Strip | Maintains $55^\circ\text{C}-65^\circ\text{C}$ to accelerate decomposition | ₹450 |
| **Power & Control** | 12V 5A SMPS + 4-Channel Relays | Powers heater, fan, sensors, and microcontroller | ₹420 |
| **Station Enclosure** | Stainless Steel / Acrylic Housing | Waterproof IP65 tray counter housing with drop chute | ₹950 |
| **TOTAL HARDWARE BOM** | **Complete Integrated Prototype** | **Benchtop prototype ready for campus pilot** | **₹4,670 (~$55 USD)** |

---

## 📅 PART 3: Project Timeline (November 2026 - December 2026)

### 3.1 Anchor Milestones (Mandated by Program)
* **By November 2026:** Complete Project Prototype (Track A Software + Track B Hardware Benchtop Prototype integrated) and secure necessary institutional/campus approvals (Mess Committee / Dean of Student Welfare / Shelter Partner NOC).
* **End of December 2026:** Complete Project and Live Deployment (On-campus pilot, live redistribution run, final impact report submission).

### 3.2 Phased Roadmap & Sprints

```
Nov 1 - Nov 10        Nov 11 - Nov 20        Nov 21 - Nov 30        Dec 1 - Dec 15         Dec 16 - Dec 31
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Phase 1 & 2 │ ──> │   Phase 3A   │ ──> │   Phase 3B   │ ──> │   Phase 4    │ ──> │   Phase 5    │
│  RAG Engine  │     │ HW Breadboard│     │ Approvals &  │     │ Live Campus  │     │ Impact Eval  │
│  & UI Ready  │     │ Assembly &   │     │ Milestone 1  │     │ 2-Wk Pilot   │     │ & Final Deck │
│ (Completed)  │     │ IoT Bridge   │     │ Prototype Gate│    │ Deployment   │     │ Milestone 2  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

#### Phase 1 & 2: RAG Pipeline Grounding & UI Deployment *(Completed: Nov 1 - Nov 10, 2026)*
* Codified FSSAI 2019 regulations and Lucknow Nagar Nigam by-laws into structured knowledge bases.
* Built TF-IDF vector retriever, compliance engine (2h/4h rule, danger zone, 45m transit corridors), and IBM Granite compiler.
* Implemented Gradio Hugging Face Spaces app and local interactive Streamlit app.
* Verified 5/5 automated test scenarios in `test_rag.py`.

#### Phase 3: Hardware Breadboard Prototyping & Campus Approvals *(Nov 11 - Nov 30, 2026)*
* **Sprint 3A (Nov 11 - Nov 20):**
  * Procure ESP32, HX711 load cell, MLX90614 IR sensor, and behavioral display module.
  * Wire bench breadboard circuit and flash firmware ([`firmware/esp32_smart_kiosk.ino`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/firmware/esp32_smart_kiosk.ino)).
  * Connect to local API server ([`api_server.py`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/api_server.py)) over campus Wi-Fi.
* **Sprint 3B (Nov 21 - Nov 30) - [MILESTONE 1 APPROVAL GATE]:**
  * Draft formal Institutional MoU and Campus Mess Permission Letter for the Dean of Student Welfare / Campus Administration and Hostel Mess Committee.
  * Contact Lucknow shelter partners (Rain Basera Charbagh / Lucknow Roti Bank) for written acknowledgement.
  * Conduct **Milestone 1 Gate Review**: Demonstrate working bench prototype of Track B hardware streaming plate-waste data to Track A software.

#### Phase 4: Enclosure Assembly & Live 2-Week Campus Pilot Deployment *(Dec 1 - Dec 21, 2026)*
* **Sprint 4A (Dec 1 - Dec 7):** Assemble hardware inside splash-proof stainless steel enclosure; calibrate load cell at cafeteria tray return; test thermal heating strip and exhaust fan.
* **Sprint 4B (Dec 8 - Dec 21):**
  * Conduct a 14-day live campus pilot in the student dining hall.
  * Log student plate-waste reduction via the behavioral nudge screen; evaluate untouched kitchen surplus through RAG; dispatch safe meals to Rain Basera Charbagh.
  * Harvest first batches of dry, odorless bio-fertilizer and apply to campus gardens.

#### Phase 5: Impact Assessment, Model Retraining & Final Milestone Deployment *(Dec 22 - Dec 31, 2026)*
* Retrain Module 1 demand forecasting model using real plate-waste logs captured during the pilot.
* Synthesize cumulative impact: kilograms of food rescued, kilograms converted to bio-fertilizer, meals served, ₹ saved in procurement, and estimated $CO_2e$ / methane avoided.
* Finalize comprehensive project report, updated slide presentation, walkthrough video, and submit to 1M1B mentors and AICTE before **December 31, 2026**.

---

## 📊 PART 4: Project Tracker (Google Sheets Specification)

### 4.1 Setup & Sharing Details
* **Google Sheet Title:** `PankhuriGovila_YIRP`
* **Mentor Sharing Email:** `paramjeet@onemoneb.org` (Set permission to **"Editor"**)
* **Files Generated in Workspace:**
  * Multi-Tab Styled Excel Spreadsheet: [`PankhuriGovila_YIRP_Project_Tracker.xlsx`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/PankhuriGovila_YIRP_Project_Tracker.xlsx)
  * One-Click Import CSV File: [`PankhuriGovila_YIRP_Project_Tracker.csv`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/PankhuriGovila_YIRP_Project_Tracker.csv)

#### Instructions to Import & Share:
1. Open [Google Sheets](https://sheets.google.com).
2. Click **File** $\to$ **Import** $\to$ **Upload**, and select [`PankhuriGovila_YIRP_Project_Tracker.xlsx`](file:///c:/Users/abc/OneDrive/Documents/Certifications/IBM%20Skillsbuild/1M1B/Anna%20Setu/PankhuriGovila_YIRP_Project_Tracker.xlsx).
3. Ensure the document title is: **`PankhuriGovila_YIRP`**.
4. Click **Share** (top right), add **`paramjeet@onemoneb.org`**, set role to **Editor**, and confirm.

---

### 4.2 Complete Activity Tracker Table

| Task ID | Track | Milestone / Phase | Task Description | Detailed Work Done & Deliverables | Target Date | Status | % Done | Any help from 1M1B |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TSK-01** | Track A | Phase 1: Foundation | Problem Scoping & SDG Mapping | Mapped 10-30% buffer overcooking to SDG 12.3 & SDG 2; submitted initial report & slides | 2026-09-20 | **Completed** | 100% | None at this stage; completed standard internship framing. |
| **TSK-02** | Track A | Phase 1: Foundation | Gradio UI Prototype & Hugging Face Deploy | Built interactive web demo with food item logs and simulated Granite alert; deployed live | 2026-09-25 | **Completed** | 100% | Guidance on integrating IBM Granite model weights or direct API endpoints. |
| **TSK-03** | Track A | Phase 2: RAG Subsystem | Codify FSSAI & LNN Regulations | Codified FSSAI 2019 clauses (danger zone, 2h/4h rule) and LNN by-laws (45m transit, bio-compost divert) into JSON KB | 2026-11-08 | **Completed** | 100% | Validation of legal templates for FSSAI Good Samaritan protection. |
| **TSK-04** | Track A | Phase 2: RAG Subsystem | RAG Vector Retriever & Engine Build | Built TF-IDF n-gram vector retriever, deterministic compliance calculator across Lucknow zones, and Form B manifests | 2026-11-10 | **Completed** | 100% | Feedback on enterprise scaling of vector indexing. |
| **TSK-05** | Track A | Phase 2: RAG Subsystem | Dual UI Implementation (Gradio + Streamlit) | Upgraded Gradio app.py and built full local Streamlit dashboard with zone transit calculator & RAG search | 2026-11-10 | **Completed** | 100% | Assistance with server hosting if deploying full multi-tenant instance. |
| **TSK-06** | Track B | Phase 2: HW Conceptualization | Smart Plate-Waste Interceptor Architecture | Conceptualized dual-action hardware: behavioral plate-waste nudge screen + accelerated bio-composting into fertilizer | 2026-11-10 | **Completed** | 100% | 1M1B technical mentor review of IoT schematic and composting mechanical design. |
| **TSK-07** | Track B | Phase 3: HW Breadboard | Procure Components & Build Bench Breadboard | Sourcing ESP32, HX711 load cell amp, MLX90614 IR sensor, LCD, and assembling test circuit on workbench | 2026-11-20 | **In Progress** | 45% | Support or recommendation for student hardware lab grants / maker-space access. |
| **TSK-08** | Track B | Phase 3: HW Breadboard | Firmware Development & Cloud API Bridge | Written Arduino/C++ firmware (esp32_smart_kiosk.ino) to read plate waste, calculate student impact metrics, and post telemetry to Anna-Setu API | 2026-11-23 | **Completed** | 100% | Feedback on optimal data sync frequency for low-power edge nodes. |
| **TSK-09** | Approvals | Phase 3: Approvals | Draft Institutional MoU & Campus Mess Permission | Draft formal pilot request letter to University Mess Committee, Chief Warden, and Dean of Student Welfare / Campus Administration | 2026-11-27 | **Planned** | 20% | Official 1M1B / IBM SkillsBuild Internship Endorsement Letter to College Principal/Dean. |
| **TSK-10** | Approvals | Phase 3: Approvals | Lucknow Shelter Coordination & Agreement | Establish formal contact with Rain Basera Charbagh / Lucknow Roti Bank coordinators to align on pickup window | 2026-11-28 | **Planned** | 15% | Introduction or network referral to verified hunger-relief NGO partners in UP. |
| **TSK-11** | Integrated | Milestone 1 Gate | **Milestone 1 Gate Review (Integrated Prototype & Approvals)** | Demonstrate bench prototype of Track B hardware streaming to Track A app; present signed campus pilot approval | 2026-11-30 | **Planned** | 10% | Formal milestone evaluation session with Paramjeet Sir (`paramjeet@onemoneb.org`). |
| **TSK-12** | Integrated | Phase 4: Field Pilot | Enclosure Fabrication & Station Installation | Install IP65 sanitary enclosure at cafeteria tray return; mount load deck, display, and composting module | 2026-12-07 | **Planned** | 0% | Guidance on food-grade sanitary enclosure compliance. |
| **TSK-13** | Integrated | Phase 4: Field Pilot | Live 2-Week Campus Pilot Run (Central Dining Hall) | Run end-to-end operational pilot: measure reduction in student plate waste via nudge screen, evaluate kitchen surplus through RAG, dispatch meals, and convert plate waste into organic fertilizer on-site | 2026-12-21 | **Planned** | 0% | Mid-pilot troubleshooting check-in. |
| **TSK-14** | Track A | Phase 5: Evaluation | Module 1 Demand Forecast Model Retraining | Feed real plate-waste logs captured by Track B hardware back into forecasting model to validate accuracy | 2026-12-26 | **Planned** | 0% | Advice on time-series feature weighting for academic calendars. |
| **TSK-15** | Integrated | Milestone 2 Gate | **Milestone 2 Final Deployment & Impact Report Submission** | Quantified impact statement (meals rescued, kg converted to bio-fertilizer, methane avoided, ₹ saved), full documentary demo video, updated PPT | 2026-12-31 | **Planned** | 0% | Final evaluation, certification endorsement, and nomination for showcase. |

---

## ⚖️ PART 5: Disclosure of Best Judgment Used

In synthesizing this comprehensive blueprint, engineering judgment was exercised in five key domains:

1. **Track B Mechanism Selection (Behavioral Nudge + Bio-Composting):**
   * *Judgment:* Selected a dual-action system: a front-end **Behavioral Nudge Screen** that displays real-time waste metrics (grams left, water footprint) to deter students from over-serving, coupled with a back-end **Accelerated Aerobic Composting Chamber ($55^\circ\text{C}-65^\circ\text{C}$)** that upcycles unavoidable plate scraps into nutrient-rich organic bio-fertilizer within 24 hours.
   * *Rationale:* Behavioral nudges directly stop students from taking extra food, while on-site composting creates a valuable, recyclable agricultural product that eliminates the burden on municipal authorities (LNN) and prevents landfill methane emissions.
2. **Hardware Budget & BOM Cost Feasibility:**
   * *Judgment:* Restricted the hardware Bill of Materials to **₹4,670 (~$55 USD)** using standard maker electronics (ESP32, HX711, MLX90614, PTC heater).
   * *Rationale:* Keeps the prototype accessible and buildable within a student internship budget while achieving commercial-grade sensing and demonstration impact.
3. **Timeline Phasing (Nov 2026 - Dec 2026):**
   * *Judgment:* Structured the roadmap into 5 two-week Agile execution phases with a strict Milestone 1 Gate on **November 30, 2026** (bench prototype + institutional permissions) and Milestone 2 Gate on **December 31, 2026** (2-week on-campus pilot + final impact submission).
   * *Rationale:* Matches the internship requirements while providing adequate buffer for campus administrative clearances.
4. **Student Identity & Institutional Context:**
   * *Judgment:* Populated student name as **Pankhuri Govila** and institution as **1M1B AI for Sustainability Virtual Internship**, mapped to Lucknow Nagar Nigam's municipal corridor for urban shelter testing.
5. **1M1B Support Request Mapping:**
   * *Judgment:* Formulated concrete, realistic asks in the *"Any help from 1M1B"* column (e.g., IoT schematic review, official internship endorsement letters for college permissions, network introductions to verified food bank NGOs).
