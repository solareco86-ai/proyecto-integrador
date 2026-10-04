# Guía de Laboratorio — Lección 4.2: Implementación del Endpoint POST /api/v1/classify/knn en FastAPI

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 4:** Aprendizaje Basado en Instancias (k-NN) en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 4.1 (Algoritmo k-NN).

---

## 1. Exposición de Vecindad de Inferencia en Tiempo Real

En la lección anterior aprendimos que el algoritmo **k-NN** compara una muestra de telemetría entrante con todo el banco histórico de mediciones almacenadas en memoria.

En esta práctica, implementaremos el endpoint `POST /api/v1/classify/knn` en FastAPI para **`energy-ml`**. A diferencia de un clasificador tradicional que solo devuelve una etiqueta opaca, este endpoint devolverá:
1. La **clase de carga identificada** (por voto mayoritario de los $k$ vecinos).
2. El vector de **distancias euclidianas normalizadas** hacia los $k$ vecinos más cercanos.
3. El parámetro configurable $k$ de consulta (permitiendo al cliente ajustar la sensibilidad del análisis).

---

## 2. Contratos de Datos con Pydantic

En `src/schemas/knn.py`, definimos los esquemas tipados:

```python
"""Esquemas de validación para inferencia de firmas eléctricas con k-NN."""

from pydantic import BaseModel, Field

class InferenciaCargaKNNRequest(BaseModel):
    """Petición de clasificación de firma eléctrica con hiperparámetro k dinámico."""
    sensor_id: str = Field(..., min_length=3, description="Identificador del medidor de planta")
    potencia_activa_w: float = Field(..., ge=0.0, description="Potencia activa medida en vatios")
    factor_potencia: float = Field(..., ge=0.0, le=1.0, description="Factor de potencia (0.0 a 1.0)")
    corriente_a: float = Field(..., ge=0.0, description="Corriente eficaz de línea en amperios")
    k_vecinos: int = Field(default=3, ge=1, le=15, description="Cantidad de vecinos más cercanos a consultar")

class ClasificacionCargaKNNResponse(BaseModel):
    """Respuesta con carga identificada y métricas de dispersión de vecindad."""
    sensor_id: str
    tipo_carga_identificada: str
    distancias_k_vecinos: list[float]
    distancia_promedio: float
    tiempo_computo_ms: float
```

---

## 3. Implementación del Router en `src/api/routes_knn.py`

Creamos el router que interactúa con el pipeline de k-NN residente en memoria:

```python
"""Router de inferencia con k-Nearest Neighbors para energy-ml."""

import time
from fastapi import APIRouter, Request, HTTPException, status
from src.schemas.knn import InferenciaCargaKNNRequest, ClasificacionCargaKNNResponse

router = APIRouter(prefix="/api/v1", tags=["Inferencia k-NN"])

@router.post(
    "/classify/knn",
    response_model=ClasificacionCargaKNNResponse,
    status_code=status.HTTP_200_OK,
    summary="Identificación de firma de carga mediante k vecinos más cercanos"
)
def clasificar_carga_knn(
    peticion: InferenciaCargaKNNRequest,
    request: Request
) -> ClasificacionCargaKNNResponse:
    t_inicio = time.perf_counter()

    # Recuperamos el pipeline (Escalador + KNeighborsClassifier) pre-cargado
    pipeline = getattr(request.app.state, "pipeline_knn", None)
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El pipeline k-NN no se encuentra inicializado en memoria."
        )

    vector_crudo = [[peticion.potencia_activa_w, peticion.factor_potencia, peticion.corriente_a]]

    # 1. Transformación con el escalador del pipeline
    scaler = pipeline.named_steps["scaler"]
    knn_estimator = pipeline.named_steps["knn"]

    vector_escalado = scaler.transform(vector_crudo)

    # 2. Búsqueda de vecinos más cercanos
    distancias, indices = knn_estimator.kneighbors(
        vector_escalado,
        n_neighbors=peticion.k_vecinos
    )

    # 3. Predicción por voto mayoritario
    clase_predicha = str(knn_estimator.predict(vector_escalado)[0])

    distancias_list = [round(float(d), 4) for d in distancias[0]]
    dist_promedio = round(sum(distancias_list) / len(distancias_list), 4)
    duracion_ms = round((time.perf_counter() - t_inicio) * 1000, 3)

    return ClasificacionCargaKNNResponse(
        sensor_id=peticion.sensor_id,
        tipo_carga_identificada=clase_predicha,
        distancias_k_vecinos=distancias_list,
        distancia_promedio=dist_promedio,
        tiempo_computo_ms=duracion_ms
    )
```

---

## 4. Pruebas Automatizadas con Pytest

Creamos `tests/test_api_knn.py` para asegurar que el endpoint maneja correctamente la parametrización de $k$ y los límites de Pydantic:

```python
"""Pruebas de integración para el endpoint de clasificación k-NN."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from src.api.routes_knn import router

# Montamos la aplicación de test con el pipeline en memoria
app_test = FastAPI()
app_test.include_router(router)

X_mock = np.array([
    [3200.0, 0.72, 14.5], [3100.0, 0.70, 14.1],
    [4500.0, 0.98, 20.4], [4600.0, 0.99, 20.9]
])
y_mock = np.array(["motor", "motor", "horno", "horno"])

pipe_test = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=2))
])
pipe_test.fit(X_mock, y_mock)
app_test.state.pipeline_knn = pipe_test

client = TestClient(app_test)

def test_classify_knn_consulta_exitosa():
    payload = {
        "sensor_id": "MED-PLANTA-02",
        "potencia_activa_w": 3150.0,
        "factor_potencia": 0.71,
        "corriente_a": 14.3,
        "k_vecinos": 2
    }
    response = client.post("/api/v1/classify/knn", json=payload)
    assert response.status_code == 200
    datos = response.json()
    assert datos["tipo_carga_identificada"] == "motor"
    assert len(datos["distancias_k_vecinos"]) == 2
    assert datos["distancia_promedio"] >= 0.0

def test_classify_knn_rechazo_factor_potencia_invalido():
    # Factor de potencia no puede ser mayor a 1.0
    payload = {
        "sensor_id": "MED-PLANTA-02",
        "potencia_activa_w": 1000.0,
        "factor_potencia": 1.45,
        "corriente_a": 5.0
    }
    response = client.post("/api/v1/classify/knn", json=payload)
    assert response.status_code == 422
```

Ejecutamos las pruebas locales:

```bash
pytest tests/test_api_knn.py -v
```

---

## 5. Conclusión y Auditoría en Git

Hemos completado el **Capítulo 4 de la Unidad 2**:
* Desarrollamos un endpoint REST modular en FastAPI para **k-NN**.
* Manejamos consultas dinámicas de vecindad con el parámetro $k$.
* Verificamos la resiliencia del servicio mediante pruebas automatizadas locales.

En el **Capítulo 5**, abordaremos el ciclo final de la Unidad 2: **Evaluación Rigurosa y TDD Asistido por Agentes (Aider y AGY CLI)**, aprendiendo a calcular matrices de confusión, precisión, recall y F1-Score sobre subestaciones de `energy-ml`.
