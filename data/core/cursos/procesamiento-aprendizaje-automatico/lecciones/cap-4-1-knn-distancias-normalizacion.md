# Guía de Laboratorio — Lección 4.1: Algoritmo k-NN: Métricas de Distancia, Estandarización y Costo de Inferencia en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 4:** Aprendizaje Basado en Instancias (k-NN) en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado los Capítulos 1, 2 y 3 de la Unidad 2.

---

## 1. El Paradigma del Aprendizaje Basado en Instancias (*Lazy Learning*)

A diferencia de modelos como Naive Bayes o regresiones que ajustan parámetros matemáticos durante el entrenamiento y luego descartan los datos crudos (*Eager Learning*), el algoritmo **k-Nearest Neighbors (k-NN)** opera bajo el paradigma del **Aprendizaje Perezoso (*Lazy Learning*)**:
* **Fase de Entrenamiento:** Prácticamente instantánea ($O(1)$). No calcula pesos; simplemente indexa y almacena en memoria RAM todas las instancias históricas etiquetadas.
* **Fase de Inferencia:** Computacionalmente demandante ($O(N \cdot D)$). Cada vez que ingresa una nueva lectura de telemetría, el algoritmo debe calcular la distancia matemática entre el nuevo punto y **todas** las $N$ muestras almacenadas en el dataset para encontrar a los $k$ vecinos más cercanos.

En **`energy-ml`**, k-NN es la técnica ideal para **desagregación de cargas eléctricas (NILM)** y detección de firmas operativas raras: si un compresor industrial enciende con un patrón transitorio idéntico al registrado hace seis meses, k-NN lo identifica inmediatamente por similitud geométrica.

---

## 2. Métricas de Distancia Geométrica

Para determinar qué tan "cerca" está una medición de otra en el espacio multidimensional de características, k-NN utiliza funciones de distancia:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   MÉTRICAS DE DISTANCIA EN ESPACIOS MULTIDIMENSIONALES │
├───────────────────────────────┬────────────────────────────────────────┤
│ 1. Distancia Euclidiana (L2)  │ La distancia en línea recta:           │
│                               │ d(x, y) = sqrt( suma( (xi - yi)^2 ) )  │
│                               │ Es la métrica estándar para variables  │
│                               │ físicas continuas isotrópicas.         │
├───────────────────────────────┼────────────────────────────────────────┤
│ 2. Distancia Manhattan (L1)   │ La suma de diferencias absolutas:      │
│                               │ d(x, y) = suma( |xi - yi| )            │
│                               │ Más robusta ante valores atípicos      │
│                               │ extremos (outliers).                   │
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. La Necesidad Crítica de Estandarización de Variables

Consideremos qué ocurre si calculamos la distancia euclidiana directa entre dos lecturas de `energy-ml` con variables en distintas escalas:

```text
Lectura A: Voltaje = 220 V,   Factor de Potencia = 0.95
Lectura B: Voltaje = 230 V,   Factor de Potencia = 0.70

Diferencia de Voltaje: (230 - 220)^2 = 10^2 = 100.0
Diferencia de Factor:  (0.70 - 0.95)^2 = (-0.25)^2 = 0.0625

Distancia = sqrt(100.0 + 0.0625) = sqrt(100.0625) ≈ 10.003
```

El voltaje domina el 99.9% del cálculo de distancia, volviendo invisible al factor de potencia, a pesar de que una variación de 0.25 en el factor de potencia representa un cambio técnico radical en la carga eléctrica.

### Regla Inviolable en k-NN
Toda variable debe ser escalada mediante **`StandardScaler`** (restando la media y dividiendo por la desviación estándar) para que todas las dimensiones tengan media 0 y varianza 1, otorgándoles el mismo peso geométrico relativo.

---

## 4. Taller Práctico: Implementación de k-NN con Pipeline en Python

Navegamos a nuestro entorno de trabajo:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos `scripts/demostracion_knn_cargas.py`:

```python
"""Demostración de k-NN para clasificación de cargas eléctricas industriales."""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Firmas de telemetría: [potencia_activa_w, factor_potencia, corriente_a]
X_historico = np.array([
    # Motores de inducción (alto consumo, factor de potencia bajo)
    [3200.0, 0.72, 14.5],
    [3100.0, 0.70, 14.1],
    [3300.0, 0.74, 15.0],
    # Hornos de resistencia (alto consumo, factor de potencia unitario)
    [4500.0, 0.98, 20.4],
    [4600.0, 0.99, 20.9],
    [4400.0, 0.97, 20.0],
    # Iluminación LED y electrónica (bajo consumo)
    [250.0,  0.92, 1.1],
    [280.0,  0.90, 1.2],
    [220.0,  0.94, 1.0]
])

y_historico = np.array([
    "motor_induccion", "motor_induccion", "motor_induccion",
    "horno_electrico", "horno_electrico", "horno_electrico",
    "iluminacion_led", "iluminacion_led", "iluminacion_led"
])

# Construimos el Pipeline que estandariza antes de calcular distancias
pipeline_knn = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=3, metric="euclidean"))
])

pipeline_knn.fit(X_historico, y_historico)
print("Pipeline k-NN indexado en memoria exitosamente.")

# Nueva lectura no vista: Potencia=3150W, FP=0.71, Corriente=14.2A
nueva_medicion = [[3150.0, 0.71, 14.2]]

prediccion = pipeline_knn.predict(nueva_medicion)[0]
distancias, indices = pipeline_knn.named_steps["knn"].kneighbors(
    pipeline_knn.named_steps["scaler"].transform(nueva_medicion)
)

print(f"\nNueva telemetría clasificada como: {prediccion}")
print("Distancias normalizadas a los 3 vecinos más cercanos:", [round(d, 4) for d in distancias[0]])
```

Ejecutamos el script:

```bash
python scripts/demostracion_knn_cargas.py
```

Comprobarás cómo el pipeline normaliza las variables y asigna la clase *"motor_induccion"* con distancias sumamente reducidas a los vecinos históricos correspondientes.

---

## 5. El Hiperparámetro k y el Balance Sesgo-Varianza

El valor de **$k$ (número de vecinos consultados)** determina la suavidad de la frontera de decisión:
* **$k = 1$:** Varianza alta (sensible al ruido y a mediciones erróneas puntuales).
* **$k$ Moderado (ej. 3 o 5):** Buen compromiso de robustez ante fluctuaciones de red.
* **$k$ Muy Grande:** Sesgo alto (la clase mayoritaria domina todas las predicciones).
* **Regla Práctica:** Elegir un valor de $k$ impar para evitar empates en problemas de clasificación binaria.

---

## 6. Conclusión

El algoritmo k-NN ofrece una solución transparente y geométrica para identificar firmas de cargas en **`energy-ml`**, supeditado siempre a una rigurosa **estandarización de características**.

En la siguiente lección, implementaremos el endpoint `POST /api/v1/classify/knn` en FastAPI para consultar la vecindad de telemetría en tiempo real.
