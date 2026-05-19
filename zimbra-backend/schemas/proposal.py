from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ProposalCreate(BaseModel):
    client_id: int
    product_id: int
    interaction_id: Optional[int] = None
    num_users: int
    proposed_amount: float
    status: str = "draft"
    estimated_close_date: Optional[date] = None
    notes: Optional[str] = None

class ProposalStatusUpdate(BaseModel):
    status: str

class ProposalOut(ProposalCreate):
    proposal_id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
