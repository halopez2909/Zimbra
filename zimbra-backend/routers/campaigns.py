from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.campaign import Campaign
from models.interaction import Interaction
from schemas.campaign import CampaignCreate, CampaignOut, CampaignStatusUpdate
from typing import List, Optional

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/", response_model=List[CampaignOut])
def get_campaigns(status: Optional[str] = None, objective: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Campaign)
    if status:
        query = query.filter(Campaign.status == status)
    if objective:
        query = query.filter(Campaign.objective == objective)
    return query.all()

@router.get("/{id}", response_model=CampaignOut)
def get_campaign(id: int, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.campaign_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return c

@router.post("/", response_model=CampaignOut, status_code=201)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db)):
    if data.end_date and data.end_date < data.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")
    if data.budget and data.budget < 0:
        raise HTTPException(status_code=400, detail="budget must be >= 0")
    c = Campaign(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/{id}", response_model=CampaignOut)
def update_campaign(id: int, data: CampaignCreate, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.campaign_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for k, v in data.model_dump().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.patch("/{id}/status", response_model=CampaignOut)
def update_campaign_status(id: int, data: CampaignStatusUpdate, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.campaign_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    valid_statuses = ["planned", "active", "finished", "cancelled"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    c.status = data.status
    db.commit()
    db.refresh(c)
    return c

@router.get("/{id}/interactions")
def get_campaign_interactions(id: int, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.campaign_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    interactions = db.query(Interaction).filter(Interaction.campaign_id == id).all()
    return {
        "campaign_id": id,
        "campaign_name": c.campaign_name,
        "total_interactions": len(interactions),
        "converted": sum(1 for i in interactions if i.converted == 1),
        "interactions": interactions
    }

@router.delete("/{id}", status_code=204)
def delete_campaign(id: int, db: Session = Depends(get_db)):
    c = db.query(Campaign).filter(Campaign.campaign_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(c)
    db.commit()
