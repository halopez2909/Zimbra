from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PropuestaCreate(BaseModel):
    id_cliente: int
    id_producto: int
    id_interaccion: Optional[int] = None
    num_usuarios: int
    monto_propuesto: float
    estado: str = "borrador"
    fecha_cierre_est: Optional[date] = None
    notas: Optional[str] = None

class PropuestaEstadoUpdate(BaseModel):
    estado: str

class PropuestaOut(PropuestaCreate):
    id_propuesta: int
    fecha_creacion: Optional[datetime] = None
    class Config:
        from_attributes = True
