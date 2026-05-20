from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientCreate(BaseModel):
    full_name: str
    company: Optional[str] = None
    email: str
    phone: Optional[str] = None
    client_type: str
    assigned_seller_id: Optional[int] = None

class ClientStatusUpdate(BaseModel):
    client_type: str

class ClientOut(ClientCreate):
    client_id: int
    registration_date: Optional[datetime] = None
    class Config:
        from_attributes = True
