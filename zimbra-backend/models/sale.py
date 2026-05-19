from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = (UniqueConstraint("proposal_id"),)
    sale_id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("sales_proposals.proposal_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    final_amount = Column(Numeric(12, 2), nullable=False)
    num_users = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=func.now())
    payment_method = Column(String(50))
    origin_channel = Column(String(50))
