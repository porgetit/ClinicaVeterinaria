from backend.app.repositories.base import BaseRepository
from backend.app.models.mascotas import Mascota

class MascotasRepository(BaseRepository[Mascota]):
    def __init__(self, db):
        super().__init__(Mascota, db)

    def get_by_cliente(self, cliente_id: int):
        return self.db.query(self.model).filter(self.model.id_cliente == cliente_id).all()
