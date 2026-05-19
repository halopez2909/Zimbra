from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sale import Sale
from models.proposal import Proposal
from models.client import Client
from schemas.sale import SaleCreate, SaleOut
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/", response_model=List[SaleOut])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()

@router.get("/{id}", response_model=SaleOut)
def get_sale(id: int, db: Session = Depends(get_db)):
    s = db.query(Sale).filter(Sale.sale_id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sale not found")
    return s

@router.post("/", response_model=SaleOut, status_code=201)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    proposal = db.query(Proposal).filter(Proposal.proposal_id == data.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status != "accepted":
        raise HTTPException(status_code=400, detail="Proposal must be accepted to register a sale")
    existing = db.query(Sale).filter(Sale.proposal_id == data.proposal_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="A sale already exists for this proposal")
    sale = Sale(**data.model_dump())
    db.add(sale)
    client = db.query(Client).filter(Client.client_id == data.client_id).first()
    if client:
        client.client_type = "commercial"
    db.commit()
    db.refresh(sale)
    return sale
