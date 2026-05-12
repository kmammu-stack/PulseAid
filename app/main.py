from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import weather, predict, heatmap, routing

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Disaster Response AI API",
    description="PRE prediction, survivor heatmaps, and rescue routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(heatmap.router, prefix="/api/heatmap", tags=["Heatmap"])
app.include_router(routing.router, prefix="/api/routing", tags=["Routing"])

@app.get("/")
def root():
    return {"status": "Disaster Response AI is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}