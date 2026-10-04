# Guía de Laboratorio — Lección 3.1: Teorema de Bayes y Clasificación Probabilística de Fallas en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 3:** Clasificación Probabilística con Naive Bayes en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado los Capítulos 1 y 2 de la Unidad 2.

---

## 1. La Necesidad de Estimaciones Probabilísticas en Sistemas Eléctricos

En la operación de redes eléctricas de potencia y subestaciones como las modeladas en **`energy-ml`**, no alcanza con que un modelo responda de forma binaria: *"falla"* o *"normal"*.

Un operador de centro de control necesita conocer el **nivel de certeza o probabilidad asociada**:
* Una alerta con probabilidad del 51% amerita programar una inspección de rutina en el próximo mantenimiento.
* Una alerta con probabilidad del 98% de falla dieléctrica inminente exige disparar de inmediato un interruptor de potencia para proteger la vida humana y salvaguardar un transformador valorado en cientos de miles de dólares.

El **Teorema de Bayes** es la piedra angular del aprendizaje inductivo probabilístico: permite actualizar la creencia sobre un estado operativo a la luz de nueva evidencia de telemetría.

---

## 2. Anatomía del Teorema de Bayes

La fórmula fundamental del Teorema de Bayes establece:

```text
P(Hipótesis | Evidencia) = [ P(Evidencia | Hipótesis) * P(Hipótesis) ] / P(Evidencia)
```

Desglosemos cada uno de sus cuatro componentes aplicados al diagnóstico de transformadores:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   LOS CUATRO TÉRMINOS BAYESIANOS                       │
├───────────────────────────────┬────────────────────────────────────────┤
│ 1. P(Hipótesis)               │ Probabilidad a Priori (Prior):         │
│                               │ La probabilidad histórica de que un    │
│                               │ transformador falle antes de medir nada│
│                               │ (ej: 2% de los transformadores fallan).│
├───────────────────────────────┼────────────────────────────────────────┤
│ 2. P(Evidencia | Hipótesis)   │ Verosimilitud (Likelihood):            │
│                               │ La probabilidad de observar alta       │
│                               │ temperatura si el transformador está   │
│                               │ efectivamente fallando.                │
├───────────────────────────────┼────────────────────────────────────────┤
│ 3. P(Evidencia)               │ Evidencia Marginal (Marginal):         │
│                               │ La probabilidad total de observar alta │
│                               │ temperatura en cualquier condición.    │
├───────────────────────────────┼────────────────────────────────────────┤
│ 4. P(Hipótesis | Evidencia)   │ Probabilidad a Posteriori (Posterior): │
│                               │ La probabilidad actualizada de falla   │
│                               │ tras comprobar la lectura del sensor.  │
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. ¿Por Qué es "Naive" (Ingenuo)?

En la práctica, un transformador transmite múltiples variables simultáneas: temperatura del aceite ($x_1$), corriente RMS ($x_2$) y vibración armónica ($x_3$).

Para calcular la verosimilitud conjunta $P(x_1, x_2, x_3 \mid \text{Falla})$ de forma exacta, necesitaríamos estimar la distribución multivariada completa, lo que exigiría millones de datos empíricos.

El clasificador **Naive Bayes** formula una simplificación matemática audaz: **asume que todas las variables son condicionalmente independientes entre sí dada la clase**:

```text
P(x1, x2, x3 | Clase) = P(x1 | Clase) * P(x2 | Clase) * P(x3 | Clase)
```

### ¿Por Qué Funciona Tan Bien a Pesar de Esta Simplificación?
Aunque en la física real la temperatura y la corriente están correlacionadas, esta "ingenuidad" reduce drásticamente el número de parámetros a aprender, previene el sobreajuste (*overfitting*), permite entrenar en milisegundos con pocos datos y produce rankings de probabilidad sumamente competitivos para detección de eventos anómalos.

---

## 4. Gaussian Naive Bayes para Variables Continuas

Dado que las lecturas de telemetría eléctrica son números reales continuos (voltajes en V, temperaturas en °C), se asume que cada característica sigue una **distribución normal o gaussiana** caracterizada por su media ($\mu$) y su varianza ($\sigma^2$):

```text
f(x) = (1 / sqrt(2 * pi * sigma^2)) * exp( - (x - mu)^2 / (2 * sigma^2) )
```

El algoritmo simplemente calcula la media y desviación estándar de cada variable para cada estado operativo durante el entrenamiento.

---

## 5. Taller Práctico: Estimación Bayesiana con Scikit-Learn

Navegamos a nuestro repositorio:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos `scripts/demostracion_bayes_energia.py`:

```python
"""Demostración de clasificación probabilística con GaussianNB en telemetría."""

import numpy as np
from sklearn.naive_bayes import GaussianNB

# Features: [temperatura_aceite_c, corriente_rms_a]
X_entrenamiento = np.array([
    # Clase 0: Normal
    [50.0, 30.0],
    [52.0, 35.0],
    [55.0, 32.0],
    [58.0, 40.0],
    [60.0, 42.0],
    # Clase 1: Falla Dieléctrica Inminente
    [90.0, 95.0],
    [95.0, 100.0],
    [98.0, 105.0],
    [105.0, 110.0]
])

y_entrenamiento = np.array([
    "normal", "normal", "normal", "normal", "normal",
    "falla_inminente", "falla_inminente", "falla_inminente", "falla_inminente"
])

# Inicializamos y ajustamos el clasificador Bayesiano
clasificador_bayes = GaussianNB()
clasificador_bayes.fit(X_entrenamiento, y_entrenamiento)

# Imprimimos las probabilidades a priori aprendidas
print("Clases del modelo:", clasificador_bayes.classes_)
print("Probabilidades a priori (Prior):", clasificador_bayes.class_prior_)

# Evaluamos una nueva lectura de telemetría sospechosa: T=85°C, I=80A
medicion_sospechosa = [[85.0, 80.0]]
clase_predicha = clasificador_bayes.predict(medicion_sospechosa)[0]
probabilidades = clasificador_bayes.predict_proba(medicion_sospechosa)[0]

print("\n--- Diagnóstico de Telemetría Sospechosa ---")
print(f"Medición: 85°C / 80A -> Diagnóstico: {clase_predicha}")
for clase, prob in zip(clasificador_bayes.classes_, probabilidades):
    print(f"  P({clase} | Telemetría) = {prob:.4f} ({prob*100:.2f}%)")
```

Ejecutamos el script:

```bash
python scripts/demostracion_bayes_energia.py
```

Observarás cómo el modelo no solo asigna la clase más probable, sino que entrega la distribución porcentual exacta de certidumbre para la toma de decisiones operativas.

---

## 6. Conclusión

El Teorema de Bayes transforma mediciones crudas de sensores en **probabilidades accionables de riesgo operacional**.

En la siguiente lección, utilizaremos **OpenCode** para construir el endpoint `POST /api/v1/classify/bayes` en FastAPI, exponiendo las probabilidades calibradas en la API pública de `energy-ml`.
