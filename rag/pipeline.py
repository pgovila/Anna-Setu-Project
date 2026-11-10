"""
Unified RAG Pipeline for Anna-Setu.
Coordinates semantic retrieval of FSSAI & Lucknow Nagar Nigam guidelines,
safety timeline verification, and IBM Granite notification generation.
"""

import os
import json
from typing import Dict, Any, List, Optional
from .retriever import RegulatoryRetriever
from .compliance_engine import FoodComplianceEngine
from .granite_generator import GraniteAlertCompiler


class AnnaSetuRAGPipeline:
    """
    High-level orchestrator for the Anna-Setu Compliance & Redistribution RAG Pipeline.
    """

    def __init__(self, kb_dir: Optional[str] = None):
        self.retriever = RegulatoryRetriever(kb_dir=kb_dir)
        self.engine = FoodComplianceEngine(retriever=self.retriever)
        self.compiler = GraniteAlertCompiler()
        self.shelters = self._load_shelters(kb_dir)

    def _load_shelters(self, kb_dir: Optional[str]) -> List[Dict[str, Any]]:
        """Loads verified Lucknow shelter directory."""
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

    def evaluate_surplus(
        self,
        item: str,
        servings: int,
        category_key: str,
        time_prepared: str,
        assessment_time: Optional[str] = None,
        storage_condition: str = "ambient",
        origin_zone: int = 4,
        dest_zone: int = 1,
        shelter_display_name: str = "Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        pickup_location: str = "Main Campus Mess, Gate 2"
    ) -> Dict[str, Any]:
        """
        Executes full pipeline:
        1. Evaluates food safety & transit timelines against FSSAI/LNN rules.
        2. Retrieves relevant statutory clauses via RAG.
        3. Compiles IBM Granite shelter notification & formal audit manifest.
        """
        # Resolve shelter metadata
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
            origin_zone=origin_zone,
            dest_zone=dest_zone,
            shelter_name=shelter_clean_name
        )

        # Generate outputs via IBM Granite prompt templates
        alert_msg = self.compiler.compile_shelter_alert(eval_result, pickup_location)
        audit_manifest = self.compiler.compile_fssai_audit_manifest(eval_result, pickup_location)

        return {
            "evaluation": eval_result,
            "broadcast_message": alert_msg,
            "audit_manifest": audit_manifest,
            "shelter_details": shelter_obj
        }

    def query_regulations(self, query: str, top_k: int = 4, filter_source: Optional[str] = None) -> List[Dict[str, Any]]:
        """Direct semantic search against FSSAI & LNN regulatory corpora."""
        return self.retriever.retrieve(query, top_k=top_k, filter_source=filter_source)

