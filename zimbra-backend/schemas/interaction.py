from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InteractionCreate(BaseModel):
    campaign_id: int
    client_id: int
    interaction_type: str
    score: Optional[int] = 0

class InteractionOut(InteractionCreate):
    interaction_id: int
    converted: int
    interaction_date: Optional[datetime] = None
    class Config:
        from_attributes = True
