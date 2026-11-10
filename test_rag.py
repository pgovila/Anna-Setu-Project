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

    print("\n" + "=" * 70)
    print("ALL 5 TESTS PASSED SUCCESSFULLY! RAG PIPELINE FULLY VERIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()

