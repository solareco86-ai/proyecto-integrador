# Guía de Laboratorio — Lección 3.2: Construcción del Endpoint POST /api/v1/classify/bayes Asistido por OpenCode

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 3:** Clasificación Probabilística con Naive Bayes en `energy-ml`  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 3.1 (Teorema de Bayes).

---

## 1. El Rol de las Respuestas Probabilísticas en la Toma de Decisiones

En los tableros de control y supervisión (SCADA) de subestaciones eléctricas, un sistema de alarma no debe emitir decisiones binarias sin contexto. Si un operador solo recibe un texto que dice *"falla"*, no sabe si el modelo tiene dudas o si la catástrofe es inminente.

En esta lección, utilizaremos **OpenCode** para construir un endpoint REST en FastAPI que exponga el diagnóstico probabilístico de **Gaussian Naive Bayes**:
* Retornará la clase más probable.
* Desglosará el diccionario de probabilidades relativas para cada estado operativo.
* Evaluará un umbral de decisión operativo: si la probabilidad de falla supera el **75%**, activará de forma automática una bandera de `disparo_alarma`.

---

## 2. Definición del Contrato con Esquemas Pydantic

En `src/schemas/bayes.py` dentro de `energy-ml`, definimos los esquemas de entrada y salida:

```python
"""Esquemas de validación para clasificación probabilística con Naive Bayes."""

from pydantic import BaseModel, Field

class DiagnosticoBayesRequest(BaseModel):
    """Lectura de telemetría de monitoreo térmico y electromecánico."""
    sensor_id: str = Field(..., min_length=3, description="Identificador del activo")
    temperatura_aceite_c: float = Field(
        ...,
        ge=-20.0,
        le=140.0,
        description="Temperatura del dieléctrico en grados Celsius"
    )
    corriente_rms_a: float = Field(
        ...,
        ge=0.0,
        le=200.0,
        description="Corriente eficaz en Amperios"
    )
    vibracion_rms_mms: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Amplitud de vibración mecánica en mm/s"
    )

class DiagnosticoBayesResponse(BaseModel):
    """Diagnóstico enriquecido con distribución de probabilidades."""
    sensor_id: str
    estado_predicho: str
    probabilidades: dict[str, float] = Field(
        ...,
        description="Distribución bayesiana de probabilidades por clase"
    )
    nivel_riesgo: str = Field(..., description="Clasificación de riesgo: bajo, moderado o critico")
    disparo_alarma: bool
    tiempo_computo_ms: float
```

---

## 3. Asistencia con OpenCode para Generar el Router

Aprovechando que contamos con **OpenCode** instalado como asistente de código abierto en la terminal, nos posicionamos en el repositorio:

```bash
cd ~/proyectos_software/energy-ml
```

Invocamos a OpenCode delimitando el contexto:

```bash
opencode --context src/schemas/bayes.py
```

### Prompt Técnico para OpenCode

> *"En `src/api/routes_bayes.py`, crea un `APIRouter` con prefijo `/api/v1` que defina el endpoint `POST /classify/bayes`. Debe recibir `DiagnosticoBayesRequest` y retornar `DiagnosticoBayesResponse`. Utiliza el modelo Bayesiano pre-cargado en `request.app.state.modelo_bayes` (si no existe, retorna HTTPException 503). Si la probabilidad de 'falla_inminente' es mayor a 0.75, asigna nivel_riesgo='critico' y disparo_alarma=True; si está entre 0.30 y 0.75 asigna nivel_riesgo='moderado'; de lo contrario nivel_riesgo='bajo'. Mide el tiempo de cómputo en ms."*

---

## 4. Implementación del Endpoint en `src/api/routes_bayes.py`

OpenCode generará la implementación modular:

```python
"""Router de inferencia probabilística con Naive Bayes para energy-ml."""

import time
from fastapi import APIRouter, Request, HTTPException, status
from src.schemas.bayes import DiagnosticoBayesRequest, DiagnosticoBayesResponse

router = APIRouter(prefix="/api/v1", tags=["Inferencia Bayesiana"])

@router.post(
    "/classify/bayes",
    response_model=DiagnosticoBayesResponse,
    status_code=status.HTTP_200_OK,
    summary="Clasificación probabilística de telemetría de transformadores"
)
def clasificar_telemetria_bayes(
    lectura: DiagnosticoBayesRequest,
    request: Request
) -> DiagnosticoBayesResponse:
    t_inicio = time.perf_counter()

    modelo = getattr(request.app.state, "modelo_bayes", None)
    if modelo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo Bayesiano no se encuentra disponible en memoria."
        )

    vector = [[lectura.temperatura_aceite_c, lectura.corriente_rms_a, lectura.vibracion_rms_mms]]
    
    clase_predicha = str(modelo.predict(vector)[0])
    probabilidades_raw = modelo.predict_proba(vector)[0]

    prob_dict = {
        str(clase): round(float(prob), 4)
        for clase, prob in zip(modelo.classes_, probabilidades_raw)
    }

    prob_falla = prob_dict.get("falla_inminente", 0.0)

    if prob_falla > 0.75:
        riesgo = "critico"
        alarma = True
    elif prob_falla >= 0.30:
        riesgo = "moderado"
        alarma = False
    else:
        riesgo = "bajo"
        alarma = False

    duracion_ms = round((time.perf_counter() - t_inicio) * 1000, 3)

    return DiagnosticoBayesResponse(
        sensor_id=lectura.sensor_id,
        estado_predicho=clase_predicha,
        probabilidades=prob_dict,
        nivel_riesgo=riesgo,
        disparo_alarma=alarma,
        tiempo_computo_ms=duracion_ms
    )
```

---

## 5. Pruebas Automatizadas con Pytest

Creamos `tests/test_api_bayes.py` para asegurar que el endpoint responde adecuadamente y que las probabilidades suman 1.0:

```python
"""Pruebas de integración para el endpoint de inferencia Bayesiana."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sklearn.naive_bayes import GaussianNB
import numpy as np
from src.api.routes_bayes import router

# Configuramos una aplicación de prueba con el modelo montado
app_test = FastAPI()
app_test.include_router(router)

# Calibramos un estimador en memoria
X_calib = np.array([[50.0, 30.0, 2.0], [95.0, 100.0, 15.0]])
y_calib = np.array(["normal", "falla_inminente"])
estimador = GaussianNB().fit(X_calib, y_calib)
app_test.state.modelo_bayes = estimador

client = TestClient(app_test)

def test_classify_bayes_falla_critica():
    payload = {
        "sensor_id": "TRF-TALAR-05",
        "temperatura_aceite_c": 98.0,
        "corriente_rms_a": 105.0,
        "vibracion_rms_mms": 18.0
    }
    response = client.post("/api/v1/classify/bayes", json=payload)
    assert response.status_code == 200
    datos = response.json()
    assert datos["estado_predicho"] == "falla_inminente"
    assert datos["disparo_alarma"] is True
    assert datos["nivel_riesgo"] == "critico"
    # Verificamos coherencia matemática: suma de probabilidades = 1.0
    suma_probs = sum(datos["probabilidades"].values())
    assert abs(suma_probs - 1.0) < 0.01

def test_classify_bayes_rechazo_pydantic_temperatura():
    payload = {
        "sensor_id": "TRF-TALAR-05",
        "temperatura_aceite_c": 250.0,  # Límite superior es 140.0
        "corriente_rms_a": 30.0,
        "vibracion_rms_mms": 2.0
    }
    response = client.post("/api/v1/classify/bayes", json=payload)
    assert response.status_code == 422
```

Ejecutamos las pruebas locales:

```bash
pytest tests/test_api_bayes.py -v
```

---

## 6. Conclusión y Auditoría en Git

Hemos completado la implementación de un **servicio web de inferencia bayesiana en tiempo real**:
* Modelado con **Pydantic** y **FastAPI**.
* Exposición de **probabilidades calibradas**.
* Automatización de pruebas unitarias verificadas localmente.

En el **Capítulo 4**, exploraremos el **Aprendizaje Basado en Instancias con el Algoritmo k-Nearest Neighbors (k-NN)**, analizando la normalización de distancias y el costo computacional de inferencia en memoria.
