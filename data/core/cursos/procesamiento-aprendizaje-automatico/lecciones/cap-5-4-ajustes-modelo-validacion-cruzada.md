# Lección 5.4: Ajustes del Modelo, Hiperparámetros y Validación Cruzada (Temporal y K-Fold)

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 5:** Evaluación Rigurosa, Validación y Ajustes del Modelo en `energy-ml`  
**Carga horaria estimada:** 35 min  
**Prerrequisitos:** Haber completado las Lecciones 5.1 a 5.3 (Matriz de confusión, TDD y métricas de observabilidad).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: *«Bloque Aprendizaje Supervisado: Ajustes del modelo»*; *«Capacidades profesionales: Utilizar técnicas de validación y verificación de modelos y experimentar con dichas técnicas en diferentes problemas reales»*; *«Referenciales para la evaluación: Validación y verificación de modelos»*).

---

## 1. Parámetros vs. Hiperparámetros en el Ciclo de Aprendizaje

En el diseño e implementación de sistemas de Machine Learning, el desempeño de un algoritmo depende de dos tipos fundamentales de variables cuantitativas:

```text
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ Parámetros del Modelo (Aprendidos)           │ Hiperparámetros (Estructurales / Ajustables) │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ Se calculan matemáticamente de forma interna │ Se definen externamente antes del proceso    │
│ durante el entrenamiento con los datos.      │ de optimización o entrenamiento.             │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ Ejemplos en energy-ml:                       │ Ejemplos en energy-ml:                       │
│ - Vector de medias y varianzas en Bayes.     │ - Número de vecinos k y métrica en k-NN.     │
│ - Umbrales de división y nodos en CART.      │ - Profundidad máxima (max_depth) en CART.    │
│ - Posición de centroides en k-medias.        │ - Número de clusters k en k-medias.          │
│ - Matriz Q de valores en Q-Learning.         │ - Tasa de aprendizaje α y factor γ en RL.    │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

El **ajuste del modelo (*model tuning*)** consiste en el proceso sistemático y experimental de encontrar la configuración de hiperparámetros que maximice la capacidad de generalización del algoritmo sobre datos no vistos, minimizando tanto el subajuste (*underfitting*) como el sobreajuste (*overfitting*).

---

## 2. Métodos de Búsqueda y Ajuste de Hiperparámetros

Existen dos estrategias principales para explorar el espacio de hiperparámetros:

### 2.1 Búsqueda en Grilla (Grid Search)
Evalúa de manera exhaustiva todas las combinaciones posibles dentro de un conjunto discreto predefinido por el desarrollador.
* **Ventaja:** Garantiza encontrar la mejor combinación dentro del espacio delimitado.
* **Desventaja:** Costo computacional exponencial respecto al número de hiperparámetros ($O(m^p)$).

### 2.2 Búsqueda Aleatoria (Randomized Search)
Muestrea combinaciones aleatorias desde distribuciones estadísticas fijadas para cada hiperparámetro durante un número prefijado de iteraciones ($N$).
* **Ventaja:** Eficiencia en espacios continuos o de alta dimensionalidad (Bergstra & Bengio, 2012). Explora mayor diversidad de valores en el mismo tiempo de cómputo.

---

## 3. Técnicas de Validación y Verificación Experimental

Una evaluación ingenua basada en una única partición fija (*Train/Test Split*) presenta dos limitaciones críticas:
1. **Alta varianza:** La métrica de rendimiento depende de la fortuna o sesgo con que se hayan repartido las muestras entre ambos conjuntos.
2. **Filtración de optimización (*Data Leakage*):** Si ajustamos los hiperparámetros mirando el conjunto de prueba (*Test Set*), el modelo terminará memorizando dicho conjunto y sobreestimará su rendimiento en producción.

Para resolver esto, se emplean esquemas de **validación cruzada (*Cross-Validation*)**.

```text
ESQUEMA DE PARTICIÓN PROFESIONAL:
┌────────────────────────────────────────────────────────┬─────────────────────┐
│             Conjunto de Desarrollo                     │  Conjunto de Test   │
│             (Entrenamiento + Validación)               │  (Ciego Final)      │
└────────────────────────────────────────────────────────┴─────────────────────┘
```

### 3.1 K-Fold Cross-Validation Estándar
Divide los datos de entrenamiento en $K$ bloques (*folds*) de tamaño idéntico. En cada una de las $K$ iteraciones, se reserva un bloque para validación y se entrena con los restantes $K - 1$. La métrica final es el promedio de las $K$ iteraciones.

### 3.2 Stratified K-Fold
En problemas desbalanceados (como fallas críticas en transformadores que representan solo el 2% de los registros), el K-Fold aleatorio puede generar bloques sin ningún ejemplo de la clase minoritaria. **Stratified K-Fold** garantiza que cada pliegue contenga exactamente la misma proporción de clases que el conjunto total.

### 3.3 Validación Cruzada Temporal (TimeSeriesSplit / Rolling Origin)
> **¡Regla Inviolable en Telemetría y Redes Eléctricas!**  
> Cuando los datos provienen de series de tiempo (sensores, demanda de potencia, flujo térmico), las observaciones no son independientes ni idénticamente distribuidas (no IID). Mezclar registros del futuro en el conjunto de entrenamiento para predecir el pasado constituye **filtración temporal (*look-ahead bias*)** y anula la validez científica del modelo.

```text
K-Fold Estándar (PROHIBIDO en Series Temporales):
Fold 1: [ Test ][ Train ][ Train ][ Train ]  <-- ¡Entrena con futuro para predecir pasado!
Fold 2: [ Train ][ Test ][ Train ][ Train ]
Fold 3: [ Train ][ Train ][ Test ][ Train ]

TimeSeriesSplit (Ventana Expansiva - OBLIGATORIO en Series Temporales):
Split 1: [ Train ]-------> [ Test ]
Split 2: [ Train ][ Train ]---------> [ Test ]
Split 3: [ Train ][ Train ][ Train ]---------> [ Test ]
Split 4: [ Train ][ Train ][ Train ][ Train ]---------> [ Test ]
           t=0                  t=k                    t=N (Tiempo)
```

En cada split temporal, el conjunto de entrenamiento solo contiene datos anteriores en el tiempo al conjunto de validación.

---

## 4. Laboratorio en `energy-ml`: Ajuste de Clasificador con TimeSeriesSplit

Implementamos un pipeline de ajuste de hiperparámetros para optimizar un clasificador de anomalías en consumo eléctrico sobre series temporales de subestaciones.

```python
"""
Pipeline de optimización de hiperparámetros y validación cruzada temporal
para el módulo energy-ml.
"""
from typing import Any
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, f1_score


def optimizar_clasificador_temporal(
    X_telemetria: np.ndarray,
    y_anomalia: np.ndarray,
    n_splits: int = 5,
) -> dict[str, Any]:
    """
    Ajusta hiperparámetros de k-NN usando TimeSeriesSplit sin fuga temporal.
    
    Args:
        X_telemetria: Matriz temporal ordenada cronológicamente (muestras, features).
        y_anomalia: Vector de etiquetas binarias (0: Normal, 1: Sobrecarga).
        n_splits: Cantidad de ventanas temporales para validación cruzada.
        
    Returns:
        Diccionario con el mejor estimador, mejores parámetros y score promedio.
    """
    # 1. Pipeline estricto: el escalado DEBE ejecutarse dentro del fold
    # para evitar fuga de estadísticas (media/desvío) desde validación a entrenamiento.
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", KNeighborsClassifier()),
    ])

    # 2. Espacio de hiperparámetros a explorar
    param_grid = {
        "classifier__n_neighbors": [3, 5, 7, 11],
        "classifier__weights": ["uniform", "distance"],
        "classifier__metric": ["euclidean", "manhattan"],
    }

    # 3. Validación cruzada temporal (respetando orden causal)
    tscv = TimeSeriesSplit(n_splits=n_splits)

    # 4. Búsqueda en grilla guiada por F1-Score macro (asimétrico)
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=tscv,
        scoring="f1_macro",
        n_jobs=-1,
        refit=True,
    )

    grid_search.fit(X_telemetria, y_anomalia)

    return {
        "mejor_modelo": grid_search.best_estimator_,
        "mejores_hiperparametros": grid_search.best_params_,
        "mejor_f1_score": float(grid_search.best_score_),
        "resultados_cv": grid_search.cv_results_,
    }


if __name__ == "__main__":
    # Simulación de telemetría eléctrica temporal (1000 horas ordenadas)
    np.random.seed(42)
    n_muestras = 1000
    potencia = np.sin(np.linspace(0, 20 * np.pi, n_muestras)) * 2000 + 5000
    ruido = np.random.normal(0, 200, n_muestras)
    corriente = (potencia / 220.0) + np.random.normal(0, 1, n_muestras)
    
    X = np.column_stack([potencia + ruido, corriente])
    # Animan anomalías cuando la potencia supera un umbral dinámico
    y = ((potencia + ruido) > 6500).astype(int)

    resultado = optimizar_clasificador_temporal(X, y, n_splits=5)
    print("Ajuste completado con éxito:")
    print("Mejores Hiperparámetros:", resultado["mejores_hiperparametros"])
    print(f"Mejor F1-Score (Macro) CV Temporal: {resultado['mejor_f1_score']:.4f}")
```

---

## 5. Verificación Rigurosa y Pruebas Unitarias de Validación

En la arquitectura de software de `energy-ml`, los pipelines de validación deben estar protegidos con pruebas automatizadas en `pytest` para verificar que:
1. No ocurra contaminación de información (*data leakage*) entre pliegues.
2. Las divisiones de `TimeSeriesSplit` sean estrictamente crecientes en sus índices temporales.

```python
# tests/test_validacion_temporal.py
import numpy as np
from sklearn.model_selection import TimeSeriesSplit


def test_time_series_split_indices_strictly_causal():
    """Verifica que el conjunto de validación nunca contenga índices menores que el entrenamiento."""
    X = np.arange(100).reshape(-1, 1)
    tscv = TimeSeriesSplit(n_splits=4)

    for train_idx, val_idx in tscv.split(X):
        max_train = int(np.max(train_idx))
        min_val = int(np.min(val_idx))
        # Causalidad estricta: todo dato de entrenamiento debe ser anterior a validación
        assert max_train < min_val, f"Fuga temporal detectada: train_max ({max_train}) >= val_min ({min_val})"
```

---

## 6. Caza de Alucinaciones y Errores Críticos de IA

> **Escenario de Bug Real:** Un asistente de IA generó el siguiente código para "normalizar y validar" un modelo predictivo de demanda eléctrica:
> ```python
> # CÓDIGO CON ERROR CRÍTICO (DATA LEAKAGE)
> scaler = StandardScaler()
> X_scaled = scaler.fit_transform(X_completo)  # <-- ¡ERROR FATAL AQUÍ!
> 
> tscv = TimeSeriesSplit(n_splits=5)
> for train_idx, test_idx in tscv.split(X_scaled):
>     modelo.fit(X_scaled[train_idx], y[train_idx])
> ```
> 
> **¿Cuál es el error y qué impacto tiene en producción?**  
> Al ejecutar `scaler.fit_transform(X_completo)` antes de la división de folds, la media y desviación estándar de toda la serie (incluyendo los períodos futuros de validación) se filtran al conjunto de entrenamiento. En el laboratorio el modelo mostrará un rendimiento artificialmente sobresaliente (*optimism bias*), pero al desplegarse en una subestación real fallará drásticamente.  
> **Solución:** Utilizar siempre un `Pipeline` o ajustar el `StandardScaler` (`scaler.fit(X[train_idx])`) exclusivamente con los índices de entrenamiento dentro de cada fold.

---

## Autoevaluación Formativa

1. ¿Cuál es la diferencia conceptual entre un parámetro interno de un modelo y un hiperparámetro de arquitectura? Proporcione dos ejemplos de cada uno en algoritmos de clasificación supervisada.
2. ¿Por qué el uso de K-Fold tradicional con mezcla aleatoria (*shuffle=True*) es metodológicamente inadmisible en series de tiempo de telemetría eléctrica?
3. Explique qué es el *overfitting* de hiperparámetros y cómo previene este fenómeno el uso de un esquema de validación cruzada anidada (*Nested Cross-Validation*).
