from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    company = Column(String(150))
    email = Column(String(100), unique=True)
    phone = Column(String(30))
    client_type = Column(String(50), nullable=False)
    assigned_seller_id = Column(Integer, ForeignKey("sellers.seller_id"))
    registration_date = Column(DateTime, default=func.now())
