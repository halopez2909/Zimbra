from sqlalchemy import Column, Integer, String, Date, Numeric
from database import Base

class Campaign(Base):
    __tablename__ = "marketing_campaigns"
    campaign_id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String(200))
    campaign_type = Column(String(50), nullable=False)
    objective = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    budget = Column(Numeric(12, 2))
    status = Column(String(50), nullable=False)
    tool = Column(String(100))
