from pydantic import BaseModel
from typing import Optional

class SellerCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None

class SellerOut(BaseModel):
    seller_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    active: int

    class Config:
        from_attributes = True
