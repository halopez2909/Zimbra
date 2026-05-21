from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductOut
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{id}/calculate")
def calculate_amount(id: int, num_users: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT fn_calculate_proposal_amount(:product_id, :num_users)"),
        {"product_id": id, "num_users": num_users}
    ).scalar()
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": id, "num_users": num_users, "calculated_amount": float(result)}

@router.get("/{id}", response_model=ProductOut)
def get_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.product_id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    p = Product(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{id}", response_model=ProductOut)
def update_product(id: int, data: ProductCreate, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.product_id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in data.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.product_id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
