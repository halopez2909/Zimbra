from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.venta import Venta
from models.propuesta import Propuesta
from schemas.venta import VentaCreate, VentaOut
from models.cliente import Cliente
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/", response_model=List[VentaOut])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Venta).all()

@router.get("/{id}", response_model=VentaOut)
def get_sale(id: int, db: Session = Depends(get_db)):
    v = db.query(Venta).filter(Venta.id_venta == id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Sale not found")
    return v

@router.post("/", response_model=VentaOut, status_code=201)
def create_sale(data: VentaCreate, db: Session = Depends(get_db)):
    # HU-09: verificar que la propuesta existe y esta aceptada
    propuesta = db.query(Propuesta).filter(Propuesta.id_propuesta == data.id_propuesta).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if propuesta.estado != "aceptada":
        raise HTTPException(status_code=400, detail="Proposal must be in 'aceptada' status to register a sale")

    # HU-09: verificar unicidad - una propuesta solo genera una venta
    existente = db.query(Venta).filter(Venta.id_propuesta == data.id_propuesta).first()
    if existente:
        raise HTTPException(status_code=400, detail="A sale already exists for this proposal")

    venta = Venta(**data.model_dump())
    db.add(venta)

    # HU-02: actualizar tipo_cliente a comercial al cerrar venta
    cliente = db.query(Cliente).filter(Cliente.id_cliente == data.id_cliente).first()
    if cliente:
        cliente.tipo_cliente = "comercial"

    db.commit()
    db.refresh(venta)
    return venta
