# 1.2 Exploración con Pandas: shape, dtypes, describe(), isnull()

## Objetivo

Desarrollar habilidades de **exploración inicial** de conjuntos de datos usando Pandas. Comprender la estructura, tipos de datos, distribuciones y valores faltantes de nuestras fuentes antes de proceder a la limpieza.

## Contenidos

### 1. Estructura básica del DataFrame

Una vez cargados los datos en un DataFrame de Pandas, lo primero es entender su **forma y composición**.

#### Atributos fundamentales

```python
import pandas as pd

# Cargar datos
df = pd.read_csv('data/raw/sensores_energia_2026.csv', parse_dates=['timestamp'])

# 1. SHAPE: dimensiones (filas, columnas)
print(f"Dimensiones: {df.shape}")  # (10000, 5) = 10000 filas, 5 columnas

# 2. COLUMNAS: nombres y orden
print(f"Columnas: {df.columns.tolist()}")
# ['timestamp', 'facility_id', 'power_kw', 'voltage_v', 'current_a']

# 3. ÍNDICE: valores de fila
print(f"Índice (primeros 5): {df.index[:5].tolist()}")

# 4. MEMORIA: tamaño en bytes
print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
```

### 2. Tipos de datos (dtypes)

Verificar que cada columna tenga el tipo correcto es crítico para análisis posteriores.

```python
# Verificar tipos
print(df.dtypes)
# timestamp       datetime64[ns]
# facility_id            object
# power_kw              float64
# voltage_v             float64
# current_a             float64

# Acceder a una columna específica
print(df['power_kw'].dtype)  # dtype('float64')

# Convertir tipos si es necesario
df['facility_id'] = df['facility_id'].astype(str)  # Forzar a string
df['timestamp'] = pd.to_datetime(df['timestamp'])   # Forzar a datetime
```

**Tipos comunes en Pandas:**
| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `int64` | Entero | 2, -5, 100 |
| `float64` | Número decimal | 2.5, -3.14 |
| `object` | String/texto | 'EDENOR', 'STU001' |
| `datetime64` | Fecha y hora | 2026-10-01 08:15:00 |
| `bool` | Booleano | True, False |
| `category` | Categórico (eficiente) | 'A', 'B', 'C' |

### 3. Valores faltantes (isnull / isna)

Detectar valores faltantes es el primer paso de la limpieza.

```python
# Contar NaN en cada columna
print(df.isnull().sum())
# timestamp       0
# facility_id     5
# power_kw       12
# voltage_v       0
# current_a       3

# Porcentaje de valores faltantes
print((df.isnull().sum() / len(df) * 100).round(2))
# timestamp       0.00%
# facility_id     0.05%
# power_kw        0.12%
# voltage_v       0.00%
# current_a       0.03%

# Filas con al menos un valor faltante
print(f"Filas incompletas: {df.isnull().any(axis=1).sum()}")  # 18

# Matriz visual de valores faltantes
import matplotlib.pyplot as plt
df.isnull().sum().plot(kind='barh')
plt.title('Valores faltantes por columna')
plt.show()
```

### 4. Estadísticas descriptivas (describe)

La función `describe()` proporciona un resumen rápido de distribuaciones.

```python
# Estadísticas de columnas numéricas
print(df.describe())
#         power_kw    voltage_v  current_a
# count    9988.00     10000.00    9997.00
# mean        2.45       230.15       10.67
# std         1.23         0.89        2.34
# min         0.10       220.00        0.50
# 25%         1.80       230.00        9.20
# 50%         2.30       230.20       10.50
# 75%         3.10       230.30       12.10
# max        15.80       235.00       18.90

# Estadísticas de todas las columnas (incluyendo object)
print(df.describe(include='all'))

# Estadísticas personalizadas
print(df['power_kw'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]))
# 0.05    0.55
# 0.25    1.80
# 0.50    2.30
# 0.75    3.10
# 0.95    5.20
```

### 5. Exploración por grupos

En datos académicos, frecuentemente exploramos por estudiante, carrera, etc.

```python
# Datos académicos: agrupación por estudiante
eventos_df = pd.read_csv('data/raw/eventos_academicos.csv')

# Eventos por estudiante
print(eventos_df.groupby('student_id').size().describe())
# count     150.00
# mean       50.23
# std        25.14
# min         1.00
# 25%       35.00
# 50%       50.00
# 75%       65.00
# max      200.00

# Promedio de score por carrera
print(eventos_df.groupby('course_id')['score'].agg(['count', 'mean', 'std']))
```

### 6. Detección de anomalías iniciales

```python
# Valores fuera de rango esperado
print((df['power_kw'] < 0).sum())  # ¿Hay potencia negativa? (anomalía)
print((df['voltage_v'] > 250).sum())  # ¿Voltaje muy alto?

# Duplicados
print(f"Filas duplicadas: {df.duplicated().sum()}")
print(f"Duplicados en timestamp + facility_id: {df.duplicated(subset=['timestamp', 'facility_id']).sum()}")

# Inconsistencias de tipo
# Si 'power_kw' tiene strings como '2.5a' o 'N/A', será dtype='object'
if df['power_kw'].dtype == 'object':
    print("⚠️ ALERTA: power_kw debería ser numérico pero es object")
    print(df[~df['power_kw'].apply(lambda x: isinstance(x, (int, float)))]['power_kw'].unique())
```

## Actividad práctica

**Tarea:** Explorar el dataset asignado (energético o académico) y crear un reporte de 5-10 puntos:

```python
import pandas as pd

# 1. Cargar datos
df = pd.read_csv('tu_archivo.csv', parse_dates=['columna_fecha'])

print("=" * 60)
print("REPORTE DE EXPLORACIÓN DE DATOS")
print("=" * 60)

# 2. Dimensiones
print(f"\n1. Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")

# 3. Tipos de datos
print(f"\n2. Tipos de datos:\n{df.dtypes}")

# 4. Valores faltantes
print(f"\n3. Valores faltantes:\n{df.isnull().sum()}")
print(f"   Porcentaje: {(df.isnull().sum() / len(df) * 100).round(2)}")

# 5. Estadísticas
print(f"\n4. Estadísticas descriptivas:\n{df.describe()}")

# 6. Filas únicas por campo de identidad
print(f"\n5. Valores únicos:\n{df.nunique()}")

# 7. Duplicados
print(f"\n6. Filas duplicadas: {df.duplicated().sum()}")

# 8. Anomalías iniciales
print(f"\n7. Anomalías detectadas:")
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    outliers = ((df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)).sum()
    print(f"   {col}: {outliers} outliers (IQR method)")

print("\n" + "=" * 60)
```

## Palabras clave

Exploración de datos (EDA), dtypes, valores faltantes, NaN, describe(), quantiles, anomalías, outliers, estadísticas descriptivas

## Referencias

- [Pandas info() y describe()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
- [Pandas isnull()](https://pandas.pydata.org/docs/reference/api/pandas.isnull.html)
- [Detección de outliers con IQR](https://en.wikipedia.org/wiki/Interquartile_range)
