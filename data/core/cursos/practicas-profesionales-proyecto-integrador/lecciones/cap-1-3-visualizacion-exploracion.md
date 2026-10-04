# 1.3 Visualización exploratoria: histogramas, boxplots, scatter plots

## Objetivo

Desarrollar **intuición visual** sobre la estructura de datos antes de modelar. Detectar patrones, anomalías y distribuciones que los números solos no revelan.

## Contenidos

### 1. Librerías de visualización

| Librería | Casos de uso | Ventajas |
|----------|-------------|----------|
| **Matplotlib** | Gráficos estáticos, control fino | Bajo nivel, máxima flexibilidad |
| **Seaborn** | Histogramas, violin plots, heatmaps | Alto nivel, temas bonitos, estadísticas integradas |
| **Plotly** | Gráficos interactivos, dashboards | Interactividad, hover info, exportable a HTML |

En este curso usamos **Seaborn** (construcción rápida) + **Plotly** (para dashboards finales).

### 2. Histogramas y Distribuciones

**¿Qué son?** Muestran cómo se distribuyen los valores de una variable numérica.

#### Ejemplo: Distribución de consumo energético

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos (Cap 1.1)
df = pd.read_csv('data/raw/sensores_energia_2026.csv', parse_dates=['timestamp'])

# Histograma simple
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='power_kw', kde=True, bins=30, ax=ax)
ax.set_title('Distribución de Consumo Energético (kW)')
ax.set_xlabel('Potencia (kW)')
ax.set_ylabel('Frecuencia')
plt.show()

# Análisis: ¿Es gaussiana? ¿Sesgada? ¿Multimodal?
```

**Interpretación:**
- **Gaussiana (normal):** campana simétrica → datos típicos, sin patrones ocultos
- **Sesgada a derecha:** cola larga → hay picos de consumo extraordinarios
- **Bimodal:** dos picos → posible cambio de ciclo (ej: horario vs pico)

#### Ejemplo: Distribución de notas académicas

```python
# Cargar datos académicos
academic_df = pd.read_csv('data/raw/eventos_academicos.csv')

# Comparar distribuciones por carrera
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for idx, carrera in enumerate(academic_df['course_id'].unique()[:6]):
    datos = academic_df[academic_df['course_id'] == carrera]['score']
    sns.histplot(data=datos, kde=True, bins=20, ax=axes[idx])
    axes[idx].set_title(f'Notas: {carrera}')
    axes[idx].set_xlabel('Score')

plt.tight_layout()
plt.show()

# Pregunta: ¿Qué carreras son más difíciles? ¿Hay estudiantes que se quedan atrás?
```

### 3. Boxplots (diagrama de cajas)

**¿Qué es?** Resume distribución en 5 números: mín, Q1 (25%), mediana (50%), Q3 (75%), máx.

```python
# Boxplot: consumo por hora del día
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x='hour', y='power_kw', ax=ax)
ax.set_title('Consumo Energético por Hora del Día')
ax.set_xlabel('Hora')
ax.set_ylabel('Potencia (kW)')
plt.show()

# Interpretación:
# - Mediana: línea roja en caja = valor típico
# - Caja = 50% central de datos (Q1 a Q3)
# - Líneas = rango (min-max)
# - Puntos = outliers (fuera de 1.5×IQR)
```

**Caso académico:** Desempeño por carrera

```python
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=academic_df, x='course_id', y='score', ax=ax)
ax.set_title('Distribución de Notas por Carrera')
ax.set_ylabel('Score')
ax.axhline(y=70, color='r', linestyle='--', label='Promoción')
ax.legend()
plt.show()

# Pregunta: ¿Hay carreras con mucha variación? ¿Cuál es más consistente?
```

### 4. Scatter plots (diagramas de dispersión)

**¿Para qué?** Ver relación entre **dos variables numéricas**.

#### Energía: Consumo vs Voltaje

```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='voltage_v', y='power_kw', alpha=0.5, ax=ax)
ax.set_title('Relación: Voltaje vs Potencia')
ax.set_xlabel('Voltaje (V)')
ax.set_ylabel('Potencia (kW)')
plt.show()

# Análisis: ¿Hay correlación? ¿Es lineal o no?
# Si no hay correlación → significa que la potencia es independiente del voltaje
# (esperado: la ley de Ohm requiere I = P/V, pero no V directamente)
```

#### Academia: Horas de estudio vs Calificación

```python
# Crear variable: minutos totales estudiados por alumno
study_time = academic_df.groupby('student_id')['duration_min'].sum().reset_index()
study_time.columns = ['student_id', 'total_minutes']

# Juntar con scores promedio
student_scores = academic_df.groupby('student_id')['score'].mean().reset_index()
merged = study_time.merge(student_scores, on='student_id')

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=merged, x='total_minutes', y='score', ax=ax)
sns.regplot(data=merged, x='total_minutes', y='score', scatter=False, color='r', ax=ax)
ax.set_title('Horas de Estudio vs Calificación')
ax.set_xlabel('Minutos estudiados')
ax.set_ylabel('Score promedio')
plt.show()

# Pregunta: ¿Hay correlación? Si la hay, ¿es fuerte? ¿Hay outliers?
```

### 5. Heatmaps de Correlación

**¿Para qué?** Ver **todas las correlaciones** de una vez.

```python
# Matriz de correlación: variables energéticas
numeric_cols = ['power_kw', 'voltage_v', 'current_a', 'pf']
corr_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax, vmin=-1, vmax=1)
ax.set_title('Correlación entre Variables Energéticas')
plt.show()

# Interpretación:
# - Rojo oscuro: correlación positiva fuerte (+1)
# - Azul oscuro: correlación negativa fuerte (-1)
# - Blanco: sin correlación (0)
```

### 6. Detección de Anomalías Visuales

#### Método 1: Outliers en boxplot (visible)

```python
# Ya vimos arriba: puntos aislados fuera de los bigotes del boxplot
```

#### Método 2: Datos faltantes (heatmap de nulos)

```python
# Matriz de valores faltantes (Cap 1.2)
import missingno as msno

msno.matrix(df)
plt.show()

# Blanco = datos faltantes
# Negro = datos presentes
# Patrón: ¿los faltantes son aleatorios o sistemáticos?
```

#### Método 3: Anomalías temporales

```python
# Serie temporal: detectar cambios abruptos
df_sorted = df.sort_values('timestamp')

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_sorted['timestamp'], df_sorted['power_kw'], linewidth=0.5, alpha=0.7)
ax.set_title('Consumo Energético en el Tiempo')
ax.set_xlabel('Fecha')
ax.set_ylabel('Potencia (kW)')
ax.grid(True, alpha=0.3)
plt.show()

# Observación: ¿Hay patrones cíclicos (diarios, semanales)?
#              ¿Hay picos o caídas anormales?
#              ¿Hay tendencia a largo plazo?
```

### 7. Visualizaciones Comparativas (por grupo)

```python
# Energía: consumo por día de la semana
df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.day_name()

fig, ax = plt.subplots(figsize=(12, 6))
sns.violinplot(data=df, x='day_of_week', y='power_kw', ax=ax)
ax.set_title('Consumo por Día de la Semana (Violin Plot)')
ax.set_ylabel('Potencia (kW)')
plt.show()

# Violin plot combina: distribución (área) + boxplot (líneas)
# Pregunta: ¿Hay diferencia entre lunes-viernes vs fin de semana?
```

## Actividad práctica

**Tarea:** Crear 5 gráficos de exploración de tu dataset (energético o académico):

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Cargar tu dataset
df = pd.read_csv('tu_archivo.csv', parse_dates=['columna_fecha'])

# 1. Histograma de variable principal
sns.histplot(data=df, x='tu_columna', kde=True, bins=30)
plt.title('Distribución de tu variable principal')
plt.show()

# 2. Boxplot por grupos
sns.boxplot(data=df, x='grupo', y='tu_variable')
plt.show()

# 3. Scatter plot de dos variables
sns.scatterplot(data=df, x='var1', y='var2')
plt.show()

# 4. Correlación
df.corr().round(2)

# 5. Heatmap de correlación
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.show()

# Preguntas:
# - ¿Qué distribuciones detectas?
# - ¿Hay outliers visibles?
# - ¿Hay correlaciones fuertes?
# - ¿Hay patrones por grupos?
```

## Palabras clave

Exploración visual, histogramas, distribuciones, boxplots, scatter plots, correlación, heatmaps, detección de anomalías, EDA (Exploratory Data Analysis)

## Referencias

- [Seaborn gallery](https://seaborn.pydata.org/examples.html)
- [Matplotlib tutorial](https://matplotlib.org/stable/tutorials/index.html)
- [Plotly for interactive plots](https://plotly.com/python/)
