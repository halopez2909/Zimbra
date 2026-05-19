from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Interaccion(Base):
    __tablename__ = "interacciones_marketing"
    id_interaccion = Column(Integer, primary_key=True, index=True)
    id_campana = Column(Integer, ForeignKey("campanas_marketing.id_campana"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    tipo_interaccion = Column(String(50), nullable=False)
    fecha_hora = Column(DateTime, default=func.now())
    puntuacion = Column(Integer, default=0)
    convertido = Column(Integer, default=0, nullable=False)
