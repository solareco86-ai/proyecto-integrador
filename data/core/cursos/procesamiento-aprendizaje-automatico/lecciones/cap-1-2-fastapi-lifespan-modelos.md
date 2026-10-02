### Gestión de memoria en FastAPI: carga del modelo en el lifespan

Cargar o reentrenar un modelo de machine learning en cada petición HTTP es un antipatrón grave que degrada la latencia y satura la CPU. El gestor de ciclo de vida (`lifespan`) de FastAPI permite cargar el modelo en memoria una sola vez al arrancar la aplicación.

#### Implementación con @asynccontextmanager
```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
import joblib

# Estado global encapsulado
ml_models: dict[str, object] = {}

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Código ejecutado antes de aceptar peticiones
    print("Cargando modelo serializado en memoria...")
    ml_models["clasificador_fallas"] = joblib.load("modelos/clasificador_bayes.joblib")
    yield
    # Código ejecutado al apagar el servidor
    print("Liberando recursos y memoria del modelo...")
    ml_models.clear()

app = FastAPI(title="Servicio de Inferencia", lifespan=lifespan)

@app.post("/predict")
def predecir(request: Request) -> dict[str, str]:
    modelo = ml_models["clasificador_fallas"]
    # El modelo ya reside en RAM listo para inferir en <5ms
    return {"resultado": "inferencia_exitosa"}
```
