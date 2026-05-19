from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Proposal(Base):
    __tablename__ = "sales_proposals"
    proposal_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    interaction_id = Column(Integer, ForeignKey("marketing_interactions.interaction_id"), nullable=True)
    num_users = Column(Integer, nullable=False)
    proposed_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    estimated_close_date = Column(Date, nullable=True)
    notes = Column(String(300))
