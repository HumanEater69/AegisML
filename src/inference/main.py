from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import time
import uuid
import hashlib
import random

app = FastAPI(
    title="AegisML Quantum Inference API",
    version="2.0.0",
    description="Enterprise-grade AI Fraud Detection Engine with Cyber Threat Intelligence."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionPayload(BaseModel):
    TransactionID: int = Field(default_factory=lambda: int(time.time()))
    TransactionAmt: float = Field(..., gt=0)
    DeviceType: str = "Unknown"
    DistanceKM: float = 0.0
    HourOfDay: int = 12
    IsNewDevice: bool = False
    FailedLogins: int = 0
    IPAddress: str = "127.0.0.1"

class ThreatIntelligence(BaseModel):
    dark_web_exposure_index: float
    botnet_signature_match: bool
    geo_velocity_alert: str
    behavioral_biometric_trust: float
    device_spoofing_probability: float
    syndicate_link_nodes: List[str]

class RiskResponse(BaseModel):
    request_id: str
    transaction_id: int
    fraud_capacity_percentage: float
    risk_tier: str
    action_protocol: str
    execution_time_ms: float
    risk_drivers: Dict[str, float]
    cyber_threat_intelligence: ThreatIntelligence

def assign_tier(prob):
    if prob >= 0.80:
        return 'Critical', 'BLOCK_AND_ISOLATE'
    elif prob >= 0.40:
        return 'Suspicious', 'STEP_UP_AUTH'
    else:
        return 'Clear', 'APPROVE_TRANSACTION'

def generate_syndicate_nodes(count: int) -> List[str]:
    return [hashlib.sha256(str(random.random()).encode()).hexdigest()[:12] for _ in range(count)]

@app.get("/health")
def health_check():
    return {"status": "AegisML Engine Online", "quantum_core": "STABLE"}

@app.post("/api/v1/predict/quantum", response_model=RiskResponse)
async def predict_quantum_fraud(payload: TransactionPayload):
    start_time = time.time()
    
    # -------------------------------------------------------------
    # 🧠 THE "CRAZY" MOCK INFERENCE ENGINE
    # In production, this runs against XGBoost/LightGBM & Graph DBs
    # -------------------------------------------------------------
    base_risk = 0.05
    risk_drivers = {}
    
    if payload.TransactionAmt > 1000:
        base_risk += 0.25
        risk_drivers["High_Amount_Variance"] = 0.25
    if payload.HourOfDay < 5 or payload.HourOfDay > 23:
        base_risk += 0.20
        risk_drivers["Anomalous_Time"] = 0.20
    if payload.DistanceKM > 500:
        base_risk += 0.15
        risk_drivers["Geo_Distance_Anomaly"] = 0.15
    if payload.IsNewDevice:
        base_risk += 0.15
        risk_drivers["Unrecognized_Device"] = 0.15
    if payload.FailedLogins > 0:
        base_risk += 0.10 * payload.FailedLogins
        risk_drivers["Brute_Force_Attempt"] = 0.10 * payload.FailedLogins

    # Add non-linear synthetic noise to simulate complex model
    noise = random.uniform(0.9, 1.2)
    fraud_prob = min(0.9999, base_risk * noise)
    
    tier, action = assign_tier(fraud_prob)
    
    # -------------------------------------------------------------
    # 🕸️ CYBER THREAT INTELLIGENCE (Simulated Dark Web & Graph Logic)
    # -------------------------------------------------------------
    is_critical = tier == 'Critical'
    
    geo_alert = "NORMAL"
    if payload.DistanceKM > 1000 and payload.HourOfDay < 4:
        geo_alert = f"IMPOSSIBLE_TRAVEL_DETECTED: {payload.DistanceKM}km in < 1 hr"

    threat_intel = ThreatIntelligence(
        dark_web_exposure_index=random.uniform(0.7, 0.99) if is_critical else random.uniform(0.01, 0.2),
        botnet_signature_match=is_critical and random.choice([True, False]),
        geo_velocity_alert=geo_alert,
        behavioral_biometric_trust=random.uniform(0.1, 0.3) if is_critical else random.uniform(0.8, 0.99),
        device_spoofing_probability=random.uniform(0.8, 0.99) if payload.IsNewDevice else 0.05,
        syndicate_link_nodes=generate_syndicate_nodes(random.randint(2, 6)) if is_critical else []
    )
    
    exec_time = round((time.time() - start_time) * 1000, 2)
    
    return RiskResponse(
        request_id=str(uuid.uuid4()),
        transaction_id=payload.TransactionID,
        fraud_capacity_percentage=round(fraud_prob * 100, 2),
        risk_tier=tier,
        action_protocol=action,
        execution_time_ms=exec_time,
        risk_drivers=risk_drivers,
        cyber_threat_intelligence=threat_intel
    )
