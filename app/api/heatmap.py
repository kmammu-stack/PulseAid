from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TowerPing(BaseModel):
    latitude: float
    longitude: float
    ping_count: int
    tower_id: str

class HeatmapRequest(BaseModel):
    pings: List[TowerPing]
    disaster_lat: float
    disaster_lon: float
    radius_km: float = 50.0

@router.post("/survivors")
def generate_survivor_heatmap(request: HeatmapRequest, db: Session = Depends(get_db)):
    """
    Takes mobile tower ping data and population density to generate
    a probability heatmap of where survivors are likely located.
    """
    try:
        heatmap_points = []

        for ping in request.pings:
            # Use PostGIS to calculate distance from disaster center
            result = db.execute(text("""
                SELECT ST_Distance(
                    ST_GeogFromText('POINT(:lon :lat)'),
                    ST_GeogFromText('POINT(:dlon :dlat)')
                ) as distance_meters
            """), {
                "lon": ping.longitude,
                "lat": ping.latitude,
                "dlon": request.disaster_lon,
                "dlat": request.disaster_lat
            }).fetchone()

            distance_km = result.distance_meters / 1000

            # Only include points within the search radius
            if distance_km <= request.radius_km:
                # Probability = more pings + closer to disaster = higher chance of survivors
                proximity_score = 1 - (distance_km / request.radius_km)
                ping_score = min(ping.ping_count / 100, 1.0)
                probability = round((proximity_score * 0.6) + (ping_score * 0.4), 3)

                heatmap_points.append({
                    "tower_id": ping.tower_id,
                    "latitude": ping.latitude,
                    "longitude": ping.longitude,
                    "ping_count": ping.ping_count,
                    "distance_km": round(distance_km, 2),
                    "survivor_probability": probability,
                    "priority": get_priority(probability)
                })

        # Sort by highest probability first
        heatmap_points.sort(key=lambda x: x["survivor_probability"], reverse=True)

        return {
            "total_zones": len(heatmap_points),
            "heatmap": heatmap_points,
            "highest_priority_zone": heatmap_points[0] if heatmap_points else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zones")
def get_high_priority_zones(
    lat: float,
    lon: float,
    radius_km: float = 50.0,
    db: Session = Depends(get_db)
):
    """
    Returns all high-risk zones within radius using PostGIS spatial query.
    """
    try:
        results = db.execute(text("""
            SELECT
                station_id,
                rainfall_mm,
                wind_speed_kmh,
                ST_AsText(location) as location_text,
                ST_Distance(
                    location::geography,
                    ST_GeogFromText('POINT(:lon :lat)')
                ) / 1000 as distance_km
            FROM weather_records
            WHERE ST_DWithin(
                location::geography,
                ST_GeogFromText('POINT(:lon :lat)'),
                :radius_meters
            )
            ORDER BY distance_km ASC
            LIMIT 20
        """), {
            "lat": lat,
            "lon": lon,
            "radius_meters": radius_km * 1000
        }).fetchall()

        return {
            "zones": [
                {
                    "station_id": r.station_id,
                    "rainfall_mm": r.rainfall_mm,
                    "wind_speed_kmh": r.wind_speed_kmh,
                    "distance_km": round(r.distance_km, 2)
                }
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_priority(probability: float) -> str:
    if probability >= 0.7:
        return "IMMEDIATE"
    elif probability >= 0.4:
        return "HIGH"
    else:
        return "MODERATE"