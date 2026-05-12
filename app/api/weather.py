from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WeatherRecord
import requests
import os
from datetime import datetime

router = APIRouter()

@router.get("/latest")
def get_latest_weather(db: Session = Depends(get_db)):
    records = db.query(WeatherRecord).order_by(
        WeatherRecord.recorded_at.desc()
    ).limit(10).all()
    
    return [
        {
            "station_id": r.station_id,
            "temperature": r.temperature,
            "rainfall_mm": r.rainfall_mm,
            "wind_speed_kmh": r.wind_speed_kmh,
            "pressure_hpa": r.pressure_hpa,
            "humidity": r.humidity,
            "recorded_at": r.recorded_at
        }
        for r in records
    ]

@router.post("/ingest")
def ingest_weather(db: Session = Depends(get_db)):
    """
    Fetches weather data from IMD open API and stores it.
    In production this runs automatically via Celery every hour.
    """
    try:
        # IMD open data endpoint (replace with real feed URL when available)
        response = requests.get(
            "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
            params={
                "api-key": os.getenv("IMD_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad38d4e3335d9b0b5c"),
                "format": "json",
                "limit": "50"
            },
            timeout=10
        )
        data = response.json()
        records_added = 0

        for item in data.get("records", []):
            record = WeatherRecord(
                station_id=item.get("station_id", "UNKNOWN"),
                temperature=float(item.get("temp", 0) or 0),
                rainfall_mm=float(item.get("rainfall", 0) or 0),
                wind_speed_kmh=float(item.get("wind_speed", 0) or 0),
                pressure_hpa=float(item.get("pressure", 1013) or 1013),
                humidity=float(item.get("humidity", 50) or 50),
                recorded_at=datetime.utcnow()
            )
            db.add(record)
            records_added += 1

        db.commit()
        return {"message": f"Ingested {records_added} weather records"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stations")
def list_stations(db: Session = Depends(get_db)):
    stations = db.query(WeatherRecord.station_id).distinct().all()
    return {"stations": [s[0] for s in stations]}