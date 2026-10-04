# 3.1 Ingeniería de features: derivación, composición, agregación

## Objetivo

Crear nuevas variables que capturen patrones y relaciones. La mayoría del tiempo en ML se va aquí, no en el modelado.

## Contenidos

### 1. Derivación de features

```python
import pandas as pd

df = pd.read_csv('data/raw/sensores_energia_2026.csv')

# Crear nuevas variables
df['power_per_voltage'] = df['power_kw'] / df['voltage_v']
df['power_per_current'] = df['power_kw'] / df['current_a']
df['pf_squared'] = df['pf'] ** 2
df['power_kw_squared'] = df['power_kw'] ** 2

# Ratios
df['efficiency_ratio'] = df['current_a'] / (df['power_kw'] + 1)  # +1 evita división por 0
```

### 2. Agregaciones

```python
# Por hora del día: consumo promedio
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
hourly_avg = df.groupby('hour')['power_kw'].mean()
df = df.merge(hourly_avg.rename('avg_power_by_hour'), left_on='hour', right_index=True)

# Por estudiante: promedio de asistencias
academic_df = pd.read_csv('data/raw/eventos_academicos.csv')
student_avg = academic_df.groupby('student_id')['score'].mean()
academic_df = academic_df.merge(student_avg.rename('avg_score'), left_on='student_id', right_index=True)
```

### 3. Lag features (pasado)

```python
# Valor de hace N períodos
df = df.sort_values('timestamp')
df['power_kw_lag1'] = df['power_kw'].shift(1)  # Hace 1 período
df['power_kw_lag12'] = df['power_kw'].shift(12)  # Hace 12 períodos

# Diferencia respecto a período anterior
df['power_kw_diff'] = df['power_kw'].diff()
```

### 4. Interacciones

```python
# Si dos variables interactúan
df['voltage_current_interaction'] = df['voltage_v'] * df['current_a']
df['high_power_evening'] = (df['power_kw'] > 30) & (df['hour'] >= 18)
```

## Actividad práctica

Crear 5 nuevas features, justificar cada una, comparar su correlación con target.

## Palabras clave

Feature engineering, derivación, agregación, lag, interacción, domain knowledge

## Referencias

- [Pandas groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)
- [tsfresh para features temporales](https://tsfresh.readthedocs.io/)
