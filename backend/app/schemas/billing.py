from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class DetalleFacturaBase(BaseModel):
    concepto: str
    descripcion: Optional[str] = None
    cantidad: int = 1
    precio_unitario: float
    subtotal: Optional[float] = None

class DetalleFactura(DetalleFacturaBase):
    id_detalle: int
    id_factura: int

    model_config = ConfigDict(from_attributes=True)

class FacturaBase(BaseModel):
    fecha_vencimiento: Optional[datetime] = None
    notas: Optional[str] = None

class FacturaCreate(FacturaBase):
    id_cliente: int
    items: List[DetalleFacturaBase]

class Factura(FacturaBase):
    id_factura: int
    id_cliente: int
    numero_factura: str
    fecha: datetime
    subtotal: float
    impuesto: float
    total: float
    estado: str
    detalles: List[DetalleFactura] = []

    model_config = ConfigDict(from_attributes=True)

class PagoBase(BaseModel):
    monto: float
    numero_referencia: Optional[str] = None

class PagoEfectivoCreate(PagoBase):
    billete_mayor: float
    vuelto: float

class PagoTarjetaCreate(PagoBase):
    ultimo_digitos: str
    nombre_titular: str

class PagoTransferenciaCreate(PagoBase):
    cuenta_origen: str
    cuenta_destino: str
    banco: str
    concepto: str

class Pago(PagoBase):
    id_pago: int
    id_factura: int
    tipo_pago: str
    fecha_procesamiento: datetime
    validado: int

    model_config = ConfigDict(from_attributes=True)
