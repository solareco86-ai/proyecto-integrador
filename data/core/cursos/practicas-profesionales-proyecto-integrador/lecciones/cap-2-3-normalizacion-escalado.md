# 2.3 Normalización y escalado: StandardScaler, MinMaxScaler, Log transform

## Objetivo

Transformar variables numéricas a escalas comparables. Esencial para algoritmos de ML que usan distancia (KNN, K-means) o descenso de gradiente (regresión lineal, redes neuronales).

## Contenidos

### 1. ¿Por qué escalar?

**Problema:** Variables con rangos muy diferentes distorsionan modelos.

```python
import pandas as pd

df = pd.read_csv('data/raw/sensores_energia_2026.csv')

# Rangos dispares:
print(df.describe())
#        power_kw    voltage_v   current_a
# min        0.10       200.00         0.50
# max       50.00       250.00       220.00
# std        5.00        10.00        50.00

# En KNN: 1 unidad de voltage (V) influye más que 1 unidad de power (kW)
# En Regresión: escala afecta coeficientes e intercepto
```

### 2. StandardScaler (media=0, std=1)

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[['power_kw', 'voltage_v', 'current_a']]),
    columns=['power_kw', 'voltage_v', 'current_a']
)

print(df_scaled.describe())
# Ahora: media ≈ 0, std ≈ 1 para todas
```

**Fórmula:** `x_scaled = (x - mean) / std`

### 3. MinMaxScaler (rango [0, 1])

```python
from sklearn.preprocessing import MinMaxScaler

scaler_minmax = MinMaxScaler(feature_range=(0, 1))
df_scaled = pd.DataFrame(
    scaler_minmax.fit_transform(df[['power_kw', 'voltage_v', 'current_a']]),
    columns=['power_kw', 'voltage_v', 'current_a']
)

# Ahora: min=0, max=1 para todas
```

**Fórmula:** `x_scaled = (x - min) / (max - min)`

### 4. Log Transform (para datos sesgados)

```python
import numpy as np

# Si power_kw está muy sesgado a derecha (cola larga)
df['power_kw_log'] = np.log1p(df['power_kw'])  # log(1 + x)

# Ahora es más simétrico → mejor para modelos
```

### 5. Paso correcto: FIT en train, APPLY en test

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df[['power_kw', 'voltage_v']], df['power_kw'], test_size=0.2)

# ✓ CORRECTO: FIT solo en train
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ✗ INCORRECTO: FIT en todo, luego split
scaler_wrong = StandardScaler()
scaler_wrong.fit(df[['power_kw', 'voltage_v']])  # Data leakage!
```

## Actividad práctica

Escalar tu dataset usando 3 métodos, comparar distribuciones.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

df = pd.read_csv('tu_archivo.csv')

# StandardScaler
scaler1 = StandardScaler()
df_std = pd.DataFrame(scaler1.fit_transform(df[['col1', 'col2']]), columns=['col1', 'col2'])

# MinMaxScaler
scaler2 = MinMaxScaler()
df_minmax = pd.DataFrame(scaler2.fit_transform(df[['col1', 'col2']]), columns=['col1', 'col2'])

# Comparar
print("Original:", df.describe())
print("StandardScaler:", df_std.describe())
print("MinMaxScaler:", df_minmax.describe())
```

## Palabras clave

Escalado, normalización, StandardScaler, MinMaxScaler, Log transform, data leakage, train-test

## Referencias

- [scikit-learn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
