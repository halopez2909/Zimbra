from sqlalchemy import Column, Integer, String
from database import Base

class Seller(Base):
    __tablename__ = "sellers"
    seller_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(30))
    active = Column(Integer, default=1)
