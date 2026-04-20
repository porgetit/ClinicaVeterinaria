from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class Factura(Base):
    __tablename__ = 'facturas'
    
    id_factura = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), index=True)
    numero_factura = Column(String, unique=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime)
    subtotal = Column(Float)
    impuesto = Column(Float)
    total = Column(Float)
    estado = Column(String, default="Pendiente")  # Pendiente, Pagada, Cancelada
    notas = Column(Text)

    # Relationships
    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="factura", cascade="all, delete-orphan")

class DetalleFactura(Base):
    __tablename__ = 'detalles_factura'
    
    id_detalle = Column(Integer, primary_key=True, index=True)
    id_factura = Column(Integer, ForeignKey('facturas.id_factura', ondelete="CASCADE"))
    concepto = Column(String)
    id_concepto = Column(Integer, nullable=True) # ID of the service (consult, treatment, etc)
    descripcion = Column(String)
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Float)
    subtotal = Column(Float)

    # Relationships
    factura = relationship("Factura", back_populates="detalles")

class Pago(Base):
    __tablename__ = 'pagos'
    
    id_pago = Column(Integer, primary_key=True, index=True)
    id_factura = Column(Integer, ForeignKey('facturas.id_factura', ondelete="CASCADE"))
    monto = Column(Float, nullable=False)
    tipo_pago = Column(String)  # Discriminator
    numero_referencia = Column(String, index=True)
    fecha_procesamiento = Column(DateTime, default=datetime.utcnow)
    validado = Column(Integer, default=1)

    __mapper_args__ = {
        'polymorphic_identity': 'pago',
        'polymorphic_on': tipo_pago
    }

    # Relationships
    factura = relationship("Factura", back_populates="pagos")

class PagoEfectivo(Pago):
    __tablename__ = 'pagos_efectivo'
    id_pago_efectivo = Column(Integer, primary_key=True, index=True)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago', ondelete="CASCADE"))
    billete_mayor = Column(Float)
    vuelto = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'efectivo',
    }

class PagoTarjeta(Pago):
    __tablename__ = 'pagos_tarjeta'
    id_pago_tarjeta = Column(Integer, primary_key=True, index=True)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago', ondelete="CASCADE"))
    ultimo_digitos = Column(String(4))
    nombre_titular = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'tarjeta',
    }

class PagoTransferencia(Pago):
    __tablename__ = 'pagos_transferencia'
    id_pago_transferencia = Column(Integer, primary_key=True, index=True)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago', ondelete="CASCADE"))
    cuenta_origen = Column(String)
    cuenta_destino = Column(String)
    banco = Column(String)
    concepto = Column(String)
    confirmado = Column(Integer, default=0)
    fecha_confirmacion = Column(DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'transferencia',
    }
