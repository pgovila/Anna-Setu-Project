# Anna-Setu: AI-Powered Campus Food Rescue & Redistribution Network 🍽️🌐

### 1M1B AI for Sustainability Virtual Internship Project Submission
*In Collaboration with IBM SkillsBuild & AICTE*

---

## 🚀 Live System Architecture Deploys
* **Interactive Live Simulation Workspace:** [Launch Gradio Interface on Hugging Face Spaces](https://huggingface.co/spaces/pgovila/Anna-Setu-Demo)


## 📌 Project Architecture Overview
**Anna-Setu** ("Anna" meaning food/sustenance and "Setu" meaning bridge) acts as an intelligent digital bridge engineered to minimize large-scale food overproduction on educational institution campuses. The framework couples historical time-series consumption analysis with a real-time, compliance-checked automated redistribution network.

* **Primary SDG Focus:** **SDG 12 — Responsible Consumption and Production** (Specifically addressing Target 12.3: Halving retail/consumer food waste by 2030).
* **Secondary SDG Focus:** **SDG 2 — Zero Hunger** (Directing surplus resources to food-insecure municipal structures).

---

## 🛑 The Core Problem
University dining ecosystems experience significant waste margins due to structured friction clusters:
1. **Arbitrary Preparation Thresholds:** Cafeterias cook fixed buffer volumes blindly (+10% to +30%) to mitigate structural inventory exhaustion risks.
2. **Volatile Demand Factors:** Academic calendars (exams, mid-term holidays), local weather extremes, and on-campus events alter diner turnout instantly.
3. **Redistribution Inefficiencies:** Safe, manual handoffs to shelters fail to occur due to localized verification constraints, logistics synchronization friction, and complex municipal regulatory parameters.

---

## 🤖 Technical AI & Logic Architecture

### Module 1: Smart Campus Dining Advisor (Predictive Forecasting)
* Utilizes historical log structures (turnstile swipe logs, menu configurations) combined with regional weather variables and holiday patterns to project optimized kitchen preparation ranges via regression models.

### Module 2: Predictive Redistribution Pipeline (Granite + RAG)
* **Vector Index Retrieval (RAG):** Evaluates leftover data fields alongside indexed municipal compliance documentation (e.g., ambient storage parameters) to verify safety compliance thresholds.
* **Large Language Models (IBM Granite):** Automatically creates clean text notifications mapping dynamic quantities and destination vectors for nearby shelters.

---

## 📁 Repository Structure
```text
├── app.py                # Main Streamlit Interactive Live Interface File
├── requirements.txt      # Engine execution prerequisites (streamlit)
└── README.md             # Standard structural project documentation index
```

---

## 🛡️ Responsible AI Framework

| Pillar | Applied Implementation Logic |
| :--- | :--- |
| **Fairness** | Analysis utilizes fully anonymized data registers aggregated at the dining hall level, preventing individual dietary profiling or biometric tracking loops. |
| **Transparency** | The engine renders explicit, plain-language text flags identifying exactly why a production value dropped (e.g., "Forecasted 15% reduction due to end-semester exam dates"). |
| **Ethics** | Embedded verification blocks completely block donation generation parameters if a batch's calculated holding time exceeds regional health limits. |
| **Privacy** | Student registration matrices are fully stripped of personal identities before log injection sequences process. |
