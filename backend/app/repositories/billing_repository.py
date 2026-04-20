from backend.app.repositories.base import BaseRepository
from backend.app.models.facturas import Factura, DetalleFactura, Pago

class FacturasRepository(BaseRepository[Factura]):
    def __init__(self, db):
        super().__init__(Factura, db)

    def get_by_cliente(self, cliente_id: int):
        return self.db.query(self.model).filter(self.model.id_cliente == cliente_id).all()

class DetallesFacturaRepository(BaseRepository[DetalleFactura]):
    def __init__(self, db):
        super().__init__(DetalleFactura, db)

class PagosRepository(BaseRepository[Pago]):
    def __init__(self, db):
        super().__init__(Pago, db)
        
    def get_by_factura(self, factura_id: int):
        return self.db.query(self.model).filter(self.model.id_factura == factura_id).all()
