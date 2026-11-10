"""
IBM Granite Prompt Compiler & Formatter for Anna-Setu.
Synthesizes compliance check results, retrieved statutory clauses,
and logistics metadata into broadcast notifications and audit manifests.
"""

from typing import Dict, Any


class GraniteAlertCompiler:
    """
    Implements IBM Granite prompt engineering logic to generate compliant
    WhatsApp/SMS alerts, campus gate passes, and audit log records.
    """

    SYSTEM_PROMPT = (
        "You are the messaging assistant for Anna-Setu, a campus food-redistribution system. "
        "Your task is to convert structured surplus-food data into a short, clear, and warm "
        "broadcast message for a verified shelter coordinator.\n\n"
        "Rules:\n"
        "1. Use only the facts provided in the input data. Never invent quantities, times, food items, or locations.\n"
        "2. Always state the safe-pickup-by time exactly as given.\n"
        "3. Reference the retrieved compliance note in one short line so the coordinator knows the food has been checked against safety guidelines.\n"
        "4. Keep the message under 60 words, in plain, respectful language suitable for WhatsApp/SMS.\n"
        "5. End with a clear call to action (how to confirm pickup).\n"
        "6. Do not include any student-identifying or personal data."
    )

    def compile_shelter_alert(self, eval_result: Dict[str, Any], pickup_location: str) -> str:
        """
        Generates the standard shelter broadcast message following IBM Granite template.
        """
        status = eval_result["status"]
        params = eval_result["parameters"]
        timeline = eval_result["timeline"]
        compliance_note = eval_result["compliance_note"]

        if status == "NON_COMPLIANT_REJECTED":
            return (
                "⚠️ *Surplus Redistribution Cancelled - Anna-Setu Safety Block*\n\n"
                f"Notice: The proposed surplus batch of {params['item']} ({int(params['servings'])} servings) "
                f"did NOT clear safety compliance checks.\n\n"
                f"Reason: {eval_result['reason']}\n\n"
                f"Action Taken: {eval_result['lnn_action']}\n\n"
                "In compliance with FSSAI regulations and LNN bylaws, this batch will not be dispatched to shelters."
            )

        urgency_flag = " [URGENT DISPATCH]" if status == "COMPLIANT_URGENT" else ""

        message = (
            f"🍽️ *Surplus Food Alert{urgency_flag} - Anna-Setu*\n\n"
            f"Hi {params['shelter']} team, we have {int(params['servings'])} servings of {params['item']} "
            f"ready for pickup, prepared at {timeline['time_prepared']} and safe until {timeline['safe_pickup_by']} "
            f"({compliance_note}).\n\n"
            f"📍 *Pickup point:* {pickup_location}.\n\n"
            f"Please reply *YES* to confirm pickup, or call the manager directly to adjust the arrival window. "
            f"Thank you for partnering with us!"
        )
        return message

    def compile_fssai_audit_manifest(self, eval_result: Dict[str, Any], pickup_location: str) -> str:
        """
        Generates the formal FSSAI Form B and LNN Campus Gate Pass Audit Record.
        """
        params = eval_result["parameters"]
        timeline = eval_result["timeline"]

        clauses_str = ""
        for rule in eval_result.get("retrieved_rules", []):
            clauses_str += f"- [{rule.get('id', 'REF')}] {rule.get('clause', '')} (Match Score: {rule.get('relevance_score', 0):.2f})\n"

        manifest = (
            "======================================================================\n"
            "   ANNA-SETU OFFICIAL SURPLUS FOOD COMPLIANCE MANIFEST (FORM B)\n"
            "   In Accordance with FSSAI Surplus Regulations 2019 & LNN SWM By-Laws\n"
            "======================================================================\n\n"
            f"BATCH STATUS:        {eval_result['badge']}\n"
            f"FOOD ITEM:           {params['item']} ({params['category']})\n"
            f"QUANTITY / SERVINGS: {int(params['servings'])} Portions\n"
            f"STORAGE CONDITION:   {params['storage_condition'].upper()}\n"
            f"PREPARATION TIME:    {timeline['time_prepared']} IST\n"
            f"VERIFICATION TIME:   {timeline['assessment_time']} IST (Elapsed: {timeline['elapsed_minutes']} mins)\n"
            f"TRANSIT ESTIMATE:    {timeline['transit_minutes']} mins (Corridor: Zone {params['origin_zone']} -> Zone {params['dest_zone']})\n"
            f"SAFE CONSUME-BY:     {timeline['safe_pickup_by']} IST\n"
            f"DISPATCH LOCATION:   {pickup_location}\n"
            f"TARGET RECIPIENT:    {params['shelter']}\n\n"
            "STATUTORY COMPLIANCE CITATIONS (RAG RETRIEVED):\n"
            f"{clauses_str}\n"
            "OPERATIONAL DIRECTIVE:\n"
            f"Compliance Note:     {eval_result['compliance_note']}\n"
            f"LNN Municipal Action: {eval_result['lnn_action']}\n\n"
            "LEGAL INDEMNITY (GOOD SAMARITAN CLAUSE):\n"
            "This donation is made in good faith in strict compliance with FSSAI Surplus Food\n"
            "Regulations 2019 Regulation 4(5) and Section 7. The donor is indemnified against civil\n"
            "and criminal liability once handed over within verified thermal and time thresholds.\n"
            "======================================================================\n"
            "DISPATCH SIGN-OFF: ___________________    RECIPIENT SIGN-OFF: ___________________\n"
            "Mess Manager, Anna-Setu Campus Hub         Verified Shelter / NGO Coordinator\n"
            "======================================================================"
        )
        return manifest

