from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VentaCreate(BaseModel):
    id_propuesta: int
    id_cliente: int
    id_producto: int
    monto_final: float
    num_usuarios: int
    metodo_pago: Optional[str] = None
    canal_origen: Optional[str] = None

class VentaOut(VentaCreate):
    id_venta: int
    fecha_venta: Optional[datetime] = None
    class Config:
        from_attributes = True
