from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertOut(BaseModel):
    alert_id: int
    interaction_id: int
    seller_id: int
    alert_date: Optional[datetime] = None
    alert_type: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class AlertStatusUpdate(BaseModel):
    status: str
