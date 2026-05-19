from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoOut
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductoOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/{id}", response_model=ProductoOut)
def get_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id_producto == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.post("/", response_model=ProductoOut, status_code=201)
def create_product(data: ProductoCreate, db: Session = Depends(get_db)):
    p = Producto(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{id}", response_model=ProductoOut)
def update_product(id: int, data: ProductoCreate, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id_producto == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in data.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id_producto == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
