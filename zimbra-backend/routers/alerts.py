from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.alert import Alert
from schemas.alert import AlertOut, AlertStatusUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/seller/{seller_id}", response_model=List[AlertOut])
def get_alerts_by_seller(seller_id: int, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.seller_id == seller_id).all()
    if not alerts:
        raise HTTPException(status_code=404, detail="No alerts found for this seller")
    return alerts

@router.patch("/{alert_id}/status", response_model=AlertOut)
def update_alert_status(alert_id: int, data: AlertStatusUpdate, db: Session = Depends(get_db)):
    valid_statuses = ["pending", "in_management", "resolved", "escalated"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = data.status
    db.commit()
    db.refresh(alert)
    return alert
