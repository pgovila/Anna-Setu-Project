# 🍛 Anna-Setu: Campus Food Rescue & Bio-Recycling Network

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pgovila-anna-setu-demo.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Anna-Setu** (*"Food Bridge"* in Hindi) is an AI-powered campus surplus food rescue and bio-recycling management platform. It bridges institutional dining halls with verified community shelters, enforces national food safety standards (FSSAI 2019), and converts non-edible plate waste into organic compost fertilizer.

---

## 🌐 Live Web Application

- **Live Streamlit App:** [https://pgovila-anna-setu-demo.streamlit.app](https://pgovila-anna-setu-demo.streamlit.app)

---

## 🌟 Key Functional Modules

### 1. 🍛 Donate Surplus Food
- **Retrieval-Augmented Generation (RAG) Safety Engine:** Real-time evaluation against FSSAI Surplus Food Regulations (2019) and Lucknow Nagar Nigam food safety limits.
- **Shelter Proximity Routing:** Automatically identifies and routes to verified local shelters within a strict 45-minute transit window.
- **Instant WhatsApp Broadcast:** Compiles ready-to-dispatch volunteer alerts with gate pickup directions and food quantities.
- **FSSAI Form B Audit Manifest:** Generates regulatory donation audit slips for mess administration.

### 2. 🔮 Plan How Much to Cook
- **Predictive Turnout Forecasting:** Predicts daily meal attendance based on day of week, weather conditions, and academic calendar.
- **Portion Optimization:** Recommends exact cooking targets to prevent overproduction food waste at the source.
- **Ingredient Bill of Materials:** Calculates precise purchasing quantities across grains, lentils, vegetables, oil, dairy, and spices.

### 3. ♻️ Plate-Waste Recycler
- **Interactive Student Kiosk:** Displays real-time environmental impact (embedded water and carbon footprint) for plate waste returned at trays.
- **Aerobic Bio-Recycling:** Simulates 24-hour on-site accelerated composting converting food scraps into garden fertilizer.

### 4. 💬 Ask a Food Safety Question
- **Semantic Rule Search:** Natural language Q&A backed by embedded vector search across FSSAI clauses and Lucknow municipal by-laws.

### 5. 📖 Food Safety Rules Reference
- Plain-language legal reference guide covering the 2-hour / 4-hour rule, temperature danger zones (5°C - 65°C), donor legal protections, and municipal compliance.

---

## 🚀 Quickstart & Local Setup

```bash
# Clone the repository
git clone https://github.com/pgovila/Anna-Setu-Project.git
cd Anna-Setu-Project

# Install dependencies
pip install -r requirements.txt

# Run the interactive Streamlit application
streamlit run streamlit_app.py
```

---

## 🏛️ Project Affiliation

Developed as part of the **1M1B (One Million for One Billion) Green Skills and Applied AI for Climate Action Virtual Internship** in partnership with **IBM SkillsBuild** and **AICTE**, by **Pankhuri Govila**.
