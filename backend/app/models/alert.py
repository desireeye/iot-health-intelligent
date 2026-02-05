from datetime import datetime
from enum import Enum
from typing import Optional
from beanie import Document
from pydantic import Field

class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class OutbreakAlert(Document):
    """
    Represents a generated alert based on ML predictions or sensor thresholds.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location_lat: Optional[float]
    location_lon: Optional[float]
    test_station_id: str
    
    severity: AlertSeverity
    risk_score: float = Field(..., description="ML Predicted Risk Score (0-100)")
    prediction_model: str = Field(..., description="Model used e.g., 'RandomForest_v1'")
    
    message: str
    status: str = Field(default="NEW", description="NEW, ACKNOWLEDGED, RESOLVED")

    class Settings:
        name = "outbreak_alerts"
