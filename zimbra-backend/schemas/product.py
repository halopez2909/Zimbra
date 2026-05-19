from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    product_name: str
    description: Optional[str] = None
    product_type: str
    base_price: float
    max_users: Optional[int] = None

class ProductOut(ProductCreate):
    product_id: int
    class Config:
        from_attributes = True
