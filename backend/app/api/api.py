from fastapi import APIRouter
from app.api.endpoints import sensors, alerts

api_router = APIRouter()
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
