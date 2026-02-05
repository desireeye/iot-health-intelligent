from fastapi import APIRouter
from typing import List
from app.models.alert import OutbreakAlert

router = APIRouter()

@router.get("/", response_model=List[OutbreakAlert])
async def get_alerts(status: str = "NEW"):
    """
    Get active alerts.
    """
    return await OutbreakAlert.find(OutbreakAlert.status == status).sort(-OutbreakAlert.timestamp).to_list()
