from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150))
    description = Column(String(250))
    product_type = Column(String(50), nullable=False)
    base_price = Column(Numeric(12, 2), nullable=False)
    max_users = Column(Integer, nullable=True)
