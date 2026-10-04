# Guía de Laboratorio — Lección 5.3: Endpoint POST /api/v1/predict/consumo con Esquemas Pydantic Asistido por OpenCode

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 5:** De Script de Consola a Servicio Web con FastAPI sobre `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 5.2 (Servidor FastAPI y Swagger UI).

---

## 1. El Peligro de los Datos Corruptos en Inferencia

En el laboratorio de la Lección 5.1 aprendimos que las peticiones `POST` transportan un cuerpo JSON. Sin embargo, en el mundo real de la telemetría eléctrica industrial, los sensores IoT y medidores inteligentes pueden fallar:
* Un sensor dañado puede enviar un voltaje negativo (`-220V`), lo cual es físicamente imposible.
* Un microcontrolador descalibrado puede enviar un texto alfanumérico (`"error_crc"`) en un campo numérico.
* Una fase eléctrica puede recibir una letra incorrecta (`"Z"` en lugar de `"R"`, `"S"` o `"T"`).

Si permitiéramos que esos datos defectuosos ingresen sin filtro a nuestros modelos de aprendizaje automático, el sistema generaría predicciones aberrantes o se detendría con un error `500 Internal Server Error`.

Para blindar nuestra API, **Pydantic** actúa como el guardián de entrada (*data validator*), rechazando peticiones inválidas con un código **`422 Unprocessable Entity`** antes de que toquen el modelo.

---

## 2. Definición del Contrato con Esquemas Pydantic

En `energy-ml`, crearemos los modelos de datos en `src/api/schemas.py`:

```python
"""Esquemas de validación y serialización con Pydantic para energy-ml."""

from pydantic import BaseModel, Field
from datetime import datetime

class LecturaSensorRequest(BaseModel):
    """Esquema de entrada con validación estricta de variables eléctricas."""
    sensor_id: str = Field(..., min_length=3, max_length=30, description="Identificador único del medidor")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de la medición")
    voltaje_v: float = Field(..., ge=180.0, le=260.0, description="Voltaje de fase válido (180V a 260V)")
    corriente_a: float = Field(..., ge=0.0, le=150.0, description="Corriente en amperios (0A a 150A)")
    potencia_activa_w: float = Field(..., ge=0.0, description="Potencia activa medida en vatios")
    fase: str = Field(..., pattern="^(R|S|T)$", description="Fase eléctrica conectada: R, S o T")

class PrediccionConsumoResponse(BaseModel):
    """Esquema de respuesta de inferencia de consumo y alerta."""
    sensor_id: str
    consumo_proyectado_kwh: float
    nivel_demanda: str = Field(..., description="Clasificación operativa: normal, moderada o critica")
    alerta_sobrecarga: bool
    tiempo_computo_ms: float
```

---

## 3. Asistencia con OpenCode para Crear el Endpoint

Aprovechando que contamos con **OpenCode** instalado como nuestro primer asistente del cuarteto, le pediremos que ensamble el endpoint en `src/api/routes.py`.

Nos posicionamos en el repositorio:

```bash
cd ~/proyectos_software/energy-ml
```

Iniciamos OpenCode suministrando una instrucción técnica precisa con restricciones claras:

> *"En `src/api/routes.py`, crea un `APIRouter` con prefijo `/api/v1` que defina el endpoint `POST /predict/consumo`. Debe recibir `LecturaSensorRequest` y retornar `PrediccionConsumoResponse`. Para la estimación, calcula el consumo proyectado a 24 horas (`potencia_activa_w * 24 / 1000`). Si la potencia supera los 5000 W, clasifica el nivel como 'critica' y activa la alerta de sobrecarga; de lo contrario clasifícala como 'normal'. Conecta este router en `src/api/main.py`."*

---

## 4. Implementación del Endpoint en `src/api/routes.py`

OpenCode generará la lógica del router:

```python
"""Rutas de la API para inferencia y telemetría de energy-ml."""

import time
from fastapi import APIRouter, status
from src.api.schemas import LecturaSensorRequest, PrediccionConsumoResponse

router = APIRouter(prefix="/api/v1", tags=["Inferencia Energética"])

@router.post(
    "/predict/consumo",
    response_model=PrediccionConsumoResponse,
    status_code=status.HTTP_200_OK,
    summary="Inferencia de consumo y alerta de sobrecarga"
)
def predecir_consumo(lectura: LecturaSensorRequest) -> PrediccionConsumoResponse:
    t_inicio = time.perf_counter()

    # Cálculo preliminar de proyección energética
    consumo_24h_kwh = round((lectura.potencia_activa_w * 24.0) / 1000.0, 2)
    es_critica = lectura.potencia_activa_w > 5000.0
    nivel = "critica" if es_critica else "normal"

    duracion_ms = round((time.perf_counter() - t_inicio) * 1000, 3)

    return PrediccionConsumoResponse(
        sensor_id=lectura.sensor_id,
        consumo_proyectado_kwh=consumo_24h_kwh,
        nivel_demanda=nivel,
        alerta_sobrecarga=es_critica,
        tiempo_computo_ms=duracion_ms
    )
```

En `src/api/main.py`, agregamos el router a la aplicación:

```python
from src.api.routes import router as api_router

app.include_router(api_router)
```

---

## 5. Pruebas Interactivas: Éxito vs. Rechazo Pydantic

Reinicia el servidor Uvicorn si no lo tienes activo:

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Caso 1: Petición Exitosa (200 OK)

Abre otra terminal y envía una lectura válida con `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict/consumo \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "MED-PLANTA-01",
    "voltaje_v": 223.5,
    "corriente_a": 25.0,
    "potencia_activa_w": 5587.5,
    "fase": "R"
  }'
```

**Respuesta recibida (HTTP 200 OK):**
```json
{
  "sensor_id": "MED-PLANTA-01",
  "consumo_proyectado_kwh": 134.1,
  "nivel_demanda": "critica",
  "alerta_sobrecarga": true,
  "tiempo_computo_ms": 0.42
}
```

### Caso 2: Petición Rechazada Automáticamente por Pydantic (422 Unprocessable Entity)

Probemos ahora enviando un voltaje anómalo (`150.0V`, por debajo del límite mínimo de 180V) y una fase inválida (`"Z"`):

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict/consumo \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "MED-PLANTA-01",
    "voltaje_v": 150.0,
    "corriente_a": 10.0,
    "potencia_activa_w": 1500.0,
    "fase": "Z"
  }'
```

**Respuesta devuelta por FastAPI (HTTP 422):**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "voltaje_v"],
      "msg": "Input should be greater than or equal to 180"
    },
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "fase"],
      "msg": "String should match pattern '^(R|S|T)$'"
    }
  ]
}
```

FastAPI rechazó la entrada automáticamente sin ejecutar código defectuoso ni requerir programación manual de validaciones.

---

## 6. Conclusión y Auditoría en Git

Hemos transformado una función matemática de consola en un **endpoint REST tipado, autovalidado y documentado**.

Salimos de la sesión y registramos nuestro avance en Git:

```bash
git status
git add src/api/
git commit -m "feat(api): implementar endpoint predict/consumo con esquemas Pydantic y router modular"
```

En la siguiente lección abordaremos la transición conceptual definitiva: cómo pasar de reglas de umbral cableadas (`if potencia > 5000`) a la inferencia basada en ejemplos y patrones de datos (el núcleo del **Machine Learning**).
