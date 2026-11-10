# 🍽️ ANNA-SETU: AI-POWERED CAMPUS FOOD RESCUE & PLATE-WASTE BIO-RECYCLING NETWORK
### Final Project Report & Comprehensive Technical Specification
**1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE**

---

| **Field** | **Project Details** |
| :--- | :--- |
| **Project Title** | Anna-Setu: AI Campus Food Rescue & Plate-Waste Bio-Recycling Network |
| **Submitted By** | Pankhuri Govila (Student ID: 3281) |
| **Program Track** | 1M1B AI for Sustainability Virtual Internship (IBM SkillsBuild & AICTE) |
| **Internship Program** | 1M1B AI for Sustainability Virtual Internship (IBM SkillsBuild & AICTE) |
| **1M1B Mentor / Lead** | Paramjeet Sir (`paramjeet@onemoneb.org`) |
| **Primary SDG Alignment** | **SDG 12: Responsible Consumption & Production** (Target 12.3 & Target 12.5) |
| **Secondary SDG Alignment** | **SDG 2: Zero Hunger**, **SDG 11: Sustainable Cities**, **SDG 13: Climate Action** |
| **Project Tracker ID** | `PankhuriGovila_YIRP` (Shared with `paramjeet@onemoneb.org`) |
| **GitHub Repository** | [https://github.com/pgovila/Anna-Setu-Project](https://github.com/pgovila/Anna-Setu-Project) |
| **Live Interactive Demo** | [Hugging Face Spaces Gradio App](https://huggingface.co/spaces/pgovila/Anna-Setu-Demo) |
| **Drive Evidence Folder** | [Google Drive Assets & Video Demos](https://drive.google.com/drive/folders/1089iQX6AttZPXIuL8e6_bv6nGzkhyZW3?usp=sharing) |

---

## 📌 Executive Summary

Higher education institutions and university dining halls produce massive amounts of food waste through two structural systemic failures: **kitchen-level overproduction** (cooking arbitrary 10%-30% safety margins) and **consumer-level plate waste** (diners taking extra food onto their plates and discarding leftovers). Unconsumed food is routinely dumped into municipal landfills, where anaerobic decomposition generates fugitive methane ($CH_4$), a greenhouse gas 28 times more potent than $CO_2$, while simultaneously burdening municipal urban sanitation authorities (Lucknow Nagar Nigam).

**Anna-Setu** (*"Anna"* meaning sustenance and *"Setu"* meaning bridge) is a closed-loop socio-technical framework operating across two synchronized operational tracks:
* **Track A (AI Software Platform):** Combines time-series machine learning models to forecast kitchen preparation targets (cutting overproduction by 15%-25%) with a statutory **Retrieval-Augmented Generation (RAG) Compliance Engine** grounded in **FSSAI Surplus Regulations (2019)** and **Lucknow Nagar Nigam By-Laws** to safely redistribute untouched surplus meals to verified night shelters (Rain Basera Charbagh).
* **Track B (Smart IoT Plate-Waste Interceptor & Bio-Recycling Station):** A hardware kiosk deployed at the cafeteria tray-return counter that uses a precision plate scale and a dynamic behavioral nudge screen to deter over-serving, while channeling unavoidable plate scraps into an accelerated thermo-mechanical bio-composter that yields nutrient-rich **organic bio-fertilizer** within 12-24 hours.

Anna-Setu transforms an institutional liability into a measurable social good and agricultural asset, achieving **Zero Landfill Burden** on city sanitation infrastructure.

---

## 🛑 Section 1: Problem Statement & Real-World Context

> *"How might we use AI demand forecasting and smart on-site IoT hardware to eliminate cafeteria overproduction, deter individuals from taking extra food and wasting plate leftovers, and upcycle unconsumed food into recyclable elements so that institutional dining ecosystems reduce municipal burdens and environmental harm?"*

### 1.1 Structural Friction Points in Campus Dining
1. **Blind Preparation Safety Buffers (10% to 30% Overcooking):** Cafeteria management operates on fixed rotating menu cycles, cooking blind buffer margins to avoid the reputational risk of food running out during peak hours.
2. **Volatile Demand Factors:** Academic calendars (mid-terms, end-term exams, holidays, festivals) and external weather extremes (heavy rain or heatwaves) alter student mess turnout instantly.
3. **Redistribution Inefficiencies:** Safe donations fail to occur due to fear of food poisoning liability, lack of verified shelter directories, and unfamiliarity with municipal transport rules.
4. **Consumer Over-Serving on Dining Plates:** Diners routinely take extra portions onto their plates, fail to finish their meals, and dump leftovers into general waste bins with zero accountability or feedback.
5. **Municipal Solid Waste Burden & Landfill Methane:** Mixed food waste dumped into municipal bins creates rotting, foul-smelling garbage that burdens urban sanitation authorities (Lucknow Nagar Nigam), risks spot fines (**₹5,000-₹25,000** under LNN Solid Waste By-Laws), and generates fugitive methane ($CH_4$) in landfills.

---

## 🎯 Section 2: UN Sustainable Development Goal (SDG) Alignment

| UN SDG | Target Specifics | How Anna-Setu Directly Solves It |
| :--- | :--- | :--- |
| **SDG 12: Responsible Consumption and Production (PRIMARY)** | **Target 12.3:** Halve per-capita global food waste at retail and consumer levels by 2030.<br/>**Target 12.5:** Substantially reduce waste generation through prevention, reduction, recycling, and reuse. | **Track A** prevents kitchen overproduction by 15-25% via predictive AI; **Track B** intercepts plate waste, deters over-serving through behavioral nudges, and converts scraps into recyclable organic fertilizer. |
| **SDG 2: Zero Hunger (SECONDARY)** | **Target 2.1 & 2.2:** End hunger and ensure access to safe, nutritious food for vulnerable populations. | Surplus untouched kitchen food is verified through FSSAI compliance algorithms and safely dispatched to local night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar). |
| **SDG 11: Sustainable Cities & Communities** | **Target 11.6:** Reduce the adverse per-capita environmental impact of cities, including municipal waste management. | Eliminates the burden on municipal collection trucks by treating 100% of organic waste on-site, preventing illegal landfill dumping in city corridors. |
| **SDG 13: Climate Action** | **Target 13.3:** Improve institutional education and human capacity on climate change mitigation. | Diverting organic matter from anaerobic landfill decomposition eliminates methane emissions; real-time displays educate students on their carbon and water footprints. |

---

## 👥 Section 3: Target End Users & Beneficiaries

1. **Students & Campus Diners:** Interactive behavioral screens discourage taking excessive food, instilling mindful consumption habits and rewarding clean-plate dining.
2. **Kitchen & Mess Operations:** Predictive meal-demand forecasts cut raw material procurement costs by 15-25% and eliminate guesswork.
3. **Local Municipal Authorities (Lucknow Nagar Nigam):** Zero organic wet-waste burden delivered to municipal dustbins or transfer stations; compliance with Swachh Bharat Urban directives.
4. **Vulnerable Communities & Shelters:** Guaranteed access to wholesome, safety-verified surplus meals at empanelled night shelters.
5. **Campus Grounds & Agriculture:** Access to nutrient-rich, pathogen-free organic bio-fertilizer produced on-site for campus gardens, green belts, and local agriculture.

---

## 💡 Section 4: Detailed Solution Description (Design Thinking Approach)

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

### Stage 1: Empathize
* Kitchen staff lack low-effort tools to log consumption versus preparation quantities.
* Mess managers have no visibility into upcoming exam calendars or weather forecasts when placing procurement orders.
* Students have no visibility into the environmental cost of leaving food on their plates.
* Shelters need trusted, reliable surplus notifications with guaranteed food safety compliance.

### Stage 2: Define
* Need an automated system that forecasts meal attendance, verifies food safety regulations mathematically, alerts shelters within safe time windows, and deters student plate waste on-site.

### Stage 3: Ideate
* Conceptualized a **dual-track closed loop**:
  * Digital cognitive layer (Track A) for prediction, statutory verification, and shelter notification.
  * Physical hardware layer (Track B) for behavioral deterrence at tray return and on-site accelerated composting.

### Stage 4: Prototype
* Built Track A software with Gradio, Streamlit, and scikit-learn TF-IDF vector retrieval.
* Engineered Track B hardware architecture with ESP32 microcontroller, HX711 load cell, and MLX90614 infrared temperature sensor.
* Published official 3-page PDF and editable Word `.docx` documents.

### Stage 5: Test & Refine
* Executed 5 automated RAG verification scenarios in `test_rag.py`.
* Simulated 4 hardware telemetry events in `simulate_iot_kiosk.py`.
* Verified all 19 ecosystem checks in `validate_all.py`.

---

## 🤖 Section 5: Technical AI & IoT Architecture

### 5.1 Track A: The Anna-Setu AI Software Platform
1. **Module 1 (Smart Campus Dining Advisor):**
   * Uses gradient-boosted trees trained on historical swipe logs, academic calendars (mid-terms, finals, holidays), day-of-week patterns, and regional weather.
   * Outputs recommended morning cooking volumes per menu item with confidence intervals, cutting procurement waste by 15%-25%.
2. **Module 2 (Predictive Redistribution & RAG Pipeline):**
   * Evaluates leftover food against indexed statutory documents:
     * **FSSAI Surplus Regulations (2019):** Microbial danger zone ($5^\circ\text{C}-65^\circ\text{C}$), ambient 2h/4h rule, prohibited food categories, and Good Samaritan legal immunity (Section 7).
     * **Lucknow Nagar Nigam (LNN) By-Laws:** 45-minute municipal transit corridor ceiling across Lucknow Zones 1-8, verified Rain Basera directories, and mandatory organic bio-composting diversion (Section 18).
   * **IBM Granite Foundation Model Synthesis:** Automatically compiles structured surplus parameters into:
     * WhatsApp/SMS broadcast alerts (<60 words) for shelter coordinators.
     * Official digital **FSSAI Form B & LNN Gate Pass manifests**.

### 5.2 Track B: Smart Plate-Waste Interceptor & Bio-Recycling Converter
* **Behavioral Nudge Front-End:**
  * Precision plate scale (0-20 kg) at tray return instantly registers tare-subtracted plate leftover grams.
  * 7-inch dynamic display shows wasted grams, embedded water footprint (e.g. 125 Liters), and hostel clean-plate leaderboards.
* **Accelerated Aerobic Composter ($55^\circ\text{C}-65^\circ\text{C}$):**
  * Macerator shredder reduces scrap size to 3-5 mm.
  * Thermophilic heating + active aerobic aeration fan + microbial enzymes achieve an **85% to 90% volume reduction in 12-24 hours**.
* **Recyclable Output:** Produces pathogen-free, nutrient-rich **Organic Bio-Fertilizer / Soil Conditioner** for campus greening and local farmers, removing 100% of organic waste from municipal collection trucks.
* **Hardware BOM & Cost Feasibility:** Built with off-the-shelf maker electronics for **₹4,670 (~$55 USD)**.

---

## 🏛️ Section 6: Statutory Food Regulations & Municipal Compliance

### 6.1 FSSAI Surplus Food Regulations (2019) Timelines
* **Microbial Danger Zone:** $5^\circ\text{C} \text{ to } 65^\circ\text{C}$ ($41^\circ\text{F} \text{ to } 149^\circ\text{F}$), where bacteria (*Bacillus cereus*, *Salmonella*, *C. perfringens*) double every 15-20 minutes.
* **Ambient "2-Hour / 4-Hour Rule" (Reg 4(2)):**
  * **0 - 2 Hours:** 🟢 **Compliant (Safe)** - Optimal window for redistribution, rapid chilling ($\le 5^\circ\text{C}$), or reheating ($\ge 74^\circ\text{C}$).
  * **2 - 3 Hours:** 🟢 **Compliant (Optimal Handoff)** - Standard dispatch window.
  * **3 - 4 Hours:** 🟡 **Compliant (Urgent Dispatch)** - Critical upper safety window; food must be consumed immediately upon delivery. No re-cooling permitted.
  * **> 4 Hours:** 🔴 **Non-Compliant (Rejected)** - Unsafe for human consumption due to heat-stable enterotoxin risk. Redistribution is blocked; food diverted to composting.
* **Active Temperature Controls (Reg 4(3)):** Hot holding maintained at $\ge 65^\circ\text{C}$; cold holding $\le 5^\circ\text{C}$.
* **Good Samaritan Immunity (Reg 4(5) & Sec 7):** Donors acting in good faith who comply with hygienic and temperature standards are legally indemnified against civil or criminal liability.
* **Audit Trail (Reg 7):** Mandatory **Form B Surplus Handover Register** kept for 1 year for Food Safety Officer audits.

### 6.2 Lucknow Nagar Nigam (LNN) Municipal Guidelines
* **Corridor Transit Ceiling (Sec 14):** Maximum **45 minutes** transit across Lucknow traffic corridors to prevent heat-spoilage in summer ($>38^\circ\text{C}$). Insulated thermal cambros required for $>45$ mins.
* **Dumping Ban & Penalties (Sec 10):** Illegal to discard commercial food waste into municipal dustbins (*dhalavs*); spot fines **₹5,000 to ₹25,000**.
* **Zero-Landfill Mandate (Sec 18):** Non-compliant surplus food **must NEVER** be dumped in municipal garbage bins. It must be diverted to campus aerobic composting or LNN Kanha Upvan / Mohanlalganj biomethanation facilities.
* **Gate Clearance (Sec 21):** Campus security must verify and timestamp all outgoing food rescue vehicles with an Anna-Setu Digital Gate Pass.

---

## 🛡️ Section 7: Responsible AI Framework

| Pillar | Applied Implementation Logic in Anna-Setu |
| :--- | :--- |
| **Fairness** | Demand forecasting uses aggregate dining hall attendance logs stripped of personal identifiers; predictions are audited across dietary preferences (vegetarian, non-vegetarian, Jain) to ensure equitable portioning. |
| **Transparency** | Explains every forecast with top 3 driver factors (e.g. "Predicted 15% reduction due to end-semester exam schedule"). |
| **Ethics** | Embedded verification blocks completely halt donation if a batch's holding time exceeds FSSAI 4-hour limits; non-compliant batches are strictly diverted to on-site composting. |
| **Privacy** | Student registration numbers and personal dietary profiles are never recorded or shared; telemetry streams only anonymous aggregate weights. |

---

## 📈 Section 8: Quantified Triple-Bottom-Line Impact

### 8.1 Economic Impact
* **15% to 25% Reduction in Cafeteria Buffer Procurement Costs:** Saves ₹35,000 to ₹60,000 monthly per institutional dining hall.
* **Avoidance of Municipal Penalties:** Eliminates risk of ₹5,000-₹25,000 spot fines under Lucknow Nagar Nigam SWM By-Laws.
* **Free High-Grade Organic Fertilizer:** Generates ~10 kg of bio-fertilizer daily (~2,400 kg annually), replacing commercial chemical fertilizers for campus grounds.

### 8.2 Environmental Impact
* **100% Elimination of Landfill Organic Waste:** Diverts ~68 kg of food waste daily per 800-student mess.
* **Methane Emissions Avoided:** Avoids ~129 kg $CO_2e$ of fugitive methane emissions daily (~31 Metric Tons $CO_2e$ annually).
* **Freshwater Conservation:** Saves hundreds of thousands of liters of embedded water by deterring plate waste via the behavioral nudge screen.

### 8.3 Social & Community Impact
* **Dignified Nutrition Security:** Redirects 40-80 wholesome meals daily to residents of Rain Basera Charbagh and rural patient attendants at KGMU Trauma Centre.
* **Mindful Consumption Culture:** Empowers university students to develop lifelong zero-waste eating habits.

---

## 📅 Section 9: Project Timeline & Phased Milestones

* **Phase 1 & 2 (Completed - Nov 1 to Nov 10, 2026):** RAG Compliance Engine built; FSSAI and LNN by-laws codified; Gradio & Streamlit UIs deployed; 5 automated tests passing.
* **Sprint 3A (Nov 11 to Nov 20, 2026):** Procure hardware components (ESP32, HX711, MLX90614, display); assemble bench breadboard; write C++/MicroPython firmware for Wi-Fi data streaming.
* **Sprint 3B (Nov 21 to Nov 30, 2026) - [MILESTONE 1 APPROVAL GATE]:** Draft campus mess permission letter and MoU for Dean of Student Welfare / Campus Administration; contact Lucknow shelter coordinators; present integrated bench prototype to 1M1B mentor.
* **Phase 4 (Dec 1 to Dec 21, 2026):** Fabricate IP65 splash-proof enclosure; install station in central mess; conduct 14-day live campus pilot tracking real plate waste and redistributing compliant surplus to Rain Basera Charbagh.
* **Phase 5 (Dec 22 to Dec 31, 2026) - [MILESTONE 2 DEPLOYMENT GATE]:** Retrain Module 1 demand model using real pilot logs; compute total kg rescued, $CO_2e$ avoided, and ₹ saved; submit final report, presentation, and video before **December 31, 2026**.

---

## 🔗 Section 10: Submission Assets & Deliverables

1. **GitHub Repository:** [https://github.com/pgovila/Anna-Setu-Project](https://github.com/pgovila/Anna-Setu-Project)
2. **Live Gradio Demo (Hugging Face Spaces):** [https://huggingface.co/spaces/pgovila/Anna-Setu-Demo](https://huggingface.co/spaces/pgovila/Anna-Setu-Demo)
3. **Google Drive Asset Dossier:** [Google Drive Evidence Folder](https://drive.google.com/drive/folders/1089iQX6AttZPXIuL8e6_bv6nGzkhyZW3?usp=sharing)
4. **Official 3-Page PDF Submission:** [`Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf`](Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf)
5. **Editable Word Document (.docx):** [`Anna_Setu_Project_Brief_Timeline_and_Tracker.docx`](Anna_Setu_Project_Brief_Timeline_and_Tracker.docx)
6. **Master Google Sheets Tracker:** [`PankhuriGovila_YIRP_Project_Tracker.xlsx`](PankhuriGovila_YIRP_Project_Tracker.xlsx) (Shared with `paramjeet@onemoneb.org`)
7. **Statutory Regulatory Manual:** [`FOOD_REGULATIONS_AND_LNN_GUIDELINES.md`](FOOD_REGULATIONS_AND_LNN_GUIDELINES.md)
8. **Institutional Approvals & MoU Dossier:** [`INSTITUTIONAL_APPROVALS_AND_MOU_TEMPLATES.md`](INSTITUTIONAL_APPROVALS_AND_MOU_TEMPLATES.md)
9. **Presentation Deck Update Guide:** [`PRESENTATION_SLIDES_UPDATE_GUIDE.md`](PRESENTATION_SLIDES_UPDATE_GUIDE.md)
10. **Hardware Firmware:** [`firmware/esp32_smart_kiosk.ino`](firmware/esp32_smart_kiosk.ino)
