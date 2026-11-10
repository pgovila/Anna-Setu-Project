"""
Anna-Setu IoT Ingestion & Compliance API Server.
Connects Track B Hardware Kiosk telemetry to Track A RAG Compliance Pipeline.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uvicorn

from rag.pipeline import AnnaSetuRAGPipeline

app = FastAPI(
    title="Anna-Setu IoT Gateway API",
    description="Bridge connecting Smart Kitchen Kiosks (Track B) to RAG Compliance Engine (Track A)",
    version="1.0.0"
)

# Initialize single instance of Anna-Setu RAG Pipeline
pipeline = AnnaSetuRAGPipeline()

# In-memory transaction telemetry ledger for the campus mess
TELEMETRY_LOGS = []


class KioskTelemetryPayload(BaseModel):
    station_id: str = Field(..., example="ANNA-SETU-KIOSK-UPES-01")
    supervisor_id: str = Field(..., example="CHEF-RAJESH-44")
    surplus_weight_kg: float = Field(..., example=18.5)
    surface_temp_c: float = Field(..., example=68.2)
    plate_waste_fill_pct: Optional[float] = Field(0.0, example=45.0)
    food_item: str = Field(default="Vegetable Pulao and Dal Tadka", example="Vegetable Pulao and Dal Tadka")
    time_prepared: str = Field(default="12:30", example="12:30")
    category_key: str = Field(default="cooked_grains_curry", example="cooked_grains_curry")
    origin_zone: int = Field(default=4, example=4)
    shelter_display_name: Optional[str] = Field(
        default="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))",
        example="Rain Basera Charbagh Railway Hub (Zone 1 (Charbagh / Station Road))"
    )
    pickup_location: Optional[str] = Field(default="Central Campus Mess, Gate 2", example="Central Campus Mess, Gate 2")


@app.get("/")
def health_check():
    return {
        "system": "Anna-Setu Dual-Track IoT Gateway",
        "status": "ONLINE",
        "timestamp": datetime.now().isoformat(),
        "registered_kiosks": ["ANNA-SETU-KIOSK-UPES-01"]
    }


@app.post("/api/iot/telemetry")
def process_kiosk_telemetry(payload: KioskTelemetryPayload):
    """
    Receives physical ground truth from Track B Smart Kiosk:
    - Automatically estimates portions from measured net weight (~350g per standard portion)
    - Automatically classifies storage condition based on IR temperature sensor:
      - surface_temp_c >= 65.0 C -> hot_holding
      - surface_temp_c <= 5.0 C  -> refrigerated
      - Else (5C - 65C)          -> ambient (Danger Zone)
    - Evaluates compliance through FSSAI and LNN RAG Pipeline
    - Generates IBM Granite shelter alert & Form B manifest
    """
    # 1. Physical estimation from weight
    estimated_servings = max(1, int(payload.surplus_weight_kg / 0.35)) # ~350g per adult meal
    
    # 2. Automated temperature classification
    if payload.surface_temp_c >= 65.0:
        storage_condition = "hot_holding"
        temp_status = "SAFE (ACTIVE HOT HOLDING >= 65C)"
    elif payload.surface_temp_c <= 5.0:
        storage_condition = "refrigerated"
        temp_status = "SAFE (ACTIVE COLD HOLDING <= 5C)"
    else:
        storage_condition = "ambient"
        temp_status = f"IN DANGER ZONE ({payload.surface_temp_c:.1f}C - Subject to 2h/4h ambient ceiling)"

    now_hhmm = datetime.now().strftime("%H:%M")

    # 3. Execute RAG Compliance Evaluation
    res = pipeline.evaluate_surplus(
        item=payload.food_item,
        servings=estimated_servings,
        category_key=payload.category_key,
        time_prepared=payload.time_prepared,
        assessment_time=now_hhmm,
        storage_condition=storage_condition,
        origin_zone=payload.origin_zone,
        shelter_display_name=payload.shelter_display_name,
        pickup_location=payload.pickup_location
    )

    eval_data = res["evaluation"]

    # 4. Formulate response payload for the IoT Kiosk actuators (LEDs / LCD / Relays)
    log_entry = {
        "event_id": f"EVT-{len(TELEMETRY_LOGS) + 1:04d}",
        "timestamp": datetime.now().isoformat(),
        "station_id": payload.station_id,
        "supervisor_id": payload.supervisor_id,
        "food_item": payload.food_item,
        "weight_kg": payload.surplus_weight_kg,
        "servings_calculated": estimated_servings,
        "surface_temp_c": payload.surface_temp_c,
        "temp_status": temp_status,
        "status": eval_data["status"],
        "badge": eval_data["badge"],
        "compliance_note": eval_data["compliance_note"],
        "lnn_action": eval_data["lnn_action"],
        "broadcast_message": res["broadcast_message"],
        "audit_manifest": res["audit_manifest"]
    }
    TELEMETRY_LOGS.append(log_entry)

    return {
        "status": eval_data["status"],
        "badge": eval_data["badge"],
        "servings": estimated_servings,
        "safe_until": eval_data["timeline"]["safe_pickup_by"],
        "reason": eval_data["reason"],
        "lnn_action": eval_data["lnn_action"],
        "broadcast_message": res["broadcast_message"],
        "event_id": log_entry["event_id"]
    }


@app.get("/api/iot/logs")
def get_telemetry_logs():
    """Returns audit log of all physical intake events captured by Track B kiosks."""
    return {
        "total_events": len(TELEMETRY_LOGS),
        "events": TELEMETRY_LOGS
    }


if __name__ == "__main__":
    print("Starting Anna-Setu IoT Ingestion API Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

