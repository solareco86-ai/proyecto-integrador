# Guía de Laboratorio: Capítulo 5 - TDD, Batería de Pruebas con Pytest y Métricas de Evaluación

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel Intermedio)  
**Slug:** `procesamiento-aprendizaje-automatico-intermedio`  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  

---

## 4. Ejercicio 5.1: Flujo TDD Asistido por Aider / AGY CLI

Antes de implementar la lógica del endpoint de métricas, utilizaremos **Aider** o **AGY CLI** para generar la especificación de las pruebas (*Red Stage*).

### Paso 1: Generación del Test con Aider
Ejecuta el asistente especificando las reglas del contrato:

```bash
aider --message "Crea el archivo tests/test_metrics_endpoint.py. Debe contener pruebas con pytest y TestClient de FastAPI para un endpoint 'GET /metrics'. Verifica que la respuesta retorne un código de estado 200, un cuerpo JSON con las llaves 'naive_bayes' y 'knn', y que cada una contenga 'accuracy', 'precision', 'recall', 'f1_score' y 'confusion_matrix'."
```

### Paso 2: Ejecución de Pytest (Fase Red)
Ejecuta la suite de pruebas para confirmar que la prueba falla por falta de implementación:

```bash
pytest tests/test_metrics_endpoint.py
```
*(Resultado esperado: `FAILED` o `404 Not Found` ya que el endpoint aún no existe).*

---

## 5. Ejercicio 5.4: Batería Completa de Pruebas de Integración con `pytest`

Construye las pruebas para verificar los tres endpoints de clasificación y métricas en `tests/test_all_endpoints.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_metrics_status_code_and_structure():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    
    # Validar llaves principales
    assert "naive_bayes" in data
    assert "knn" in data
    
    # Validar estructura interna de Naive Bayes
    nb_metrics = data["naive_bayes"]
    assert "accuracy" in nb_metrics
    assert "precision" in nb_metrics
    assert "recall" in nb_metrics
    assert "f1_score" in nb_metrics
    assert "confusion_matrix" in nb_metrics
    assert isinstance(nb_metrics["confusion_matrix"], list)

def test_metrics_values_range():
    response = client.get("/metrics")
    data = response.json()
    
    for model_key in ["naive_bayes", "knn"]:
        m = data[model_key]
        assert 0.0 <= m["accuracy"] <= 1.0
        assert 0.0 <= m["precision"] <= 1.0
        assert 0.0 <= m["recall"] <= 1.0
        assert 0.0 <= m["f1_score"] <= 1.0
```

Ejecuta la suite completa de pruebas (*Green Stage*):
```bash
pytest -v
```
