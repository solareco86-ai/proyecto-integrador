# 3.2 Features temporales: extracción de hora, día, mes; ventanas deslizantes

## Objetivo

Extraer señales del tiempo para capturar ciclos (diario, semanal, estacional).

## Contenidos

### 1. Extracción de componentes

```python
import pandas as pd

df = pd.read_csv('data/raw/sensores_energia_2026.csv', parse_dates=['timestamp'])

# Hora, día, mes, año
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.day_name()
df['day_of_month'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['quarter'] = df['timestamp'].dt.quarter
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
df['is_holiday'] = ...  # Requiere calendario de feriados
```

### 2. Ventanas deslizantes (rolling windows)

```python
df = df.sort_values('timestamp')

# Media móvil (últimas 24 horas)
df['power_kw_rolling_24h'] = df['power_kw'].rolling(window=24).mean()

# Máximo en últimas 7 horas
df['power_kw_rolling_max_7h'] = df['power_kw'].rolling(window=7).max()

# Desviación estándar
df['power_kw_rolling_std_12h'] = df['power_kw'].rolling(window=12).std()
```

### 3. Lags de cambios

```python
# Cambio porcentual vs ayer
df['power_kw_pct_change_24h'] = df['power_kw'].pct_change(24)

# Diferencia vs mismo día semana anterior
df['power_kw_yoy_7d'] = df['power_kw'] - df['power_kw'].shift(7*24)
```

## Actividad práctica

Crear features temporales de tu dataset. Visualizar qué captures ciclos.

## Palabras clave

Datetime, hour, day, rolling, lag, seasonal, trend

## Referencias

- [Pandas datetime components](https://pandas.pydata.org/docs/user_guide/timeseries.html)
