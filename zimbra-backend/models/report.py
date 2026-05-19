from sqlalchemy import Column, Integer, Date, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class PerformanceReport(Base):
    __tablename__ = "performance_reports"
    report_id = Column(Integer, primary_key=True, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_visitors = Column(Integer, default=0)
    total_downloads = Column(Integer, default=0)
    total_prospects = Column(Integer, default=0)
    total_proposals = Column(Integer, default=0)
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Numeric(14, 2), default=0)
    conversion_rate_pct = Column(Numeric(5, 2), default=0)
    close_rate_pct = Column(Numeric(5, 2), default=0)
    generated_at = Column(DateTime, default=func.now())
