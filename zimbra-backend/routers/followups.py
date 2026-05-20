from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.followup import FollowUp
from schemas.followup import FollowUpCreate, FollowUpOut

router = APIRouter(prefix="/followups", tags=["Follow-ups"])

@router.post("/", response_model=FollowUpOut, status_code=201)
def create_followup(data: FollowUpCreate, db: Session = Depends(get_db)):
    valid_types = ["call", "email", "visit"]
    if data.contact_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"contact_type must be one of: {valid_types}")
    followup = FollowUp(**data.model_dump())
    db.add(followup)
    db.commit()
    db.refresh(followup)
    return followup

@router.get("/client/{client_id}", response_model=List[FollowUpOut])
def get_followups_by_client(client_id: int, db: Session = Depends(get_db)):
    followups = (
        db.query(FollowUp)
        .filter(FollowUp.client_id == client_id)
        .order_by(FollowUp.contact_date.desc())
        .limit(5)
        .all()
    )
    if not followups:
        raise HTTPException(status_code=404, detail="No follow-ups found for this client")
    return followups
