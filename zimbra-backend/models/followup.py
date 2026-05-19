from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from database import Base

class FollowUp(Base):
    __tablename__ = "follow_ups"
    followup_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"), nullable=False)
    alert_id = Column(Integer, ForeignKey("sales_alerts.alert_id"), nullable=True)
    contact_type = Column(String(50), nullable=False)
    contact_date = Column(DateTime, default=func.now())
    result = Column(String(100))
    notes = Column(String(300))
    next_contact = Column(Date, nullable=True)
