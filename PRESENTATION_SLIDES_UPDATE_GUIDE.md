# 📊 Anna-Setu: 1M1B Presentation Deck Slide-by-Slide Update Guide
### Aligned with 1M1B AI for Sustainability Guidelines (In Collab with IBM SkillsBuild & AICTE)
**Author:** Pankhuri Govila | **Institution:** University of Petroleum and Energy Studies (UPES)  
**Mentor:** Paramjeet Sir (`paramjeet@onemoneb.org`) | **Project Tracker ID:** `PankhuriGovila_YIRP`

---

## 📌 Presentation Structure (10-Slide Deck Specification)

Use this guide to update your PowerPoint deck (`Anna-Setu_Presentation.pptx`) or compile your final presentation for the 1M1B mentors and jury.

---

### Slide 1: Title & Project Overview
* **Slide Title:** **Anna-Setu: AI-Powered Campus Food Rescue & Plate-Waste Bio-Recycling Network**
* **Subtitle:** 1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE
* **Student Name & Institution:** Pankhuri Govila | University of Petroleum and Energy Studies (UPES)
* **Mentorship Acknowledgement:** Mentored by Paramjeet Sir (`paramjeet@onemoneb.org`)
* **Core Philosophy:** *"Anna"* (Sustenance) + *"Setu"* (Bridge) — A socio-technical bridge connecting cafeteria overproduction and plate waste with community nutrition and campus circularity.
* **Primary SDG:** **SDG 12: Responsible Consumption and Production** (Target 12.3 & 12.5)
* **Secondary SDGs:** **SDG 2: Zero Hunger**, **SDG 11: Sustainable Cities**, **SDG 13: Climate Action**

---

### Slide 2: The Two-Fold Problem in Campus Dining
* **Slide Header:** Two Structural Failure Points in Higher Education Cafeterias
* **Left Column — Kitchen-Level Inefficiency (Overcooking Buffers):**
  * Cafeteria staff cook **10% to 30% arbitrary buffers** to prevent running out.
  * Rotating menus are blind to volatile demand drivers: mid-terms/finals, rainstorms, heatwaves, and weekend campus departures.
  * Fear of food poisoning liability and lack of verified shelter connections lead to untouched food being dumped.
* **Right Column — Diner-Level Inefficiency (Consumer Plate Waste):**
  * Students routinely take extra food onto their plates ("eyes bigger than stomach") and throw uneaten food into trash bins.
  * Zero feedback loop or awareness of embedded freshwater and carbon footprints.
* **The Downstream Municipal Crisis:**
  * Rotting food waste dumped into municipal bins creates foul odors, burdens city collection authorities (Lucknow Nagar Nigam), risks ₹5,000–₹25,000 fines, and generates fugitive methane ($CH_4$) in landfills.

---

### Slide 3: The Anna-Setu Closed-Loop Circular Solution
* **Slide Header:** A Dual-Track Socio-Technical Framework
* **Visual Diagram:** Flowchart showing Kitchen Surplus going to Track A and Plate Scraps going to Track B:
  * **Track A (AI Software Platform):** Predictive meal forecasting to eliminate kitchen buffers + statutory RAG compliance engine grounded in FSSAI 2019 & municipal by-laws to safely redistribute untouched food to verified shelters.
  * **Track B (Smart IoT Bio-Recycling Station):** Benchtop hardware installed at tray return with a plate scale and behavioral nudge screen to deter over-serving + accelerated thermo-mechanical bio-composter that upcycles unavoidable scraps into **organic bio-fertilizer**.
* **Impact Summary:** Complete circularity — food feeds hungry people, and unavoidable scraps feed campus soil, achieving **Zero Landfill Burden** on municipal authorities.

---

### Slide 4: Track A Architecture — Forecasting & RAG Compliance
* **Slide Header:** Track A: Predictive Dining Advisor & Statutory RAG Pipeline
* **Module 1 — Smart Dining Advisor (Predictive Forecasting):**
  * Machine learning time-series regression trained on historical swipe logs, academic calendars (exams, holidays), and weather.
  * Delivers morning recommended cooking volumes per dish with confidence intervals, cutting procurement waste by 15%–25%.
* **Module 2 — Statutory RAG Compliance Pipeline:**
  * **FSSAI Surplus Food Regulations (2019):** Vector retriever indexes microbial danger zone ($5^\circ\text{C}-65^\circ\text{C}$), ambient 2h/4h rule, and Good Samaritan legal immunity (Section 7).
  * **Lucknow Nagar Nigam (LNN) By-Laws:** Enforces 45-minute municipal corridor transit limit across Lucknow Zones 1–8 and mandatory bio-compost diversion for expired food (Section 18).
* **IBM Granite Foundation Model Synthesis:**
  * Automatically compiles structured surplus parameters into concise WhatsApp/SMS alerts (<60w) for shelter coordinators.
  * Generates digital **FSSAI Form B & LNN Gate Pass manifests**.

---

### Slide 5: Track B Architecture — Smart Plate-Waste Bio-Recycler
* **Slide Header:** Track B: Behavioral Interception & On-Site Upcycling
* **The Behavioral Front-End (Deterring Over-Serving):**
  * Precision load cell (0–20 kg) at tray return instantly registers tare-subtracted plate leftover grams.
  * **Dynamic Nudge Display:** Shows the student their wasted grams, embedded water footprint (e.g. 125 Liters), and hostel block clean-plate leaderboard.
* **The Bio-Recycling Converter (Creating Recyclable Fertilizer):**
  * Macerator shredder reduces scrap size to 3–5 mm.
  * **Accelerated Composting Chamber ($55^\circ\text{C}-65^\circ\text{C}$):** Thermophilic heat + aerobic fan aeration + microbial enzymes achieve an **85% to 90% volume reduction in 12–24 hours**.
* **Output Product:** Dark, earthy, pathogen-free **Organic Bio-Fertilizer** for campus greening and local farmers.

---

### Slide 6: Engineering Feasibility & Hardware BOM
* **Slide Header:** Hardware Component Bill of Materials (BOM) & Budget
* **Table of Components:**
  * ESP32 WROOM-32 MCU: ₹450
  * 0–20 kg Load Cell + HX711 ADC: ₹550
  * 7-inch IPS Behavioral Display: ₹850
  * MLX90614 Contactless IR Thermal Probe: ₹750
  * Composting Fan + Carbon Filter: ₹250
  * 100W PTC Ceramic Heating Strip: ₹450
  * Power Supply & Relays: ₹420
  * Sanitary Stainless Steel Kiosk Housing: ₹950
* **Total Prototype Budget:** **₹4,670 (~$55 USD)** — Affordable, low-risk, student-built IoT hardware station.

---

### Slide 7: Live Prototypes & Working Demonstrations
* **Slide Header:** Demonstrated Proof-of-Concept & Repository Assets
* **Live Web App (Hugging Face Spaces):** `https://huggingface.co/spaces/pgovila/Anna-Setu-Demo`
* **Local Interactive Streamlit Dashboard:** `streamlit_app.py` (Includes Dual-Track Simulator, RAG QA, and live Project Tracker).
* **Automated Verification Test Suite:** `test_rag.py` (5/5 passing test scenarios: Fresh batch, Urgent batch, Expired batch, Prohibited raw salad, and Semantic municipal query).
* **Hardware Firmware & Simulation:** `firmware/esp32_smart_kiosk.ino`, `api_server.py`, and `simulate_iot_kiosk.py`.
* **GitHub Repository:** `https://github.com/pgovila/Anna-Setu-Project`

---

### Slide 8: Project Timeline & Phased Execution Roadmap
* **Slide Header:** Two-Month Phased Roadmap (Nov – Dec 2026)
* **Milestone 1 Gate (Target: End of November 2026):**
  * Complete integrated benchtop prototype (Track A Software + Track B Hardware).
  * Secure institutional campus permissions from Dean of Student Welfare / Mess Committee (UPES).
  * Establish coordination agreement with local shelter partners (Rain Basera Charbagh).
* **Phase 4 (Dec 01 – Dec 21, 2026):** Live 14-day campus pilot in central dining hall; measure real plate-waste reduction via nudge screen; harvest first bio-fertilizer batch.
* **Milestone 2 Gate (Target: End of December 2026):**
  * Retrain demand forecasting model using real pilot plate-waste logs.
  * Quantified final impact report submission to 1M1B & AICTE.

---

### Slide 9: Project Tracker & Mentorship Governance
* **Slide Header:** Structured Monitoring & Collaborative Tracker
* **Google Sheets Register Name:** `PankhuriGovila_YIRP`
* **Mentor Sharing:** Shared with **Paramjeet Sir (`paramjeet@onemoneb.org`)** with Editor permissions.
* **Core Columns:** Task ID, Track, Milestone Phase, Description, Detailed Work Done, Start/Target/Actual Dates, Status %, Links/Artifacts, and **Any help from 1M1B**.
* **Offline Master Files:** Available in workspace as `PankhuriGovila_YIRP_Project_Tracker.xlsx` and CSV export.

---

### Slide 10: Expected Impact Statement & Sustainability Vision
* **Slide Header:** Measuring Triple-Bottom-Line Sustainability Impact
* **Economic Impact:**
  * 15% to 25% reduction in cafeteria buffer procurement costs.
  * Elimination of municipal waste dumping fines (₹5,000–₹25,000 under LNN by-laws).
  * Free organic fertilizer replacing chemical fertilizers for campus grounds.
* **Environmental Impact:**
  * Zero organic wet waste sent to landfills $\to$ 100% elimination of fugitive methane emissions.
  * Thousands of liters of embedded water conserved through clean-plate awareness.
* **Social & Community Impact:**
  * Dignified, consistent access to safety-verified surplus meals for night shelter residents and rural hospital patient attendants.
  * Fosters a culture of mindful consumption among student diners.
* **Closing Call to Action:** *"Anna-Setu demonstrates how AI and IoT can transform an institutional waste liability into social nutrition, agricultural wealth, and measurable planetary impact."*

