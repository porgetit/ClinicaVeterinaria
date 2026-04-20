from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class Persona(Base):
    __tablename__ = 'personas'
    
    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False, index=True)
    tipo = Column(String)  # Discriminator for polymorphism
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'persona',
        'polymorphic_on': tipo
    }

class Veterinario(Persona):
    __tablename__ = 'veterinarios'
    
    id_veterinario = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona', ondelete="CASCADE"), unique=True)
    licencia = Column(String, unique=True, index=True)
    especialidad = Column(String)
    estado = Column(String, default="Activo")  # Activo, Inactivo, Licencia
    fecha_contratacion = Column(DateTime, default=datetime.utcnow)

    # Relationships
    consultas = relationship("Consulta", back_populates="veterinario")
    hospitalizaciones = relationship("Hospitalizacion", back_populates="veterinario_supervisor")

    __mapper_args__ = {
        'polymorphic_identity': 'veterinario',
    }

class Recepcionista(Persona):
    __tablename__ = 'recepcionistas'
    
    id_recepcionista = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona', ondelete="CASCADE"), unique=True)
    turno = Column(String)  # Mañana, Tarde, Noche
    estado = Column(String, default="Activo")
    fecha_contratacion = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'recepcionista',
    }

class Cliente(Persona):
    __tablename__ = 'clientes'
    
    id_cliente = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona', ondelete="CASCADE"), unique=True)
    telefono = Column(String)
    email = Column(String, index=True)
    direccion = Column(String)
    ciudad = Column(String)
    codigo_postal = Column(String)
    activo = Column(Integer, default=1)  # 1 for True, 0 for False

    # Relationships
    mascotas = relationship("Mascota", back_populates="cliente")
    facturas = relationship("Factura", back_populates="cliente")

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }
