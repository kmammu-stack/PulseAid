from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "disaster_tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery_app.conf.beat_schedule = {
    "ingest-weather-every-hour": {
        "task": "app.tasks.ingest_weather_task",
        "schedule": 3600.0,  # every hour in seconds
    }
}

@celery_app.task
def ingest_weather_task():
    """
    Runs every hour automatically to fetch fresh IMD weather data.
    """
    import requests
    print("Running scheduled weather ingestion...")
    try:
        response = requests.post("http://localhost:8000/api/weather/ingest")
        print(f"Weather ingestion result: {response.json()}")
    except Exception as e:
        print(f"Weather ingestion failed: {e}")

@celery_app.task
def run_risk_predictions_task():
    """
    Runs risk predictions for all active weather stations.
    Can be triggered manually or on a schedule.
    """
    print("Running risk predictions for all stations...")