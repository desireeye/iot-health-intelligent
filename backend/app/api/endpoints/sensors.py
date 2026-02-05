from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.sensor_data import SensorReading
from beanie.operators import In

router = APIRouter()

@router.get("/", response_model=List[SensorReading])
async def get_readings(
    sensor_id: Optional[str] = None,
    limit: int = 100
):
    """
    Get latest sensor readings.
    """
    query = SensorReading.find_all()
    if sensor_id:
        query = SensorReading.find(SensorReading.sensor_id == sensor_id)
    
    return await query.sort(-SensorReading.timestamp).limit(limit).to_list()

@router.post("/", response_model=SensorReading)
async def create_reading(reading: SensorReading):
    """
    Manually create a reading (Useful for testing without MQTT/Edge).
    """
    await reading.insert()
    return reading
