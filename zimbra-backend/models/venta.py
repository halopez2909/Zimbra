from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

class Venta(Base):
    __tablename__ = "ventas"
    __table_args__ = (UniqueConstraint("id_propuesta"),)
    id_venta = Column(Integer, primary_key=True, index=True)
    id_propuesta = Column(Integer, ForeignKey("propuestas_ventas.id_propuesta"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    monto_final = Column(Numeric(12, 2), nullable=False)
    num_usuarios = Column(Integer, nullable=False)
    fecha_venta = Column(DateTime, default=func.now())
    metodo_pago = Column(String(50))
    canal_origen = Column(String(50))
