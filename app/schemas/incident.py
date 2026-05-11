from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    location: str

    latitude: str
    longitude: str

    severity: str