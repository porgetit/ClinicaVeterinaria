# Protocolo de Pruebas - Clínica Veterinaria

Este directorio contiene la suite de pruebas de integración para el backend del sistema de gestión veterinaria. Las pruebas están diseñadas para ejecutarse sobre una base de datos SQLite en memoria para asegurar un estado limpio en cada ejecución.

## Estructura de Pruebas

Se utiliza el framework **pytest** en conjunto con **httpx** para realizar peticiones asíncronas a la API de FastAPI.

### Casos de Prueba Implementados

1.  **`test_login`**:
    *   **Objetivo**: Validar el sistema de autenticación mediante el usuario maestro.
    *   **Verificación**: Comprueba que las credenciales `admin` / `admin123` retornan un `access_token` válido.

2.  **`test_create_cliente`**:
    *   **Objetivo**: Validar el registro de clientes y la persistencia en la base de datos.
    *   **Verificación**: Envía datos de cliente y confirma que el servidor responde con el objeto persistido y un ID asignado.

3.  **`test_create_veterinario`**:
    *   **Objetivo**: Validar la jerarquía de herencia de personas aplicada a veterinarios.
    *   **Verificación**: Comprueba el registro exitoso de un veterinario con su licencia y especialidad.

4.  **`test_full_clinica_flow`**:
    *   **Objetivo**: Prueba de integración de extremo a extremo (E2E) que simula un ciclo de vida real.
    *   **Flujo**: Creación de Cliente -> Registro de Mascota -> Generación de Consulta Médica -> Facturación del Servicio -> Procesamiento de Pago Polimórfico (Efectivo).

## Resultados de la Ejecución

**Estado Actual**: ✅ EXITOSO (4 PASSED)

El sistema ha superado todas las pruebas de lógica de negocio. Sin embargo, la suite reporta **14 advertencias (warnings)** que han sido analizadas para garantizar la transparencia del estado del código.

### Análisis de Advertencias (Warnings)

Aunque las pruebas pasan, el log de ejecución muestra avisos de deprecación que se detallan a continuación:

| Categoría | Cantidad | Descripción | Motivo |
| :--- | :---: | :--- | :--- |
| **Pydantic V2** | ~4 | `.dict()` is deprecated | Cambio global en Pydantic 2.0 hacia `.model_dump()`. |
| **SQLAlchemy Legacy** | ~4 | `Query.get()` is legacy | Recomendación de usar `Session.get()` para búsquedas por ID. |
| **Python Datetime** | ~4 | `utcnow()` is deprecated | Python 3.12+ prefiere `now(datetime.UTC)` para evitar ambigüedades horarias. |
| **Pytest Logic** | 2 | `ReturnNotNoneWarning` | Pytest prefiere que las funciones de prueba no retornen valores (uso de fixtures). |

---

## Instrucciones de Ejecución

Para ejecutar las pruebas en un entorno controlado, utilice el script automatizado en la raíz del proyecto:

```batch
.\test_system.bat
```

Este script se encarga de configurar el `PYTHONPATH`, activar el entorno virtual y lanzar `pytest` con el reporte detallado.
