### Endpoint de predicción con modelos de Machine Learning

Una vez entrenado un modelo, el objetivo es exponerlo como **servicio**: recibir datos de entrada vía HTTP y devolver una predicción. FastAPI es ideal para esto gracias a Pydantic y a la gestión del ciclo de vida de la aplicación.

El modelo `regresion.pkl` que usaremos se entrenó con el **dataset de telemetría industrial `data/core/datasets/curvas_de_carga.csv`** (el mismo que trabajaste en el curso *Python y Entorno para Ciencia de Datos*). Así se cierra el círculo narrativo del catálogo: el análisis inicial en Pandas se convierte en un servicio de predicción en producción.

### De Pandas a producción: el entrenamiento

El modelo se entrenó a partir de las variables de las curvas de carga:

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("data/core/datasets/curvas_de_carga.csv")

# Características y objetivo
X = df[["potencia_kw", "factor_potencia"]]
y = df["potencia_kw"] * 24  # energía diaria estimada en kWh

modelo = LinearRegression().fit(X, y)
joblib.dump(modelo, "models/regresion.pkl")
```

En esta lección no reentrenamos el modelo: lo **cargamos** y lo exponemos como API.

### Carga del modelo una sola vez

Entrenar o cargar un modelo es una operación costosa. Hacerlo en cada petición degradaría la API. La solución es cargarlo **una única vez** al arrancar la aplicación, usando el mecanismo de `lifespan`:

```python
from contextlib import asynccontextmanager
import joblib

modelo = None

@asynccontextmanager
async def lifespan(app):
    global modelo
    modelo = joblib.load("models/regresion.pkl")
    print("Modelo cargado")
    yield
    print("Apagando aplicación")
```

Luego se registra en la app:

```python
app = FastAPI(lifespan=lifespan)
```

### Schema de entrada y salida con Pydantic

Pydantic valida los datos de entrada en tiempo de ejecución y garantiza que la respuesta tenga la estructura esperada:

```python
from pydantic import BaseModel

class PredictRequest(BaseModel):
    potencia_kw: float
    factor_potencia: float
    armonicos_thd: float

class PredictResponse(BaseModel):
    prediccion_kwh: float
```

### El endpoint POST /predict

El endpoint recibe el schema, construye el array de características y devuelve la predicción:

```python
@app.post("/predict", response_model=PredictResponse)
async def predict(data: PredictRequest):
    features = [[
        data.potencia_kw,
        data.factor_potencia,
        data.armonicos_thd,
    ]]
    resultado = modelo.predict(features)[0]
    return PredictResponse(prediccion_kwh=float(resultado))
```

### Manejo de errores

Si el modelo no se cargó o la entrada es inválida, FastAPI responde con códigos adecuados:

```python
from fastapi import HTTPException

@app.post("/predict", response_model=PredictResponse)
async def predict(data: PredictRequest):
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    # ... resto del flujo
```

### Verificación con HTTPie o httpx

```bash
http POST http://localhost:8000/predict \
  potencia_kw=45.2 factor_potencia=0.92 armonicos_thd=8.1
```

Respuesta esperada:

```json
{
  "prediccion_kwh": 2840.5
}
```

### Buenas prácticas de MLOps

1. **Versioná los modelos**: asociá cada artefacto a una versión y a los datos con los que se entrenó (en nuestro caso, `curvas_de_carga.csv`).
2. **Cacheá la carga**: el modelo se carga una vez y se reutiliza en todas las peticiones.
3. **Validá las características**: los rangos de entrada deben coincidir con el entrenamiento.
4. **Monitoreá en producción**: registrá latencia y drift de los datos de entrada.
5. **Trazabilidad del dataset**: documentá qué versión de datos generó cada modelo publicado.

### Micro-desafío práctico

> Extendé el endpoint para aceptar un array de muestras (`list[PredictRequest]`) y devolver todas las predicciones en una sola respuesta, aprovechando la vectorización del modelo.

### Resumen

- El modelo se carga una sola vez mediante `lifespan`.
- Pydantic valida la entrada y estructura la salida.
- El endpoint `POST /predict` aplica el modelo y devuelve la predicción.
- Versionado, caché, validación y monitoreo son prácticas clave de MLOps.
