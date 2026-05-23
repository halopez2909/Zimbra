from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from database import get_db
from models.seller import Seller
from schemas.seller import SellerCreate, SellerOut

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.post("/", response_model=SellerOut, status_code=201)
def create_seller(data: SellerCreate, db: Session = Depends(get_db)):
    if db.query(Seller).filter(Seller.email == data.email).first():
        raise HTTPException(status_code=400, detail="correo ya registrado")
    seller = Seller(full_name=data.full_name, email=data.email, phone=data.phone, active=1)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller

@router.get("/", response_model=List[SellerOut])
def get_sellers(only_active: bool = True, db: Session = Depends(get_db)):
    q = db.query(Seller)
    if only_active:
        q = q.filter(Seller.active == 1)
    return q.all()

# HT-S3-12 (HU-01) - seller management report via fn_seller_report()
@router.get("/{seller_id}/report")
def get_seller_report(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    row = db.execute(
        text("SELECT * FROM fn_seller_report(:seller_id)"),
        {"seller_id": seller_id}
    ).fetchone()
    return {
        "seller_id": seller_id,
        "full_name": seller.full_name,
        "total_alerts": row[0],
        "attended_alerts": row[1],
        "total_followups": row[2],
        "managed_clients": row[3],
        "attention_rate": float(row[4]),
    }

# HT-S3-11b (HU-06) - alert response rate via fn_alert_response_rate()
@router.get("/{seller_id}/alert-rate")
def get_alert_rate(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    rate = db.execute(
        text("SELECT fn_alert_response_rate(:seller_id)"),
        {"seller_id": seller_id}
    ).scalar()
    return {"seller_id": seller_id, "alert_response_rate": float(rate or 0)}

# HT-S3-12b (HU-07) - follow-up summary via fn_followup_summary()
@router.get("/{seller_id}/followup-summary")
def get_followup_summary(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    row = db.execute(
        text("SELECT * FROM fn_followup_summary(:seller_id)"),
        {"seller_id": seller_id}
    ).fetchone()
    return {
        "seller_id": seller_id,
        "total_followups": row[0],
        "pending_contacts": row[1],
        "most_used_contact_type": row[2],
        "most_common_result": row[3],
    }

@router.get("/{seller_id}", response_model=SellerOut)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller

@router.patch("/{seller_id}/deactivate", response_model=SellerOut)
def deactivate_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    seller.active = 0
    db.commit()
    db.refresh(seller)
    return seller
