from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Interaction(Base):
    __tablename__ = "marketing_interactions"
    interaction_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("marketing_campaigns.campaign_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    interaction_date = Column(DateTime, default=func.now())
    score = Column(Integer, default=0)
    converted = Column(Integer, default=0, nullable=False)
