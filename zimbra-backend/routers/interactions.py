from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.interaction import Interaction
from schemas.interaction import InteractionCreate, InteractionOut
from typing import List

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.get("/", response_model=List[InteractionOut])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()

@router.get("/client/{client_id}", response_model=List[InteractionOut])
def get_by_client(client_id: int, db: Session = Depends(get_db)):
    return db.query(Interaction).filter(Interaction.client_id == client_id).all()

@router.post("/", response_model=InteractionOut, status_code=201)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    # alert and converted flag are now handled automatically by trg_auto_alert trigger
    interaction = Interaction(**data.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction
