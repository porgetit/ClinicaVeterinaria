# Modelo de Datos y Arquitectura - Clínica Veterinaria

## 📋 Índice

1. [Modelo de Datos Relacional](#modelo-de-datos-relacional)
2. [Descripción de Tablas](#descripción-de-tablas)
3. [Relaciones y Cardinalidades](#relaciones-y-cardinalidades)
4. [Vistas SQL Útiles](#vistas-sql-útiles)
5. [Arquitectura de Componentes](#arquitectura-de-componentes)
6. [Consideraciones para Implementación en Python](#consideraciones-para-implementación-en-python)

---

## Modelo de Datos Relacional

### Diagrama Conceptual

```
PERSONAS (Tabla Base Abstracta)
├── VETERINARIOS (Herencia)
├── RECEPCIONISTAS (Herencia)
└── CLIENTES (Herencia)
    └── MASCOTAS (Agregación)
        ├── CONSULTAS (Asociación N:N con Veterinarios)
        │   └── TRATAMIENTOS (Composición)
        └── HOSPITALIZACIONES

FACTURAS (Polimorfismo de Métodos de Pago)
├── PAGOS_EFECTIVO
├── PAGOS_TARJETA
└── PAGOS_TRANSFERENCIA

DETALLES_FACTURA (Relación con Servicios)
METODOS_PAGO (Tabla de Configuración)
```

---

## Descripción de Tablas

### 1. **PERSONAS** (Tabla Base - Abstracción)

**Propósito**: Almacenar información común de todos los usuarios del sistema.

**Campos**:
- `id_persona`: PK, identificador único
- `nombre`: Nombre completo
- `documento`: DNI/RUC único
- `tipo`: Categoría de persona (Veterinario, Recepcionista, Cliente)
- `fecha_registro`: Timestamp de creación

**Notas**: 
- Implementa el **PILAR 1: ABSTRACCIÓN**
- Patrón Single Table Inheritance (STI)
- Permite polimorfismo a nivel base de datos

---

### 2. **VETERINARIOS** (Herencia)

**Propósito**: Datos específicos del personal médico veterinario.

**Campos**:
- `id_veterinario`: PK
- `id_persona`: FK a PERSONAS (relación 1:1)
- `licencia`: Número de licencia profesional
- `especialidad`: Área de especialización (Cirugía, Cardiología, etc.)
- `estado`: Activo, Inactivo, Licencia
- `fecha_contratacion`: Cuando se unió

**Notas**:
- Implementa el **PILAR 2: HERENCIA**
- El campo `id_persona` es UNIQUE (relación 1:1)
- Clave foránea con ON DELETE CASCADE

---

### 3. **RECEPCIONISTAS** (Herencia)

**Propósito**: Datos de personal administrativo.

**Campos**:
- `id_recepcionista`: PK
- `id_persona`: FK a PERSONAS (relación 1:1)
- `turno`: Mañana, Tarde, Noche
- `estado`: Activo, Inactivo
- `fecha_contratacion`: Cuando se unió

**Notas**: Similar a VETERINARIOS, heredando de PERSONAS

---

### 4. **CLIENTES** (Herencia)

**Propósito**: Información de los propietarios de mascotas.

**Campos**:
- `id_cliente`: PK
- `id_persona`: FK a PERSONAS (relación 1:1)
- `telefono`: Contacto telefónico
- `email`: Correo electrónico
- `direccion`: Domicilio
- `ciudad`, `codigo_postal`: Localización
- `fecha_registro`: Cuando se registró
- `activo`: Si puede hacer transacciones

**Notas**:
- Datos de contacto y ubicación extensos
- Flag de activo para soft-deletes

---

### 5. **MASCOTAS** (Agregación)

**Propósito**: Registro de animales bajo cuidado de la clínica.

**Relación con CLIENTES**:
- Un cliente POSEE muchas mascotas (1:N)
- Una mascota pertenece a un cliente
- **PILAR 4: AGREGACIÓN** - La mascota puede existir sin el cliente (cambio de propietario)

**Campos**:
- `id_mascota`: PK
- `id_cliente`: FK a CLIENTES
- `nombre`: Nombre del animal
- `especie`: Perro, Gato, Conejo, Hamster, Pájaro, Otro
- `raza`: Raza específica
- `fecha_nacimiento`: Para calcular edad
- `peso_actual`: Último peso registrado
- `color_caracteristicas`: Descripción física
- `alergias`: Alergias conocidas
- `historial_medico`: Nota de historial general
- `activo`: Si está bajo cuidado

**Notas**:
- Índice en `id_cliente` para búsquedas rápidas
- La edad se calcula en tiempo de consulta usando `julianday()`

---

### 6. **CONSULTAS** (Asociación N:N)

**Propósito**: Tabla intermedia que resuelve relación muchos-a-muchos entre Veterinarios y Mascotas.

**Campos**:
- `id_consulta`: PK
- `id_veterinario`: FK a VETERINARIOS
- `id_mascota`: FK a MASCOTAS
- `fecha`: Fecha de la consulta
- `hora`: Hora de la cita
- `motivo`: Por qué acude (síntomas, revisión, etc.)
- `diagnostico`: Diagnóstico del veterinario
- `notas`: Observaciones adicionales
- `estado`: Programada, En Proceso, Completada, Cancelada
- `fecha_registro`: Cuándo se registró

**Notas**:
- Implementa el **PILAR 3: ASOCIACIÓN**
- Índices en `id_veterinario` e `id_mascota`
- UNIQUE en (id_veterinario, id_mascota, fecha, hora) para evitar duplicados
- Relaciona tanto VETERINARIOS como MASCOTAS, evitando una relación directa N:N

---

### 7. **TRATAMIENTOS** (Composición)

**Propósito**: Prescripciones y planes de tratamiento derivados de una consulta.

**Relación con CONSULTAS**:
- Una consulta GENERA muchos tratamientos (1:N)
- Un tratamiento pertenece a una consulta
- **PILAR 5: COMPOSICIÓN** - El tratamiento NO EXISTE sin la consulta

**Campos**:
- `id_tratamiento`: PK
- `id_consulta`: FK a CONSULTAS (ON DELETE CASCADE)
- `tipo`: Medicamento, Terapia, Cirugía, Dieta, Rehabilitación
- `descripcion`: Qué consiste el tratamiento
- `medicamentos`: Nombres y dosis
- `duracion_dias`: Cuántos días debe durar
- `costo`: Precio del tratamiento
- `estado`: Pendiente, En Progreso, Completado, Suspendido
- `fecha_inicio`: Cuándo empieza
- `fecha_fin_estimada`: Cuándo debería terminar
- `notas`: Instrucciones especiales

**Notas**:
- ON DELETE CASCADE: si se elimina la consulta, se eliminan sus tratamientos
- Implementa composición fuerte (no solo agregación)

---

### 8. **HOSPITALIZACIONES**

**Propósito**: Registro de internaciones de mascotas en la clínica.

**Campos**:
- `id_hospitalizacion`: PK
- `id_mascota`: FK a MASCOTAS
- `id_veterinario_supervisor`: FK a VETERINARIOS
- `fecha_ingreso`: Cuándo entra
- `fecha_salida`: Cuándo sale (NULL si aún está)
- `razon`: Por qué se hospitaliza
- `costo_diario`: Tarifa por día
- `diagnostico`: Diagnóstico durante internación
- `tratamiento_durante_hospitalizacion`: Procedimientos realizados
- `alta_medica`: Si recibe alta médica
- `estado`: Activa, Alta, Cancelada

**Notas**:
- Índice en `id_mascota` y `fecha_ingreso`
- Permite calcular costo total: `(fecha_salida - fecha_ingreso) * costo_diario`

---

### 9-11. **PAGOS_EFECTIVO**, **PAGOS_TARJETA**, **PAGOS_TRANSFERENCIA**

**Propósito**: Tablas especializadas para cada método de pago (Polimorfismo).

**Implementan el PILAR 6: POLIMORFISMO**

#### PAGOS_EFECTIVO
```sql
- id_pago_efectivo
- id_factura (FK)
- monto
- billete_mayor (para calcular vuelto)
- vuelto
- numero_referencia
- fecha_procesamiento
- validado
```

#### PAGOS_TARJETA
```sql
- id_pago_tarjeta
- id_factura (FK)
- monto
- numero_tarjeta (ENCRIPTADO en producción)
- ultimo_digitos ("1234")
- cvv (ENCRIPTADO)
- fecha_vencimiento (MM/YY)
- nombre_titular
- numero_referencia
- fecha_procesamiento
- validado
```

#### PAGOS_TRANSFERENCIA
```sql
- id_pago_transferencia
- id_factura (FK)
- monto
- cuenta_origen
- cuenta_destino
- banco
- concepto
- numero_referencia (UNIQUE)
- fecha_procesamiento
- validado
- confirmado
- fecha_confirmacion
```

**Notas**:
- Cada tabla tiene el mismo interfaz: `procesar_pago(monto) -> boolean`
- La columna `numero_referencia` es UNIQUE en cada tabla
- FK hacia FACTURAS con ON DELETE CASCADE

---

### 12. **FACTURAS**

**Propósito**: Documentos de cobro a clientes.

**Campos**:
- `id_factura`: PK
- `id_cliente`: FK a CLIENTES
- `numero_factura`: ID legible (ej: "FAC-2025-001") - UNIQUE
- `fecha`: Fecha de emisión
- `fecha_vencimiento`: Cuándo vence
- `subtotal`: Total sin impuesto
- `impuesto`: IVA u otros impuestos
- `total`: Subtotal + impuesto
- `estado`: Pendiente, Pagada, Parcialmente Pagada, Cancelada
- `metodo_pago_id`: FK a METODOS_PAGO (informativo)
- `notas`: Observaciones

**Notas**:
- Índices en `id_cliente`, `numero_factura`, `fecha`
- El estado se actualiza cuando se procesa un pago
- Usa POLIMORFISMO: cualquiera de los 3 métodos de pago puede procesarla

---

### 13. **DETALLES_FACTURA**

**Propósito**: Desglose de items/servicios en una factura.

**Campos**:
- `id_detalle`: PK
- `id_factura`: FK a FACTURAS (ON DELETE CASCADE)
- `concepto`: Tipo de servicio (Consulta, Tratamiento, Hospitalización, etc.)
- `id_concepto`: ID del item referenciado (id_consulta, id_tratamiento, etc.)
- `descripcion`: Descripción legible
- `cantidad`: Cuántas unidades
- `precio_unitario`: Precio por unidad
- `subtotal`: cantidad * precio_unitario

**Notas**:
- Permite facturas con múltiples servicios
- `id_concepto` puede ser NULL para items genéricos

---

### 14. **METODOS_PAGO**

**Propósito**: Tabla de configuración con métodos de pago disponibles.

**Campos**:
- `id_metodo_pago`: PK (1=Efectivo, 2=Tarjeta, 3=Transferencia)
- `tipo`: Nombre único del método
- `descripcion`: Detalles
- `activo`: Si está habilitado

**Notas**: Inicialmente populada con 3 registros (ver script SQL)

---

## Relaciones y Cardinalidades

### Resumen de relaciones

| Relación | Tipo | Cardinalidad | Implementación |
|----------|------|--------------|----------------|
| PERSONAS → VETERINARIOS | Herencia (STI) | 1:1 (Optional) | FK UNIQUE |
| PERSONAS → RECEPCIONISTAS | Herencia (STI) | 1:1 (Optional) | FK UNIQUE |
| PERSONAS → CLIENTES | Herencia (STI) | 1:1 (Optional) | FK UNIQUE |
| CLIENTES → MASCOTAS | Agregación | 1:N | FK CLIENTES |
| VETERINARIOS ↔ MASCOTAS | Asociación N:N | N:N | Tabla CONSULTAS |
| CONSULTAS → TRATAMIENTOS | Composición | 1:N | FK ON DELETE CASCADE |
| MASCOTAS → HOSPITALIZACIONES | Composición | 1:N | FK ON DELETE CASCADE |
| VETERINARIOS → HOSPITALIZACIONES | Uno a Muchos | 1:N | FK RESTRICT |
| CLIENTES → FACTURAS | Uno a Muchos | 1:N | FK RESTRICT |
| FACTURAS ← PAGOS (Polimorfismo) | N:N | 1:N cada tabla | FK ON DELETE CASCADE |
| FACTURAS → DETALLES_FACTURA | Composición | 1:N | FK ON DELETE CASCADE |

---

## Vistas SQL Útiles

El script SQL incluye 4 vistas pre-creadas:

### 1. **vw_clientes_mascotas**
```sql
SELECT cliente, mascota, especie, edad_anos
FROM vw_clientes_mascotas
WHERE cliente_nombre LIKE '%Juan%'
```
- Combina CLIENTES, PERSONAS, MASCOTAS
- Calcula edad automáticamente

### 2. **vw_historial_consultas**
```sql
SELECT * FROM vw_historial_consultas
WHERE mascota = 'Rex'
ORDER BY fecha DESC
```
- Historial médico completo por mascota
- Incluye veterinario y número de tratamientos

### 3. **vw_resumen_facturacion**
```sql
SELECT * FROM vw_resumen_facturacion
WHERE pendiente > 0
ORDER BY pendiente DESC
```
- Montos pagados vs pendientes por cliente
- Últimas facturas

### 4. **vw_hospitalizaciones_activas**
```sql
SELECT * FROM vw_hospitalizaciones_activas
```
- Todas las internaciones en curso
- Calcula costo acumulado automáticamente
- Útil para dashboard

---

## Arquitectura de Componentes

### Capas de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PRESENTACIÓN (UI)                   │
│  Dashboard │ Agenda de Citas │ Facturación │ Reportes      │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│              CAPA DE NEGOCIOS (Lógica de Aplicación)        │
│  • Servicio de Personal    (Veterinarios, Recepcionistas)   │
│  • Servicio de Mascotas    (Registro, Historial)            │
│  • Servicio de Consultas   (Programación, Diagnóstico)      │
│  • Servicio de Tratamientos (Prescripción, Seguimiento)     │
│  • Servicio de Hospitalizaciones (Internación, Supervisión) │
│  • Servicio de Pagos y Facturación (POLIMORFISMO)           │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌──────────────────────────────────────────────────────────────┐
│                CAPA DE ACCESO A DATOS (DAL)                 │
│  • ORM / Data Access Layer (Abstracción de acceso)           │
│  • Repositorios (CRUD para cada entidad)                     │
│    - PersonasRepository                                      │
│    - MascotasRepository                                      │
│    - ConsultasRepository                                     │
│    - TratamientosRepository                                  │
│    - HospitalizacionesRepository                             │
│    - FacturasRepository                                      │
│    - PagosRepository                                         │
└──────────────────────────────────────────────────────────────┘
                              ↑
┌──────────────────────────────────────────────────────────────┐
│              CAPA DE BASE DE DATOS (Persistencia)            │
│  SQLite: 14 tablas, 9 índices, 4 vistas, transacciones ACID │
└──────────────────────────────────────────────────────────────┘
```

### Servicios Externos
- **Pasarela de Pago**: Para procesar tarjetas
- **Generador PDF**: Para reportes
- **Email/SMS**: Para notificaciones

---

## Consideraciones para Implementación en Python

### 1. **ORM Recomendado**
```python
# SQLAlchemy con SQLite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///clinica_veterinaria.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
```

### 2. **Mapeo de Clases (Herencia Polimórfica)**
```python
# Patrón Single Table Inheritance (STI)
class Persona(Base):
    __tablename__ = 'personas'
    id_persona = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False)
    tipo = Column(String)  # Discriminador
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'Persona'
    }

class Veterinario(Persona):
    __tablename__ = 'veterinarios'
    id_veterinario = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona'))
    licencia = Column(String, unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'Veterinario'
    }
```

### 3. **Polimorfismo de Pagos**
```python
# Clase base abstracta
from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto: float) -> bool:
        pass
    
    @abstractmethod
    def validar_datos(self) -> bool:
        pass

class PagoEfectivo(MetodoPago):
    def procesar_pago(self, monto: float) -> bool:
        # Lógica para efectivo
        pass

class PagoTarjeta(MetodoPago):
    def procesar_pago(self, monto: float) -> bool:
        # Llamar a pasarela de pago
        pass

class PagoTransferencia(MetodoPago):
    def procesar_pago(self, monto: float) -> bool:
        # Registrar transferencia como pendiente de confirmación
        pass
```

### 4. **Composición vs Agregación**
```python
# Composición: Tratamientos dependen de Consulta
class Consulta(Base):
    tratamientos = relationship("Tratamiento", cascade="all, delete-orphan")
    # cascade="all, delete-orphan" = composición fuerte

# Agregación: Mascotas pueden existir sin Cliente
class Cliente(Base):
    mascotas = relationship("Mascota", cascade="all")
    # sin delete-orphan = agregación débil
```

### 5. **Transacciones y Integridad**
```python
from sqlalchemy import event
from sqlalchemy.orm import Session

# Habilitar FK constraints en SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

### 6. **Índices para Rendimiento**
```python
# En las definiciones de columnas
class Mascota(Base):
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), index=True)
    nombre = Column(String, index=True)
    fecha_nacimiento = Column(Date, index=True)
```

### 7. **Validaciones en Python**
```python
from datetime import datetime, date

class Mascota(Base):
    # ...
    
    @validates('fecha_nacimiento')
    def validate_fecha_nacimiento(self, key, value):
        if value > date.today():
            raise ValueError("La fecha no puede ser en el futuro")
        return value
    
    @property
    def edad_anos(self):
        today = date.today()
        age = today.year - self.fecha_nacimiento.year
        if today.month < self.fecha_nacimiento.month or \
           (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
            age -= 1
        return age
```

### 8. **Estructura de Proyecto Recomendada**
```
clinica_veterinaria/
├── models/
│   ├── __init__.py
│   ├── base.py           # Clase base y configuración SQLAlchemy
│   ├── personas.py       # Personas, Veterinarios, Recepcionistas, Clientes
│   ├── mascotas.py       # Mascotas
│   ├── consultas.py      # Consultas, Tratamientos
│   ├── hospitalizaciones.py
│   ├── facturas.py       # Facturas, Detalles
│   └── pagos.py          # Pagos (3 tipos polimórficos)
├── services/
│   ├── personal_service.py
│   ├── mascotas_service.py
│   ├── consultas_service.py
│   ├── tratamientos_service.py
│   ├── hospitalizaciones_service.py
│   └── pagos_service.py
├── repositories/
│   ├── base_repository.py
│   ├── personas_repository.py
│   ├── mascotas_repository.py
│   └── ... (una por cada entidad)
├── database.py           # Conexión y sesiones
├── config.py             # Configuración
└── main.py               # Punto de entrada
```

### 9. **Patrón Repository + Service**
```python
# Base Repository
class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model
    
    def crear(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def obtener_por_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model).filter(
            self.model.id == id
        ).first()
    
    def listar_todos(self) -> List[T]:
        return self.session.query(self.model).all()
    
    def actualizar(self, obj: T) -> T:
        self.session.commit()
        return obj
    
    def eliminar(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()

# Servicio de Mascotas
class MascotasService:
    def __init__(self, mascotas_repo: MascotasRepository):
        self.repo = mascotas_repo
    
    def registrar_mascota(self, cliente_id: int, datos: dict) -> Mascota:
        mascota = Mascota(
            id_cliente=cliente_id,
            nombre=datos['nombre'],
            especie=datos['especie'],
            raza=datos.get('raza'),
            fecha_nacimiento=datos['fecha_nacimiento']
        )
        return self.repo.crear(mascota)
    
    def obtener_historial(self, mascota_id: int) -> List[Consulta]:
        mascota = self.repo.obtener_por_id(mascota_id)
        return mascota.consultas
```

### 10. **Excepciones Personalizadas**
```python
class ClinicaException(Exception):
    pass

class MascotaNoEncontradaException(ClinicaException):
    pass

class VeterinarioOcupadoException(ClinicaException):
    pass

class PagoFallidoException(ClinicaException):
    pass
```

---

## Resumen

Este modelo de datos y arquitectura:

✅ **Respeta los 6 Pilares de POO**:
- Abstracción en PERSONAS
- Herencia mediante tablas especializadas
- Asociación N:N vía tabla CONSULTAS
- Agregación en CLIENTES-MASCOTAS
- Composición en CONSULTAS-TRATAMIENTOS
- Polimorfismo en PAGOS

✅ **Normalizado** para SQLite (3NF)

✅ **Escalable** con índices y vistas

✅ **Fácil de mapear** a clases Python con SQLAlchemy

✅ **Seguro** con constraints e integridad referencial

✅ **Mantenible** con documentación clara

---

**Documento generado**: Abril 2025  
**Versión**: 1.0
