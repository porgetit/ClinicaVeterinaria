from typing import List, Optional
from datetime import datetime, date
from backend.app.models.consultas import Consulta, Tratamiento
from backend.app.repositories.base import BaseRepository

class ClinicaService:
    def __init__(self, consulta_repo: BaseRepository[Consulta], tratamiento_repo: BaseRepository[Tratamiento]):
        self.consulta_repo = consulta_repo
        self.tratamiento_repo = tratamiento_repo

    def registrar_consulta(self, data: dict) -> Consulta:
        consulta = Consulta(**data)
        return self.consulta_repo.create(consulta)

    def agregar_tratamiento(self, consulta_id: int, data: dict) -> Tratamiento:
        data['id_consulta'] = consulta_id
        tratamiento = Tratamiento(**data)
        return self.tratamiento_repo.create(tratamiento)

    def obtener_historial_mascota(self, mascota_id: int) -> List[Consulta]:
        # Filter consultas by mascota_id
        return self.consulta_repo.db.query(Consulta).filter(Consulta.id_mascota == mascota_id).all()
