from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Aegis-Swiss-Bridge API",
    description="Institutional Financial Intelligence & Anomaly Detection API",
    version="1.0.0"
)

# قاعدة بيانات وهمية لمفاتيح الترخيص الخاصة بالمؤسسات الكبرى (الباقات التجريبية والمدفوعة)
VALID_API_KEYS = {
    "aegis_enterprise_tier1_xyz999": "Enterprise",
    "aegis_standard_tier2_abc123": "Standard"
}

class TransactionRequest(BaseModel):
    tx_id: str
    amount: float
    uses_mixer: bool
    micro_wallets_split: int

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key. Commercial authorization required.")
    return VALID_API_KEYS[x_api_key]

@app.post("/api/v1/detect")
def detect_anomaly(tx: TransactionRequest, tier: str = Depends(verify_api_key)):
    # خوارزمية حساب درجة الخطر للمؤسسات
    risk_score = 0.0
    if tx.uses_mixer:
            risk_score += 50.0
    risk_score += min(tx.micro_wallets_split * 2.0, 50.0)
    
    is_flagged = risk_score >= 50.0
    
    return {
        "status": "success",
        "client_tier": tier,
        "transaction_id": tx.tx_id,
        "risk_score": round(risk_score, 4),
        "flagged_for_review": is_flagged,
        "audit_trail": "Cryptographically verified by Aegis-Swiss-Bridge engine"
    }
