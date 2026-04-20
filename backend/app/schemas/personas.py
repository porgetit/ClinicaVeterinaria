from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class PersonaBase(BaseModel):
    nombre: str
    documento: str

class PersonaCreate(PersonaBase):
    pass

class Persona(PersonaBase):
    id_persona: int
    tipo: str
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)

class VeterinarioBase(BaseModel):
    licencia: str
    especialidad: Optional[str] = None
    estado: Optional[str] = "Activo"

class VeterinarioCreate(PersonaCreate, VeterinarioBase):
    pass

class Veterinario(Persona, VeterinarioBase):
    id_veterinario: int
    id_persona: int
    fecha_contratacion: datetime

    model_config = ConfigDict(from_attributes=True)

class ClienteBase(BaseModel):
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None

class ClienteCreate(PersonaCreate, ClienteBase):
    pass

class Cliente(Persona, ClienteBase):
    id_cliente: int
    id_persona: int
    activo: int

    model_config = ConfigDict(from_attributes=True)
