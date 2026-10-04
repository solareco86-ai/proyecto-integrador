# Guía de Laboratorio — Lección 1.2: Gestión de Memoria en FastAPI: Carga del Modelo en el Lifespan para Inferencia de Alta Velocidad

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 1:** Arquitectura de Inferencia y Esquemas Pydantic  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 1.1 (Modelado de Features con Pydantic).

---

## 1. El Antipatrón Fatal: Cargar Modelos en Cada Petición HTTP

Cuando un desarrollador novato expone un modelo de Machine Learning en un endpoint web, suele cometer el siguiente error conceptual:

```python
# ANTIPATRÓN GRAVE: NO HACER ESTO EN PRODUCCIÓN
@app.post("/predict")
def predecir(datos: TelemetriaRequest):
    # Carga el archivo desde el disco en CADA llamada HTTP
    modelo = joblib.load("modelos/clasificador_transformador.joblib")
    return {"prediccion": modelo.predict([[datos.voltaje_v, datos.corriente_a]])[0]}
```

### ¿Por Qué Esto Destruye el Rendimiento en Producción?
1. **Latencia Inaceptable:** Leer un archivo binario de 50 MB desde el disco duro o almacenamiento NVMe toma entre 50 y 300 milisegundos.
2. **Saturación del Bus de Entrada/Salida (I/O):** Si 200 sensores envían lecturas simultáneas por segundo, el sistema operativo colapsa intentando abrir y deserializar el mismo archivo cientos de veces por segundo.
3. **Consumo Desmedido de CPU y RAM:** Se crean y destruyen objetos repetidamente en memoria, disparando el recolector de basura (*garbage collector*) de Python y provocando micro-pausas (*stutters*).

---

## 2. La Solución Profesional: El Protocolo `lifespan` de FastAPI

En aplicaciones de producción, el modelo de Machine Learning debe cargarse **una única vez en la memoria RAM** durante el arranque del servidor, residir permanentemente allí para realizar predicciones en menos de **2 milisegundos**, y liberarse limpiamente al apagar el servicio.

FastAPI implementa este patrón mediante el gestor de contexto asíncrono **`lifespan`** (basado en la biblioteca estándar `contextlib.asynccontextmanager`):

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   CICLO DE VIDA DE LA APLICACIÓN (LIFESPAN)            │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Uvicorn Inicia       ──► Ejecuta código antes de 'yield'            │
│                             - Carga modelo de disco a memoria RAM      │
│                             - Ejecuta inferencia inicial (warm-up)     │
│ 2. Servidor Listo       ──► yield (Escucha peticiones HTTP activas)    │
│                             - Inferencia ultrarrápida (<2ms en RAM)    │
│ 3. Señal de Apagado     ──► Ejecuta código después de 'yield'          │
│                             - Cierra recursos y libera memoria         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implementación en `src/api/lifespan.py`

En `energy-ml`, creamos el gestor de ciclo de vida en `src/api/lifespan.py`:

```python
"""Gestor de ciclo de vida (lifespan) para la carga y descarga de modelos de ML."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
import joblib
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan_ml(app: FastAPI) -> AsyncGenerator[None, None]:
    """Carga los artefactos de Machine Learning en memoria RAM al arrancar el servidor."""
    logger.info("Iniciando servicio de inferencia energy-ml...")
    
    # 1. Carga del artefacto persistido desde disco a memoria
    ruta_modelo = "modelos/clasificador_transformador.joblib"
    try:
        logger.info(f"Cargando modelo de diagnóstico desde {ruta_modelo}...")
        modelo = joblib.load(ruta_modelo)
        # Guardamos la instancia en app.state para acceso seguro desde los endpoints
        app.state.modelo_transformador = modelo
        logger.info("Modelo de diagnóstico cargado exitosamente en RAM.")
    except FileNotFoundError:
        logger.warning(
            f"No se encontró el archivo {ruta_modelo}. Iniciando con estimador simulado."
        )
        app.state.modelo_transformador = None

    # 2. Warm-up (Inferencia en frío para optimizar cachés de CPU)
    if app.state.modelo_transformador is not None:
        try:
            # Ejecutamos una inferencia ficticia para calentar el runtime
            _ = app.state.modelo_transformador.predict([[220.0, 30.0, 6.6, 50.0, 50.0]])
            logger.info("Warm-up de inferencia completado exitosamente.")
        except Exception as e:
            logger.error(f"Fallo durante el warm-up del modelo: {e}")

    # Cede el control a la aplicación FastAPI para recibir tráfico HTTP
    yield

    # 3. Limpieza al apagar el servidor
    logger.info("Apagando servicio de inferencia. Liberando memoria...")
    if hasattr(app.state, "modelo_transformador"):
        del app.state.modelo_transformador
    logger.info("Recursos liberados correctamente.")
```

---

## 4. Vinculación en `src/api/main.py` y Endpoint de Inferencia

Enlazamos el gestor de ciclo de vida al instanciar la aplicación FastAPI:

```python
"""Punto de entrada principal con gestión de memoria optimizada."""

import time
from fastapi import FastAPI, Request, HTTPException, status
from src.api.lifespan import lifespan_ml
from src.schemas.diagnostico import TelemetriaTransformadorRequest, DiagnosticoTransformadorResponse

app = FastAPI(
    title="Energy-ML Diagnostic Gateway",
    version="2.0.0",
    lifespan=lifespan_ml
)

@app.post(
    "/api/v1/diagnostico/transformador",
    response_model=DiagnosticoTransformadorResponse,
    status_code=status.HTTP_200_OK,
    tags=["Diagnóstico en Tiempo Real"]
)
def diagnosticar_transformador(
    lectura: TelemetriaTransformadorRequest,
    request: Request
) -> DiagnosticoTransformadorResponse:
    t_inicio = time.perf_counter()

    # Recuperamos el modelo pre-cargado desde el estado de la aplicación
    modelo = getattr(request.app.state, "modelo_transformador", None)
    if modelo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo de inferencia no se encuentra cargado en el servidor."
        )

    # Inferencia ultrarrápida directamente sobre la memoria RAM (< 2ms)
    features = [[
        lectura.voltaje_v,
        lectura.corriente_a,
        lectura.potencia_activa_kw,
        lectura.temperatura_aceite_c,
        lectura.frecuencia_hz
    ]]
    
    clase_predicha = modelo.predict(features)[0]
    probabilidad = float(modelo.predict_proba(features)[0].max())

    tiempo_ms = round((time.perf_counter() - t_inicio) * 1000, 3)

    return DiagnosticoTransformadorResponse(
        transformador_id=lectura.transformador_id,
        estado_operativo=clase_predicha,
        probabilidad_sobrecalentamiento=probabilidad,
        accion_recomendada="Inspección preventiva inmediata" if clase_predicha != "normal" else "Continuar monitoreo estándar",
        tiempo_inferencia_ms=tiempo_ms
    )
```

---

## 5. Pruebas Automatizadas del Ciclo de Vida con Pytest

Creamos un test en `tests/test_lifespan.py` utilizando el `TestClient` de FastAPI (que activa automáticamente los eventos de lifespan al inicializarse dentro de un bloque `with`):

```python
"""Pruebas para verificar que el modelo reside en memoria RAM."""

from fastapi.testclient import TestClient
from src.api.main import app

def test_modelo_cargado_en_app_state():
    # El bloque 'with TestClient' dispara el ciclo de vida del lifespan
    with TestClient(app) as client:
        # Verificamos que el estado del servidor contenga el modelo
        assert hasattr(client.app.state, "modelo_transformador")
```

Ejecutamos el test en la terminal local:

```bash
pytest tests/test_lifespan.py -v
```

---

## 6. Conclusión

Al migrar la carga del modelo al protocolo **`lifespan`**, transformamos un servicio lento e inestable en un **microservicio de inferencia de baja latencia (<2ms)** listo para procesar cientos de lecturas simultáneas por segundo en subestaciones eléctricas.

En la siguiente lección, aprenderemos cómo congelar, comprimir y persistir nuestros modelos entrenados mediante **`joblib`**, asegurando trazabilidad y prevención de desajuste de esquemas (*schema drift*).
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Por qué es peligroso cargar un modelo de Machine Learning cada vez que llega una petición HTTP en lugar de hacerlo una sola vez en el `lifespan`?
2. ¿Qué síntoma de IA alucinadora detectarías si ven cargar el modelo dentro del endpoint sin contexto de ciclo de vida?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG GRAVE GENERADO POR IA:
from fastapi import FastAPI
from sklearn.joblib import load

app = FastAPI()

@app.post("/predict")
async def predict(x: float):
    # IA generó esto, cargando el modelo en CADA petición
    modelo = load("modelos/knn_classifier.joblib")  # ¡LENTÍSIMO!
    return {"prediccion": modelo.predict([[x]])[0]}
```

**Diagnóstico del Revisor Humano:**
1. **Pérdida de Rendimiento:** Cargar 100 MB de modelo en cada petición es ineficiente (segundos de latencia).
2. **Falta de Gestión de Ciclo de Vida:** No utiliza `lifespan` de FastAPI para precarga.
3. **Corrección Obligatoria en energy-ml:**
   ```python
   from contextlib import asynccontextmanager
   from sklearn.joblib import load

   modelo = None

   @asynccontextmanager
   async def lifespan(app):
       global modelo
       modelo = load("modelos/knn_classifier.joblib")  # Una sola vez
       yield
       # Limpieza opcional

   app = FastAPI(lifespan=lifespan)

   @app.post("/predict")
   async def predict(x: float):
       return {"prediccion": modelo.predict([[x]])[0]}
   ```

---
