# Guía de Laboratorio — Lección 5.4: Del if/else de Firmas Eléctricas a la Inferencia Basada en Datos (Machine Learning)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 5:** De Script de Consola a Servicio Web con FastAPI sobre `energy-ml`  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado las Lecciones 5.1 a 5.3.

---

## 1. El Límite Insuperable de las Reglas Rígidas (if/else)

En la Lección 5.3 clasificamos el nivel de demanda eléctrica mediante una regla manual sencilla:
```python
if potencia_activa_w > 5000.0:
    nivel = "critica"
```

Esto funciona para un umbral estático de un solo parámetro. Pero supongamos el desafío central de **`energy-ml`**: **Desagregación de Cargas Eléctricas (NILM — *Non-Intrusive Load Monitoring*)**, donde el objetivo es identificar qué maquinaria o equipamiento está encendido en una fábrica (ej: un compresor industrial, una soldadora eléctrica, iluminación LED o un horno de inducción) analizando únicamente la firma de telemetría:

```text
Variables de entrada: Potencia Activa (W), Factor de Potencia (FP) y Corriente (A).
```

### Intento con Programación Tradicional (Reglas Cableadas):

```python
def identificar_carga_manual(potencia: float, fp: float, corriente: float) -> str:
    # Reglas empíricas construidas manualmente por el programador
    if potencia > 3000 and fp < 0.75:
        return "motor_induccion"
    elif potencia > 4000 and fp >= 0.95:
        return "horno_electrico"
    elif potencia < 500 and fp > 0.90:
        return "iluminacion_led"
    elif 1500 <= potencia <= 2800 and 0.80 <= fp <= 0.90:
        return "sistema_ventilacion"
    return "desconocido"
```

### ¿Por Qué Este Enfoque Falla en Producción?
1. **Fragilidad ante Variaciones:** Si la tensión de red cae de 220V a 205V, la potencia del motor variará, rompiendo los rangos estáticos.
2. **Explosión Combinatoria:** A medida que la planta incorpora 20 tipos de cargas diferentes, escribir combinaciones de `if/elif/else` se vuelve inmanejable y propenso a contradicciones.
3. **Imposibilidad de Generalizar:** El programador no puede anticipar manualmente cada pequeña distorsión o ruido de medición.

---

## 2. El Paradigma de Machine Learning: Decisiones Guiadas por Datos

En lugar de programar las reglas a mano, el **Aprendizaje Automático (Machine Learning)** invierte la ecuación:

```text
Programación Tradicional:
  [Datos] + [Reglas if/else] ───────────────► [Respuestas]

Machine Learning (Aprendizaje Basado en Datos):
  [Datos Históricos] + [Respuestas Conocidas] ──► [Modelo / Reglas Aprendidas]
```

### Conjunto de Datos Históricos de Firmas Eléctricas

En `energy-ml`, disponemos de lecturas previas etiquetadas por ingenieros de planta:

```python
# Registros conocidos: [potencia_w, factor_potencia, corriente_a] -> clase
FIRMAS_HISTORICAS = [
    {"firma": [3200.0, 0.72, 14.5], "etiqueta": "motor_induccion"},
    {"firma": [3100.0, 0.70, 14.1], "etiqueta": "motor_induccion"},
    {"firma": [4500.0, 0.98, 20.4], "etiqueta": "horno_electrico"},
    {"firma": [4600.0, 0.99, 20.9], "etiqueta": "horno_electrico"},
    {"firma": [250.0,  0.92, 1.1],  "etiqueta": "iluminacion_led"},
    {"firma": [2200.0, 0.85, 10.0], "etiqueta": "sistema_ventilacion"}
]
```

---

## 3. Clasificador por Similitud Euclidiana en `src/modelo.py`

Implementamos un algoritmo que compara una nueva medición con los ejemplos conocidos calculando la **distancia euclidiana normalizada**:

```python
"""Módulo de inferencia basada en datos históricos para energy-ml."""

import math
from typing import Any

def calcular_distancia(p1: list[float], p2: list[float]) -> float:
    """Calcula la distancia euclidiana entre dos firmas eléctricas."""
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        ((p1[1] - p2[1]) * 1000) ** 2 +   # Escalamiento para equiparar rangos
        ((p1[2] - p2[2]) * 100) ** 2
    )

def clasificar_por_similitud(
    potencia_w: float,
    factor_potencia: float,
    corriente_a: float,
    historico: list[dict[str, Any]]
) -> dict[str, Any]:
    """Encuentra la carga histórica más cercana en el espacio de características."""
    punto_nuevo = [potencia_w, factor_potencia, corriente_a]

    mejor_coincidencia = min(
        historico,
        key=lambda ej: calcular_distancia(punto_nuevo, ej["firma"])
    )

    distancia_minima = calcular_distancia(punto_nuevo, mejor_coincidencia["firma"])

    return {
        "carga_identificada": mejor_coincidencia["etiqueta"],
        "confianza_distancia": round(distancia_minima, 2)
    }
```

---

## 4. Exposición en FastAPI: Endpoint `POST /api/v1/identify-loads`

Añadimos la ruta de inferencia inteligente en `src/api/routes.py`:

```python
from pydantic import BaseModel, Field
from src.modelo import clasificar_por_similitud, FIRMAS_HISTORICAS

class InferenciaCargaRequest(BaseModel):
    potencia_activa_w: float = Field(..., ge=0.0)
    factor_potencia: float = Field(..., ge=0.0, le=1.0)
    corriente_a: float = Field(..., ge=0.0)

class InferenciaCargaResponse(BaseModel):
    carga_identificada: str
    confianza_distancia: float
    metodo: str

@router.post("/identify-loads", response_model=InferenciaCargaResponse)
def identificar_carga(req: InferenciaCargaRequest) -> InferenciaCargaResponse:
    resultado = clasificar_por_similitud(
        req.potencia_activa_w,
        req.factor_potencia,
        req.corriente_a,
        FIRMAS_HISTORICAS
    )
    return InferenciaCargaResponse(
        carga_identificada=resultado["carga_identificada"],
        confianza_distancia=resultado["confianza_distancia"],
        metodo="k-nearest-neighbors-similitud"
    )
```

---

## 5. Pruebas Automatizadas con Pytest y TestClient

En Ciencia de Datos moderna, la validación de un servicio web no se hace únicamente haciendo clic en el navegador, sino mediante **pruebas automatizadas continuas**.

Creamos `tests/test_api.py`:

```python
"""Pruebas de integración para la API de energy-ml."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_healthcheck_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_identify_loads_motor_induccion():
    payload = {
        "potencia_activa_w": 3150.0,
        "factor_potencia": 0.71,
        "corriente_a": 14.3
    }
    response = client.post("/api/v1/identify-loads", json=payload)
    assert response.status_code == 200
    datos = response.json()
    assert datos["carga_identificada"] == "motor_induccion"

def test_identify_loads_validacion_falla_factor_potencia():
    # Factor de potencia no puede ser superior a 1.0
    payload = {
        "potencia_activa_w": 1000.0,
        "factor_potencia": 1.5,
        "corriente_a": 5.0
    }
    response = client.post("/api/v1/identify-loads", json=payload)
    assert response.status_code == 422
```

Ejecutamos los tests en la terminal:

```bash
pytest tests/test_api.py -v
```

---

## 6. Balance del Nivel 0 (Nivelación)

¡Felicitaciones! Has completado el ciclo fundacional completo de la carrera técnica:
1. **Capítulo 1:** Dominio de la **Terminal Bash**, rutas relativas/absolutas y aislamiento en **entornos virtuales (`venv`)**.
2. **Capítulo 2:** Higiene y trazabilidad con **Git y GitHub CLI (`gh`)** sobre el repositorio real `energy-ml`.
3. **Capítulo 3:** Asistentes estudiantiles accesibles: **OpenCode** (libre sin tarjeta) y **Antigravity CLI** (plan estudiante 5 USD y navegación web).
4. **Capítulo 4:** Ecosistema avanzado: **Claude Code** corporativo, **Aider con DeepSeek API** (repomap, AST y horario valle) y **Arneses Autónomos** (Codex, Kimi y DPH).
5. **Capítulo 5:** Transformación de scripts analíticos en un **Servicio Web REST de Inferencia con FastAPI**, contratos de datos en **JSON**, validación rigurosa con **Pydantic** y el salto conceptual hacia el **Machine Learning**.

En la **Unidad 2**, profundizaremos en el entrenamiento formal de modelos matemáticos avanzados, curvas de aprendizaje, hiperparámetros y serialización con `joblib` para llevar la inteligencia artificial a escala productiva.
