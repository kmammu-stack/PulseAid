from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base

from sqlalchemy import Boolean

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    location = Column(String)

    latitude = Column(String)
    longitude = Column(String)

    severity = Column(String)

    status = Column(String, default="ACTIVE")

    image_url = Column(String, nullable=True)

    reported_by = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    resolved = Column(Boolean, default=False)