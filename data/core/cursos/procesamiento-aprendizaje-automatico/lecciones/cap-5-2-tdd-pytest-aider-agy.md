# Guía de Laboratorio — Lección 5.2: Flujo TDD en FastAPI con Pytest Asistido por Aider y AGY CLI

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 5:** Evaluación Rigurosa y TDD Asistido por Agentes en `energy-ml`  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 5.1 (Métricas de Confusión y F1-Score).

---

## 1. La Metodología TDD (Test-Driven Development) en Machine Learning

El **Desarrollo Guiado por Pruebas (TDD)** es una disciplina de ingeniería que invierte el orden tradicional de desarrollo: **primero se escriben las pruebas automatizadas que definen el comportamiento esperado, y recién después se implementa el código de producción**.

En la era del desarrollo asistido por Inteligencia Artificial, TDD se convierte en el **marco de control definitivo**:
* En lugar de pedirle a un agente (Aider o AGY CLI) que "haga una función" y rezar para que funcione, le entregas un **arnés de pruebas estricto**.
* El agente sabe exactamente qué aserciones debe cumplir y no puede alucinar salidas fuera del contrato.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   EL CICLO RED - GREEN - REFACTOR CON AGENTES          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. FASE ROJA (Red)      ──► Escribir test en tests/test_metricas.py    │
│                             Ejecutar pytest: Falla (código no existe)  │
│ 2. FASE VERDE (Green)   ──► Instruir a Aider / AGY CLI para codificar  │
│                             la implementación mínima que pase el test. │
│ 3. REFACTOR (Refactor)  ──► Pulir tipado, optimizar imports y docstrings│
│                             sin romper las pruebas existentes.         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Fase 1 (Red): Especificación del Test Automatizado

Navegamos a nuestro repositorio local:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Escribimos la prueba unitaria en `tests/test_calculador_metricas.py` definiendo qué esperamos de nuestro módulo de métricas:

```python
"""Pruebas unitarias para el calculador de métricas de telemetría."""

import pytest

def test_calculo_metricas_clasificacion_completo():
    # Importamos una función que todavía NO existe en el proyecto
    from src.evaluacion.metricas import calcular_metricas_clasificacion

    y_verdadero = [0, 1, 0, 1, 0, 1, 1, 0]
    y_predicho  = [0, 1, 0, 0, 0, 1, 1, 1]

    resultado = calcular_metricas_clasificacion(y_verdadero, y_predicho)

    # Verificamos estructura del contrato de salida
    assert "exactitud" in resultado
    assert "precision" in resultado
    assert "recall" in resultado
    assert "f1_score" in resultado
    assert "matriz_confusion" in resultado

    # Verificaciones numéricas esperadas
    assert resultado["matriz_confusion"]["tp"] == 3
    assert resultado["matriz_confusion"]["fn"] == 1
    assert resultado["matriz_confusion"]["fp"] == 1
    assert resultado["matriz_confusion"]["tn"] == 3
    assert 0.0 <= resultado["f1_score"] <= 1.0
```

Ejecutamos `pytest` para certificar la **Fase Roja**:

```bash
pytest tests/test_calculador_metricas.py
```
*(Resultado esperado: `FAILED` con `ModuleNotFoundError` o `ImportError`)*.

---

## 3. Fase 2 (Green): Instrucción a Aider o AGY CLI

Iniciamos **AGY CLI** o **Aider** con el archivo de test en el contexto:

```bash
agy
```
*(o `aider tests/test_calculador_metricas.py`)*.

### Prompt Técnico para Pasar a Verde:

> *"Examina `tests/test_calculador_metricas.py`. Implementa el módulo `src/evaluacion/metricas.py` con la función `calcular_metricas_clasificacion(y_true: list[int], y_pred: list[int]) -> dict[str, Any]` utilizando Scikit-Learn (`confusion_matrix`, `precision_score`, `recall_score`, `f1_score`, `accuracy_score`). Asegúrate de que las claves y la estructura de la matriz de confusión (`tp`, `tn`, `fp`, `fn`) coincidan exactamente con las aserciones de la prueba. Incluye anotaciones de tipo completas."*

El agente creará el archivo `src/evaluacion/metricas.py`:

```python
"""Módulo de evaluación y cálculo de métricas para modelos de energía."""

from typing import Any
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

def calcular_metricas_clasificacion(y_true: list[int], y_pred: list[int]) -> dict[str, Any]:
    """Calcula indicadores analíticos y matriz de confusión estructurada."""
    matriz = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = matriz.ravel()

    return {
        "exactitud": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "matriz_confusion": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp)
        }
    }
```

---

## 4. Verificación de la Fase Verde en CPU Local ($0 Tokens)

Salimos del asistente y ejecutamos las pruebas en la terminal Bash:

```bash
pytest tests/test_calculador_metricas.py -v
```

**Salida esperada:**
```text
tests/test_calculador_metricas.py::test_calculo_metricas_clasificacion_completo PASSED
============================== 1 passed in 0.15s ==============================
```

¡La prueba está en verde!

---

## 5. Fase 3 (Refactor) y Commit Atómico

Revisamos la calidad del código generado con herramientas estáticas locales:

```bash
ruff check src/evaluacion/metricas.py
ruff format --check src/evaluacion/metricas.py
```

Consolidamos el ciclo TDD en Git:

```bash
git status
git add src/evaluacion/ tests/test_calculador_metricas.py
git commit -m "feat(evaluacion): implementar calcular_metricas_clasificacion mediante TDD asistido"
```

---

## 6. Conclusión

El flujo **TDD asistido por agentes** garantiza que la Inteligencia Artificial opere como una herramienta subordinada a tus especificaciones de calidad, garantizando cero código muerto y cobertura de pruebas total desde el minuto cero.

En la lección final de la Unidad 2, integraremos este módulo analítico en un **endpoint de observabilidad `GET /api/v1/metrics`** en FastAPI.
