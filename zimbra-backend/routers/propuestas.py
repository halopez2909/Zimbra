from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.propuesta import Propuesta
from models.venta import Venta
from schemas.propuesta import PropuestaCreate, PropuestaOut, PropuestaEstadoUpdate
from typing import List

router = APIRouter(prefix="/proposals", tags=["Proposals"])

@router.get("/", response_model=List[PropuestaOut])
def get_proposals(db: Session = Depends(get_db)):
    return db.query(Propuesta).all()

@router.get("/{id}", response_model=PropuestaOut)
def get_proposal(id: int, db: Session = Depends(get_db)):
    p = db.query(Propuesta).filter(Propuesta.id_propuesta == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return p

@router.post("/", response_model=PropuestaOut, status_code=201)
def create_proposal(data: PropuestaCreate, db: Session = Depends(get_db)):
    p = Propuesta(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.patch("/{id}/status", response_model=PropuestaOut)
def update_status(id: int, data: PropuestaEstadoUpdate, db: Session = Depends(get_db)):
    p = db.query(Propuesta).filter(Propuesta.id_propuesta == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # HU-08: si se acepta, verificar que no tenga venta ya creada
    if data.estado == "aceptada":
        venta_existente = db.query(Venta).filter(Venta.id_propuesta == id).first()
        if venta_existente:
            raise HTTPException(status_code=400, detail="This proposal already has a registered sale")

    p.estado = data.estado
    db.commit()
    db.refresh(p)
    return p
