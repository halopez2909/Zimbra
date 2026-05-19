from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.proposal import Proposal
from models.sale import Sale
from schemas.proposal import ProposalCreate, ProposalOut, ProposalStatusUpdate
from typing import List

router = APIRouter(prefix="/proposals", tags=["Proposals"])

@router.get("/", response_model=List[ProposalOut])
def get_proposals(db: Session = Depends(get_db)):
    return db.query(Proposal).all()

@router.get("/{id}", response_model=ProposalOut)
def get_proposal(id: int, db: Session = Depends(get_db)):
    p = db.query(Proposal).filter(Proposal.proposal_id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return p

@router.post("/", response_model=ProposalOut, status_code=201)
def create_proposal(data: ProposalCreate, db: Session = Depends(get_db)):
    p = Proposal(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.patch("/{id}/status", response_model=ProposalOut)
def update_status(id: int, data: ProposalStatusUpdate, db: Session = Depends(get_db)):
    p = db.query(Proposal).filter(Proposal.proposal_id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if data.status == "accepted":
        existing = db.query(Sale).filter(Sale.proposal_id == id).first()
        if existing:
            raise HTTPException(status_code=400, detail="This proposal already has a registered sale")
    p.status = data.status
    db.commit()
    db.refresh(p)
    return p
