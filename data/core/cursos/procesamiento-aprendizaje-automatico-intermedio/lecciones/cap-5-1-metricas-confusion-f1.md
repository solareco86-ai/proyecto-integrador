# Guía de Laboratorio: Capítulo 5 - TDD, Batería de Pruebas con Pytest y Métricas de Evaluación

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel Intermedio)  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  
**Nivel:** Intermedio  
**Slug:** `procesamiento-aprendizaje-automatico-intermedio`  

---

## 1. Objetivos y Conceptos Clave

### Objetivos de Aprendizaje
* Aplicar la metodología de **Desarrollo Guiado por Pruebas (TDD - Test-Driven Development)** para la construcción de servicios de Machine Learning apoyándose en asistentes de código (**Aider** / **AGY CLI**).
* Diseñar una batería de pruebas unitarias y de integración automatizadas utilizando **`pytest`** y el cliente de pruebas de FastAPI (`TestClient`).
* Calcular e interpretar métricas de evaluación de clasificadores supervisados: **Matriz de Confusión**, **Precisión (Precision)**, **Sensibilidad (Recall)**, **F1-Score** y **Exactitud (Accuracy)**.
* Exponer un endpoint analítico `GET /metrics` en FastAPI que entregue el rendimiento consolidado de los modelos desplegados (`Naive Bayes` y `k-NN`).

### Conceptos Clave
* **TDD (Test-Driven Development):** Ciclo *Red-Green-Refactor* donde se escriben primero las pruebas automatizadas que definen el comportamiento esperado y luego se implementa o refactoriza el código con la asistencia de la IA.
* **FastAPI `TestClient`:** Cliente HTTP basado en `httpx` que permite simular peticiones a los endpoints de la API de forma sincrónica en las pruebas de `pytest` sin necesidad de levantar el servidor web manualmente.
* **Matriz de Confusión:** Tabla de doble entrada que contrasta las etiquetas reales (*Ground Truth*) frente a las predicciones del modelo para contabilizar Verdaderos Positivos (TP), Verdaderos Negativos (TN), Falsos Positivos (FP) y Falsos Negativos (FN).

---

## 2. Preparación del Entorno

Asegúrate de contar con el entorno virtual activado y las dependencias de testing instaladas:

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar pytest y dependencias de cálculo científico
pip install pytest httpx scikit-learn numpy
```

Verifica la estructura proyectada para el laboratorio:
```text
laboratorio-intermedio-cap5/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── bayes_model.py
│   │   └── knn_model.py
│   └── metrics.py
├── tests/
│   ├── __init__.py
│   ├── test_bayes_endpoint.py
│   ├── test_knn_endpoint.py
│   └── test_metrics_endpoint.py
├── pytest.ini
└── .env
```

---

## 3. Módulo de Cálculo de Métricas y Matriz de Confusión (`app/metrics.py`)

Crea el módulo `app/metrics.py` que calculará las métricas a partir de arreglos de valores reales y predichos utilizando `scikit-learn`:

```python
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from pydantic import BaseModel
from typing import List, Dict

class ModelMetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]

class GlobalMetricsResponse(BaseModel):
    naive_bayes: ModelMetricsResponse
    knn: ModelMetricsResponse

def calcular_metricas_clasificacion(y_true: List[int], y_pred: List[int]) -> ModelMetricsResponse:
    """Calcula la matriz de confusión y métricas clave de evaluación."""
    cm = confusion_matrix(y_true, y_pred).tolist()
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    rec = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))

    return ModelMetricsResponse(
        accuracy=round(acc, 4),
        precision=round(prec, 4),
        recall=round(rec, 4),
        f1_score=round(f1, 4),
        confusion_matrix=cm
    )
```
