from typing import List, Optional
from datetime import datetime, timedelta
from backend.app.models.facturas import Factura, DetalleFactura, Pago, PagoEfectivo, PagoTarjeta, PagoTransferencia
from backend.app.repositories.billing_repository import FacturasRepository, DetallesFacturaRepository, PagosRepository

class FacturacionService:
    def __init__(
        self, 
        factura_repo: FacturasRepository, 
        detalle_repo: DetallesFacturaRepository, 
        pago_repo: PagosRepository
    ):
        self.factura_repo = factura_repo
        self.detalle_repo = detalle_repo
        self.pago_repo = pago_repo

    def generar_factura(self, cliente_id: int, items: List[dict], notas: str = "") -> Factura:
        subtotal = sum(item['cantidad'] * item['precio_unitario'] for item in items)
        impuesto = subtotal * 0.15  # 15% taxa example
        total = subtotal + impuesto
        
        # Generate a simple factura number
        numero_factura = f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        factura = Factura(
            id_cliente=cliente_id,
            numero_factura=numero_factura,
            fecha_vencimiento=datetime.now() + timedelta(days=30),
            subtotal=subtotal,
            impuesto=impuesto,
            total=total,
            notas=notas
        )
        
        db_factura = self.factura_repo.create(factura)
        
        for item in items:
            detalle = DetalleFactura(
                id_factura=db_factura.id_factura,
                concepto=item.get('concepto'),
                descripcion=item.get('descripcion'),
                cantidad=item.get('cantidad', 1),
                precio_unitario=item.get('precio_unitario'),
                subtotal=item.get('cantidad', 1) * item.get('precio_unitario')
            )
            self.detalle_repo.create(detalle)
            
        return db_factura

    def procesar_pago(self, factura_id: int, tipo_pago: str, monto: float, data: dict) -> Pago:
        factura = self.factura_repo.get(factura_id)
        if not factura:
            raise ValueError("Factura no encontrada")

        if tipo_pago == "efectivo":
            pago = PagoEfectivo(
                id_factura=factura_id,
                monto=monto,
                billete_mayor=data.get('billete_mayor'),
                vuelto=data.get('vuelto'),
                numero_referencia=data.get('numero_referencia')
            )
        elif tipo_pago == "tarjeta":
            pago = PagoTarjeta(
                id_factura=factura_id,
                monto=monto,
                ultimo_digitos=data.get('ultimo_digitos'),
                nombre_titular=data.get('nombre_titular'),
                numero_referencia=data.get('numero_referencia')
            )
        elif tipo_pago == "transferencia":
            pago = PagoTransferencia(
                id_factura=factura_id,
                monto=monto,
                cuenta_origen=data.get('cuenta_origen'),
                cuenta_destino=data.get('cuenta_destino'),
                banco=data.get('banco'),
                concepto=data.get('concepto'),
                numero_referencia=data.get('numero_referencia')
            )
        else:
            raise ValueError("Tipo de pago no soportado")

        db_pago = self.pago_repo.create(pago)
        
        # Check if fully paid
        pagos_realizados = self.pago_repo.get_by_factura(factura_id)
        total_pagado = sum(p.monto for p in pagos_realizados)
        
        if total_pagado >= factura.total:
            factura.estado = "Pagada"
            self.factura_repo.db.commit()
            
        return db_pago
