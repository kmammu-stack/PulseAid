from fastapi import APIRouter, Depends, UploadFile, File, Form,HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.deps import require_role
import math
import os

from app.websocket_manager import connected_clients
from app.database_deps import get_db
from app.models.incident import Incident
from app.utils.deps import get_current_user


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


# -------------------------------
# Severity Detection
# -------------------------------

def detect_severity(description):

    text = description.lower()

    high_keywords = [
        "death",
        "collapsed",
        "fire",
        "explosion",
        "flood",
        "earthquake",
        "trapped"
    ]

    medium_keywords = [
        "injury",
        "damage",
        "waterlogging"
    ]

    for word in high_keywords:

        if word in text:
            return "HIGH"

    for word in medium_keywords:

        if word in text:
            return "MEDIUM"

    return "LOW"

def validate_description(description):

    text = description.strip()

    if len(text) < 10:

        return "Description too short"

    if text.isdigit():

        return "Description cannot contain only numbers"

    words = text.split()

    if len(words) < 3:

        return "Please provide more details"

    return None




# -------------------------------
# Create Incident
# -------------------------------

@router.post("/")
async def create_incident(

    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),

    latitude: str = Form(...),
    longitude: str = Form(...),

    image: UploadFile = File(None),

    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)

):

    # -------------------------------
    # Validation
    # -------------------------------

    severity = detect_severity(description)

    error = validate_description(description)

    if error:

     raise HTTPException(
        status_code=400,
        detail=error
    )


    try:

        lat = float(latitude)
        lon = float(longitude)

    except:

       raise HTTPException(
    status_code=400,
    detail="Latitude and Longitude must be valid numbers"
)

    if lat < -90 or lat > 90:

      raise HTTPException(
    status_code=400,
    detail="Latitude must be between -90 and 90"
)

    if lon < -180 or lon > 180:

        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180"
        )

    

  

    # -------------------------------
    # Image Upload
    # -------------------------------

    image_path = None

    if image:

        os.makedirs("uploads", exist_ok=True)

        image_path = f"uploads/{image.filename}"

        with open(image_path, "wb") as buffer:

            content = await image.read()

            buffer.write(content)

    # -------------------------------
    # Save Incident
    # -------------------------------

    new_incident = Incident(

        title=title,
        description=description,
        location=location,

        latitude=latitude,
        longitude=longitude,

        severity=severity,

        image_url=image_path,

        reported_by=current_user,

        resolved=False,
        status="ACTIVE"
    )

    db.add(new_incident)

    db.commit()

    db.refresh(new_incident)

    # -------------------------------
    # WebSocket Alert
    # -------------------------------

    disconnected_clients = []

    for client in connected_clients:

        try:

            await client.send_text(
                f"🚨 New Incident Reported: {title} | Severity: {severity}"
            )

        except:

            disconnected_clients.append(client)

    for client in disconnected_clients:

        connected_clients.remove(client)

    # -------------------------------
    # Response
    # -------------------------------

    return {

        "message": "Incident created successfully",

        "data": {

            "id": new_incident.id,
            "title": new_incident.title,
            "description": new_incident.description,
            "location": new_incident.location,

            "latitude": new_incident.latitude,
            "longitude": new_incident.longitude,

            "severity": new_incident.severity,

            "status": new_incident.status,
            "resolved": new_incident.resolved,

            "reported_by": new_incident.reported_by,

            "image_url": new_incident.image_url
        }
    }


# -------------------------------
# Get All Incidents
# -------------------------------

@router.get("/")
def get_all_incidents(

    db: Session = Depends(get_db)

):

    incidents = db.query(Incident).all()

    return incidents


# -------------------------------
# Filter Incidents
# -------------------------------

@router.get("/filter")
def filter_incidents(

    severity: str = None,
    status: str = None,

    db: Session = Depends(get_db)

):

    query = db.query(Incident)

    if severity:

        query = query.filter(
            Incident.severity == severity.upper()
        )

    if status:

        query = query.filter(
            Incident.status == status.upper()
        )

    return query.all()


# -------------------------------
# Update Incident Status
# -------------------------------

@router.put("/{incident_id}")
def update_incident_status(

    incident_id: int,
    status: str,

    db: Session = Depends(get_db),

    current_user: User=Depends(get_current_user)

):
    if current_user.role not in ["admin", "volunteer"]:

     raise HTTPException(
        status_code=403,
        detail="Access denied"
    )

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:

        raise HTTPException(
    status_code=404,
    detail="Incident not found"
)

    incident.status = status.upper()

    if status.upper() == "RESOLVED":

        incident.resolved = True

    else:

        incident.resolved = False

    db.commit()

    db.refresh(incident)

    return {

        "message": "Incident status updated",

        "data": {

            "id": incident.id,
            "status": incident.status,
            "resolved": incident.resolved
        }
    }


# -------------------------------
# Delete Incident
# -------------------------------

@router.delete("/{incident_id}")
def delete_incident(

    incident_id: int,

    db: Session = Depends(get_db),

    current_user: User=Depends(require_role("admin"))


):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)

    db.commit()

    return {
        "message": "Incident deleted successfully"
    }


# -------------------------------
# Nearby Incidents
# -------------------------------

@router.get("/nearby")
def nearby_incidents(

    latitude: float,
    longitude: float,

    radius: float = 5,

    db: Session = Depends(get_db)

):

    incidents = db.query(Incident).all()

    nearby = []

    for incident in incidents:

        try:

            incident_lat = float(incident.latitude)
            incident_lon = float(incident.longitude)

        except:

            continue

        distance = math.sqrt(

            (latitude - incident_lat) ** 2 +

            (longitude - incident_lon) ** 2
        )

        if distance <= radius / 100:

            nearby.append({

                "id": incident.id,
                "title": incident.title,

                "location": incident.location,

                "severity": incident.severity,

                "distance": round(distance, 4)
            })

    return nearby