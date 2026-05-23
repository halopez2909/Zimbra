from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from typing import Optional

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/performance")
def get_performance_report(start: str, end: str, db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM fn_performance_report(:p_start, :p_end)"),
        {"p_start": start, "p_end": end}
    ).fetchall()
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
