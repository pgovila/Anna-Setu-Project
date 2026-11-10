"""
Hardware Telemetry Simulation Script for Anna-Setu Track B.
Simulates real-world events from the Smart Plate-Waste & Bio-Recycling Kiosk:
1. Fresh kitchen surplus batch (Hot-holding >= 65C) -> Evaluates COMPLIANT_SAFE
2. Delayed kitchen surplus batch (Danger zone 42C, 3.5h elapsed) -> Evaluates COMPLIANT_URGENT
3. Expired kitchen surplus batch (Danger zone 32C, 5h elapsed) -> Evaluates NON_COMPLIANT_REJECTED (Actuates Green Bio-Compost Divert)
4. Plate-waste clearing session: Computes student plate waste, embedded water footprint, and bio-fertilizer yield!
"""

import time
from datetime import datetime, timedelta
from rag.pipeline import AnnaSetuRAGPipeline

def run_simulation():
    pipeline = AnnaSetuRAGPipeline()
    print("=" * 80)
    print("   ANNA-SETU TRACK B: SMART KIOSK & TELEMETRY SIMULATION ENGINE")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
    print("Connecting to Virtual Kiosk: ANNA-SETU-KIOSK-01\n")

    # -------------------------------------------------------------------------
    # SCENARIO 1: Fresh Kitchen Surplus Batch (Hot Holding >= 65C)
    # -------------------------------------------------------------------------
    print(">>> [HARDWARE EVENT 1]: Kitchen Supervisor places hot vessel on load deck")
    weight_kg_1 = 17.5
    temp_c_1 = 68.4  # Above 65C threshold
    prep_time_1 = (datetime.now() - timedelta(minutes=45)).strftime("%H:%M")
    now_time_1 = datetime.now().strftime("%H:%M")

    print(f"    * Load Cell Telemetry: {weight_kg_1} kg (~{int(weight_kg_1 / 0.35)} portions)")
    print(f"    * MLX90614 Contactless IR Temp: {temp_c_1}°C [HOT HOLDING ACTIVE >= 65°C]")
    print(f"    * Time Prepared: {prep_time_1} IST | Evaluation Time: {now_time_1} IST")

    res1 = pipeline.evaluate_surplus(
        item="Mixed Vegetable Pulao & Dal Tadka",
        servings=int(weight_kg_1 / 0.35),
        category_key="cooked_grains_curry",
        time_prepared=prep_time_1,
        assessment_time=now_time_1,
        storage_condition="hot_holding",
        origin_zone=4,
        shelter_display_name="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location="Central Campus Mess, Gate 2"
    )

    eval1 = res1["evaluation"]
    print(f"\n    [RAG COMPLIANCE VERDICT]: {eval1['badge']}")
    print(f"    * Safe Pickup By: {eval1['timeline']['safe_pickup_by']} IST")
    print(f"    * Transit Buffer: {eval1['timeline']['transit_minutes']} mins")
    print(f"    * Hardware Actuator Signal: GREEN LED ON | AUDIO CHIME | DISPATCH UNLOCKED")
    print("    * AI-Drafted Broadcast Preview:")
    print("      " + res1["broadcast_message"].replace("\n", "\n      "))

    # -------------------------------------------------------------------------
    # SCENARIO 2: Delayed Batch Approaching Safety Ceiling (In Danger Zone)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print(">>> [HARDWARE EVENT 2]: Afternoon survey detects vessel held ambiently")
    weight_kg_2 = 12.0
    temp_c_2 = 38.5  # In danger zone (5C - 65C)
    prep_time_2 = (datetime.now() - timedelta(minutes=165)).strftime("%H:%M") # 2h 45m elapsed
    now_time_2 = datetime.now().strftime("%H:%M")

    print(f"    * Load Cell Telemetry: {weight_kg_2} kg (~{int(weight_kg_2 / 0.35)} portions)")
    print(f"    * MLX90614 Contactless IR Temp: {temp_c_2}°C [IN DANGER ZONE 5°C - 65°C]")
    print(f"    * Elapsed Time: 165 mins")

    res2 = pipeline.evaluate_surplus(
        item="Paneer Butter Masala & Rotis",
        servings=int(weight_kg_2 / 0.35),
        category_key="dairy_sweets",
        time_prepared=prep_time_2,
        assessment_time=now_time_2,
        storage_condition="ambient",
        origin_zone=4,
        shelter_display_name="Rain Basera Gomti Nagar (Zone 4 (Gomti Nagar))",
        pickup_location="North Dining Hall, Loading Bay"
    )

    eval2 = res2["evaluation"]
    print(f"\n    [RAG COMPLIANCE VERDICT]: {eval2['badge']}")
    print(f"    * Reason: {eval2['reason']}")
    print(f"    * Hardware Actuator Signal: AMBER LED ON | URGENT DISPATCH MANDATE")

    # -------------------------------------------------------------------------
    # SCENARIO 3: Expired Batch (> 4 Hours) -> Triggers Bio-Compost Diversion
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print(">>> [HARDWARE EVENT 3]: Evening batch exceeding FSSAI 4-hour ambient ceiling")
    weight_kg_3 = 22.0
    temp_c_3 = 28.0
    prep_time_3 = (datetime.now() - timedelta(minutes=280)).strftime("%H:%M") # 4h 40m elapsed
    now_time_3 = datetime.now().strftime("%H:%M")

    print(f"    * Load Cell Telemetry: {weight_kg_3} kg (~{int(weight_kg_3 / 0.35)} portions)")
    print(f"    * Elapsed Time: 280 mins (Exceeds 240 mins FSSAI ceiling)")

    res3 = pipeline.evaluate_surplus(
        item="Puri and Chole Curry",
        servings=int(weight_kg_3 / 0.35),
        category_key="cooked_grains_curry",
        time_prepared=prep_time_3,
        assessment_time=now_time_3,
        storage_condition="ambient",
        origin_zone=4,
        shelter_display_name="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location="Central Campus Mess, Gate 2"
    )

    eval3 = res3["evaluation"]
    print(f"\n    [RAG COMPLIANCE VERDICT]: {eval3['badge']}")
    print(f"    * Reason: {eval3['reason']}")
    print(f"    * LNN Municipal Action: {eval3['lnn_action']}")
    print(f"    * Hardware Actuator Signal: RED LED ON | WARN BUZZER | SOLENOID GREEN BIN UNLOCKED")
    print(f"    * Human Consumption BLOCKED. Diverted directly into Track B Bio-Composter!")

    # -------------------------------------------------------------------------
    # SCENARIO 4: Student Tray Return Plate-Waste Interception & Upcycling
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print(">>> [HARDWARE EVENT 4]: Student returns lunch tray at clearing counter")
    plate_waste_grams = 185.0
    embedded_water_liters = plate_waste_grams * 0.76  # ~760L water per kg of grain/lentil meal
    carbon_footprint_grams = plate_waste_grams * 2.3  # ~2.3kg CO2e per kg cooked meal

    print(f"    * Plate Scale (HX711): {plate_waste_grams}g leftover scraped from plate")
    print("    * Dynamic Behavioral Nudge Screen Output:")
    print("      +-------------------------------------------------------------+")
    print(f"      | ⚠️ ATTENTION DINER: You left {plate_waste_grams:.0f}g of food uneaten!       |")
    print(f"      | 💧 Embedded Water Wasted: ~{embedded_water_liters:.1f} Liters                 |")
    print(f"      | 🌍 Carbon Equivalent: {carbon_footprint_grams:.0f}g CO2e                        |")
    print("      | 🏆 HOSTEL LEADERBOARD: Block B in 1st Place (94% Clean Plates)|")
    print("      | 💡 Action: Take only what you finish next time!             |")
    print("      +-------------------------------------------------------------+")

    # Upcycling Calculation
    daily_mess_diners = 800
    avg_waste_per_diner_kg = 0.085  # 85 grams avg
    total_daily_plate_waste_kg = daily_mess_diners * avg_waste_per_diner_kg  # 68 kg
    compost_yield_kg = total_daily_plate_waste_kg * 0.15  # 85% volume/moisture reduction -> 15% dry bio-fertilizer

    print(f"\n    * Track B Bio-Recycling Yield Projection:")
    print(f"      - Cumulative Daily Campus Plate Waste: {total_daily_plate_waste_kg:.1f} kg")
    print(f"      - Accelerated Composting Chamber (55°C - 65°C Aerobic Breakdown)")
    print(f"      - High-Grade Organic Bio-Fertilizer Harvested: {compost_yield_kg:.1f} kg / day")
    print(f"      - Landfill Methane Avoided: ~{total_daily_plate_waste_kg * 1.9:.1f} kg CO2e / day")
    print(f"      - Burden on Lucknow Nagar Nigam Municipal Sanitation: 0.0 kg (100% on-site valorization)")

    print("\n" + "=" * 80)
    print("   END-TO-END TELEMETRY SIMULATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_simulation()

