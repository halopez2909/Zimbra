from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaleCreate(BaseModel):
    proposal_id: int
    client_id: int
    product_id: int
    final_amount: float
    num_users: int
    payment_method: Optional[str] = None
    origin_channel: Optional[str] = None

class SaleOut(SaleCreate):
    sale_id: int
    sale_date: Optional[datetime] = None
    class Config:
        from_attributes = True
