from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.sensor_data import SensorReading
from app.models.alert import OutbreakAlert
from app.core.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(database=client.iot_health_db, document_models=[SensorReading, OutbreakAlert])
