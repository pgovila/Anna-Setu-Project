"""
Deterministic & Semantic Compliance Engine for Anna-Setu.
Evaluates surplus food donations against FSSAI 2019 Timelines,
Temperature Danger Zones, and Lucknow Nagar Nigam Municipal By-Laws.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .retriever import RegulatoryRetriever


class FoodComplianceEngine:
    """
    Evaluates whether surplus food qualifies for safe redistribution
    under FSSAI Surplus Food Regulations and Lucknow Nagar Nigam bylaws.
    """

    # Category risk metadata and baseline maximum ambient shelf-life (in minutes)
    CATEGORY_PROFILES = {
        "cooked_grains_curry": {
            "name": "Cooked Grains, Rice, Dal & Gravies",
            "ambient_max_minutes": 240,       # 4 hours hard ceiling
            "ambient_safe_dispatch": 150,     # 2.5 hours optimal handoff
            "reheat_required": True,
            "danger_organism": "Bacillus cereus, Clostridium perfringens",
            "prohibited": False
        },
        "dry_staples_roti": {
            "name": "Dry Cooked Staples (Rotis, Chapatis, Dry Sabzi)",
            "ambient_max_minutes": 300,       # 5 hours
            "ambient_safe_dispatch": 210,     # 3.5 hours
            "reheat_required": False,
            "danger_organism": "Molds, airborne contaminants",
            "prohibited": False
        },
        "dairy_sweets": {
            "name": "Dairy, Paneer Curries, Milk Sweets & Kheer",
            "ambient_max_minutes": 180,       # 3 hours strict
            "ambient_safe_dispatch": 90,      # 1.5 hours
            "reheat_required": True,
            "danger_organism": "Staphylococcus aureus, Listeria monocytogenes",
            "prohibited": False
        },
        "fried_snacks": {
            "name": "Dry Fried Snacks (Samosas, Cutlets, Pakoras)",
            "ambient_max_minutes": 300,       # 5 hours
            "ambient_safe_dispatch": 210,
            "reheat_required": False,
            "danger_organism": "Aerobic mesophiles",
            "prohibited": False
        },
        "raw_salads_cut_fruits": {
            "name": "Raw Cut Salads, Sliced Fruits & Chutneys",
            "ambient_max_minutes": 120,       # 2 hours max
            "ambient_safe_dispatch": 60,
            "reheat_required": False,
            "danger_organism": "Salmonella, E. coli (Cannot be reheated)",
            "prohibited": True                # FSSAI bans surplus unsealed raw salads
        },
        "plate_waste": {
            "name": "Plate Waste / Post-Consumer Leftovers",
            "ambient_max_minutes": 0,
            "ambient_safe_dispatch": 0,
            "reheat_required": False,
            "danger_organism": "Cross-contamination, bodily fluids",
            "prohibited": True                # FSSAI strict exclusion
        }
    }

    # Transit duration matrix between Lucknow Municipal Zones (minutes)
    LUCKNOW_ZONE_TRANSIT = {
        (1, 1): 20, (1, 2): 25, (1, 3): 25, (1, 4): 35, (1, 5): 30, (1, 6): 40, (1, 7): 40, (1, 8): 45,
        (4, 1): 35, (4, 2): 40, (4, 3): 25, (4, 4): 20, (4, 5): 40, (4, 6): 50, (4, 7): 25, (4, 8): 45,
        (5, 1): 30, (5, 2): 25, (5, 3): 40, (5, 4): 40, (5, 5): 20, (5, 6): 40, (5, 7): 50, (5, 8): 30,
        (7, 1): 40, (7, 2): 45, (7, 3): 35, (7, 4): 25, (7, 5): 50, (7, 6): 60, (7, 7): 20, (7, 8): 55
    }

    def __init__(self, retriever: Optional[RegulatoryRetriever] = None):
        self.retriever = retriever or RegulatoryRetriever()

    def _parse_time(self, time_str: str) -> datetime:
        """Parses HH:MM string into today's datetime object."""
        time_str = time_str.strip()
        now = datetime.now()
        for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p"):
            try:
                parsed = datetime.strptime(time_str, fmt)
                return now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse time string: '{time_str}'. Please use HH:MM format (24-hour).")

    def _estimate_transit_minutes(self, origin_zone: int, dest_zone: int) -> int:
        """Estimates transit duration across Lucknow Nagar Nigam corridors."""
        if (origin_zone, dest_zone) in self.LUCKNOW_ZONE_TRANSIT:
            return self.LUCKNOW_ZONE_TRANSIT[(origin_zone, dest_zone)]
        elif (dest_zone, origin_zone) in self.LUCKNOW_ZONE_TRANSIT:
            return self.LUCKNOW_ZONE_TRANSIT[(dest_zone, origin_zone)]
        elif origin_zone == dest_zone:
            return 25
        else:
            return 35

    def evaluate(
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
        shelter_name: str = "Rain Basera Charbagh"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end regulatory compliance assessment.
        
        Args:
            item: Name of surplus food item (e.g. "Vegetable pulao and dal")
            servings: Quantity in portions
            category_key: One of CATEGORY_PROFILES keys
            time_prepared: HH:MM time when cooking completed
            assessment_time: HH:MM time of current evaluation (defaults to now)
            storage_condition: 'ambient', 'hot_holding' (>=65C), or 'refrigerated' (<=5C)
            measured_temp_celsius: Optional physical thermal sensor reading (e.g. from Track B MLX90614)
            origin_zone: Lucknow zone ID of campus mess (1-8)
            dest_zone: Lucknow zone ID of receiving shelter (1-8)
            shelter_name: Destination shelter name
        
        Returns:
            Dictionary with compliance verdict, timeline metrics, and retrieved rules
        """
        profile = self.CATEGORY_PROFILES.get(category_key, self.CATEGORY_PROFILES["cooked_grains_curry"])
        
        dt_prepared = self._parse_time(time_prepared)
        if assessment_time:
            dt_assess = self._parse_time(assessment_time)
        else:
            dt_assess = datetime.now()

        # If assessment time appears earlier than prepared time, assume same-day continuity
        if dt_assess < dt_prepared:
            elapsed_minutes = int((dt_assess + timedelta(days=1) - dt_prepared).total_seconds() / 60)
        else:
            elapsed_minutes = int((dt_assess - dt_prepared).total_seconds() / 60)

        transit_minutes = self._estimate_transit_minutes(origin_zone, dest_zone)
        total_projected_exposure = elapsed_minutes + transit_minutes

        # Temperature Sensor Verification & Danger Zone Assessment (FSSAI Reg 4(3))
        temp_alert = None
        temp_status_summary = "NOT MEASURED"
        effective_storage = storage_condition

        if measured_temp_celsius is not None:
            if storage_condition == "hot_holding":
                if measured_temp_celsius < 65.0:
                    temp_alert = (
                        f"⚠️ TEMPERATURE ABUSE: Stated hot-holding temperature is {measured_temp_celsius:.1f}°C, "
                        f"which has fallen below the statutory 65°C threshold (FSSAI Reg 4(3)). "
                        f"Food has entered the Microbial Danger Zone (5°C-65°C). Reverting to strict ambient holding rules."
                    )
                    temp_status_summary = f"DANGER ZONE BREACH ({measured_temp_celsius:.1f}°C < 65°C)"
                    effective_storage = "ambient"
                else:
                    temp_status_summary = f"HOT-HOLDING VERIFIED ({measured_temp_celsius:.1f}°C >= 65°C)"
                    temp_alert = f"✅ Active hot-holding verified at {measured_temp_celsius:.1f}°C (Compliant with FSSAI Reg 4(3))."

            elif storage_condition == "refrigerated":
                if measured_temp_celsius > 5.0:
                    temp_alert = (
                        f"⚠️ COLD-CHAIN BREACH: Chilled temperature is {measured_temp_celsius:.1f}°C "
                        f"(exceeds statutory 5°C ceiling under FSSAI Reg 4(3)). Ambient holding rules applied."
                    )
                    temp_status_summary = f"COLD CHAIN BREACH ({measured_temp_celsius:.1f}°C > 5°C)"
                    effective_storage = "ambient"
                else:
                    temp_status_summary = f"COLD-CHAIN VERIFIED ({measured_temp_celsius:.1f}°C <= 5°C)"
                    temp_alert = f"✅ Active cold-chain verified at {measured_temp_celsius:.1f}°C (Compliant with FSSAI Reg 4(3))."

            else:  # ambient
                if 5.0 <= measured_temp_celsius <= 65.0:
                    temp_status_summary = f"IN DANGER ZONE ({measured_temp_celsius:.1f}°C)"
                    temp_alert = f"⚠️ Ambient batch is within the Bacterial Danger Zone ({measured_temp_celsius:.1f}°C). FSSAI 2h/4h rules strictly enforced."
                else:
                    temp_status_summary = f"AMBIENT ({measured_temp_celsius:.1f}°C)"

        # Formulate query for RAG retriever
        query_terms = (
            f"{item} {profile['name']} {effective_storage} holding time "
            f"danger zone safe donation Lucknow transit"
        )
        if measured_temp_celsius is not None:
            query_terms += f" temperature danger zone {measured_temp_celsius}C"

        retrieved_rules = self.retriever.retrieve(query_terms, top_k=3)

        # Base calculations for safe pickup by
        if effective_storage == "ambient":
            max_allowed_minutes = profile["ambient_max_minutes"]
        elif effective_storage == "hot_holding":
            max_allowed_minutes = profile["ambient_max_minutes"] + 90  # 1.5 hr extension under >=65C
        else:  # refrigerated
            max_allowed_minutes = 1440  # 24 hours under <=5C

        safe_until_dt = dt_prepared + timedelta(minutes=max_allowed_minutes)
        safe_until_str = safe_until_dt.strftime("%H:%M")

        # Decision Logic
        if profile["prohibited"]:
            status = "NON_COMPLIANT_REJECTED"
            verdict_badge = "🔴 REJECTED (FSSAI PROHIBITED ITEM)"
            reason = (
                f"{profile['name']} is strictly prohibited from surplus redistribution under "
                f"FSSAI Regulation 4(4) due to high microbiological hazard ({profile['danger_organism']})."
            )
            lnn_action = (
                "Segregate immediately into GREEN Wet Waste bin. Route to campus aerobic composting "
                "or LNN Kanha Upvan / Mohanlalganj biomethanation plant as per LNN SWM By-Law Sec 18."
            )
            compliance_note = "Violates FSSAI Reg 4(4) prohibited surplus food criteria."

        elif total_projected_exposure > max_allowed_minutes:
            status = "NON_COMPLIANT_REJECTED"
            verdict_badge = "🔴 REJECTED (HOLDING TIME EXCEEDED)"
            overdue_mins = total_projected_exposure - max_allowed_minutes
            reason = (
                f"Total projected holding time ({total_projected_exposure} mins) exceeds the statutory "
                f"ambient limit of {max_allowed_minutes} mins by {overdue_mins} mins. Food has entered "
                f"the bacterial growth hazard window under FSSAI Regulation 4(2)."
            )
            lnn_action = (
                "DO NOT DISPATCH. Under LNN SWM By-Law Sec 18 & Sec 10, batch must be diverted "
                "to decentralized bio-composting or LNN Biomethanation plant. Landfill dumping prohibited."
            )
            compliance_note = (
                f"Exceeds FSSAI 4-hour ambient ceiling ({elapsed_minutes}m elapsed + {transit_minutes}m transit). "
                f"Condemned per FSSAI Reg 4(2) & LNN By-Law Sec 18."
            )

        elif total_projected_exposure > profile["ambient_safe_dispatch"]:
            status = "COMPLIANT_URGENT"
            verdict_badge = "🟡 COMPLIANT (URGENT DISPATCH MANDATED)"
            remaining_mins = max_allowed_minutes - total_projected_exposure
            reason = (
                f"Food is approaching the upper microbial safety boundary. Handover and consumption must "
                f"occur within {remaining_mins} minutes upon delivery. Immediate transit dispatch required."
            )
            lnn_action = (
                f"Clear via Campus Security Gate Pass under LNN Health Sec 21. Ensure covered transit "
                f"within {transit_minutes} min corridor window under LNN Transit Protocol Sec 14."
            )
            compliance_note = (
                f"Within FSSAI 4-hour ambient holding limit ({elapsed_minutes}m elapsed). "
                f"Urgent consumption mandated before {safe_until_str} per FSSAI Reg 4(2) and LNN Sec 14."
            )

        else:
            status = "COMPLIANT_SAFE"
            verdict_badge = "🟢 COMPLIANT (SAFE FOR REDISTRIBUTION)"
            remaining_mins = max_allowed_minutes - total_projected_exposure
            reason = (
                f"Batch is freshly prepared ({elapsed_minutes} mins elapsed) and well within FSSAI and LNN "
                f"food safety parameters with a healthy {remaining_mins}-minute safety buffer."
            )
            lnn_action = (
                f"Standard dispatch approved. Issue Gate Pass under LNN Health Sec 21 to {shelter_name}. "
                f"Transit corridor window: {transit_minutes} mins."
            )
            compliance_note = (
                f"Compliant with FSSAI Surplus Reg 4(2) & 4(3) temperature-holding standards. "
                f"Safe consumption window active until {safe_until_str}."
            )

        if temp_alert and ("TEMPERATURE ABUSE" in temp_alert or "COLD-CHAIN BREACH" in temp_alert):
            reason = f"{temp_alert} {reason}"
            compliance_note = f"{temp_alert} {compliance_note}"

        return {
            "status": status,
            "badge": verdict_badge,
            "reason": reason,
            "compliance_note": compliance_note,
            "lnn_action": lnn_action,
            "temp_summary": temp_status_summary,
            "temp_status": "DANGER_ZONE_BREACH" if "BREACH" in temp_status_summary else ("VERIFIED" if "VERIFIED" in temp_status_summary else "NORMAL"),
            "timeline": {
                "time_prepared": time_prepared,
                "assessment_time": dt_assess.strftime("%H:%M"),
                "elapsed_minutes": elapsed_minutes,
                "transit_minutes": transit_minutes,
                "total_exposure_minutes": total_projected_exposure,
                "safe_pickup_by": safe_until_str,
                "max_allowed_minutes": max_allowed_minutes,
                "measured_temp_celsius": measured_temp_celsius,
                "temp_status_summary": temp_status_summary,
                "temp_alert": temp_alert
            },
            "parameters": {
                "item": item,
                "servings": servings,
                "category": profile["name"],
                "storage_condition": effective_storage,
                "stated_storage_condition": storage_condition,
                "measured_temp_celsius": measured_temp_celsius,
                "origin_zone": origin_zone,
                "dest_zone": dest_zone,
                "shelter": shelter_name
            },
            "retrieved_rules": retrieved_rules
        }

