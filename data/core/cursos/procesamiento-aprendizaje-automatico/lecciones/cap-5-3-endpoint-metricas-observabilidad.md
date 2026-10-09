# Guía de Laboratorio — Lección 5.3: Exposición de Métricas de Rendimiento en el Endpoint GET /api/v1/metrics en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 5:** Evaluación Rigurosa y TDD Asistido por Agentes en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado las Lecciones 5.1 y 5.2.

---

## 1. La Necesidad de Observabilidad en Sistemas de MLOps

En un entorno de producción crítica como la red eléctrica de **`energy-ml`**, no basta con que los endpoints de inferencia respondan con código `200 OK`. Los ingenieros de MLOps y los operadores de subestación necesitan vigilar en tiempo real la **salud analítica de los modelos**:
* ¿El modelo de diagnóstico térmico está manteniendo su nivel de **Recall** superior al 95% ante las nuevas olas de calor?
* ¿El clasificador de cargas k-NN está sufriendo degradación por la incorporación de nuevas maquinarias en la planta (*Model Drift*)?

Para permitir que herramientas de monitoreo continuo (como Prometheus, Grafana o tableros de control SCADA) supervisen el desempeño, implementaremos un endpoint analítico estandarizado: **`GET /api/v1/metrics`**.

---

## 2. Definición del Contrato con Esquemas Pydantic

En `src/schemas/metricas.py`, modelamos la respuesta consolidada de métricas:

```python
"""Esquemas de observabilidad y métricas de rendimiento para energy-ml."""

from datetime import datetime
from pydantic import BaseModel, Field

class MetricasModeloDetalle(BaseModel):
    """Métricas individuales de un estimador en memoria."""
    nombre_modelo: str
    muestras_evaluadas: int
    exactitud: float = Field(..., ge=0.0, le=1.0)
    precision: float = Field(..., ge=0.0, le=1.0)
    recall: float = Field(..., ge=0.0, le=1.0)
    f1_score: float = Field(..., ge=0.0, le=1.0)
    matriz_confusion: dict[str, int]

class ObservabilidadMetricsResponse(BaseModel):
    """Respuesta global de observabilidad de la plataforma."""
    timestamp: datetime
    plataforma: str = "energy-ml Gateway"
    modelos_activos: dict[str, MetricasModeloDetalle]
    estado_general_ia: str = Field(..., description="operativo, advertencia_drift o degradado")
```

---

## 3. Implementación del Endpoint en `src/api/routes_metrics.py`

Creamos el router analítico que recopila las evaluaciones recientes de los modelos activos (`Naive Bayes` y `k-NN`):

```python
"""Router de observabilidad y métricas de rendimiento analítico."""

from datetime import datetime
from fastapi import APIRouter, status
from src.schemas.metricas import ObservabilidadMetricsResponse, MetricasModeloDetalle
from src.evaluacion.metricas import calcular_metricas_clasificacion

router = APIRouter(prefix="/api/v1", tags=["Observabilidad y Métricas"])

# Simulamos la última auditoría de validación de los modelos desplegados
EVALUACIONES_RECIENTES = {
    "clasificador_bayesiano_termico": {
        "y_true": [0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
        "y_pred": [0, 1, 0, 1, 0, 1, 1, 0, 0, 1]
    },
    "clasificador_knn_cargas": {
        "y_true": [0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
        "y_pred": [0, 1, 0, 0, 0, 1, 1, 0, 0, 1]  # 1 falso negativo
    }
}

@router.get(
    "/metrics",
    response_model=ObservabilidadMetricsResponse,
    status_code=status.HTTP_200_OK,
    summary="Métricas consolidadas de rendimiento de modelos de Machine Learning"
)
def obtener_metricas_globales() -> ObservabilidadMetricsResponse:
    detalles = {}

    for nombre, datos in EVALUACIONES_RECIENTES.items():
        res = calcular_metricas_clasificacion(datos["y_true"], datos["y_pred"])
        detalles[nombre] = MetricasModeloDetalle(
            nombre_modelo=nombre,
            muestras_evaluadas=len(datos["y_true"]),
            exactitud=res["exactitud"],
            precision=res["precision"],
            recall=res["recall"],
            f1_score=res["f1_score"],
            matriz_confusion=res["matriz_confusion"]
        )

    # Evaluación de degradación operativa global
    min_f1 = min(m.f1_score for m in detalles.values())
    estado = "operativo" if min_f1 >= 0.85 else "advertencia_drift"

    return ObservabilidadMetricsResponse(
        timestamp=datetime.utcnow(),
        modelos_activos=detalles,
        estado_general_ia=estado
    )
```

---

## 4. Pruebas Automatizadas con Pytest

Creamos `tests/test_api_metrics.py`:

```python
"""Pruebas de integración para el endpoint de observabilidad /metrics."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.routes_metrics import router

app_test = FastAPI()
app_test.include_router(router)
client = TestClient(app_test)

def test_get_metrics_endpoint_retorna_200_y_modelos_esperados():
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    datos = response.json()

    assert "modelos_activos" in datos
    assert "clasificador_bayesiano_termico" in datos["modelos_activos"]
    assert "clasificador_knn_cargas" in datos["modelos_activos"]
    
    nb_metrics = datos["modelos_activos"]["clasificador_bayesiano_termico"]
    assert nb_metrics["exactitud"] == 1.0
    assert nb_metrics["f1_score"] == 1.0
    assert "matriz_confusion" in nb_metrics
    assert datos["estado_general_ia"] == "operativo"
```

Ejecutamos las pruebas locales:

```bash
pytest tests/test_api_metrics.py -v
```

---

## 5. Balance Completo de la Unidad 2 (Machine Learning)

¡Felicitaciones! Has completado integralmente la **Unidad 2: Machine Learning** con foco ininterrumpido en **`energy-ml`**:
1. **Capítulo 1:** Arquitectura de inferencia de baja latencia con **Pydantic**, ciclo de vida **`lifespan`** en memoria RAM y persistencia comprimida con **`joblib`**.
2. **Capítulo 2:** Fronteras epistemológicas de la IA: **Deducción de LLMs vs. Inducción de ML**, partición temporal estricta y prevención total de **Data Leakage**.
3. **Capítulo 3:** Clasificación probabilística con el **Teorema de Bayes**, asunción Naive y endpoint REST con probabilidades calibradas asistido por **OpenCode**.
4. **Capítulo 4:** Aprendizaje basado en instancias con **k-NN**, estandarización obligatoria de señales eléctricas y endpoint con vecindad dinámica.
5. **Capítulo 5:** Evaluación rigurosa sin trampas de exactitud (**Matriz de Confusión, Precisión, Recall, F1**), metodología **TDD** con **Aider / AGY CLI** y observabilidad continua con el endpoint `GET /api/v1/metrics`.

En la **Unidad 3**, profundizaremos en la **Programación Lógica y Aprendizaje de Conceptos**, explorando algoritmos de inducción formal de reglas explicables (como el Espacio de Versiones y Candidate-Elimination) para auditar decisiones automatizadas.
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Por qué es crítico que el endpoint `/metrics` devuelva true positives, false positives, false negatives, true negatives en lugar de solo un número de "exactitud"?
2. ¿Qué haría un SRE si ve un endpoint que no registra métricas de precisión/recall en tiempo real?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG DE OBSERVABILIDAD GENERADO POR IA:
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/metrics")
async def get_metrics():
    # IA generó esto: métricas resumidas sin granularidad
    return {
        "ultima_evaluacion": datetime.now().isoformat(),
        "exactitud": 0.95,  # ¡Número único sin desglose!
    }
```

**Diagnóstico del Revisor Humano:**
1. **Falta de Matriz de Confusión:** No desagrega TP, FP, FN, TN.
2. **Falta de Métricas por Clase:** No muestra precisión/recall separadamente.
3. **Corrección Obligatoria en energy-ml:**

```python
@app.get("/metrics")
async def get_metrics():
    return {
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn
        },
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "timestamp": datetime.now().isoformat()
    }
```

---
