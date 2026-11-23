"""
Unified RAG Pipeline for Anna-Setu.
Coordinates lexical (TF-IDF) retrieval of FSSAI & Lucknow Nagar Nigam guidelines,
safety timeline verification, and template-based notification generation.
"""

import os
import json
from typing import Dict, Any, List, Optional
from .retriever import RegulatoryRetriever
from .compliance_engine import FoodComplianceEngine
from .granite_generator import TemplateAlertCompiler


class AnnaSetuRAGPipeline:
    """
    High-level orchestrator for the Anna-Setu Compliance & Redistribution RAG Pipeline.
    """

    # Maps UI filter values (which may differ from document source_type tags) to the
    # canonical source_type strings stored on each document by the retriever.
    _FILTER_SOURCE_MAP = {
        "FSSAI": "FSSAI",
        "LUCKNOW_NAGAR_NIGAM": "LNN",
        "LNN": "LNN",
    }

    def __init__(self, kb_dir: Optional[str] = None):
        self.retriever = RegulatoryRetriever(kb_dir=kb_dir)
        self.engine = FoodComplianceEngine(retriever=self.retriever)
        self.compiler = TemplateAlertCompiler()
        self.shelters = self._load_shelters(kb_dir)

    def _load_shelters(self, kb_dir: Optional[str]) -> List[Dict[str, Any]]:
        """Loads illustrative Lucknow shelter directory (sample data - confirm before use)."""
        if kb_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            kb_dir = os.path.join(base_dir, "knowledge_base")
        path = os.path.join(kb_dir, "shelters_lucknow.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_shelter_names(self) -> List[str]:
        """Returns list of formatted shelter names for UI dropdowns."""
        return [f"{s['name']} ({s['zone_name']})" for s in self.shelters]

    def get_shelter_by_name(self, formatted_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves shelter record by its display string."""
        for s in self.shelters:
            if s['name'] in formatted_name:
                return s
        return None

    def get_category_choices(self) -> List[tuple]:
        """Returns tuple of (key, display_label) for food categories."""
        return [
            ("cooked_grains_curry", "Cooked Grains, Rice, Dal & Gravies (High Moisture)"),
            ("dry_staples_roti", "Dry Cooked Staples (Rotis, Chapatis, Dry Sabzi)"),
            ("dairy_sweets", "Dairy, Paneer Curries, Milk Sweets & Kheer"),
            ("fried_snacks", "Dry Fried Snacks (Samosas, Cutlets, Pakoras)"),
            ("raw_salads_cut_fruits", "Raw Cut Salads, Sliced Fruits (High Risk)"),
            ("plate_waste", "Plate Waste / Post-Consumer Leftovers (Prohibited)")
        ]

    def match_optimal_shelter(
        self,
        origin_zone: int = 4,
        servings: int = 40,
        requires_cold_storage: bool = False
    ) -> Dict[str, Any]:
        """
        Heuristic shelter-matching based on zone proximity, transit time, capacity,
        and cold-chain availability (illustrative sample data - confirm before dispatch).
        Transit durations are read directly from the compliance engine's zone matrix so
        that the display value and the safety verdict always agree.
        """
        best_shelter = None
        best_score = -999.0
        best_transit = 35
        best_distance_km = 8.0

        for s in self.shelters:
            s_zone = s.get("zone_id", 1)
            capacity = s.get("capacity_servings", 100)
            has_cold = s.get("cold_storage_available", False)

            # Use the engine's transit matrix so display and verdict always agree.
            transit = self.engine._estimate_transit_minutes(origin_zone, s_zone)

            # Zone proximity score derived from transit time (lower = better proximity).
            if transit <= 20:
                zone_score = 50.0
                distance_km = 2.1
            elif transit <= 30:
                zone_score = 35.0
                distance_km = 4.5
            elif transit <= 40:
                zone_score = 20.0
                distance_km = 6.5
            else:
                zone_score = 10.0
                distance_km = 9.0

            # Capacity matching score
            cap_score = 20.0 if capacity >= servings else (capacity / max(1, servings)) * 10.0

            # Cold storage matching
            cold_score = 15.0 if (requires_cold_storage and has_cold) else (5.0 if not requires_cold_storage else -10.0)

            total_score = zone_score + cap_score + cold_score

            if total_score > best_score:
                best_score = total_score
                best_shelter = s
                best_transit = transit
                best_distance_km = distance_km

        if not best_shelter and self.shelters:
            best_shelter = self.shelters[0]
            best_transit = self.engine._estimate_transit_minutes(origin_zone, best_shelter.get("zone_id", 1))

        zone_label = best_shelter.get('zone_name', f"Zone {best_shelter.get('zone_id')}")

        # Capacity warning
        capacity = best_shelter.get("capacity_servings", 100)
        capacity_note = ""
        if servings > capacity:
            capacity_note = (
                f" ⚠️ Capacity {capacity} servings < {servings} requested - "
                "consider splitting between two shelters."
            )

        display_str = (
            f"{best_shelter['name']} ({zone_label} - "
            f"{best_distance_km:.1f} km away | Route Transit: {best_transit} mins | "
            f"Meal capacity: {capacity} servings){capacity_note}"
        )

        return {
            "shelter": best_shelter,
            "display_str": display_str,
            "estimated_transit_mins": best_transit,
            "distance_km": best_distance_km,
            "capacity_exceeded": servings > capacity
        }

    def sync_ai_pipeline_configurations(
        self,
        origin_zone: int = 4,
        item: str = "Vegetable pulao and dal",
        servings: int = 45,
        category_key: str = "cooked_grains_curry",
        time_prepared: str = "12:30",
        assessment_time: Optional[str] = None,
        storage_condition: str = "ambient",
        measured_temp_celsius: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Dynamically computes and populates the fields in 'Simulated AI Pipeline Configurations':
        1. Retrieved Safety Compliance Rule (RAG)
        2. AI Matched Shelter Destination
        """
        matched = self.match_optimal_shelter(
            origin_zone=origin_zone,
            servings=servings,
            requires_cold_storage=(storage_condition == "refrigerated")
        )

        # Quick evaluation of safety parameters
        eval_res = self.engine.evaluate(
            item=item,
            servings=servings,
            category_key=category_key,
            time_prepared=time_prepared,
            assessment_time=assessment_time,
            storage_condition=storage_condition,
            measured_temp_celsius=measured_temp_celsius,
            origin_zone=origin_zone,
            dest_zone=matched["shelter"].get("zone_id", 1),
            shelter_name=matched["shelter"].get("name", "Rain Basera")
        )

        timeline = eval_res["timeline"]
        top_rules = eval_res.get("retrieved_rules", [])
        rule_tag = f"[{top_rules[0].get('id', 'FSSAI-REG-4-2')}]" if top_rules else "[FSSAI-REG-4-2]"

        if eval_res["status"] == "NON_COMPLIANT_REJECTED":
            if "prohibited" in eval_res["reason"].lower():
                compliance_rule_str = f"{rule_tag} PROHIBITED ITEM: Raw salads/cut perishables strictly banned under FSSAI Surplus Food Reg 4(4). Divert to bio-compost (not landfill)."
            else:
                compliance_rule_str = f"{rule_tag} HOLDING LIMIT EXCEEDED: Elapsed ({timeline['elapsed_minutes']}m) + transit ({timeline['transit_minutes']}m) > limit ({timeline['max_allowed_minutes']}m). Divert to bio-compost."
        elif eval_res["status"] == "COMPLIANT_URGENT":
            compliance_rule_str = f"{rule_tag} URGENT DISPATCH: Within 4-hour limit ({timeline['elapsed_minutes']}m elapsed + {timeline['transit_minutes']}m transit). Must consume before {timeline['safe_pickup_by']} IST per FSSAI Surplus Food Reg 4(2)."
        else:
            if storage_condition == "hot_holding":
                compliance_rule_str = f"{rule_tag} Active Hot-Holding (>=65°C) verified per FSSAI Surplus Food Reg 4(3). Safe window active until {timeline['safe_pickup_by']} IST."
            elif storage_condition == "refrigerated":
                compliance_rule_str = f"{rule_tag} Active Cold-Chain (<=5°C) verified per FSSAI Surplus Food Reg 4(3). Safe window active until {timeline['safe_pickup_by']} IST (24h)."
            else:
                compliance_rule_str = f"{rule_tag} Within 4-hour ambient holding limit per FSSAI Surplus Food Reg 4(2). Safe redistribution active until {timeline['safe_pickup_by']} IST."

        return {
            "retrieved_safety_rule": compliance_rule_str,
            "ai_matched_shelter": matched["display_str"],
            "matched_shelter_obj": matched["shelter"]
        }

    def evaluate_surplus(
        self,
        item: str,
        servings: int,
        category_key: str,
        time_prepared: str,
        assessment_time: Optional[str] = None,
        storage_condition: str = "ambient",
        measured_temp_celsius: Optional[float] = None,
        origin_zone: int = 4,
        dest_zone: int = 1,
        shelter_display_name: str = "Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location: str = "Main Campus Mess, Gate 2",
        facility_place: Optional[str] = None,
        meal_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes full pipeline:
        1. Evaluates food safety & transit timelines against FSSAI/LNN rules.
        2. Retrieves relevant statutory clauses via RAG.
        3. Compiles IBM Granite shelter notification & formal audit manifest.
        """
        # Resolve shelter metadata or auto match
        if not shelter_display_name or shelter_display_name == "AUTO_MATCH" or "Auto-Match" in shelter_display_name:
            matched_obj = self.match_optimal_shelter(
                origin_zone=origin_zone,
                servings=servings,
                requires_cold_storage=(storage_condition == "refrigerated")
            )
            shelter_obj = matched_obj["shelter"]
            dest_zone = shelter_obj.get("zone_id", 1)
            shelter_clean_name = shelter_obj.get("name", "Rain Basera")
            shelter_display_name = matched_obj["display_str"]
        else:
            shelter_obj = self.get_shelter_by_name(shelter_display_name)
            if shelter_obj:
                dest_zone = shelter_obj.get("zone_id", dest_zone)
                shelter_clean_name = shelter_obj.get("name", shelter_display_name)
            else:
                shelter_clean_name = shelter_display_name

        # Run compliance check + RAG retrieval
        eval_result = self.engine.evaluate(
            item=item,
            servings=servings,
            category_key=category_key,
            time_prepared=time_prepared,
            assessment_time=assessment_time,
            storage_condition=storage_condition,
            measured_temp_celsius=measured_temp_celsius,
            origin_zone=origin_zone,
            dest_zone=dest_zone,
            shelter_name=shelter_clean_name
        )

        # Generate outputs via template-based alert compiler
        alert_msg = self.compiler.compile_shelter_alert(
            eval_result,
            pickup_location=pickup_location,
            facility_place=facility_place,
            meal_type=meal_type
        )
        audit_manifest = self.compiler.compile_fssai_audit_manifest(
            eval_result,
            pickup_location=pickup_location,
            facility_place=facility_place,
            meal_type=meal_type
        )

        # Sync AI configurations for direct display
        sync_data = self.sync_ai_pipeline_configurations(
            origin_zone=origin_zone,
            item=item,
            servings=servings,
            category_key=category_key,
            time_prepared=time_prepared,
            assessment_time=assessment_time,
            storage_condition=storage_condition,
            measured_temp_celsius=measured_temp_celsius
        )

        return {
            "evaluation": eval_result,
            "broadcast_message": alert_msg,
            "audit_manifest": audit_manifest,
            "shelter_details": shelter_obj,
            "retrieved_safety_rule": sync_data["retrieved_safety_rule"],
            "ai_matched_shelter": sync_data["ai_matched_shelter"]
        }

    def query_regulations(self, query: str, top_k: int = 4, filter_source: Optional[str] = None) -> List[Dict[str, Any]]:
        """Direct lexical (TF-IDF) search against FSSAI & LNN regulatory corpora."""
        # Normalise UI filter values to the canonical source_type tag in documents.
        if filter_source:
            filter_source = self._FILTER_SOURCE_MAP.get(filter_source, filter_source)
        return self.retriever.retrieve(query, top_k=top_k, filter_source=filter_source)

    def ask_regulations(self, query: str, top_k: int = 4, filter_source: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes end-to-end lexical RAG Q&A:
        1. Retrieves relevant FSSAI 2019 and Lucknow Nagar Nigam statutory clauses via TF-IDF.
        2. Assembles an authoritative compliance answer citing legal clauses, temperature thresholds, and directives.
        """
        # Normalise UI filter values (e.g. "LUCKNOW_NAGAR_NIGAM") to doc source_type ("LNN").
        if filter_source:
            filter_source = self._FILTER_SOURCE_MAP.get(filter_source, filter_source)
        retrieved_rules = self.retriever.retrieve(query, top_k=top_k, filter_source=filter_source)
        res = self.compiler.compile_rag_qa_answer(query, retrieved_rules)
        res["synthesized_answer"] = res["answer_markdown"]
        res["retrieved_clauses"] = retrieved_rules
        return res

    def predict_meal_demand(
        self,
        enrolled_students: int = 1000,
        meal_type: str = "lunch",
        day_of_week: str = "Wednesday",
        academic_period: str = "Regular Academic Term",
        weather_condition: str = "Sunny / Normal (32C)",
        academic_calendar: Optional[str] = None,
        weather: Optional[str] = None,
        base_turnout_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Attendance Multiplier Demand Estimator (Module 1 - Smart Campus Dining Advisor).
        Applies fixed day-of-week, weather, and academic-calendar multipliers to estimate
        dining turnout. This is a multiplier model, not a regression-trained time-series model.
        Outputs are illustrative and should be calibrated against real swipe-card data.
        """
        if academic_calendar:
            academic_period = academic_calendar
        if weather:
            weather_condition = weather

        # Per-meal baseline attendance rates (illustrative defaults from typical campus data).
        # When the user supplies base_turnout_rate from the slider, we keep the slider value
        # as the LUNCH baseline and scale other meals proportionally, so the meal selector
        # actually changes the output.
        MEAL_BASE_DEFAULTS = {
            "breakfast": 0.70,
            "lunch": 0.88,
            "snacks": 0.55,
            "dinner": 0.82
        }
        LUNCH_DEFAULT = MEAL_BASE_DEFAULTS["lunch"]
        meal_key = meal_type.lower()
        per_meal_default = MEAL_BASE_DEFAULTS.get(meal_key, 0.85)

        if base_turnout_rate is not None:
            # Scale the slider value by the per-meal ratio so Breakfast/Dinner differ from Lunch.
            meal_base = base_turnout_rate * (per_meal_default / LUNCH_DEFAULT)
        else:
            meal_base = per_meal_default

        dow_factor = {
            "monday": 0.98,
            "tuesday": 0.99,
            "wednesday": 1.00,
            "thursday": 0.98,
            "friday": 0.90,
            "saturday": 0.68,
            "sunday": 0.60
        }.get(day_of_week.lower(), 0.95)

        academic_factor = 1.0
        # Check more specific strings first so "post-exam" does not accidentally match "exam".
        _ap = academic_period.lower()
        if "post-exam" in _ap or "post exam" in _ap or "festival eve" in _ap or "fest" in _ap or "cultural" in _ap:
            academic_factor = 0.86
        elif "exam" in _ap:
            academic_factor = 1.14
        elif "fest" in _ap or "cultural" in _ap:
            academic_factor = 0.86
        elif "holiday" in _ap or "long weekend" in _ap:
            academic_factor = 0.62
        elif "vacation" in _ap or "break" in _ap:
            academic_factor = 0.22

        weather_factor = 1.0
        if "rain" in weather_condition.lower() or "monsoon" in weather_condition.lower():
            weather_factor = 1.08
        elif "extreme heat" in weather_condition.lower() or "summer" in weather_condition.lower():
            weather_factor = 0.96

        final_rate = min(1.0, max(0.15, meal_base * dow_factor * academic_factor * weather_factor))
        predicted_turnout = int(round(enrolled_students * final_rate))

        # NOTE: unforecasted_prep uses a fixed 105% baseline for the engine's internal
        # portions_saved / cost_savings_inr fields. The Streamlit UI overrides this with
        # the user's buffer slider (see Tab 2) - use _prevented and multiply by 42.5 there.
        unforecasted_prep = int(round(enrolled_students * 1.05)) if final_rate > 0.7 else int(round(enrolled_students * 0.90))
        recommended_prep = int(round(predicted_turnout * 1.05))

        portions_saved = max(0, unforecasted_prep - recommended_prep)
        procurement_saved_inr = portions_saved * 42.50

        # Ingredient breakdown (illustrative ratios - calibrate against actual mess recipe cards).
        # Raw weights per diner: rice/grains 140 g, dal/lentils 60 g, vegetables 150 g,
        # cooking oil 25 g, dairy/paneer 50 g, spices 12 g.
        ingredient_breakdown = {
            "rice_or_grains_kg": round(predicted_turnout * 0.14, 1),
            "dal_or_lentils_kg": round(predicted_turnout * 0.06, 1),   # typical raw dal ~60 g/diner
            "vegetables_kg": round(predicted_turnout * 0.15, 1),
            "cooking_oil_kg": round(predicted_turnout * 0.025, 1),
            "dairy_or_paneer_kg": round(predicted_turnout * 0.05, 1),  # typical dairy ~50 g/diner
            "spices_kg": round(predicted_turnout * 0.012, 1)
        }

        rec_summary = (
            f"Morning Kitchen Directive: Prepare {recommended_prep} portions for {meal_type.title()} "
            f"({predicted_turnout} expected diners + 5% safety buffer). "
            f"Engine estimate: saves ~{portions_saved} surplus meals vs. 105% baseline "
            f"(₹{procurement_saved_inr:,.2f}). Actual savings depend on your kitchen's buffer - "
            f"adjust the buffer slider on-screen."
        )

        return {
            "enrolled_students": enrolled_students,
            "meal_type": meal_type.title(),
            "day_of_week": day_of_week.title(),
            "academic_period": academic_period,
            "weather_condition": weather_condition,
            "predicted_turnout": predicted_turnout,
            "predicted_turnout_students": predicted_turnout,
            "turnout_pct": round(final_rate * 100, 1),
            "turnout_rate_pct": round(final_rate * 100, 1),
            # NOTE: "indicative ±4%" range - there is no statistical 95% confidence interval
            # behind this figure. Rename if publishing to avoid implying a fitted distribution.
            "indicative_range_4pct": (int(predicted_turnout * 0.96), int(predicted_turnout * 1.04)),
            "confidence_interval_95": (int(predicted_turnout * 0.96), int(predicted_turnout * 1.04)),  # kept for back-compat
            "unforecasted_prep": unforecasted_prep,
            "traditional_unoptimized_target": unforecasted_prep,
            "recommended_prep": recommended_prep,
            "recommended_cooking_target": recommended_prep,
            "portions_saved": portions_saved,
            "portions_prevented_from_waste": portions_saved,
            "procurement_saved_inr": procurement_saved_inr,
            "cost_savings_inr": procurement_saved_inr,
            "overproduction_buffer_cut_pct": 80.0,
            "ingredient_breakdown_kg": ingredient_breakdown,
            "recommendation_summary": rec_summary,
            "ingredients_kg": {
                "rice_grains_kg": ingredient_breakdown["rice_or_grains_kg"],
                "pulses_dal_kg": ingredient_breakdown["dal_or_lentils_kg"],
                "vegetables_kg": ingredient_breakdown["vegetables_kg"],
                "roti_pieces": int(predicted_turnout * 2.5),
                "cooking_oil_liters": ingredient_breakdown["cooking_oil_kg"]
            }
        }

