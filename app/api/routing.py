from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import os

router = APIRouter()

class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    profile: str = "driving-car"

class EvacuationRequest(BaseModel):
    disaster_lat: float
    disaster_lon: float
    disaster_radius_km: float
    safe_zones: List[dict]

@router.post("/evacuation")
def get_evacuation_route(request: RouteRequest):
    """
    Gets the fastest route between two points using OpenRouteService.
    Used for both evacuation routes and NDRF rescue team dispatch.
    """
    ORS_KEY = os.getenv("ORS_API_KEY")

    if not ORS_KEY:
        # Return a mock route if no API key yet
        return {
            "message": "Mock route — add ORS_API_KEY to .env for real routes",
            "start": [request.start_lat, request.start_lon],
            "end": [request.end_lat, request.end_lon],
            "distance_km": 25.4,
            "duration_minutes": 38,
            "geometry": []
        }

    try:
        response = requests.post(
            f"https://api.openrouteservice.org/v2/directions/{request.profile}",
            headers={
                "Authorization": ORS_KEY,
                "Content-Type": "application/json"
            },
            json={
                "coordinates": [
                    [request.start_lon, request.start_lat],
                    [request.end_lon, request.end_lat]
                ]
            },
            timeout=10
        )
        data = response.json()

        route = data["routes"][0]
        summary = route["summary"]

        return {
            "distance_km": round(summary["distance"] / 1000, 2),
            "duration_minutes": round(summary["duration"] / 60, 1),
            "geometry": route.get("geometry", ""),
            "start": [request.start_lat, request.start_lon],
            "end": [request.end_lat, request.end_lon]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dispatch")
def dispatch_rescue_team(request: EvacuationRequest):
    """
    Given a disaster location and list of safe zones,
    returns ranked evacuation routes to each safe zone.
    """
    routes = []

    for zone in request.safe_zones:
        routes.append({
            "safe_zone": zone.get("name", "Unknown"),
            "safe_zone_lat": zone.get("lat"),
            "safe_zone_lon": zone.get("lon"),
            "estimated_distance_km": zone.get("distance_km", 0),
            "recommended": zone.get("distance_km", 999) < 30
        })

    routes.sort(key=lambda x: x["estimated_distance_km"])

    return {
        "disaster_location": {
            "lat": request.disaster_lat,
            "lon": request.disaster_lon
        },
        "recommended_routes": routes,
        "nearest_safe_zone": routes[0] if routes else None
    }