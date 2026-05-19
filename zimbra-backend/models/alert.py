from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Alert(Base):
    __tablename__ = "sales_alerts"
    alert_id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("marketing_interactions.interaction_id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"), nullable=False)
    alert_date = Column(DateTime, default=func.now())
    alert_type = Column(String(100))
    status = Column(String(50), nullable=False)
