from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    empresa = Column(String(150))
    correo = Column(String(100), unique=True)
    telefono = Column(String(30))
    tipo_cliente = Column(String(50), nullable=False)
    id_vendedor_asignado = Column(Integer, ForeignKey("vendedores.id_vendedor"))
    fecha_registro = Column(DateTime, default=func.now())
