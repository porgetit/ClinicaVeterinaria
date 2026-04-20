from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Mascota(Base):
    __tablename__ = 'mascotas'
    
    id_mascota = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), index=True)
    nombre = Column(String, index=True, nullable=False)
    especie = Column(String, nullable=False)  # Perro, Gato, etc.
    raza = Column(String)
    fecha_nacimiento = Column(Date)
    peso_actual = Column(Float)
    color_caracteristicas = Column(String)
    alergias = Column(String)
    historial_medico = Column(String)
    activo = Column(Integer, default=1)

    # Relationships
    cliente = relationship("Cliente", back_populates="mascotas")
    consultas = relationship("Consulta", back_populates="mascota")
    hospitalizaciones = relationship("Hospitalizacion", back_populates="mascota")
