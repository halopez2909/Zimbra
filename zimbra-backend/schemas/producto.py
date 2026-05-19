from pydantic import BaseModel
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: str
    precio_base: float
    max_usuarios: Optional[int] = None

class ProductoOut(ProductoCreate):
    id_producto: int
    class Config:
        from_attributes = True
