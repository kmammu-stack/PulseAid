from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import RiskPrediction
from app.ml.predictor import predict_risk
from datetime import datetime

router = APIRouter()

class PredictRequest(BaseModel):
    latitude: float
    longitude: float
    rainfall_mm: float
    wind_speed_kmh: float
    pressure_hpa: float
    temperature: float
    humidity: float

@router.post("/risk")
def get_risk_prediction(request: PredictRequest, db: Session = Depends(get_db)):
    """
    Takes weather features for a location and returns a disaster risk score.
    """
    features = {
        "rainfall_mm": request.rainfall_mm,
        "wind_speed_kmh": request.wind_speed_kmh,
        "pressure_hpa": request.pressure_hpa,
        "temperature": request.temperature,
        "humidity": request.humidity
    }

    try:
        risk_score, disaster_type = predict_risk(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML model error: {str(e)}")

    prediction = RiskPrediction(
        location=f"POINT({request.longitude} {request.latitude})",
        risk_score=risk_score,
        disaster_type=disaster_type,
        predicted_at=datetime.utcnow(),
        features_used=features
    )
    db.add(prediction)
    db.commit()

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "risk_score": round(risk_score, 3),
        "disaster_type": disaster_type,
        "alert_level": get_alert_level(risk_score),
        "predicted_at": prediction.predicted_at
    }

def get_alert_level(score: float) -> str:
    if score >= 0.75:
        return "CRITICAL"
    elif score >= 0.50:
        return "HIGH"
    elif score >= 0.25:
        return "MODERATE"
    else:
        return "LOW"

@router.get("/history")
def get_prediction_history(db: Session = Depends(get_db)):
    predictions = db.query(RiskPrediction).order_by(
        RiskPrediction.predicted_at.desc()
    ).limit(20).all()

    return [
        {
            "risk_score": p.risk_score,
            "disaster_type": p.disaster_type,
            "alert_level": get_alert_level(p.risk_score),
            "predicted_at": p.predicted_at
        }
        for p in predictions
    ]