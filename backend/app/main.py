from fastapi import FastAPI
from app.db import init_db
from app.services.mqtt_service import start_mqtt, stop_mqtt
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    start_mqtt()
    yield
    # Shutdown
    stop_mqtt()

app = FastAPI(
    title="Predictive IoT Health Intelligence",
    version="1.0.0",
    lifespan=lifespan
)

from app.api.api import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "System Online", "service": "IoT Health Intelligence API"}

@app.get("/health")
def health_check():
    return {"database": "connected", "redis": "connected"} # Todo: Real checks
