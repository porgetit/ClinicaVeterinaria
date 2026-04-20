from backend.app.repositories.base import BaseRepository
from backend.app.models.consultas import Consulta, Tratamiento
from backend.app.models.hospitalizaciones import Hospitalizacion

class ConsultasRepository(BaseRepository[Consulta]):
    def __init__(self, db):
        super().__init__(Consulta, db)

class TratamientosRepository(BaseRepository[Tratamiento]):
    def __init__(self, db):
        super().__init__(Tratamiento, db)

class HospitalizacionesRepository(BaseRepository[Hospitalizacion]):
    def __init__(self, db):
        super().__init__(Hospitalizacion, db)
