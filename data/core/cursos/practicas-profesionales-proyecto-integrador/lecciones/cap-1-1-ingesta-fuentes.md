# 1.1 Fuentes de datos: sensores energéticos, logs académicos y APIs

## Objetivo

Identificar y conectar las múltiples fuentes de datos que alimentarán el proyecto integrador:
- **Proyecto energético**: Telemetría de sensores de consumo eléctrico, facturas, reportes de distribuidoras
- **Proyecto académico**: Logs de plataforma de aprendizaje, datos de inscripción, métricas de interacción

## Contenidos

### 1. Fuentes de datos del proyecto energético

#### a) Sensores de energía (telemetría en tiempo real)

**Datos disponibles:**
- Consumo de potencia (kW) cada X minutos
- Voltaje, corriente, factor de potencia
- Temperatura ambiente (correlación)
- Marca de tiempo y geolocalización

**Formato típico:** CSV, JSON desde API REST o MQTT

**Ejemplo de estructura:**
```csv
timestamp,facility_id,power_kw,voltage_v,current_a,pf,temp_c
2026-10-01 06:00:00,001,2.5,230,10.8,0.95,18.2
2026-10-01 06:05:00,001,2.3,230,10.0,0.94,18.5
2026-10-01 06:10:00,001,2.8,229,12.2,0.96,18.1
```

#### b) Facturas de electricidad

**Fuentes:**
- Archivos PDF de distribuidoras (EDENOR, EDESUR, etc.)
- Fotografías de facturas capturadas
- APIs de distribuidoras (si disponibles)

**Datos relevantes:**
- Período de facturación
- Consumo en kWh
- Tarifa aplicada
- Monto total

#### c) Reportes históricos

- Bases de datos de consumo mensual
- Reportes anuales del instituto
- Información de proyectos anteriores

### 2. Fuentes de datos del proyecto académico

#### a) Plataforma de Learning Management System (LMS)

**Datos disponibles:**
- Logs de acceso a cursos (timestamp, estudiante, duración)
- Calificaciones y entregas
- Participación en foros
- Acceso a recursos

**Formato:** Base de datos SQL, exportaciones CSV

**Ejemplo:**
```csv
student_id,course_id,event_type,timestamp,score,duration_min
STU001,CIS-301,login,2026-10-01 08:15:00,,2
STU001,CIS-301,resource_access,2026-10-01 08:17:00,,5
STU001,CIS-301,assignment_submit,2026-10-01 09:30:00,85,45
```

#### b) Sistema de inscripción y documentación

- DNI, nombre, fecha de ingreso
- Carrera, año y comisión
- Antecedentes académicos
- Información de contacto

#### c) Encuestas y feedback

- Satisfacción con cursos
- Dificultades reportadas
- Datos de clima institucional

### 3. Conexión a fuentes mediante Python

#### Lectura desde CSV

```python
import pandas as pd

# Cargar datos de sensores
sensores_df = pd.read_csv('data/raw/sensores_energia_2026.csv', parse_dates=['timestamp'])
print(sensores_df.head())
print(sensores_df.info())
```

#### Conexión a base de datos SQL

```python
import pandas as pd
from sqlalchemy import create_engine

# Configurar conexión (usuario, contraseña, host, base de datos)
engine = create_engine('mysql+pymysql://usuario:contraseña@localhost/isft_lms')

# Consultar datos académicos
query = "SELECT * FROM student_events WHERE course_id = 'CIS-301' LIMIT 1000"
eventos_df = pd.read_sql(query, engine)
```

#### Lectura desde API REST

```python
import requests
import pandas as pd

# API de sensores energéticos (ejemplo hipotético)
response = requests.get('https://api.energia.local/v1/sensores?facility=001&period=2026-10')
datos = response.json()

# Convertir a DataFrame
sensores_df = pd.DataFrame(datos['records'])
```

#### Lectura desde PDFs (facturas)

```python
import pdfplumber

# Abrir PDF de factura
with pdfplumber.open('data/raw/facturas/factura_octubre_2026.pdf') as pdf:
    tabla = pdf.pages[0].extract_table()
    print(tabla)
    # Posterior: parsear datos de consumo, período, monto
```

### 4. Validación inicial de fuentes

**Preguntas clave antes de empezar:**

1. ¿Qué período de datos históricos tenemos disponibles?
2. ¿Cuál es la frecuencia de actualización de cada fuente?
3. ¿Existen valores faltantes o inconsistencias conocidas?
4. ¿Hay restricciones de acceso o confidencialidad?
5. ¿Los datos están en el mismo zona horaria?
6. ¿Existen identificadores comunes para cruzar datos (ej: facility_id, student_id)?

## Actividad práctica

**Tarea:** Conectar a una de las fuentes de datos reales del proyecto y mostrar las primeras 10 filas + info básica.

```python
# Pseudocódigo - adaptar según tu fuente
import pandas as pd

# 1. Cargar datos
datos = pd.read_csv('ruta/a/archivo.csv')  # O tu método de lectura

# 2. Inspeccionar
print(f"Shape: {datos.shape}")
print(f"\nPrimeras filas:\n{datos.head(10)}")
print(f"\nTipos de datos:\n{datos.dtypes}")
print(f"\nValores faltantes:\n{datos.isnull().sum()}")

# 3. Resumen estadístico
print(f"\nResumen:\n{datos.describe()}")
```

## Palabras clave

Ingesta, ETL (Extract-Transform-Load), fuentes heterogéneas, conectores, pandas, sqlalchemy, API REST, CSV, JSON, PDF, MQTT

## Referencias

- [Pandas read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Requests: HTTP library](https://requests.readthedocs.io/)
- [pdfplumber: PDF parsing](https://github.com/jsvine/pdfplumber)
