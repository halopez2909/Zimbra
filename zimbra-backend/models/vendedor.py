from sqlalchemy import Column, Integer, String
from database import Base

class Vendedor(Base):
    __tablename__ = "vendedores"
    id_vendedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100), unique=True)
    telefono = Column(String(30))
    activo = Column(Integer, default=1)
