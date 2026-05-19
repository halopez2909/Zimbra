from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150))
    descripcion = Column(String(250))
    tipo = Column(String(50), nullable=False)
    precio_base = Column(Numeric(12, 2), nullable=False)
    max_usuarios = Column(Integer, nullable=True)
