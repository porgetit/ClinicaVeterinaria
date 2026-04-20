from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_actual: Optional[float] = None
    color_caracteristicas: Optional[str] = None
    alergias: Optional[str] = None
    historial_medico: Optional[str] = None

class MascotaCreate(MascotaBase):
    id_cliente: int

class Mascota(MascotaBase):
    id_mascota: int
    id_cliente: int
    activo: int

    model_config = ConfigDict(from_attributes=True)
