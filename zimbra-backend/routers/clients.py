from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.client import Client
from schemas.client import ClientCreate, ClientOut, ClientStatusUpdate
from typing import List, Optional

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=List[ClientOut])
def get_clients(client_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Client)
    if client_type:
        query = query.filter(Client.client_type == client_type)
    return query.all()

@router.get("/{id}", response_model=ClientOut)
def get_client(id: int, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.client_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    return c

@router.post("/", response_model=ClientOut, status_code=201)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    c = Client(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/{id}", response_model=ClientOut)
def update_client(id: int, data: ClientCreate, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.client_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    for k, v in data.model_dump().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.patch("/{id}/status", response_model=ClientOut)
def update_client_type(id: int, data: ClientStatusUpdate, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.client_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    c.client_type = data.client_type
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.client_id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(c)
    db.commit()
