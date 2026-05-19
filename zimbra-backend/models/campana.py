from sqlalchemy import Column, Integer, String, Date, Numeric
from database import Base

class Campana(Base):
    __tablename__ = "campanas_marketing"
    id_campana = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200))
    tipo = Column(String(50), nullable=False)
    objetivo = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    presupuesto = Column(Numeric(12, 2))
    estado = Column(String(50), nullable=False)
    herramienta = Column(String(100))
