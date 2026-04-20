from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class Consulta(Base):
    __tablename__ = 'consultas'
    
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_veterinario = Column(Integer, ForeignKey('veterinarios.id_veterinario'), index=True)
    id_mascota = Column(Integer, ForeignKey('mascotas.id_mascota'), index=True)
    fecha = Column(Date, index=True)
    hora = Column(String)
    motivo = Column(String)
    diagnostico = Column(Text)
    notas = Column(Text)
    estado = Column(String, default="Programada")  # Programada, En Proceso, Completada, Cancelada
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relationships
    veterinario = relationship("Veterinario", back_populates="consultas")
    mascota = relationship("Mascota", back_populates="consultas")
    tratamientos = relationship("Tratamiento", back_populates="consulta", cascade="all, delete-orphan")

class Tratamiento(Base):
    __tablename__ = 'tratamientos'
    
    id_tratamiento = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey('consultas.id_consulta', ondelete="CASCADE"))
    tipo = Column(String)  # Medicamento, Terapia, Cirugía, etc.
    descripcion = Column(Text)
    medicamentos = Column(Text)
    duracion_dias = Column(Integer)
    costo = Column(Float)
    estado = Column(String, default="Pendiente")
    fecha_inicio = Column(Date)
    fecha_fin_estimada = Column(Date)
    notas = Column(Text)

    # Relationships
    consulta = relationship("Consulta", back_populates="tratamientos")
