from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.schemas import personas as schemas
from backend.app.models import personas as models
from backend.app.repositories.personas_repository import VeterinarioRepository, ClienteRepository, PersonaRepository
from backend.app.api.auth import get_current_user

router = APIRouter(prefix="/personas", tags=["personas"])

@router.get("/veterinarios", response_model=List[schemas.Veterinario])
def list_veterinarios(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repo = VeterinarioRepository(db)
    return repo.get_all()

@router.post("/veterinarios", response_model=schemas.Veterinario)
def create_veterinario(obj_in: schemas.VeterinarioCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repo = VeterinarioRepository(db)
    # Map SchemaCreate to SQLAlchemy Model
    db_obj = models.Veterinario(**obj_in.model_dump())
    return repo.create(db_obj)

@router.get("/clientes", response_model=List[schemas.Cliente])
def list_clientes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repo = ClienteRepository(db)
    return repo.get_all()

@router.post("/clientes", response_model=schemas.Cliente)
def create_cliente(obj_in: schemas.ClienteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repo = ClienteRepository(db)
    # Map SchemaCreate to SQLAlchemy Model
    db_obj = models.Cliente(**obj_in.model_dump())
    return repo.create(db_obj)

@router.get("/{id}", response_model=schemas.Persona)
def get_persona(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repo = PersonaRepository(db)
    persona = repo.get(id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona non encontrada")
    return persona
