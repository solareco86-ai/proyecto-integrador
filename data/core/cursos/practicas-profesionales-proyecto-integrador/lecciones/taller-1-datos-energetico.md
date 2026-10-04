# Taller 1: Ingesta y preprocesamiento de datos de sensores energéticos

## Objetivo

Integrar los aprendizajes de la Unidad 1 (Caps 1-3) en un proyecto fin con entrega evaluada.

**Entrega:** Dataset preprocesado y limpio, listo para modelado. Metadata de decisiones documentada.

## Proyecto: Pipeline de datos energéticos

### Fase 1: Ingesta (Cap 1)

```python
import pandas as pd
from src.infrastructure.integrations.csv_loader import CSVDataLoader

# Cargar sensores
df_sensores = CSVDataLoader.load_energy_sensors('data/raw/sensores_2026.csv')
print(f"Sensores: {df_sensores.shape}")

# Cargar facturas OCR (preprocesadas en Cap 2, aquí usamos CSV)
df_facturas = pd.read_csv('data/processed/facturas_parsed_2026.csv')
```

### Fase 2: Exploración (Cap 1.3)

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Visualizar distribuciones
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(data=df_sensores, x='power_kw', kde=True, ax=axes[0,0])
sns.boxplot(data=df_sensores, y='voltage_v', ax=axes[0,1])
sns.scatterplot(data=df_sensores, x='timestamp', y='power_kw', ax=axes[1,0])

plt.tight_layout()
plt.savefig('exploracion_sensores.png')
```

### Fase 3: Limpieza (Caps 2.1-2.3)

```python
from src.application.services.data_cleaning_service import DataCleaningService

service = DataCleaningService()
df_clean, metadata = service.clean_energy_data(df_sensores)

print("Reporte de limpieza:")
for action in metadata['actions']:
    print(f"  - {action}")
```

### Fase 4: Feature Engineering (Cap 3)

```python
# Agregar features temporales
df_clean['hour'] = pd.to_datetime(df_clean['timestamp']).dt.hour
df_clean['day_of_week'] = pd.to_datetime(df_clean['timestamp']).dt.day_name()

# Lags
df_clean['power_lag1'] = df_clean['power_kw'].shift(1)

# Rolling
df_clean['power_rolling_24h'] = df_clean['power_kw'].rolling(24).mean()
```

### Fase 5: Selección de Features (Cap 3.3)

```python
from sklearn.ensemble import RandomForestRegressor

X = df_clean[['voltage_v', 'current_a', 'hour', 'day_of_week', 'power_lag1', 'power_rolling_24h']]
y = df_clean['power_kw']

rf = RandomForestRegressor()
rf.fit(X, y)

importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Top features:", importances.head())
```

## Entrega esperada

1. **Dataset limpio:** `data/processed/sensores_pp_clean_2026.csv`
2. **Metadata:** `data/processed/metadata_limpieza_2026.json`
   ```json
   {
     "rows_original": 10000,
     "rows_final": 9850,
     "null_counts": {...},
     "outliers_handled": 5,
     "features_engineered": 8
   }
   ```
3. **Informe corto:** documento Markdown explicando decisiones
4. **Gráficos:** antes/después de limpieza

## Criterios de evaluación

- ✓ Dataset sin valores faltantes
- ✓ Outliers detectados y documentados
- ✓ Features relevantes creadas (correlación o importancia > 0.05)
- ✓ Metadata de decisiones completa
- ✓ Código limpio, tipado (spec)
- ✓ Reproducible: same input → same output

## Palabras clave

Pipeline, ETL, limpieza, validación, reproducibilidad, documentación

