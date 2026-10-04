# Guía de Laboratorio — Lección 2.2: Subtareas del Aprendizaje: Partición Train/Test y Prevención de Fugas (Data Leakage) en Series Temporales de energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 2:** Tareas de Aprendizaje y Deducción vs. Inducción en `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 2.1 (Deducción vs. Inducción).

---

## 1. El Riesgo de la Memorización: Generalización vs. Overfitting

El objetivo fundamental de cualquier algoritmo de Machine Learning no es memorizar los datos históricos con los que fue alimentado, sino adquirir la **capacidad de generalizar**: predecir con exactitud el comportamiento de nuevas lecturas de sensores que jamás observó durante su entrenamiento.

Si evaluamos el rendimiento de un modelo sobre los mismos datos que utilizó para ajustar sus pesos, obtendremos una falsa ilusión de éxito. El modelo podría simplemente haber memorizado cada caso particular (*sobreajuste* o *overfitting*), fallando estrepitosamente en cuanto se conecte al flujo en vivo de una red eléctrica.

Para medir científicamente su verdadera capacidad analítica, dividimos rigurosamente los datos en dos conjuntos disjuntos:
* **Conjunto de Entrenamiento (*Train Set*):** Empleado exclusivamente para el ajuste inductivo de parámetros (habitualmente 70% a 80% de los datos).
* **Conjunto de Evaluación o Prueba (*Test Set*):** Reservado estrictamente para auditar el desempeño final del modelo ante datos desconocidos (20% a 30%).

---

## 2. El Peligro Mortal en Telemetría de Energía: El Data Leakage Temporal

En problemas tradicionales (como clasificar imágenes de gatos o perros), mezclar aleatoriamente el dataset con `train_test_split(shuffle=True)` es una práctica estándar.

Sin embargo, en **sistemas de energía eléctrica como `energy-ml`**, los datos son **Series Temporales (Time Series)**: cada medición depende intrínsecamente del tiempo (inercia térmica del transformador, curva solar de generación, horarios de encendido industrial).

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ERROR GRAVE: MEZCLA ALEATORIA TEMPORAL               │
├────────────────────────────────────────────────────────────────────────┤
│ 10:00 (Train) ──► 10:05 (Test) ──► 10:10 (Train) ──► 10:15 (Test)      │
│                                                                        │
│ ¡FUGA DE INFORMACIÓN DEL FUTURO AL PASADO!                             │
│ El modelo "espía" qué ocurrió a las 10:00 y a las 10:10 para predecir  │
│ las 10:05, obteniendo un falso 99.9% de exactitud en laboratorio que   │
│ colapsa en producción real cuando el futuro aún no ha ocurrido.        │
└────────────────────────────────────────────────────────────────────────┘
```

Este fenómeno se denomina **Fuga de Información Temporal (*Temporal Data Leakage*)**.

### La Solución Correcta: Partición Cronológica Estricta

Para respetar la flecha del tiempo, la separación debe realizarse de forma secuencial:

```text
┌───────────────────────────────────────────────┬────────────────────────┐
│ Datos Históricos Pasados (Mes 1 a Mes 8)      │ Futuro No Visto (Mes 9)│
│               CONJUNTO DE TRAIN               │    CONJUNTO DE TEST    │
└───────────────────────────────────────────────┴────────────────────────┘
```

---

## 3. Prevención de Fugas en el Preprocesamiento (*Pre-processing Leakage*)

Otro error crítico de diseño ocurre durante la normalización de variables numéricas:
* Si calculas la media (`mu`) y la desviación estándar (`sigma`) sobre **todo el dataset junto** antes de separarlo en train y test, la media del futuro contaminará el entrenamiento.
* **Regla Inviolable:** Los escaladores (como `StandardScaler` o `MinMaxScaler`) deben ajustarse con `.fit()` **únicamente sobre `X_train`**. Luego, esos parámetros congelados se aplican con `.transform()` sobre `X_test` y en los endpoints de producción.

Para garantizar esta separación sin fisuras, Scikit-Learn provee la clase **`Pipeline`**.

---

## 4. Taller Práctico: Partición Cronológica y Pipeline Seguro en Python

Nos posicionamos en el repositorio:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos `scripts/validar_particion_temporal.py`:

```python
"""Demostración de partición cronológica segura y Pipeline sin data leakage."""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error

def simular_serie_temporal_energia() -> pd.DataFrame:
    """Genera 1000 horas consecutivas de consumo y temperatura."""
    np.random.seed(42)
    fechas = pd.date_range(start="2026-01-01", periods=1000, freq="h")
    # Temperatura con ciclo diario
    temperatura = 20.0 + 10.0 * np.sin(np.linspace(0, 50, 1000)) + np.random.normal(0, 1, 1000)
    # Potencia dependiente de la temperatura (refrigeración)
    potencia_kw = 5.0 + 0.8 * temperatura + np.random.normal(0, 2, 1000)

    return pd.DataFrame({
        "timestamp": fechas,
        "temperatura_c": temperatura,
        "potencia_activa_kw": potencia_kw
    })

def particion_segura():
    df = simular_serie_temporal_energia()
    print("Total de horas de telemetría registradas:", len(df))

    # 1. PARTICIÓN CRONOLÓGICA (80% pasado para Train, 20% futuro para Test)
    punto_corte = int(len(df) * 0.8)
    df_train = df.iloc[:punto_corte]
    df_test = df.iloc[punto_corte:]

    print(f"Entrenamiento: Desde {df_train['timestamp'].min()} hasta {df_train['timestamp'].max()}")
    print(f"Evaluación:    Desde {df_test['timestamp'].min()} hasta {df_test['timestamp'].max()}")

    X_train = df_train[["temperatura_c"]]
    y_train = df_train["potencia_activa_kw"]

    X_test = df_test[["temperatura_c"]]
    y_test = df_test["potencia_activa_kw"]

    # 2. PIPELINE ANTI-LEAKAGE: Escalador + Estimador unidos
    # El StandardScaler se ajusta SOLO con X_train durante el pipeline.fit()
    pipeline = Pipeline([
        ("escalador", StandardScaler()),
        ("regresor", Ridge(alpha=1.0))
    ])

    print("\nEntrenando Pipeline sobre datos de Train...")
    pipeline.fit(X_train, y_train)

    print("Evaluando predicción sobre datos futuros de Test...")
    y_pred = pipeline.predict(X_test)
    error_rmse = root_mean_squared_error(y_test, y_pred)
    print(f"Error RMSE en Test (Futuro no visto): {error_rmse:.3f} kW")

if __name__ == "__main__":
    particion_segura()
```

Ejecutamos el script:

```bash
python scripts/validar_particion_temporal.py
```

Observarás cómo el pipeline entrena sobre las primeras 800 horas del año y valida sobre las 200 horas subsiguientes con absoluta fidelidad metodológica.

---

## 5. Pruebas Automatizadas con Pytest

Creamos `tests/test_pipeline_temporal.py`:

```python
"""Pruebas para verificar ausencia de fugas de datos en el pipeline."""

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

def test_pipeline_no_data_leakage():
    X_train = pd.DataFrame({"temperatura": [10.0, 20.0, 30.0]})
    y_train = [15.0, 25.0, 35.0]
    X_test = pd.DataFrame({"temperatura": [40.0, 50.0]})

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge())
    ])
    pipe.fit(X_train, y_train)
    
    # La media del escalador debe ser exactamente la media de X_train (20.0), sin contaminarse con X_test
    scaler = pipe.named_steps["scaler"]
    assert scaler.mean_[0] == 20.0, "Fuga detectada: la media fue calculada fuera de X_train"
```

Ejecutamos las pruebas locales:

```bash
pytest tests/test_pipeline_temporal.py -v
```

---

## 6. Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. Si un modelo de predicción de demanda eléctrica obtiene un `R2 = 0.998` en pruebas iniciales, ¿por qué un ingeniero experimentado sospecha inmediatamente de fuga de datos antes de celebrar el resultado?
   - *Respuesta:* Porque en series temporales industriales reales existe ruido no determinístico (clima, eventos de red). Un ajuste casi perfecto suele delatar que una variable del futuro (como la medición real del consumo posterior) se incluyó inadvertidamente en la matriz de features.
2. ¿Qué diferencia crítica existe entre llamar a `.fit()` sobre todo el dataset o hacerlo exclusivamente dentro de las particiones de entrenamiento de un `Pipeline` de Scikit-Learn?
   - *Respuesta:* Si se ajusta el escalador sobre todo el dataset, la media y la varianza de los datos futuros (test) contaminan las transformaciones de entrenamiento, invalidando las garantías de generalización.

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente pipeline generado por un asistente de IA para predecir la carga eléctrica en subestaciones:

```python
# CÓDIGO CON BUG SUTIL GENERADO POR IA:
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Paso 1: Escalar características
scaler = StandardScaler()
X_escalado = scaler.fit_transform(X_telemetria_temporal)

# Paso 2: Particionar datos
X_train, X_test, y_train, y_test = train_test_split(
    X_escalado, y_demanda, test_size=0.2, shuffle=True, random_state=42
)
```

**Diagnóstico del Revisor Humano:**
1. **Doble Fuga de Datos:**
   - **Fuga 1:** `scaler.fit_transform()` se ejecutó antes de la partición, filtrando la media y desviación estándar del conjunto de test hacia el entrenamiento.
   - **Fuga 2:** `shuffle=True` destruye la causalidad temporal, mezclando muestras del futuro en el conjunto de entrenamiento. El modelo predecirá el pasado habiendo memorizado puntos adyacentes del futuro.
2. **Corrección Obligatoria en energy-ml:**
   ```python
   # 1. Partición estrictamente cronológica
   X_train, X_test, y_train, y_test = train_test_split(
       X_telemetria_temporal, y_demanda, test_size=0.2, shuffle=False
   )
   # 2. Ajuste de escala encapsulado únicamente sobre X_train
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)  # Solo transform(), nunca fit()
   ```

---

## 7. Conclusión del Capítulo 2 de la Unidad 2

Has incorporado las dos salvaguardas metodológicas más críticas de la Ciencia de Datos aplicada:
1. Reconocer la frontera entre la **deducción simbólica** de un asistente de IA y la **inducción empírica** de un modelo matemático.
2. Aplicar **particiones cronológicas rigurosas** y pipelines encapsulados para erradicar el **Data Leakage temporal** en series de tiempo de `energy-ml`.

En el **Capítulo 3**, entraremos de lleno en los modelos matemáticos de aprendizaje: comenzando con la **Clasificación Probabilística mediante el Teorema de Bayes** para diagnóstico predictivo de fallas eléctricas en subestaciones.
