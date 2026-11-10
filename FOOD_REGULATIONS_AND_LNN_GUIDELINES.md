# 🍽️ Anna-Setu: Food Regulations, Timelines & Compliance Framework
### Comprehensive Guide to FSSAI Surplus Food Regulations (2019) & Lucknow Nagar Nigam (LNN) Food Service By-Laws
*Integrated into the Anna-Setu Retrieval-Augmented Generation (RAG) Architecture*

---

## 📌 Executive Summary

**Anna-Setu** (*"Anna"* meaning sustenance and *"Setu"* meaning bridge) is an AI-powered campus surplus food rescue network designed for educational institutions, hostels, and institutional cafeterias. While the core mission aligns with **UN SDG 12 (Target 12.3: Halving Food Waste)** and **UN SDG 2 (Zero Hunger)**, redistributing prepared food introduces strict legal, microbiological, and municipal responsibilities.

Foodborne pathogen proliferation, thermal abuse during ambient holding, and unauthorized waste disposal pose severe risks to vulnerable community members and expose institutions to regulatory liability. To solve this, Anna-Setu integrates an automated **Retrieval-Augmented Generation (RAG) Compliance Pipeline** that checks every prospective surplus batch against:
1. **The Food Safety and Standards Authority of India (FSSAI)** statutory regulations, holding times, and temperature danger zones.
2. **Lucknow Nagar Nigam (LNN / Lucknow Municipal Corporation)** food sanitation, street service, shelter network, and solid waste management (SWM) by-laws.

This document serves as the authoritative operational manual, regulatory reference, and implementation specification for institutional food operators, mess committees, and AI pipeline administrators.

---

## 🏛️ Section 1: Statutory Framework 1 — FSSAI National Regulations

The regulatory governance of surplus food donation in India is established under the **Food Safety and Standards Act, 2006 (Sections 16 & 31)** and formally enacted in the **Food Safety and Standards (Recovery and Distribution of Surplus Food) Regulations, 2019** (Notification No. 1-100/FSSAI/SP(SP-Surplus Food)/2018).

### 1.1 Key Statutory Definitions (Regulation 2)
* **Food Business Operator (FBO):** Any entity running a food business, including university dining halls, residential mess facilities, private college canteens, catering services, and cloud kitchens.
* **Surplus Food:** Untouched, wholesome, prepared, or packaged edible food that has not been served to diners, remains within its microbiologically safe shelf-life, and would otherwise be discarded due to demand mismatches.
* **Surplus Food Distribution Organization (SFDO):** A registered non-governmental organization (NGO), charity, or community food bank empanelled with FSSAI to collect, transport, and distribute surplus food directly to needy beneficiaries.

### 1.2 The Microbial Danger Zone & Biological Risk Factors
Microorganisms such as *Bacillus cereus*, *Clostridium perfringens*, *Salmonella spp.*, and *Staphylococcus aureus* multiply exponentially at room temperature.

$$\text{Microbial Danger Zone: } 5^\circ\text{C} \text{ to } 65^\circ\text{C} \quad (41^\circ\text{F} \text{ to } 149^\circ\text{F})$$

* Between $20^\circ\text{C}$ and $45^\circ\text{C}$ (typical ambient indoor room temperatures in Lucknow), bacterial cell division doubles approximately every **15 to 20 minutes**.
* *Bacillus cereus*, common in cooked rice and grain preparations, produces heat-stable emetic enterotoxins if cooked starchy food is held at ambient temperatures. These toxins are not inactivated even by subsequent boiling or reheating.

### 1.3 Timelines: The 2-Hour / 4-Hour Ambient Holding Rule (Regulation 4(2))
For cooked perishable foods maintained without active heating ($\ge 65^\circ\text{C}$) or active refrigeration ($\le 5^\circ\text{C}$), FSSAI mandates strict time-in-danger-zone ceilings:

| Cumulative Time in Danger Zone | Compliance Status | Operational & Redistribution Directive |
| :--- | :--- | :--- |
| **0 to 2 Hours (0 – 120 mins)** | 🟢 **COMPLIANT (SAFE)** | Optimal window. Food may be redistributed, chilled down to $\le 5^\circ\text{C}$, or reheated to an internal core temperature of $\ge 74^\circ\text{C}$. |
| **2 to 3 Hours (121 – 180 mins)** | 🟢 **COMPLIANT (OPTIMAL HANDOFF)** | Prime redistribution dispatch window. Must be handed over to shelter volunteers with transit scheduled immediately. |
| **3 to 4 Hours (181 – 240 mins)** | 🟡 **COMPLIANT (URGENT DISPATCH)** | Upper critical safety threshold. Must be dispatched immediately for **instant consumption**. No secondary storage, refrigeration, or re-chilling is legally permitted. |
| **> 4 Hours (> 240 mins)** | 🔴 **NON-COMPLIANT (REJECTED)** | **UNFIT FOR HUMAN CONSUMPTION.** Food enters the exponential bacterial enterotoxin phase. Distribution is strictly prohibited. Food must be diverted to organic bio-composting. |

### 1.4 Active Temperature Holding Standards (Regulation 4(3))
When active commercial kitchen equipment is employed:
* **Active Hot Holding:** Food must be held continuously at or above **$65^\circ\text{C}$ ($149^\circ\text{F}$)**. Safe holding time extends up to **4.5 hours (270 mins)**, provided core temperature never drops below $65^\circ\text{C}$.
* **Active Cold Holding:** Food must be held continuously at or below **$5^\circ\text{C}$ ($41^\circ\text{F}$)**.
* **Rapid Chilling Curve:** If hot surplus food is preserved for deferred redistribution, it must be cooled from $65^\circ\text{C}$ to $21^\circ\text{C}$ within **2 hours**, and further chilled from $21^\circ\text{C}$ down to $\le 5^\circ\text{C}$ within an additional **4 hours**.

### 1.5 Food Categorization & Suitability Matrix (Regulation 4(4))

| Category Key | Category Description | Examples | Max Ambient Holding Window | Reheating Internal Temp | Risk Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cooked_grains_curry` | High-moisture cooked grains, lentils, curries | Rice, Dal Tadka, Vegetable Pulao, Sambhar, Kadhi | **4 Hours (240 mins)** | $\ge 74^\circ\text{C}$ | High risk (*B. cereus*, *C. perfringens*) |
| `dry_staples_roti` | Dry cooked breads and stir-fried vegetables | Chapatis, Phulkas, Rotis, Pooris, Dry Aloo Jeera | **5 Hours (300 mins)** | Optional | Moderate risk (moisture condensation) |
| `dairy_sweets` | Perishable dairy, paneer, and milk-based desserts | Paneer Butter Masala, Kheer, Rasgulla, Halwa | **3 Hours (180 mins)** | $\ge 74^\circ\text{C}$ | High risk (*Staph aureus*, *Listeria*) |
| `fried_snacks` | Deep-fried dry savories | Samosas, Vegetable Cutlets, Mathri | **5 Hours (300 mins)** | Not required | Low to moderate risk |
| `raw_salads_cut_fruits` | Cut raw vegetables, fruits, wet chutneys | Sliced onions, cucumbers, tomatoes, mint chutney | **2 Hours (120 mins)** | Cannot reheat | **PROHIBITED** from donation under FSSAI Reg 4(4) |
| `plate_waste` | Uneaten table scraps / consumer buffet returns | Food left over on customer dining plates | **0 Minutes** | N/A | **STRICTLY FORBIDDEN** (Biological contamination) |

### 1.6 Mandatory Packaging & Labeling Standards (Regulation 5)
Surplus food must be placed in clean, food-grade non-toxic containers (FSSAI Packaging Regulations 2018). Each consignment dispatched from an institutional dining hall must bear an **Anna-Setu Dispatch Label**:
1. Food Item Description & Net Servings
2. Dietary Emblem: **Green Dot** (Vegetarian) or **Brown Triangle** (Non-Vegetarian)
3. Batch Preparation Timestamp: `YYYY-MM-DD HH:MM` (24-hour IST)
4. Safe-Pickup-By and Must-Consume-By Deadline: `HH:MM IST`
5. Storage Instructions: *"Keep Hot ($\ge 65^\circ\text{C}$)"* or *"Consume within 45 mins of delivery"*
6. Donor Establishment Name & Mess Supervisor Contact

### 1.7 Good Samaritan Protection (Regulation 4(5) & Section 7)
Section 7 of the 2019 Regulations affords full **legal immunity** to food donors:
> *"No food business operator shall be liable for any civil or criminal proceedings for any death or injury caused to any person resulting from consumption of surplus food donated in good faith, provided that the food business operator complied with all food safety and hygiene requirements at the time of donation."*

### 1.8 Mandatory Handover Register — Form B (Regulation 7)
Institutions must record all surplus donations in a permanent **Surplus Food Handover Register (Form B)**, retained on campus for a minimum of **1 year** for audit by State Food Safety Officers (FSOs).

---

## 🏛️ Section 2: Statutory Framework 2 — Lucknow Nagar Nigam (LNN) Guidelines

In addition to national FSSAI mandates, all campus operations within the urban agglomeration of Lucknow are subject to the **Lucknow Nagar Nigam (Lucknow Municipal Corporation / LMC)** Sanitation By-Laws, the **UP Food Safety and Drug Administration (FSDA - Lucknow Division)**, and the **Swachh Lucknow Zero-Food-Waste Initiative**.

### 2.1 LNN Municipal Jurisdiction & Zonal Transit Windows
Lucknow is divided into **8 Administrative Zones**. Because traffic congestion along primary corridors (Hazratganj Chauraha, Polytechnic Chauraha, Charbagh Station, Awadh Chauraha) can be severe, and summer ambient temperatures frequently exceed $40^\circ\text{C}$, LNN imposes an intra-city transport limit.

```
                    ┌───────────────────────────┐
                    │  LUCKNOW MUNICIPAL ZONES  │
                    └─────────────┬─────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
  Zone 1: Central         Zone 4: East IT/Campus    Zone 5: South Transit
 (Hazratganj, Chowk,     (Gomti Nagar, Extension,   (Alambagh, ISBT,
  Charbagh, KGMU)         Indira Nagar, BBD)         Singar Nagar)
 [Transit: ~30-35m]       [Transit: ~20-25m]         [Transit: ~30-35m]
```

* **LNN Corridor Transit Ceiling (Section 14):** Cooked surplus food transported at ambient temperature must spend **no more than 45 minutes in road transit**.
* If the transit calculation between campus origin (e.g., Zone 4 Gomti Nagar) and destination shelter (e.g., Zone 1 Charbagh or Zone 6 Hardoi Road) exceeds 45 minutes, the vehicle must be equipped with **insulated thermal cambros or insulated food delivery bags**.

### 2.2 Verified LNN Shelter Network (Rain Basera & NGOs)
Under LNN Sanitation Directive Section 12, campus surplus must be prioritized toward verified municipal night shelters and empanelled charities:

| Facility Identifier | Facility Name | LNN Zone | Typical Beneficiaries | Cold Chain Available? |
| :--- | :--- | :--- | :--- | :--- |
| `SHELTER-LNN-01` | **Rain Basera Charbagh Railway Hub** | Zone 1 (Station Road) | Unhoused daily-wage workers, stranded passengers | No |
| `SHELTER-LNN-02` | **Rain Basera KGMU Trauma Centre** | Zone 1 (Chowk) | Rural patients' attendants, economically distressed families | **Yes** (Commercial Chiller) |
| `SHELTER-LNN-03` | **Rain Basera Gomti Nagar** | Zone 4 (Vibhuti Khand) | Urban night-shift & construction labour camps | No |
| `SHELTER-LNN-04` | **Rain Basera Alambagh Bus Terminus** | Zone 5 (ISBT Gate 3) | Inter-state transit labourers, unhoused commuters | No |
| `SHELTER-NGO-05` | **Lucknow Roti Bank (Central Chapter)** | Zone 1 (Hazratganj) | Slum clusters, destitute elders, mobile food vans | **Yes** (Deep Freezers) |
| `SHELTER-NGO-06` | **Asha Jyoti Kendra Shelter** | Zone 4 (Gomti Nagar Ext) | Women and children in institutional care | **Yes** (Standard Chiller) |

### 2.3 LNN SWM By-Law Section 10: Ban on Food Waste Dumping
Educational institutions, university cafeterias, and hostel messes producing over $100\text{ kg}$ of waste per day are classified as **Bulk Waste Generators (BWGs)**:
* Dumping edible surplus or unsegregated commercial food waste into municipal dustbins, open dumps (*dhalavs*), or storm drains (*nullahs*) is strictly illegal.
* Violations trigger spot financial penalties under LNN By-Laws:
  * **First Offense:** INR 5,000 spot fine.
  * **Second Offense:** INR 10,000 spot fine.
  * **Persistent Non-Compliance:** INR 25,000 spot fine plus cancellation of the commercial trade/sanitation license.

### 2.4 LNN SWM By-Law Section 18: Expired Food Diversion Mandate
When a surplus food consignment fails FSSAI microbial criteria (e.g., $>4$ hours ambient holding, sensory souring, broken cold chain):
1. The food **CANNOT** be delivered to any shelter or human beneficiary.
2. It **CANNOT** be dumped in municipal waste bins.
3. It must be segregated into **100% Green Wet Organic Waste** containers and routed to:
   * **On-Campus Decentralized Aerobic Composting Pits**, OR
   * **Lucknow Nagar Nigam Wet Waste Processing Plants:**
     * *Kanha Upvan Decentralized Biomethanation Plant* (Zone 5/8)
     * *Mohanlalganj 300 TPD Bio-CNG & Waste-to-Energy Processing Facility*

### 2.5 LNN Health Section 21: Campus Gate Clearance Protocol
Every vehicle transporting rescued food out of an educational campus must present an **Anna-Setu Digital Gate Pass** to institutional security guards, recording:
* Vehicle Registration & Volunteer/Driver Identity
* Time of Campus Exit
* Verified FSSAI Compliance Status (`COMPLIANT_SAFE` or `COMPLIANT_URGENT`)
* Designated Destination Shelter

---

## 🤖 Section 3: The Anna-Setu RAG System Architecture

The Anna-Setu system implements a production-grade, modular **Retrieval-Augmented Generation (RAG)** pipeline that evaluates kitchen logs, computes time-temperature physics, queries legal statutory corpora, and generates IBM Granite-formatted outputs.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ANNA-SETU RAG PIPELINE FLOW                           │
└─────────────────────────────────────────────────────────────────────────────┘

  [Cafeteria Log Input]
  Item: Veg Pulao & Dal | Servings: 50 | Prep Time: 12:30 | Condition: Ambient
  Campus Origin: Zone 4 (Gomti Nagar) | Destination: Rain Basera Charbagh
                                │
                                ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 1. FoodComplianceEngine (Deterministic Verification Engine)   │
  │    - Calculates: Elapsed Time (90m) + Transit Corridor (35m)   │
  │    - Evaluates: Total Exposure = 125m <= 240m Ambient Max     │
  │    - Computes: Safe-Pickup-By = 16:30 IST                     │
  │    - Verdict: 🟢 COMPLIANT_SAFE                               │
  └─────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 2. RegulatoryRetriever (Vector Semantic Search Engine)        │
  │    - TF-IDF Vectorizer (1-3 N-Grams) + Cosine Similarity      │
  │    - Indexes: fssai_guidelines.json & lnn_guidelines.json     │
  │    - Retrieves: FSSAI-REG-4-2 (Holding limits), LNN-SEC-14    │
  └─────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 3. GraniteAlertCompiler (IBM Granite Prompt Synthesizer)      │
  │    - Formulates: Context-grounded WhatsApp/SMS Alert (<60 w)  │
  │    - Formulates: FSSAI Form B Audit Manifest + Gate Pass      │
  │    - Formulates: LNN Biomethanation Divert (if non-compliant) │
  └─────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
           [Human-in-the-Loop Mess Manager Approval]
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
 [WhatsApp/SMS to Shelter]                   [Security Gate Pass]
```

### 3.1 Subsystem Components

1. **`rag/knowledge_base/`**:
   * `fssai_guidelines.json`: Contains 9 codified clauses covering definitions, ambient limits, active holding temperatures, exclusions, Good Samaritan protection, packaging, and Form B logs.
   * `lnn_guidelines.json`: Contains 5 municipal by-laws covering dumping bans, shelter empanelment, corridor transit buffers, biomethanation diversion, and gate security.
   * `shelters_lucknow.json`: Complete directory of Lucknow shelters with zonal coordinates, contacts, and capacities.

2. **`rag/retriever.py` (`RegulatoryRetriever`)**:
   * Uses an n-gram $(1, 3)$ TF-IDF vector matrix combined with cosine similarity matching to return statutory clauses relevant to the exact operational query.
   * Guarantees zero hallucination: the model cites statutory identifiers (e.g., `FSSAI-REG-4-2`, `LNN-BYLAW-SEC-10`).

3. **`rag/compliance_engine.py` (`FoodComplianceEngine`)**:
   * Implements exact microbiological time-temperature bounds.
   * Cross-references origin and destination zones across the Lucknow Municipal transit matrix to guarantee that transit buffers are factored in before food is cleared for pickup.

4. **`rag/granite_generator.py` (`GraniteAlertCompiler`)**:
   * Follows IBM Granite prompt engineering principles from the 1M1B report:
     * Never invents facts, quantities, or times.
     * Accurately cites the retrieved compliance rule.
     * Adheres strictly to the 60-word limit for WhatsApp/SMS readability.
     * Incorporates Good Samaritan indemnity and Form B audit formatting.

5. **`rag/pipeline.py` (`AnnaSetuRAGPipeline`)**:
   * High-level unified coordinator providing single-line evaluation (`evaluate_surplus`) and open-ended regulatory semantic search (`query_regulations`).

---

## 📋 Section 4: Standard Operating Procedures (SOPs)

### SOP-01: Cafeteria Surplus Logging (End of Service)
1. **Timing:** At the close of each lunch (14:00) or dinner (21:30) service, the mess supervisor logs remaining untouched bulk food.
2. **Exclusion Check:** Inspect the food to ensure zero plate waste, zero customer contact, and zero table returns.
3. **Data Entry:** Enter food name, estimated portions, cooking completion time, and storage mode into Anna-Setu.

### SOP-02: Organoleptic Quality Inspection Checklist
Before submitting a batch to Anna-Setu, the mess supervisor must complete a 3-point sensory check:
* **Visual:** No surface discoloration, mold spots, unusual bubbling, or skinning.
* **Olfactory:** Fresh, characteristic aroma. Discard immediately if any souring, rancidity, or off-odor is detected.
* **Thermal Core Check:** If hot-held, probe internal temperature using a calibrated digital stem thermometer ($\ge 65^\circ\text{C}$). If ambient, check against the 4-hour clock.

### SOP-03: Packaging & Dispatch Labeling
1. Decant approved food into sanitized, food-grade stainless steel vessels or food-grade containers.
2. Print or handwrite the Anna-Setu Dispatch Label:
   ```text
   ┌────────────────────────────────────────────────────────┐
   │ 🍽️ ANNA-SETU SURPLUS FOOD DISPATCH LABEL              │
   │ Item: Vegetable Pulao & Dal Tadka     Portions: 45     │
   │ Dietary: [🟢 VEG]                     Batch ID: AS-245 │
   │ Prepared: 12:30 IST                  Safe Until: 16:30 │
   │ Condition: Ambient - Consume within 45 mins of arrival │
   │ Campus: UPES / Lucknow Central Mess, Gate 2            │
   └────────────────────────────────────────────────────────┘
   ```
3. Secure lids with tamper-evident paper seals.

### SOP-04: Non-Compliant Food Diversion (Zero-Landfill Protocol)
If Anna-Setu flags a batch as `NON_COMPLIANT_REJECTED`:
1. **DO NOT DISPATCH** to any shelter or individual.
2. Transfer the batch into **Green Wet Waste Bins**.
3. Log the rejection in the campus waste management register with the Anna-Setu Rejection ID.
4. Transport to on-campus aerobic compost beds or arrange pickup by the LNN Wet Waste biomethanation vehicle.

---

## 📑 Section 5: Official Compliance Manifest Templates

### 5.1 FSSAI Form B Surplus Handover Register (Logbook Record)

```text
======================================================================
   ANNA-SETU OFFICIAL SURPLUS FOOD COMPLIANCE MANIFEST (FORM B)
   In Accordance with FSSAI Surplus Regulations 2019 & LNN SWM By-Laws
======================================================================

BATCH STATUS:        🟢 COMPLIANT (SAFE FOR REDISTRIBUTION)
FOOD ITEM:           Vegetable Pulao and Dal Tadka (Cooked Grains, Rice, Dal)
QUANTITY / SERVINGS: 50 Portions
STORAGE CONDITION:   AMBIENT
PREPARATION TIME:    12:30 IST
VERIFICATION TIME:   14:00 IST (Elapsed: 90 mins)
TRANSIT ESTIMATE:    35 mins (Corridor: Zone 4 -> Zone 1)
SAFE CONSUME-BY:     16:30 IST
DISPATCH LOCATION:   Main Campus Dining Hall, Gate 2
TARGET RECIPIENT:    Rain Basera Charbagh Railway Hub

STATUTORY COMPLIANCE CITATIONS (RAG RETRIEVED):
- [FSSAI-REG-4-2] Ambient Storage Danger Zone & Holding Timeline Ceiling
- [FSSAI-REG-6] Transit Sanitation and Cross-Contamination Prevention
- [LNN-BYLAW-SEC-14] Municipal Transit Buffer Ceiling & Hot Season Precautions

OPERATIONAL DIRECTIVE:
Compliance Note: Compliant with FSSAI Surplus Reg 4(2) & 4(3) temperature-holding standards.
LNN Municipal Action: Standard dispatch approved. Issue Gate Pass under LNN Health Sec 21.

LEGAL INDEMNITY (GOOD SAMARITAN CLAUSE):
This donation is made in good faith in strict compliance with FSSAI Surplus Food
Regulations 2019 Regulation 4(5) and Section 7. The donor is indemnified against civil
and criminal liability once handed over within verified thermal and time thresholds.
======================================================================
DISPATCH SIGN-OFF: ___________________    RECIPIENT SIGN-OFF: ___________________
Mess Manager, Anna-Setu Campus Hub         Verified Shelter / NGO Coordinator
======================================================================
```

### 5.2 LNN Gate Clearance Pass (Campus Security Copy)

```text
======================================================================
         LUCKNOW NAGAR NIGAM CAMPUS GATE SECURITY PASS (SEC 21)
======================================================================
Pass ID:         ANNA-SETU-GP-2026-1110-01
Timestamp:       10-Nov-2026, 14:15 IST
Vehicle No:      UP-32-XX-XXXX (Dedicated Covered Vehicle)
Driver / Lead:   Rakesh Kumar (Verified Shelter Volunteer)
Destination:     Rain Basera Charbagh Hub (Zone 1)
Approved Window: Exit permitted between 14:10 and 14:30 IST only
FSSAI Clearance: [VERIFIED 🟢] Max transit time: 35 minutes
======================================================================
Security Guard Signature: __________________   Gate No: Gate 2
======================================================================
```

---

## 🧪 Section 6: Verification & Automated Testing

The integrated RAG pipeline is thoroughly tested via `test_rag.py` across five realistic scenarios:
1. **Fresh Batch Test:** 1.5 hours elapsed, ambient $\to$ Confirms `COMPLIANT_SAFE`, safe pickup by 16:30, pulls FSSAI Reg 4(2).
2. **Critical Threshold Test:** 2 hours 45 minutes elapsed, ambient $\to$ Confirms `COMPLIANT_URGENT`, flags rapid consumption mandate.
3. **Expired Batch Test:** 4.5 hours elapsed, ambient $\to$ Confirms `NON_COMPLIANT_REJECTED`, blocks redistribution, activates LNN Section 18 biomethanation directive.
4. **Prohibited Category Test:** Raw cut cucumber salad $\to$ Confirms `NON_COMPLIANT_REJECTED` under FSSAI Reg 4(4).
5. **Direct Semantic Search Test:** Direct query for municipal dumping penalties $\to$ Correctly retrieves LNN SWM By-Law Section 10 citing INR 5,000 to INR 25,000 fines.

To execute the test suite locally:
```bash
python test_rag.py
```

To run the interactive Streamlit interface:
```bash
streamlit run streamlit_app.py
```

To launch the Hugging Face Gradio space interface:
```bash
python app.py
```

