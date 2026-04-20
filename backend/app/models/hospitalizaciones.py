from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Hospitalizacion(Base):
    __tablename__ = 'hospitalizaciones'
    
    id_hospitalizacion = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey('mascotas.id_mascota'), index=True)
    id_veterinario_supervisor = Column(Integer, ForeignKey('veterinarios.id_veterinario'))
    fecha_ingreso = Column(DateTime, index=True)
    fecha_salida = Column(DateTime, nullable=True)
    razon = Column(String)
    costo_diario = Column(Float)
    diagnostico = Column(Text)
    tratamiento_durante_hospitalizacion = Column(Text)
    alta_medica = Column(Integer, default=0)
    estado = Column(String, default="Activa")  # Activa, Alta, Cancelada

    # Relationships
    mascota = relationship("Mascota", back_populates="hospitalizaciones")
    veterinario_supervisor = relationship("Veterinario", back_populates="hospitalizaciones")
