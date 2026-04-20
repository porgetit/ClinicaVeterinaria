from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from backend.app.core.database import get_db
from backend.app.schemas import billing as schemas
from backend.app.repositories.billing_repository import FacturasRepository, DetallesFacturaRepository, PagosRepository
from backend.app.services.facturacion_service import FacturacionService
from backend.app.api.auth import get_current_user

router = APIRouter(prefix="/facturacion", tags=["facturacion"])

def get_billing_service(db: Session = Depends(get_db)):
    factura_repo = FacturasRepository(db)
    detalle_repo = DetallesFacturaRepository(db)
    pago_repo = PagosRepository(db)
    return FacturacionService(factura_repo, detalle_repo, pago_repo)

@router.post("/facturas", response_model=schemas.Factura)
def create_factura(obj_in: schemas.FacturaCreate, service: FacturacionService = Depends(get_billing_service), current_user = Depends(get_current_user)):
    return service.generar_factura(obj_in.id_cliente, [item.model_dump() for item in obj_in.items], obj_in.notas)

@router.get("/facturas/cliente/{cliente_id}", response_model=List[schemas.Factura])
def get_facturas_cliente(cliente_id: int, service: FacturacionService = Depends(get_billing_service), current_user = Depends(get_current_user)):
    return service.factura_repo.get_by_cliente(cliente_id)

@router.post("/pagos/{factura_id}", response_model=schemas.Pago)
def process_pago(factura_id: int, tipo_pago: str, monto: float, data: dict, service: FacturacionService = Depends(get_billing_service), current_user = Depends(get_current_user)):
    try:
        return service.procesar_pago(factura_id, tipo_pago, monto, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
