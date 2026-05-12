from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from datetime import datetime
from app.database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String, index=True)
    temperature = Column(Float)
    rainfall_mm = Column(Float)
    wind_speed_kmh = Column(Float)
    pressure_hpa = Column(Float)
    humidity = Column(Float)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    recorded_at = Column(DateTime, default=datetime.utcnow)

class DisasterEvent(Base):
    __tablename__ = "disaster_events"

    id = Column(Integer, primary_key=True, index=True)
    disaster_type = Column(String)
    severity = Column(Float)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    affected_radius_km = Column(Float)
    occurred_at = Column(DateTime)
    extra_data = Column(JSONB)

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    risk_score = Column(Float)
    disaster_type = Column(String)
    predicted_at = Column(DateTime, default=datetime.utcnow)
    features_used = Column(JSONB)