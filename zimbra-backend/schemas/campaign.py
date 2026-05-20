from pydantic import BaseModel
from typing import Optional
from datetime import date

class CampaignCreate(BaseModel):
    campaign_name: str
    campaign_type: str
    objective: str
    start_date: date
    end_date: Optional[date] = None
    budget: Optional[float] = 0.0
    status: str = "planned"
    tool: Optional[str] = "OneView"

class CampaignStatusUpdate(BaseModel):
    status: str

class CampaignOut(CampaignCreate):
    campaign_id: int
    class Config:
        from_attributes = True
