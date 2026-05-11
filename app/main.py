from fastapi import FastAPI

from fastapi import WebSocket

from app.websocket_manager import connected_clients

from app.routes import auth, user, incident

from app.database import engine, Base

from fastapi.staticfiles import StaticFiles

from app.models import user as user_model
from app.models import incident as incident_model

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(incident.router)


@app.get("/")
def root():
    return {"message": "Disaster Backend Running 🚀"}





@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
        connected_clients.remove(websocket)