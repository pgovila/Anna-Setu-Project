"""
Comprehensive Test Script for Anna-Setu RAG Compliance Pipeline.
Tests multiple realistic scenarios for FSSAI 2019 and Lucknow Nagar Nigam rules.
"""

import sys
from rag.pipeline import AnnaSetuRAGPipeline


def run_tests():
    pipeline = AnnaSetuRAGPipeline()
    print("=" * 70)
    print("TESTING ANNA-SETU RAG PIPELINE (FSSAI + LUCKNOW NAGAR NIGAM)")
    print("=" * 70)

    # Test 1: Compliant Safe Batch
    print("\n--- TEST 1: Fresh Cooked Rice & Dal (1h 30m elapsed, Ambient) ---")
    res1 = pipeline.evaluate_surplus(
        item="Vegetable Pulao and Dal Tadka",
        servings=50,
        category_key="cooked_grains_curry",
        time_prepared="12:30",
        assessment_time="14:00",
        storage_condition="ambient",
        origin_zone=4,  # Gomti Nagar
        shelter_display_name="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location="Main Campus Mess, Gate 2"
    )
    eval1 = res1["evaluation"]
    print("Status:", eval1["badge"])
    print("Safe Pickup By:", eval1["timeline"]["safe_pickup_by"])
    print("Transit Est:", eval1["timeline"]["transit_minutes"], "mins")
    print("Retrieved Rules Count:", len(eval1["retrieved_rules"]))
    for r in eval1["retrieved_rules"]:
        print(f"  * [{r['id']}] {r['title']} (Score: {r['relevance_score']})")
    print("\n[AI Broadcast Message]:")
    print(res1["broadcast_message"])

    assert eval1["status"] == "COMPLIANT_SAFE", f"Expected COMPLIANT_SAFE, got {eval1['status']}"

    # Test 2: Compliant Urgent Batch (Approaching 4h threshold)
    print("\n--- TEST 2: Approaching Threshold Cooked Meal (2h 45m elapsed, Ambient) ---")
    res2 = pipeline.evaluate_surplus(
        item="Mixed Vegetable Korma & Rice",
        servings=35,
        category_key="cooked_grains_curry",
        time_prepared="11:30",
        assessment_time="14:15",
        storage_condition="ambient",
        origin_zone=4,
        shelter_display_name="Rain Basera Gomti Nagar (Zone 4 (Gomti Nagar))",
        pickup_location="North Hostel Kitchen, Gate 1"
    )
    eval2 = res2["evaluation"]
    print("Status:", eval2["badge"])
    print("Reason:", eval2["reason"])
    print("Compliance Note:", eval2["compliance_note"])
    assert eval2["status"] == "COMPLIANT_URGENT", f"Expected COMPLIANT_URGENT, got {eval2['status']}"

    # Test 3: Holding Time Exceeded (> 4 Hours)
    print("\n--- TEST 3: Expired Meal (4h 30m elapsed, Ambient) ---")
    res3 = pipeline.evaluate_surplus(
        item="Puri and Chole",
        servings=40,
        category_key="cooked_grains_curry",
        time_prepared="09:00",
        assessment_time="13:30",
        storage_condition="ambient",
        origin_zone=4,
        shelter_display_name="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location="Central Dining Hall"
    )
    eval3 = res3["evaluation"]
    print("Status:", eval3["badge"])
    print("Reason:", eval3["reason"])
    print("LNN Directive:", eval3["lnn_action"])
    print("\n[AI Cancellation Notice]:")
    print(res3["broadcast_message"])
    assert eval3["status"] == "NON_COMPLIANT_REJECTED", f"Expected NON_COMPLIANT_REJECTED, got {eval3['status']}"

    # Test 4: Prohibited Item (Raw Salads / Cut Fruits)
    print("\n--- TEST 4: Prohibited Item (Raw Cut Cucumber & Onion Salad) ---")
    res4 = pipeline.evaluate_surplus(
        item="Sliced Cucumber & Onion Salad",
        servings=25,
        category_key="raw_salads_cut_fruits",
        time_prepared="12:00",
        assessment_time="13:00",
        storage_condition="ambient",
        origin_zone=4,
        shelter_display_name="Asha Jyoti Kendra (Women & Child Shelter) (Zone 4 (Gomti Nagar Extension))",
        pickup_location="Salad Counter"
    )
    eval4 = res4["evaluation"]
    print("Status:", eval4["badge"])
    print("Reason:", eval4["reason"])
    assert eval4["status"] == "NON_COMPLIANT_REJECTED"

    # Test 5: Semantic Regulatory Query (RAG search)
    print("\n--- TEST 5: Direct Semantic Regulatory Query ---")
    query = "What is the penalty for dumping food waste into municipal dustbins in Lucknow?"
    matches = pipeline.query_regulations(query, top_k=2)
    print(f"Query: '{query}'")
    for m in matches:
        print(f"  * [{m['id']}] {m['clause']} | Score: {m['relevance_score']}")
        print(f"    Excerpt: {m['text'][:120]}...")
    assert len(matches) > 0

    # Test 6: Physical Temperature Danger Zone Breach
    print("\n--- TEST 6: Physical Temperature Danger Zone Breach (Hot-Holding dropped to 52°C) ---")
    res6 = pipeline.evaluate_surplus(
        item="Dal Makhani and Jeera Rice",
        servings=60,
        category_key="cooked_grains_curry",
        time_prepared="12:00",
        assessment_time="13:30",
        storage_condition="hot_holding",
        measured_temp_celsius=52.0, # Breaches >= 65C threshold!
        origin_zone=4,
        shelter_display_name="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))"
    )
    eval6 = res6["evaluation"]
    print("Status:", eval6["badge"])
    print("Temp Summary:", eval6["timeline"]["temp_status_summary"])
    assert "DANGER ZONE BREACH" in eval6["timeline"]["temp_status_summary"]

    # Test 7: Generative RAG Q&A Synthesis
    print("\n--- TEST 7: Generative RAG Q&A Synthesis (IBM Granite Compiler) ---")
    qa_res = pipeline.ask_regulations("Can I donate cooked paneer curry after 3 hours at room temperature?")
    print("Authority:", qa_res["authority"])
    print("Confidence:", qa_res["confidence_score"])
    print("Citations Count:", len(qa_res["citations"]))
    print("\n[Synthesized RAG Answer Excerpt]:")
    print(qa_res["answer_markdown"][:300] + "...")
    assert qa_res["confidence_score"] > 0.1
    assert len(qa_res["citations"]) > 0

    # Test 8: Predictive Meal Demand Forecasting (Module 1)
    print("\n--- TEST 8: Predictive Meal Demand Forecasting (Module 1) ---")
    demand = pipeline.predict_meal_demand(
        enrolled_students=1200,
        meal_type="lunch",
        day_of_week="Wednesday",
        academic_period="Regular Academic Term",
        weather_condition="Sunny / Normal (32C)"
    )
    print("Enrolled Students:", demand["enrolled_students"])
    print("Predicted Turnout:", demand["predicted_turnout"], f"({demand['turnout_pct']}%)")
    print("Recommended Cooking Target:", demand["recommended_prep"], "meals")
    print("Portions Prevented from Waste:", demand["portions_saved"], "meals")
    print(f"Cost Savings: ₹{demand['procurement_saved_inr']:,.2f}")
    assert demand["predicted_turnout"] > 800
    assert demand["portions_saved"] > 100

    # Test 9: Place & Meal-based AI Pipeline Configuration Sync
    print("\n--- TEST 9: Place & Meal-based AI Pipeline Configuration Sync ---")
    sync_res = pipeline.sync_ai_pipeline_configurations(
        origin_zone=4,
        item="Vegetable Poha & Boiled Eggs",
        servings=35,
        category_key="cooked_grains_curry",
        time_prepared="08:00",
        assessment_time="09:30",
        storage_condition="ambient"
    )
    print("Retrieved Safety Rule:", sync_res["retrieved_safety_rule"])
    print("AI Matched Shelter:", sync_res["ai_matched_shelter"])
    assert "FSSAI" in sync_res["retrieved_safety_rule"]
    assert "Zone 4" in sync_res["ai_matched_shelter"]

    print("\n" + "=" * 70)
    print("ALL 9 TESTS PASSED SUCCESSFULLY! RAG PIPELINE & PREDICTIVE SUITE FULLY VERIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()

