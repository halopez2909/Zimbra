from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class FollowUpCreate(BaseModel):
    client_id: int
    seller_id: int
    alert_id: Optional[int] = None
    contact_type: str
    result: Optional[str] = None
    notes: Optional[str] = None
    next_contact: Optional[date] = None

class FollowUpOut(BaseModel):
    followup_id: int
    client_id: int
    seller_id: int
    alert_id: Optional[int] = None
    contact_type: str
    contact_date: Optional[datetime] = None
    result: Optional[str] = None
    notes: Optional[str] = None
    next_contact: Optional[date] = None

    class Config:
        from_attributes = True
