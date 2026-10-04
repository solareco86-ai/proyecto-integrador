# 2.2 Detección y tratamiento de outliers, validación de rangos

## Objetivo

Identificar y manejar valores anómalos (outliers) que distorsionan modelos. Diferenciar entre outliers válidos (eventos reales) e inválidos (errores de sensor).

## Contenidos

### 1. Métodos de detección

#### 1.1 IQR (Interquartile Range)

**Criterio:** Outlier si `x < Q1 - 1.5×IQR` o `x > Q3 + 1.5×IQR`

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data/raw/sensores_energia_2026.csv')

Q1 = df['power_kw'].quantile(0.25)
Q3 = df['power_kw'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_mask = (df['power_kw'] < lower_bound) | (df['power_kw'] > upper_bound)
print(f"Outliers (IQR): {outliers_mask.sum()}")
```

#### 1.2 Z-score

**Criterio:** Outlier si `|z| > 3`

```python
from scipy import stats

z_scores = np.abs(stats.zscore(df['power_kw'].dropna()))
outliers_mask = z_scores > 3
print(f"Outliers (Z>3): {outliers_mask.sum()}")
```

#### 1.3 Isolation Forest

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(contamination=0.05, random_state=42)
outlier_labels = iso_forest.fit_predict(df[['power_kw', 'voltage_v', 'current_a']])
outliers_mask = outlier_labels == -1
```

### 2. ¿Error o evento real?

```python
# Análisis contextual: ¿hay patrón?
picos = df[df['power_kw'] > 40]
print(picos[['timestamp', 'facility_id', 'day_of_week']])
# Si patrón → mantener. Si aleatorio → investigar sensor.
```

### 3. Estrategias de tratamiento

#### 3.1 Eliminar (cautela)

```python
df_clean = df[(df['power_kw'] >= lower_bound) & (df['power_kw'] <= upper_bound)]
```

#### 3.2 Capping (limitar a percentiles)

```python
p5, p95 = df['power_kw'].quantile([0.05, 0.95])
df['power_kw_capped'] = df['power_kw'].clip(p5, p95)
```

#### 3.3 Marcar (recomendado)

```python
df['is_outlier'] = outliers_mask
# Modelos robustos (RF, XGBoost) pueden entrenar con esta bandera
```

### 4. Validación de rangos (lógica de negocio)

```python
def validate_energy_reading(power_kw: float, voltage_v: float, current_a: float) -> tuple[bool, str]:
    if not (0 <= power_kw <= 100):
        return False, f"power_kw={power_kw} fuera de [0, 100]"
    if not (200 <= voltage_v <= 250):
        return False, f"voltage_v={voltage_v} fuera de [200, 250]"
    
    expected_power = voltage_v * current_a * 0.9 / 1000
    if abs(power_kw - expected_power) > 10:
        return False, f"power_kw no concuerda con V×I"
    
    return True, "OK"
```

## Actividad práctica

Detectar outliers con 3 métodos, visualizar, decidir estrategia, documentar.

## Palabras clave

Outliers, IQR, Z-score, Isolation Forest, capping, validación, anomalías

## Referencias

- [scipy.stats.zscore](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html)
- [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
