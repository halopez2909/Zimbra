from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Seguimiento(Base):
    __tablename__ = "seguimientos"
    id_seguimiento = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_vendedor = Column(Integer, ForeignKey("vendedores.id_vendedor"), nullable=False)
    id_alerta = Column(Integer, ForeignKey("alertas_ventas.id_alerta"), nullable=True)
    tipo_contacto = Column(String(50), nullable=False)
    fecha_contacto = Column(DateTime, default=func.now())
    resultado = Column(String(100))
    observaciones = Column(String(300))
    proximo_contacto = Column(Date, nullable=True)
