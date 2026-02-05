from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING

class SensorReading(Document):
    """
    Represents a single sensor reading from an edge node.
    Stored in a MongoDB TimeSeries collection.
    """
    sensor_id: str = Field(..., description="Unique ID of the sensor/edge node")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of reading")
    
    # Water Quality Parameters
    ph: float = Field(..., description="pH Level (0-14)")
    turbidity: float = Field(..., description="Turbidity in NTU")
    temperature: float = Field(..., description="Temperature in Celsius")
    tds: float = Field(..., description="Total Dissolved Solids in ppm")
    
    # Optional: Prediction inputs or pre-processed flags
    is_anomalous: bool = Field(default=False, description="Flagged by Edge device")

    class Settings:
        name = "sensor_readings"
        timeseries = {
            "time_field": "timestamp",
            "meta_field": "sensor_id",
            "granularity": "seconds"
        }
        indexes = [
            IndexModel([("sensor_id", ASCENDING), ("timestamp", DESCENDING)]),
        ]
