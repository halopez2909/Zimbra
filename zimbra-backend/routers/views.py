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
