from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.interaction import Interaction
from models.alert import Alert
from models.client import Client
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
    interaction = Interaction(**data.model_dump())
    if interaction.score >= 80:
        interaction.converted = 1
    db.add(interaction)
    db.flush()
    if interaction.converted == 1:
        client = db.query(Client).filter(Client.client_id == data.client_id).first()
        if client and client.assigned_seller_id:
            alert = Alert(
                interaction_id=interaction.interaction_id,
                seller_id=client.assigned_seller_id,
                alert_type="high_lead_score",
                status="pending"
            )
            db.add(alert)
    db.commit()
    db.refresh(interaction)
    return interaction
