# Guía de Laboratorio — Lección 5.1: Matriz de Confusión, Precisión, Recall y F1-Score en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 5:** Evaluación Rigurosa y TDD Asistido por Agentes en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado los Capítulos 1 al 4 de la Unidad 2.

---

## 1. La Trampa de la Exactitud (Accuracy Paradox) en Redes Eléctricas

En problemas de diagnóstico de fallas industriales como los de **`energy-ml`**, los eventos críticos son **altamente desbalanceados**:
* El 98% de los días un transformador de potencia opera en condiciones normales.
* Solo el 2% de los días presenta una falla dieléctrica o cortocircuito incipiente.

Si un modelo simplista predice ciegamente *"operación normal"* para el 100% de las lecturas, tendrá una **Exactitud (Accuracy) del 98%**. A pesar de este número aparentemente exitoso, el sistema es **completamente inútil y peligroso**: no detectará ninguna falla real, permitiendo que transformadores colapsen sin previo aviso.

Por este motivo, en la Ciencia de Datos profesional se descarta la exactitud como métrica única y se utiliza la **Matriz de Confusión** junto con **Precisión**, **Recall (Sensibilidad)** y **F1-Score**.

---

## 2. Anatomía de la Matriz de Confusión

La matriz de confusión es una tabla de doble entrada que compara las etiquetas reales de planta (*Ground Truth*) frente a las decisiones emitidas por el clasificador:

```text
┌───────────────────────────┬────────────────────────────────────────────┐
│                           │ Condición Real (Planta Industrial)         │
│                           ├────────────────────┬───────────────────────┤
│                           │ Positivo (Falla)   │ Negativo (Normal)     │
├─────────┬─────────────────┼────────────────────┼───────────────────────┤
│ Decisión│ Positivo (Falla)│ Verdadero Positivo │ Falso Positivo (FP)   │
│ del     │                 │ (TP - Acierto)     │ (Falsa Alarma)        │
│ Modelo  ├─────────────────┼────────────────────┼───────────────────────┤
│ (FastAPI│ Negativo (Normal│ Falso Negativo (FN)│ Verdadero Negativo    │
│ Endpoint│                 │ (¡Falla no vista!) │ (TN - Acierto)        │
└─────────┴─────────────────┴────────────────────┴───────────────────────┘
```

### El Costo Asimétrico del Error en Ingeniería Eléctrica:
* **Falso Positivo (FP):** El modelo predice falla pero el transformador está sano. Consecuencia: una brigada de mantenimiento viaja a la subestación a verificar el equipo (costo operativo moderado).
* **Falso Negativo (FN):** El modelo predice normal pero el transformador se está quemando. Consecuencia: explosión del tanque de aceite, corte masivo de suministro eléctrico a miles de usuarios y pérdidas millonarias (costo catastrófico).

En `energy-ml`, nuestro objetivo primordial es **minimizar los Falsos Negativos**, lo que equivale a **maximizar el Recall**.

---

## 3. Métricas Derivadas: Precisión, Recall y F1-Score

```text
┌───────────────────────────────┬────────────────────────────────────────┐
│ Métrica                       │ Definición Conceptual                  │
├───────────────────────────────┼────────────────────────────────────────┤
│ Precisión (Precision)         │ TP / (TP + FP)                         │
│                               │ De todas las alarmas que emitió el     │
│                               │ modelo, ¿cuántas fueron reales?        │
├───────────────────────────────┼────────────────────────────────────────┤
│ Sensibilidad / Recall         │ TP / (TP + FN)                         │
│                               │ De todas las fallas reales que ocurrie-│
│                               │ ron en planta, ¿cuántas atrapó el      │
│                               │ modelo? (Vital en energía).            │
├───────────────────────────────┼────────────────────────────────────────┤
│ F1-Score                      │ Media armónica entre Precisión y Recall│
│                               │ 2 * (Precision * Recall) / (Prec + Rec)│
│                               │ Balance equilibrado para datasets      │
│                               │ fuertemente desbalanceados.            │
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 4. Taller Práctico: Evaluación Rigurosa con Scikit-Learn

Navegamos a nuestro repositorio local:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos `scripts/evaluar_metricas_diagnostico.py`:

```python
"""Cálculo riguroso de matriz de confusión y métricas en telemetría de transformadores."""

import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

# 1. Etiquetas reales observadas en 100 eventos de subestación (1: Falla, 0: Normal)
# Dataset fuertemente desbalanceado: 95 normales, 5 fallas críticas
np.random.seed(42)
y_reales = np.array([0]*95 + [1]*5)

# 2. Predicciones emitidas por un modelo de prueba
# El modelo detectó 4 fallas reales (TP=4), ignoró 1 falla (FN=1) y generó 2 falsas alarmas (FP=2)
y_predicciones = np.array([0]*93 + [1]*2 + [1]*4 + [0]*1)

print("--- 1. Matriz de Confusión ---")
matriz = confusion_matrix(y_reales, y_predicciones)
tn, fp, fn, tp = matriz.ravel()
print(f"Verdaderos Negativos (TN): {tn}")
print(f"Falsos Positivos    (FP): {fp} (Falsas alarmas)")
print(f"Falsos Negativos    (FN): {fn} (¡Fallas ignoradas!)")
print(f"Verdaderos Positivos(TP): {tp} (Fallas detectadas)")

print("\n--- 2. Métricas de Rendimiento en Falla Crítica (Clase 1) ---")
precision = precision_score(y_reales, y_predicciones)
recall = recall_score(y_reales, y_predicciones)
f1 = f1_score(y_reales, y_predicciones)

print(f"Precisión: {precision:.4f} ({precision*100:.1f}%)")
print(f"Recall:    {recall:.4f} ({recall*100:.1f}%)")
print(f"F1-Score:  {f1:.4f} ({f1*100:.1f}%)")

print("\n--- 3. Reporte Completo de Clasificación ---")
print(classification_report(y_reales, y_predicciones, target_names=["Normal", "Falla"]))
```

Ejecutamos el script:

```bash
python scripts/evaluar_metricas_diagnostico.py
```

Observarás cómo el reporte de clasificación desglosa con exactitud matemática el comportamiento asimétrico del sistema de diagnóstico.

---

## 5. Conclusión

Comprender la **Matriz de Confusión**, la **Precisión** y el **Recall** es el fundamento para diseñar sistemas de Inteligencia Artificial responsables en infraestructuras críticas.

En la siguiente lección, aplicaremos la metodología de **Desarrollo Guiado por Pruebas (TDD)** asistidos por **Aider** y **AGY CLI**, escribiendo primero los tests automatizados antes de codificar la lógica del servicio.
