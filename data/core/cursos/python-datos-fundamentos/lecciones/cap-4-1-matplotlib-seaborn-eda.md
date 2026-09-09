### Visualización para entender los datos

La visualización es la forma más rápida de detectar patrones, valores atípicos y relaciones. **Matplotlib** es la librería base de gráficos; **Seaborn** la complementa con gráficos estadísticos de alto nivel y estética cuidada.

Continuamos con el **caso de estudio del dataset `data/core/datasets/curvas_de_carga.csv`** (telemetría de variadores de frecuencia), aplicando un Análisis Exploratorio de Datos (EDA) sobre el consumo energético.

### Carga y preparación

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/core/datasets/curvas_de_carga.csv", parse_dates=["timestamp"])
df["hora"] = df["timestamp"].dt.hour
print(df.head())
```

### Curva de carga diaria

El primer gráfico revela el perfil de consumo del conjunto:

```python
perfil = df.groupby("hora")["potencia_kw"].mean()

plt.figure(figsize=(10, 5))
plt.plot(perfil.index, perfil.values, marker="o")
plt.title("Curva de carga promedio (potencia por hora)")
plt.xlabel("Hora")
plt.ylabel("Potencia promedio (kW)")
plt.grid(True)
plt.show()
```

Se observan los picos de mañana y tarde propios de una planta industrial, y los valles nocturnos.

### Gráficos estadísticos con Seaborn

```python
# Histograma de la potencia
sns.histplot(df["potencia_kw"], bins=20)
plt.title("Distribución de la potencia activa")
plt.show()

# Diagrama de caja por sensor
sns.boxplot(data=df, x="id_sensor", y="potencia_kw")
plt.title("Potencia por variador de frecuencia")
plt.show()

# Relación entre temperatura y potencia
sns.scatterplot(data=df, x="potencia_kw", y="temperatura_c", hue="id_sensor")
plt.title("Temperatura del inverter vs potencia")
plt.show()
```

### Análisis Exploratorio de Datos (EDA) completo

El **EDA** es el proceso de investigar los datos antes de modelar:

```python
# 1. Dimensiones y tipos
print(df.shape)
print(df.dtypes)

# 2. Datos faltantes
print(df.isna().sum())

# 3. Resumen estadístico
print(df.describe())

# 4. Distribución de variables
df.hist(column=["potencia_kw", "temperatura_c", "corriente_a"], figsize=(10, 6))
plt.tight_layout()
plt.show()

# 5. Correlaciones
corr = df[["potencia_kw", "tension_v", "corriente_a", "factor_potencia", "temperatura_c"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f")
plt.show()
```

### Interpretación de hallazgos

| Hallazgo típico en el dataset | Posible acción |
| :--- | :--- |
| Picos de consumo en mañana/tarde | Programar el mantenimiento fuera de esas horas |
| Valores atípicos de potencia | Investigar eventos como el del `vfd-01` (posible falla) |
| Alta correlación potencia-temperatura | Monitorear el inverter como señal predictiva |
| Sensor detenido (`estado_vfd = 0`) | Filtrarlo en los análisis de rendimiento |

### Micro-desafío práctico

> Cargá `curvas_de_carga.csv`, generá un histograma de `potencia_kw` separado por `id_sensor` y un gráfico de líneas de la curva de carga del sensor `vfd-01`. Documentá con una celda Markdown qué patrones observaste.

### Resumen

- Matplotlib es la base para gráficos de línea, barras e histogramas.
- Seaborn agrega gráficos estadísticos de alto nivel.
- El EDA combina estadísticos, distribución y correlaciones.
- El dataset de curvas de carga conecta la visualización con el dominio energético del catálogo.
