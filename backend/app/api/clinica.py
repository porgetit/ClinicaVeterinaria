from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.schemas import clinica as schemas
from backend.app.repositories.clinica_repository import ConsultasRepository, TratamientosRepository
from backend.app.services.clinica_service import ClinicaService
from backend.app.api.auth import get_current_user

router = APIRouter(prefix="/clinica", tags=["clinica"])

def get_clinica_service(db: Session = Depends(get_db)):
    consulta_repo = ConsultasRepository(db)
    tratamiento_repo = TratamientosRepository(db)
    return ClinicaService(consulta_repo, tratamiento_repo)

@router.post("/consultas", response_model=schemas.Consulta)
def create_consulta(obj_in: schemas.ConsultaCreate, service: ClinicaService = Depends(get_clinica_service), current_user = Depends(get_current_user)):
    return service.registrar_consulta(obj_in.model_dump())

@router.get("/historial/{mascota_id}", response_model=List[schemas.Consulta])
def get_historial(mascota_id: int, service: ClinicaService = Depends(get_clinica_service), current_user = Depends(get_current_user)):
    return service.obtener_historial_mascota(mascota_id)

@router.post("/tratamientos", response_model=schemas.Tratamiento)
def add_tratamiento(obj_in: schemas.TratamientoCreate, service: ClinicaService = Depends(get_clinica_service), current_user = Depends(get_current_user)):
    return service.agregar_tratamiento(obj_in.id_consulta, obj_in.model_dump())
