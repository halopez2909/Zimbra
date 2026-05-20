from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
