from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/views", tags=["Views"])

@router.get("/pipeline")
def get_pipeline_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_sales_pipeline")).fetchall()
    return [
        {
            "status": row[0],
            "total_proposals": row[1],
            "total_amount": float(row[2]),
            "percentage": float(row[3])
        }
        for row in rows
    ]

@router.get("/traceability")
def get_traceability_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_sales_traceability")).fetchall()
    return [
        {
            "sale_id": row[0],
            "sale_date": str(row[1]),
            "client_name": row[2],
            "client_type": row[3],
            "product_name": row[4],
            "proposed_amount": float(row[5]),
            "final_amount": float(row[6]),
            "payment_method": row[7],
            "origin_channel": row[8],
            "origin_campaign": row[9],
            "campaign_type": row[10],
            "seller_name": row[11]
        }
        for row in rows
    ]

@router.get("/performance")
def get_performance_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_performance_summary")).fetchall()
    return [
        {
            "period_start": str(row[0]),
            "period_end": str(row[1]),
            "total_visitors": row[2],
            "total_downloads": row[3],
            "total_prospects": row[4],
            "total_proposals": row[5],
            "total_sales": row[6],
            "total_revenue": float(row[7]),
            "conversion_rate_pct": float(row[8]),
            "close_rate_pct": float(row[9])
        }
        for row in rows
    ]

@router.get("/campaigns")
def get_campaigns_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_campaign_effectiveness")).fetchall()
    return [
        {
            "campaign_id": row[0],
            "campaign_name": row[1],
            "campaign_type": row[2],
            "status": row[3],
            "budget": float(row[4]) if row[4] else 0,
            "total_interactions": row[5],
            "total_converted": row[6],
            "conversion_rate": float(row[7]) if row[7] else 0,
            "cost_per_conversion": float(row[8]) if row[8] else 0
        }
        for row in rows
    ]
