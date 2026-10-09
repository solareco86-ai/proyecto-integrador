# Lección 3.2: Árboles de Regresión y Poda para Prevención de Overfitting en energy-ml

En la lección anterior exploramos árboles de decisión para clasificar categorías discretas de fallas. Sin embargo, en la operación diaria del sistema eléctrico de ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md), muchas variables críticas son cuantitativas y continuas:
- **Potencia activa demandada** por un alimentador (en Megavatios, MW).
- **Temperatura del punto caliente (*hotspot*)** en los devanados del transformador (en °C).
- **Pérdidas técnicas de transmisión** (en kilovatios-hora, kWh).

Para estas tareas se emplean **Árboles de Regresión** (*Regression Trees*). En lugar de calcular distribuciones de probabilidad entre clases, el modelo predice un valor numérico real continuo en cada hoja del árbol.

---

## 1. Mecánica del Árbol de Regresión

Un árbol de regresión particiona el espacio de características en regiones rectangulares disjuntas `R_1, R_2, ..., R_J`. Para cualquier nueva muestra de telemetría `x` que caiga en la región `R_j`, la predicción del modelo es simplemente el promedio aritmético de las muestras de entrenamiento pertenecientes a dicha región:

```
y_pred(x) = Promedio(y_i)   para todas las muestras i en la region R_j
```

### Criterio de Partición: Minimización del Error Cuadrático Medio (MSE)
En cada división candidata de una variable continua `X_k` con umbral `s`, el algoritmo evalúa las dos regiones resultantes (`R_izq` y `R_der`) y calcula la suma total del error cuadrático residual:

```
MSE_nodo = (1 / N) * Sumatoria [ (y_i - y_promedio)^2 ]
```

El algoritmo selecciona la variable `k` y el umbral `s` que maximicen la **Reducción de Varianza**:
```
Delta_MSE = MSE_padre - [ (N_izq / N_padre) * MSE_izq + (N_der / N_padre) * MSE_der ]
```

---

## 2. El Riesgo Crítico del Sobreajuste (Overfitting)

Los árboles de decisión son modelos no paramétricos de alta capacidad. Si permitimos que el árbol crezca sin restricciones:
1. El algoritmo continuará dividiendo el espacio hasta que cada muestra de entrenamiento quede aislada en su propia hoja individual (`N_hoja = 1`).
2. En este estado patológico, el error de entrenamiento es exactamente cero (`MSE_train = 0.0`), pero el árbol ha memorizado el ruido aleatorio de los sensores de telemetría.
3. Al enfrentarse a nuevas condiciones operativas en producción, el error de generalización (`MSE_test`) se dispara.

```
Error
  ^
  |        Error de Test (Generalización)
  |           \            /   <--- OVERFITTING
  |            \          /
  |             \________/
  |              \
  |               \______    Error de Entrenamiento
  |                      \
  +-----------------------------------> Complejidad del Árbol (Profundidad)
                         ^
                 Punto Óptimo
```

---

## 3. Estrategias de Regularización: Pre-Poda (Early Stopping)

La forma más directa y computacionalmente eficiente de evitar el sobreajuste es limitar a priori el crecimiento del árbol mediante hiperparámetros de Scikit-Learn:

- **`max_depth` (Profundidad Máxima):** Limita la longitud del camino más largo desde la raíz hasta cualquier hoja (ej. `max_depth=4` o `5`). Impide particiones infinitesimales.
- **`min_samples_split`:** Número mínimo de muestras requeridas en un nodo para permitir una partición adicional (ej. `min_samples_split=20`).
- **`min_samples_leaf`:** Número mínimo de observaciones que deben residir obligatoriamente en cada hoja final (ej. `min_samples_leaf=10`). Evita hojas sustentadas por casos atípicos o espurios.
- **`max_leaf_nodes`:** Techo absoluto en la cantidad total de hojas del árbol.

---

## 4. Post-Poda por Complejidad de Costo (Cost-Complexity Pruning)

A veces una partición aparentemente poco útil en una etapa temprana desbloquea particiones sumamente informativas más abajo en el árbol. La pre-poda puede detener el crecimiento prematuramente debido a su naturaleza voraz (*greedy*).

La **Post-Poda por Complejidad de Costo** (*Minimal Cost-Complexity Pruning*) resuelve esto permitiendo que el árbol crezca primero a su tamaño completo y luego podando ramas de abajo hacia arriba minimizando la función de costo regularizada:

```
Costo(T) = Sumatoria [ MSE(hoja) * N_hoja ] + ccp_alpha * |T|
```
Donde:
- `|T|` representa el número total de hojas terminales en el árbol `T`.
- `ccp_alpha` (parámetro de penalización): controla el compromiso (*trade-off*) entre el ajuste a los datos y la simplicidad estructural del árbol.
  - Si `ccp_alpha = 0.0`: El árbol no se poda (crecimiento máximo).
  - A medida que `ccp_alpha` se incrementa: Se eliminan progresivamente las ramas más débiles, consolidando hojas más robustas y generalizables.

---

## 5. Implementación en energy-ml con Scikit-Learn

En `src/infrastructure/sklearn/demand_regressor.py`:

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


def entrenar_arbol_regresion_energia(
    X: np.ndarray, y: np.ndarray, max_depth: int = 5, ccp_alpha: float = 0.01
) -> tuple[DecisionTreeRegressor, dict[str, float]]:
    """Entrena un árbol de regresión regularizado para predicción de demanda MW."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    regresor = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_leaf=15,
        ccp_alpha=ccp_alpha,
        random_state=42,
    )
    regresor.fit(X_train, y_train)

    preds_train = regresor.predict(X_train)
    preds_test = regresor.predict(X_test)

    metricas = {
        "rmse_train": float(np.sqrt(mean_squared_error(y_train, preds_train))),
        "rmse_test": float(np.sqrt(mean_squared_error(y_test, preds_test))),
        "mae_test": float(mean_absolute_error(y_test, preds_test)),
        "profundidad_final": int(regresor.get_depth()),
        "hojas_totales": int(regresor.get_n_leaves()),
    }

    return regresor, metricas
```

---

## 6. Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. En un árbol de regresión, ¿cuál es el valor predicho para cualquier muestra que caiga dentro de una hoja terminal?
   - *Respuesta:* El promedio aritmético (`y_promedio`) de las muestras de entrenamiento que alcanzaron dicha hoja durante el ajuste.
2. Si aumentamos el hiperparámetro `ccp_alpha` desde `0.0` hacia un valor positivo alto, ¿qué ocurre con el tamaño del árbol y con el sesgo/varianza?
   - *Respuesta:* El árbol se poda agresivamente reduciendo su profundidad y número de hojas, disminuyendo la varianza (menor sobreajuste) a costa de un incremento controlado del sesgo.

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente entrenamiento propuesto por un asistente de IA para predecir la demanda pico en Megavatios:

```python
# CÓDIGO CON ERROR PROPUESTO POR LA IA:
from sklearn.tree import DecisionTreeRegressor

def entrenar_modelo_pico_alucinado(X_telemetria, y_mw):
    # La IA no define ningún límite de profundidad ni muestras por hoja
    modelo = DecisionTreeRegressor(random_state=42)
    modelo.fit(X_telemetria, y_mw)
    # Reporta un error de entrenamiento nulo:
    print("MSE en Entrenamiento:", modelo.score(X_telemetria, y_mw))  # R^2 = 1.0!
    return modelo
```

**Diagnóstico del Revisor Humano:**
1. **Sobreajuste Catastrófico:** Sin restricciones (`max_depth=None`, `min_samples_split=2`), el árbol dividirá hasta crear una hoja por cada medición histórica, memorizando perturbaciones espurias de la red. En producción, el error de predicción explotará.
2. **Corrección con Regularización Obligatoria:**

```python
def entrenar_modelo_pico_robusto(X_telemetria, y_mw):
    # Restricciones estructurales y regularización por complejidad
    modelo = DecisionTreeRegressor(
        max_depth=5,
        min_samples_leaf=15,
        ccp_alpha=0.015,
        random_state=42
    )
    modelo.fit(X_telemetria, y_mw)
    return modelo
```

---

## 7. Conclusión

En la siguiente lección veremos cómo transformar la estructura interna de este árbol de Scikit-Learn en un esquema **JSON nativo** consumible por agentes de IA autónomos para proveer explicabilidad y trazabilidad operativa.
