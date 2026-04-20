from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date

class TratamientoBase(BaseModel):
    tipo: str
    descripcion: Optional[str] = None
    medicamentos: Optional[str] = None
    duracion_dias: Optional[int] = None
    costo: Optional[float] = 0.0
    estado: Optional[str] = "Pendiente"
    fecha_inicio: Optional[date] = None
    fecha_fin_estimada: Optional[date] = None
    notas: Optional[str] = None

class TratamientoCreate(TratamientoBase):
    id_consulta: int

class Tratamiento(TratamientoBase):
    id_tratamiento: int
    id_consulta: int

    model_config = ConfigDict(from_attributes=True)

class ConsultaBase(BaseModel):
    fecha: date
    hora: str
    motivo: str
    diagnostico: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[str] = "Programada"

class ConsultaCreate(ConsultaBase):
    id_veterinario: int
    id_mascota: int

class Consulta(ConsultaBase):
    id_consulta: int
    id_veterinario: int
    id_mascota: int
    fecha_registro: datetime
    tratamientos: List[Tratamiento] = []

    model_config = ConfigDict(from_attributes=True)

class HospitalizacionBase(BaseModel):
    id_mascota: int
    id_veterinario_supervisor: int
    fecha_ingreso: datetime
    razon: str
    costo_diario: float
    diagnostico: Optional[str] = None
    tratamiento_durante_hospitalizacion: Optional[str] = None

class HospitalizacionCreate(HospitalizacionBase):
    pass

class Hospitalizacion(HospitalizacionBase):
    id_hospitalizacion: int
    fecha_salida: Optional[datetime] = None
    alta_medica: int
    estado: str

    model_config = ConfigDict(from_attributes=True)
