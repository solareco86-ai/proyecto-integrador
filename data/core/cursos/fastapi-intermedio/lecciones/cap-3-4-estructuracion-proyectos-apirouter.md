### 3.4 Estructuración de Proyectos Complejos con APIRouter (Structuring a Bigger Project with Multiple Routers)

Cuando una aplicación en FastAPI crece, mantener todos los controladores en un único archivo `main.py` dificulta el mantenimiento y el trabajo en equipo. La solución estándar es modularizar el proyecto utilizando **`APIRouter`**.

---

### 1. Arquitectura Recomendada para Proyectos de Producción

Una estructura limpia para aplicaciones medianas y grandes separa las rutas, esquemas Pydantic y configuración global:

```text
mi_proyecto_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Instanciación de FastAPI e inclusión de routers
│   ├── core/                    # Configuración global
│   │   └── config.py
│   ├── routers/                 # Módulos de rutas independientes
│   │   ├── __init__.py
│   │   ├── sensores.py
│   │   └── modelos_ml.py
│   └── schemas/                 # Modelos de Pydantic
│       └── sensor_schema.py
```

---

### 2. Creación de Routers Modulares con `APIRouter`

Cada archivo en `app/routers/` declara su propio objeto `APIRouter`:

#### Archivo `app/routers/sensores.py`:
```python
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/sensores",
    tags=["Monitoreo de Sensores Industrial"],
    responses={404: {"description": "Sensor no encontrado"}}
)

sensores_db = {"s1": {"temp": 42.5}, "s2": {"temp": 88.0}}

@router.get("/")
def listar_sensores():
    return list(sensores_db.values())

@router.get("/{sensor_id}")
def obtener_sensor(sensor_id: str):
    if sensor_id not in sensores_db:
        raise HTTPException(status_code=404, detail="Sensor no registrado")
    return sensores_db[sensor_id]
```

#### Archivo `app/routers/modelos_ml.py`:
```python
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/modelos",
    tags=["Inferencia Machine Learning"]
)

@router.post("/predict", status_code=status.HTTP_200_OK)
def predecir(features: list[float]):
    return {"prediccion": "Optimo", "confianza": 0.96}
```

---

### 3. Montaje de Routers en la Aplicación Principal (`app/main.py`)

En el archivo `main.py`, importamos e incluimos los routers utilizando **`app.include_router()`**:

```python
from fastapi import FastAPI
from app.routers import sensores, modelos_ml

app = FastAPI(
    title="Plataforma de Telemetría DataMaq",
    description="API RESTful Modular",
    version="2.0.0"
)

# Montaje de routers modulares bajo el prefijo global /api/v1
app.include_router(sensores.router, prefix="/api/v1")
app.include_router(modelos_ml.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"mensaje": "API Modular DataMaq v2.0 Online"}
```

#### Rutas Generadas:
- `GET /api/v1/sensores/`
- `GET /api/v1/sensores/{sensor_id}`
- `POST /api/v1/modelos/predict`

---

### Resumen de la Lección
`APIRouter` permite estructurar proyectos de gran escala dividiendo los endpoints por dominios funcionales, facilitando la colaboración entre desarrolladores y manteniendo un código limpio y mantenible.
