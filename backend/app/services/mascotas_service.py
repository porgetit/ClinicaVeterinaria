from datetime import datetime
from typing import List, Optional
from backend.app.repositories.mascotas_repository import MascotasRepository
from backend.app.models.mascotas import Mascota

class MascotasService:
    def __init__(self, repository: MascotasRepository):
        self.repository = repository

    def registrar_mascota(self, data: dict) -> Mascota:
        # Business logic: validate age or something if needed
        # For now, simple creation
        mascota = Mascota(**data)
        return self.repository.create(mascota)

    def obtener_mascotas_cliente(self, cliente_id: int) -> List[Mascota]:
        return self.repository.get_by_cliente(cliente_id)

    def obtener_detalle_mascota(self, mascota_id: int) -> Optional[Mascota]:
        return self.repository.get(mascota_id)
