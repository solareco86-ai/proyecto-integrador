### Por qué el código limpio importa en datos

Un análisis que nadie puede leer, ejecutar o modificar tiene poco valor. El código limpio es **legible**, **reproducible** y **fácil de mantener**, y es la puerta de entrada a proyectos más grandes como las APIs.

### Nombres descriptivos

Elegí nombres que expliquen el propósito:

```python
# ❌ Confuso
a = 45.2
b = a * 24

# ✅ Claro
potencia_kw = 45.2
energia_diaria_kwh = potencia_kw * 24
```

### Funciones con responsabilidad única

Cada función debe hacer **una sola cosa**:

```python
def cargar_datos(ruta):
    """Lee el dataset y devuelve un DataFrame."""
    return pd.read_csv(ruta)

def calcular_promedio_consumo(df):
    """Calcula el consumo promedio por zona."""
    return df.groupby("zona")["potencia_kw"].mean()
```

### Docstrings y comentarios

Los docstrings documentan qué hace la función; los comentarios explican *por qué* (no *qué*):

```python
def estandarizar(df, columna):
    """Estandariza una columna numérica (media 0, desvío 1)."""
    media = df[columna].mean()
    desvio = df[columna].std()
    return (df[columna] - media) / desvio
```

### Refactorización

**Refactorizar** es mejorar el código sin cambiar su comportamiento. Pasos típicos:

1. Identificar código duplicado y extraerlo a funciones.
2. Eliminar variables innecesarias.
3. Dividir funciones largas en funciones pequeñas.
4. Reemplazar números mágicos por constantes con nombre.

### Preparación para APIs

El mismo código de análisis puede exponerse como servicio:

```python
# funciones_analisis.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Sensor(BaseModel):
    potencia_kw: float
    horas: float = 24.0

@app.post("/energia")
def energia(sensor: Sensor):
    return {"kwh": sensor.potencia_kw * sensor.horas}
```

Este es el puente natural hacia el curso de FastAPI del catálogo.

### Buenas prácticas de organización

| Práctica | Beneficio |
| :--- | :--- |
| Código en módulos (`src/`) | Reutilización y testeo |
| Constantes con nombre | Claridad y fácil ajuste |
| Documentación de funciones | Legibilidad para el equipo |
| Estilo consistente (PEP 8) | Uniformidad en todo el proyecto |

### Micro-desafío práctico

> Refactorizá un script que tengas: extraé la lógica de carga de datos a una función con docstring, eliminá nombres poco descriptivos y verificá que el resultado sea el mismo.

### Resumen

- El código limpio es legible, reproducible y mantenible.
- Usá nombres descriptivos y funciones con responsabilidad única.
- La refactorización mejora el código sin cambiar su comportamiento.
- Un análisis bien estructurado se transforma fácilmente en una API.
