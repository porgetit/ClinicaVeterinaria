from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.schemas import mascotas as schemas
from backend.app.repositories.mascotas_repository import MascotasRepository
from backend.app.services.mascotas_service import MascotasService
from backend.app.api.auth import get_current_user

router = APIRouter(prefix="/mascotas", tags=["mascotas"])

def get_mascotas_service(db: Session = Depends(get_db)):
    repo = MascotasRepository(db)
    return MascotasService(repo)

@router.get("/", response_model=List[schemas.Mascota])
def list_mascotas(service: MascotasService = Depends(get_mascotas_service), current_user = Depends(get_current_user)):
    return service.repository.get_all()

@router.post("/", response_model=schemas.Mascota)
def create_mascota(obj_in: schemas.MascotaCreate, service: MascotasService = Depends(get_mascotas_service), current_user = Depends(get_current_user)):
    return service.registrar_mascota(obj_in.model_dump())

@router.get("/cliente/{cliente_id}", response_model=List[schemas.Mascota])
def get_by_cliente(cliente_id: int, service: MascotasService = Depends(get_mascotas_service), current_user = Depends(get_current_user)):
    return service.obtener_mascotas_cliente(cliente_id)

@router.get("/{id}", response_model=schemas.Mascota)
def get_mascota(id: int, service: MascotasService = Depends(get_mascotas_service), current_user = Depends(get_current_user)):
    mascota = service.obtener_detalle_mascota(id)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota
