# Guía de Laboratorio: Capítulo 5 - TDD, Batería de Pruebas con Pytest y Métricas de Evaluación

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel Intermedio)  
**Slug:** `procesamiento-aprendizaje-automatico-intermedio`  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  

---

## 6. Ejercicio 5.3: Implementación del Endpoint `GET /metrics` en FastAPI

Integra el cálculo de métricas acumuladas en `app/main.py`:

```python
from fastapi import FastAPI
from app.metrics import GlobalMetricsResponse, calcular_metricas_clasificacion

app = FastAPI(title="API Intermedia con Métricas y TDD")

# Simulación de historial de validación guardado en memoria o app.state
EVALUACION_HISTORICA = {
    "naive_bayes": {
        "y_true": [0, 1, 0, 1, 0, 1, 1, 0],
        "y_pred": [0, 1, 0, 0, 0, 1, 1, 1]
    },
    "knn": {
        "y_true": [0, 1, 0, 1, 0, 1, 1, 0],
        "y_pred": [0, 1, 0, 1, 0, 1, 1, 0]
    }
}

@app.get("/metrics", response_model=GlobalMetricsResponse)
def get_metrics():
    nb_data = EVALUACION_HISTORICA["naive_bayes"]
    knn_data = EVALUACION_HISTORICA["knn"]

    metrics_nb = calcular_metricas_clasificacion(nb_data["y_true"], nb_data["y_pred"])
    metrics_knn = calcular_metricas_clasificacion(knn_data["y_true"], knn_data["y_pred"])

    return GlobalMetricsResponse(
        naive_bayes=metrics_nb,
        knn=metrics_knn
    )
```

---

## 7. Auditoría y Control de Versiones con Git

Aplica la auditoría de cambios antes de finalizar la entrega:

1. Revisa los archivos modificados y nuevos:
   ```bash
   git status
   ```

2. Inspecciona el código de pruebas generado por Aider/AGY:
   ```bash
   git diff tests/
   ```

3. Registra la suite de tests en un commit atómico:
   ```bash
   git add tests/ app/metrics.py app/main.py
   git commit -m "test(intermedio): agrega suite de pruebas pytest para endpoints y calculador de métricas GET /metrics"
   ```

---

## 8. Rúbrica de Evaluación del Laboratorio

| Criterio | Excelente (100%) | Satisfactorio (75%) | Requiere Mejora (50%) | No Aprobado (0%) |
| :--- | :--- | :--- | :--- | :--- |
| **Metodología TDD asistida por Agentes** | Escribe pruebas primero apoyándose en Aider/AGY; demuestra el ciclo Red-Green-Refactor. | Utiliza pytest con asistentes pero escribe el código y las pruebas simultáneamente. | Pruebas escritas únicamente al final sin metodología TDD. | No utiliza pruebas automatizadas. |
| **Cálculo de Métricas y Matriz de Confusión** | Implementa matriz de confusión, exactitud, precisión, recall y F1-score correctamente formateados. | Calcula métricas clave pero omite la matriz de confusión o el formateo decimal. | Errores en el cálculo matemático o en las dimensiones de la matriz. | No realiza el módulo de métricas. |
| **Endpoint `GET /metrics` & Pydantic** | Endpoint tipado con esquemas Pydantic estrictos y respuesta clara consolidada. | Endpoint funciona pero sin modelos de respuesta Pydantic explícitos. | Retorna métricas incompletas o sin formato JSON coherente. | No implementa el endpoint `GET /metrics`. |
| **Suite de Tests `pytest` & Auditoría Git** | Pruebas `100% PASSED` con `TestClient`; auditoría limpia mediante `git diff` y commits estructurados. | Pruebas pasan pero faltan aserciones sobre los rangos de valores o los tipos. | Algunas pruebas fallan o requieren intervención manual. | No entrega suite de pruebas en `pytest`. |
