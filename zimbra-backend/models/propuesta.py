from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Propuesta(Base):
    __tablename__ = "propuestas_ventas"
    id_propuesta = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_interaccion = Column(Integer, ForeignKey("interacciones_marketing.id_interaccion"), nullable=True)
    num_usuarios = Column(Integer, nullable=False)
    monto_propuesto = Column(Numeric(12, 2), nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_cierre_est = Column(Date, nullable=True)
    notas = Column(String(300))
