# 2.1 Manejo de valores faltantes: detección, imputación y estrategias

## Objetivo

Estrategias principiadas para detectar, documentar y tratar valores faltantes (NaN, None) sin introducir sesgos. Aprender cuándo imputar, cuándo eliminar, y cómo documentar cada decisión en la capa `application/` (spec).

## Contenidos

### 1. Detección y cuantificación

**¿Cuándo aparecen?**
- Fallos de sensores (ej: sensor energético desconectado por 2 horas)
- No participación académica (estudiante ausente a clase)
- Truncamiento en exportación (últimos días del mes incompletos)
- Corrupción de datos (valor ilegible)

```python
import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv('data/raw/sensores_energia_2026.csv', parse_dates=['timestamp'])

# Cantidad de nulos POR COLUMNA
print(df.isnull().sum())
# timestamp           0
# facility_id         5
# power_kw           12
# voltage_v           0
# current_a           3

# Porcentaje de completitud
print((df.isnull().sum() / len(df) * 100).round(2))
# timestamp        0.00%
# facility_id      0.05%
# power_kw         0.12%
# voltage_v        0.00%
# current_a        0.03%

# ¿Qué filas tienen AL MENOS UN nulo?
incomplete_rows = df[df.isnull().any(axis=1)]
print(f"Filas incompletas: {len(incomplete_rows)} / {len(df)}")

# Visualizar patrón (¿son aleatorios o sistemáticos?)
df.isnull().sum().plot(kind='barh')
```

**Caso académico:**
```python
# Cargar eventos LMS
academic_df = pd.read_csv('data/raw/eventos_academicos.csv')

# Análisis de ausencias
print(academic_df.isnull().sum())

# Estudiantes con datos faltantes
null_by_student = academic_df.groupby('student_id').apply(lambda x: x.isnull().sum()).sum(axis=1)
print(null_by_student.sort_values(ascending=False).head(10))
# Pregunta: ¿Los estudiantes con muchos nulos son los que se retiraron?
```

### 2. Estrategias de imputación

#### 2.1 Eliminación (¿cuándo es válida?)

**Criterio:** Eliminar fila/columna si **> 30-40%** de datos faltantes O si el patrón es *Missing Completely At Random* (MCAR).

```python
# Eliminar columnas con > 50% nulos
df_clean = df.dropna(thresh=len(df)*0.5, axis=1)

# Eliminar filas con AL MENOS UN nulo
df_clean = df.dropna(axis=0)  # ⚠️ Cuidado: puede eliminar demasiado

# Eliminar solo si TODOS son nulos en la fila
df_clean = df.dropna(how='all', axis=0)

# Eliminar si falta una columna específica
df_clean = df.dropna(subset=['power_kw'], axis=0)
print(f"Filas eliminadas: {len(df) - len(df_clean)}")
```

**¿Cuándo usar?** Solo si:
1. La cantidad es < 5% del dataset, O
2. Los nulos representan observaciones realmente inválidas (ej: sensor que nunca funcionó)

#### 2.2 Imputación por media/mediana (para datos numéricos)

```python
from sklearn.impute import SimpleImputer

# Media (sensible a outliers)
imputer_mean = SimpleImputer(strategy='mean')
df['power_kw'] = imputer_mean.fit_transform(df[['power_kw']])

# Mediana (más robusto)
imputer_median = SimpleImputer(strategy='median')
df['current_a'] = imputer_median.fit_transform(df[['current_a']])

# Forward fill (series temporales): usar valor anterior
df.loc[df['power_kw'].isnull(), 'power_kw'] = df['power_kw'].fillna(method='ffill')

# Backward fill: usar valor siguiente
df['facility_id'] = df['facility_id'].fillna(method='bfill')
```

**Caso académico:**
```python
# Imputar notas faltantes con media del grupo
academic_df['score'] = academic_df.groupby('course_id')['score'].transform(
    lambda x: x.fillna(x.mean())
)
```

⚠️ **Riesgo:** Imputar con media introduce **sesgo hacia la central** (reduce varianza).

#### 2.3 Imputación por valor constante

```python
# Llenar con un valor específico
df['facility_id'] = df['facility_id'].fillna('UNKNOWN')
df['power_kw'] = df['power_kw'].fillna(0)  # ⚠️ Solo si 0 es significativo

# Llenar solo ciertos grupos
df['score'] = df.groupby('carrera')['score'].transform(
    lambda x: x.fillna(x.median())
)
```

**Caso académico:**
```python
# Estudiante ausente a clase → score = 0 (no participó)
academic_df['participation_score'] = academic_df['participation_score'].fillna(0)
```

#### 2.4 Imputación KNN (valores vecinos)

```python
from sklearn.impute import KNNImputer

# Llenar basado en los K vecinos más cercanos (por características)
imputer_knn = KNNImputer(n_neighbors=5)
df_imputed = pd.DataFrame(
    imputer_knn.fit_transform(df[['power_kw', 'voltage_v', 'current_a']]),
    columns=['power_kw', 'voltage_v', 'current_a']
)

# Ventaja: preserva estructura y relaciones
# Desventaja: computacionalmente costoso en datasets grandes
```

#### 2.5 Modelo predictivo (MICE)

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Multiple Imputation by Chained Equations
imputer_mice = IterativeImputer(max_iter=10, random_state=42)
df_imputed = pd.DataFrame(
    imputer_mice.fit_transform(df[['power_kw', 'voltage_v', 'current_a']]),
    columns=['power_kw', 'voltage_v', 'current_a']
)

# Más sofisticado pero también más lento
```

### 3. Documentación según Clean Architecture (spec)

**Capa domain/ (value objects, sin dependencias):**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EnergyReading:
    """Registro de consumo energético con metadatos de limpieza"""
    timestamp: str  # ISO 8601
    power_kw: float
    voltage_v: float
    current_a: float
    was_imputed: bool = False
    imputation_method: str = ""
```

**Capa application/services/ (lógica de negocio):**
```python
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataCleaningService:
    """Documenta TODAS las decisiones de imputación"""
    
    def clean_energy_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Limpia datos de sensores. Retorna: (df_limpio, metadata_limpieza)
        Ver: spec/backend/srs § Logging estructurado
        """
        metadata = {
            'rows_original': len(df),
            'null_counts_before': df.isnull().sum().to_dict(),
            'actions': []
        }
        
        # 1. Eliminar filas con nulos en timestamp (inaceptable)
        removed = df[df['timestamp'].isnull()]
        if len(removed) > 0:
            metadata['actions'].append({
                'column': 'timestamp',
                'action': 'dropped',
                'count': len(removed),
                'reason': 'timestamp es identificador único, no puede faltar'
            })
            logger.warning(f"Dropped {len(removed)} rows with missing timestamp")
        df = df.dropna(subset=['timestamp'])
        
        # 2. Imputar power_kw con mediana horaria
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['power_kw'] = df.groupby('hour')['power_kw'].transform(
            lambda x: x.fillna(x.median())
        )
        metadata['actions'].append({
            'column': 'power_kw',
            'action': 'imputed',
            'method': 'median_by_hour',
            'reason': 'consumo sigue patrón horario; preserva ciclo diario'
        })
        logger.info(f"Imputed power_kw using median_by_hour")
        
        # 3. Eliminar filas residuales con nulos
        remaining_nulls = df.isnull().sum().sum()
        if remaining_nulls > 0:
            df = df.dropna()
            metadata['actions'].append({
                'action': 'dropped_remaining_nulls',
                'count': remaining_nulls
            })
            logger.info(f"Dropped {remaining_nulls} remaining null values")
        
        metadata['rows_final'] = len(df)
        metadata['null_counts_after'] = df.isnull().sum().to_dict()
        
        return df, metadata
```

### 4. Validación: ¿mi imputación fue aceptable?

```python
import matplotlib.pyplot as plt

# Comparar distribuciones ANTES y DESPUÉS
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Antes (con nulos)
df_before = pd.read_csv('data/raw/sensores_energia_2026.csv')
axes[0].hist(df_before['power_kw'].dropna(), bins=30, alpha=0.7, color='blue')
axes[0].set_title('Distribución ANTES (con nulos)')
axes[0].set_ylabel('Frecuencia')

# Después (imputado)
axes[1].hist(df_imputed['power_kw'], bins=30, alpha=0.7, color='green')
axes[1].set_title('Distribución DESPUÉS (imputado)')
axes[1].set_ylabel('Frecuencia')

plt.tight_layout()
plt.show()

# Comparar estadísticas
print("ANTES (sin nulos):")
print(df_before['power_kw'].describe())
print("\nDESPUÉS (imputado):")
print(df_imputed['power_kw'].describe())

# ¿Cambió mucho la media/std/percentiles? Si sí, revisar estrategia
```

## Actividad práctica

**Tarea:** Tomar tu dataset, elegir una estrategia de imputación, documentar y validar:

```python
import pandas as pd

# Paso 1: Cargar y diagnosticar
df = pd.read_csv('tu_archivo.csv', parse_dates=['timestamp'])
print(f"Nulos totales: {df.isnull().sum().sum()}")

# Paso 2: Aplicar estrategia
service = DataCleaningService()
df_clean, metadata = service.clean_energy_data(df)

# Paso 3: Documentar
print("METADATA DE LIMPIEZA:")
for action in metadata['actions']:
    print(f"  - {action}")

# Paso 4: Validar
print(f"\nFILAS: {metadata['rows_original']} → {metadata['rows_final']}")
print(f"NULOS DESPUÉS: {metadata['null_counts_after']}")
```

## Palabras clave

Valores faltantes, NaN, imputación, media, mediana, forward fill, KNN, MICE, documentación, logging, validación, bias

## Referencias

- [Pandas dropna/fillna](https://pandas.pydata.org/docs/reference/frame.html#missing-data-handling)
- [scikit-learn Imputers](https://scikit-learn.org/stable/modules/impute.html)
- [spec § Logging estructurado](https://github.com/datamaq-automation/spec/blob/main/backend/srs-spec-backend-fastapi.md)
