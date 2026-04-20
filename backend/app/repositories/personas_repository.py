from backend.app.repositories.base import BaseRepository
from backend.app.models.personas import Persona, Veterinario, Recepcionista, Cliente

class PersonaRepository(BaseRepository[Persona]):
    def __init__(self, db):
        super().__init__(Persona, db)

class VeterinarioRepository(BaseRepository[Veterinario]):
    def __init__(self, db):
        super().__init__(Veterinario, db)

class ClienteRepository(BaseRepository[Cliente]):
    def __init__(self, db):
        super().__init__(Cliente, db)
