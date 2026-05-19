from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Alerta(Base):
    __tablename__ = "alertas_ventas"
    id_alerta = Column(Integer, primary_key=True, index=True)
    id_interaccion = Column(Integer, ForeignKey("interacciones_marketing.id_interaccion"), nullable=False)
    id_vendedor = Column(Integer, ForeignKey("vendedores.id_vendedor"), nullable=False)
    fecha_alerta = Column(DateTime, default=func.now())
    tipo_alerta = Column(String(100))
    estado = Column(String(50), nullable=False)
