from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.interaccion import Interaccion
from models.alerta import Alerta
from schemas.interaccion import InteraccionCreate, InteraccionOut
from typing import List

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.get("/", response_model=List[InteraccionOut])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaccion).all()

@router.get("/client/{id_cliente}", response_model=List[InteraccionOut])
def get_by_client(id_cliente: int, db: Session = Depends(get_db)):
    return db.query(Interaccion).filter(Interaccion.id_cliente == id_cliente).all()

@router.post("/", response_model=InteraccionOut, status_code=201)
def create_interaction(data: InteraccionCreate, db: Session = Depends(get_db)):
    interaccion = Interaccion(**data.model_dump())

    # HU-05: si puntuacion >= 80 marcar convertido = 1 y generar alerta
    if interaccion.puntuacion >= 80:
        interaccion.convertido = 1

    db.add(interaccion)
    db.flush()

    if interaccion.convertido == 1:
        # buscar vendedor asignado al cliente
        from models.cliente import Cliente
        cliente = db.query(Cliente).filter(Cliente.id_cliente == data.id_cliente).first()
        if cliente and cliente.id_vendedor_asignado:
            alerta = Alerta(
                id_interaccion=interaccion.id_interaccion,
                id_vendedor=cliente.id_vendedor_asignado,
                tipo_alerta="lead_scoring_alto",
                estado="pendiente"
            )
            db.add(alerta)

    db.commit()
    db.refresh(interaccion)
    return interaccion
