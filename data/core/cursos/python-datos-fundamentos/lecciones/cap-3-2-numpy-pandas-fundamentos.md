### La dupla NumPy + Pandas

**NumPy** aporta arrays multidimensionales y operaciones vectoriales de alto rendimiento. **Pandas** se construye sobre NumPy y ofrece estructuras tabulares (Series y DataFrames) pensadas para datos estructurados. Juntas son el núcleo del análisis de datos en Python.

En este curso trabajaremos con un **caso de estudio real**: el dataset `data/core/datasets/curvas_de_carga.csv`, que contiene registros de telemetría industrial de variadores de frecuencia (VFD). Cada fila es una medición horaria de potencia, tensión, corriente, factor de potencia y temperatura, que se integra con el dominio energético del catálogo.

### NumPy: operaciones vectoriales

```python
import numpy as np

# Array unidimensional
consumos = np.array([45.2, 47.1, 46.8, 45.9])

# Operaciones vectorizadas (sin bucles explícitos)
consumos_escala = consumos * 1.1
print(consumos_escala)

# Estadísticas básicas
print(consumos.mean())
print(consumos.max())
print(np.percentile(consumos, 90))
```

### Pandas: Series y DataFrame

La **Series** es una columna etiquetada:

```python
import pandas as pd

s = pd.Series([45.2, 47.1, 46.8], index=["lun", "mar", "mié"])
print(s["mar"])
```

El **DataFrame** es una tabla con filas y columnas. Cargá el dataset de curvas de carga:

```python
import pandas as pd

df = pd.read_csv("data/core/datasets/curvas_de_carga.csv")
print(df.head())
print(df.shape)  # (504, 8): 504 mediciones y 8 columnas
```

Cada columna corresponde a una variable del dominio:

| Columna | Descripción |
| :--- | :--- |
| `timestamp` | Fecha y hora de la medición |
| `id_sensor` | Identificador del VFD (`vfd-01`, `vfd-02`, `vfd-03`) |
| `potencia_kw` | Potencia activa consumida |
| `tension_v` | Tensión de línea |
| `corriente_a` | Corriente por fase |
| `factor_potencia` | Factor de potencia |
| `temperatura_c` | Temperatura del inverter |
| `estado_vfd` | 1 en operación, 0 detenido |

### Operaciones básicas con DataFrames

```python
# Ver las primeras filas
df.head()

# Resumen estadístico
df.describe()

# Seleccionar una columna
df["potencia_kw"]

# Filtrar filas con alta potencia
df[df["potencia_kw"] > 40]

# Agrupar por sensor y promediar
df.groupby("id_sensor")["potencia_kw"].mean()
```

### Agregación por hora

El `timestamp` permite extraer la hora y estudiar la **curva de carga diaria**:

```python
df["hora"] = pd.to_datetime(df["timestamp"]).dt.hour

# Potencia promedio por hora, considerando todos los sensores
perfil_horario = df.groupby("hora")["potencia_kw"].mean()
print(perfil_horario)
```

Este perfil muestra los picos de consumo de mañana y tarde, y los valles nocturnos: el patrón típico de una planta industrial.

### Carga y guardado de datos

```python
# Leer el CSV con un parseo de fechas correcto
df = pd.read_csv("data/core/datasets/curvas_de_carga.csv", parse_dates=["timestamp"])

# Guardar el resultado procesado
df.to_csv("data/consumo_procesado.csv", index=False)
```

### Ventajas de las operaciones vectoriales

| Enfoque | Ejemplo | Eficiencia |
| :--- | :--- | :--- |
| Bucle Python | `for i in range(len(x))` | Lento en datos grandes |
| Vectorizado NumPy | `x * 1.1` | Mucho más rápido |

### Micro-desafío práctico

> Cargá `curvas_de_carga.csv`, calculá la potencia promedio por hora para el sensor `vfd-01` y guardá el resultado en `data/perfil_vfd01.csv`. Identificá la hora de mayor consumo.

### Resumen

- NumPy permite operaciones vectoriales de alto rendimiento.
- Pandas ofrece Series (columna) y DataFrame (tabla).
- `head()`, `describe()`, filtrado y `groupby` son operaciones esenciales.
- `read_csv` y `to_csv` conectan tus datos con el mundo exterior.
- El dataset `curvas_de_carga.csv` es el hilo conductor entre este curso y el dominio energético.
