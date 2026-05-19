from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InteraccionCreate(BaseModel):
    id_campana: int
    id_cliente: int
    tipo_interaccion: str
    puntuacion: Optional[int] = 0

class InteraccionOut(InteraccionCreate):
    id_interaccion: int
    convertido: int
    fecha_hora: Optional[datetime] = None
    class Config:
        from_attributes = True
