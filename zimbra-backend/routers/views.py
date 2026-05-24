from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/views", tags=["Views"])

# HT-S4-09 (HU-06/07) - seller performance ranking from vw_seller_performance
@router.get("/sellers")
def seller_performance(db: Session = Depends(get_db)):
    rows = db.execute(text(
        "SELECT seller_id, full_name, total_alerts, attended_alerts, "
        "total_followups, attention_rate "
        "FROM vw_seller_performance "
        "ORDER BY attention_rate DESC, total_alerts DESC"
    )).fetchall()
    return [
        {
            "seller_id": row[0],
            "full_name": row[1],
            "total_alerts": row[2],
            "attended_alerts": row[3],
            "total_followups": row[4],
            "attention_rate": float(row[5]),
        }
        for row in rows
    ]

# HT-S4-09 (HU-06/07) - global pending alerts from vw_pending_alerts (oldest first)
@router.get("/pending-alerts")
def pending_alerts(db: Session = Depends(get_db)):
    rows = db.execute(text(
        "SELECT alert_id, interaction_id, seller_id, alert_date, alert_type, "
        "status, seller_name, client_name "
        "FROM vw_pending_alerts"
    )).fetchall()
    return [
        {
            "alert_id": row[0],
            "interaction_id": row[1],
            "seller_id": row[2],
            "alert_date": str(row[3]) if row[3] else None,
            "alert_type": row[4],
            "status": row[5],
            "seller_name": row[6],
            "client_name": row[7],
        }
        for row in rows
    ]
