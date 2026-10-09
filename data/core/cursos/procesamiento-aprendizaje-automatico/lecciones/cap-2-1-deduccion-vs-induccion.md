# Guía de Laboratorio — Lección 2.1: Deducción del LLM vs. Inducción Estadística de Parámetros en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 2:** Tareas de Aprendizaje y Deducción vs. Inducción en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado el Capítulo 1 de la Unidad 2 (Arquitectura de Inferencia y Pydantic).

---

## 1. Dos Formas Radicalmente Distintas de Inteligencia Computacional

Cuando un estudiante de Ciencia de Datos e Inteligencia Artificial utiliza herramientas agénticas (como OpenCode o Antigravity CLI) para construir clasificadores de Machine Learning en **`energy-ml`**, está combinando dos paradigmas cognitivos complementarios:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   DEDUCCIÓN SIMBÓLICA VS. INDUCCIÓN ESTADÍSTICA        │
├───────────────────────────────┬────────────────────────────────────────┤
│ Razonamiento Deductivo (LLM)  │ Aprendizaje Inductivo (Machine Learning│
├───────────────────────────────┼────────────────────────────────────────┤
│ • De la regla general al caso │ • De las observaciones empíricas       │
│   particular.                 │   a la función matemática subyacente.  │
│ • Opera sobre semántica,      │ • Opera sobre vectores numéricos y     │
│   contratos y tipos en código.│   distribuciones de probabilidad.      │
│ • Si las premisas son válidas │ • Siempre sujeto a error inductivo     │
│   y la lógica es sólida, la   │   ante muestras fuera de distribución  │
│   conclusión es exacta.       │   (Out-of-Distribution - OOD).         │
│ • Ejemplo: El LLM deduce el   │ • Ejemplo: Un modelo Scikit-Learn      │
│   esqueleto de una función    │   aprende a predecir fallas a partir   │
│   FastAPI a partir de un DTO. │   de 100.000 lecturas de telemetría.   │
└───────────────────────────────┴────────────────────────────────────────┘
```

Comprender esta distinción es el antídoto fundamental contra dos errores habituales:
1. Intentar usar un LLM como clasificador numérico de telemetría en tiempo real (lo cual sería ineficiente y astronómicamente caro).
2. Intentar usar un algoritmo inductivo tradicional para razonar sobre arquitectura de software o refactorización de código.

---

## 2. El Enfoque Deductivo en `energy-ml`: Razonamiento Asistido por Agentes

En la ingeniería de software asistida por IA, el modelo de lenguaje opera de manera **deductiva**:
* **Premisa Mayor (Contrato):** *"El estándar de calidad de red exige que la frecuencia en Argentina sea de 50 Hz con tolerancia de ±1%."*
* **Premisa Menor (Dato puntual):** *"La medición actual es `frecuencia = 48.2 Hz`."*
* **Deducción Lógica (Código):**

```python
def validar_frecuencia_red(frecuencia_hz: float) -> bool:
    """Aplica deducción lógica sobre límites normativos."""
    frecuencia_nominal = 50.0
    tolerancia = frecuencia_nominal * 0.01  # ±0.5 Hz (49.5 a 50.5)
    return (frecuencia_nominal - tolerancia) <= frecuencia_hz <= (frecuencia_nominal + tolerancia)
```

El LLM sobresale aquí porque no necesita "entrenar pesos" para deducir esta regla: interpreta el lenguaje natural, conoce la normativa eléctrica y genera código determinístico.

---

## 3. El Enfoque Inductivo: Aprender Patrones Ocultos en Telemetría

Ahora consideremos el problema de **predecir la degradación del aislamiento en un transformador de potencia**:
* Ningún ingeniero puede escribir una regla `if/else` cerrada porque el envejecimiento del aceite depende de interacciones no lineales entre temperatura ambiente, picos de corriente armónica, ciclos de histéresis y humedad relativa.
* No disponemos de una fórmula deductiva perfecta.
* **Solución Inductiva:** Recopilamos 50.000 registros históricos de transformadores con sus condiciones operativas y el resultado de laboratorio (falla vs. óptimo). El algoritmo inductivo (como Naive Bayes o una regresión logística) optimiza sus parámetros estadísticos internos ($\mu, \sigma, w$) para minimizar el error de clasificación.

```text
Entrada Numérica [V, I, kW, °C, Hz] ──► Algoritmo Inductivo ──► P(falla | datos) = 0.87
```

---

## 4. Taller Práctico: Laboratorio Comparativo en Python

Navegamos a nuestro entorno de trabajo:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos `scripts/comparar_deduccion_induccion.py`:

```python
"""Demostración práctica de razonamiento deductivo vs inducción estadística."""

import numpy as np
from sklearn.linear_model import LogisticRegression

# 1. ENFOQUE DEDUCTIVO (Reglas formales explícitas)
def clasificador_deductivo_norma(temperatura_c: float, corriente_a: float) -> str:
    """Aplica la regla física de placa: sobrecarga si I > 100A o T > 90°C."""
    if temperatura_c > 90.0 or corriente_a > 100.0:
        return "alerta_critica"
    return "operacion_normal"

# 2. ENFOQUE INDUCTIVO (Aprendizaje de parámetros a partir de datos empíricos)
def entrenar_clasificador_inductivo():
    # Observaciones empíricas: [temperatura_c, corriente_a]
    X_historico = np.array([
        [45.0, 30.0],
        [50.0, 40.0],
        [60.0, 55.0],
        [75.0, 80.0],
        [88.0, 95.0],
        [95.0, 105.0],
        [102.0, 110.0],
        [85.0, 115.0]
    ])
    # Etiquetas reales observadas en planta
    y_historico = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # 0: normal, 1: crítica

    modelo_inductivo = LogisticRegression()
    modelo_inductivo.fit(X_historico, y_historico)

    print("Parámetros inductivos aprendidos:")
    print(f"Coeficientes de peso (w): {modelo_inductivo.coef_[0]}")
    print(f"Sesgo / Intercepto (b): {modelo_inductivo.intercept_[0]:.4f}")

    return modelo_inductivo

if __name__ == "__main__":
    print("--- 1. Evaluación Deductiva ---")
    caso_prueba = (89.5, 92.0)  # T=89.5°C, I=92A
    resultado_deductivo = clasificador_deductivo_norma(*caso_prueba)
    print(f"Medición {caso_prueba} -> Deducción formal: {resultado_deductivo}")

    print("\n--- 2. Evaluación Inductiva ---")
    modelo = entrenar_clasificador_inductivo()
    probabilidad = modelo.predict_proba([[caso_prueba[0], caso_prueba[1]]])[0][1]
    prediccion = "alerta_critica" if probabilidad > 0.5 else "operacion_normal"
    print(f"Medición {caso_prueba} -> Inducción estadística: {prediccion} (Probabilidad: {probabilidad:.2%})")
```

Ejecutamos el script:

```bash
python scripts/comparar_deduccion_induccion.py
```

### Análisis del Resultado:
* El clasificador **deductivo** evalúa que 89.5°C < 90°C y 92A < 100A, por lo que dictamina *"operacion_normal"* de forma rígida.
* El clasificador **inductivo** detecta que la combinación simultánea de alta temperatura y alta corriente aproxima al transformador a la frontera de fallo, asignando una probabilidad de riesgo elevada.

---

## 5. La Simbiosis en el Flujo de Trabajo Profesional

En el desarrollo de `energy-ml`, los dos paradigmas colaboran estrechamente:
1. Usamos el **razonamiento deductivo de agentes de IA** (como Antigravity CLI u OpenCode) para diseñar la arquitectura de software, formular tests unitarios con Pytest, crear esquemas con Pydantic y escribir el pipeline de datos.
2. Usamos los **algoritmos inductivos de Machine Learning** (como Scikit-Learn) para entrenar estimadores matemáticos sobre los registros masivos de telemetría eléctrica.

---

## 6. Conclusión

Dominar la distinción entre deducción e inducción previene alucinaciones conceptuales y permite seleccionar la herramienta correcta para cada desafío técnico.

En la siguiente lección, abordaremos las **subtareas del aprendizaje inductivo**: partición rigurosa de datos (Train/Test) y la prevención crítica del **Data Leakage temporal** en series de tiempo energéticas.
