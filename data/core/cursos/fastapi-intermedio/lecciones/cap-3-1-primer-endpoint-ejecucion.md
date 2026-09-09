### 3.1 Creación del Primer Endpoint y Ejecución Local (Creating the First Endpoint)

En esta lección construiremos una API inicial con **FastAPI** y la pondremos en marcha localmente mediante el servidor ASGI **Uvicorn**.

---

### 1. Estructura de la Aplicación en FastAPI

FastAPI utiliza decoradores de Python (como `@app.get()`, `@app.post()`) para vincular una ruta URL y un método HTTP a una función controladora (*path operation function*).

#### Archivo `main.py`:

```python
from fastapi import FastAPI

# 1. Crear la instancia principal de FastAPI
app = FastAPI(
    title="DataMaq API - Primer Endpoint",
    description="API de telemetría y diagnóstico industrial",
    version="1.0.0"
)

# 2. Endpoint GET en la raíz "/"
@app.get("/")
def read_root():
    """
    Endpoint de bienvenida que confirma el estado operativo de la API.
    """
    return {
        "mensaje": "¡Bienvenido a la API de Ciencia de Datos DataMaq!",
        "estado": "online",
        "version": "1.0.0"
    }

# 3. Endpoint de estado de salud (Healthcheck)
@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "cpu_usage_percent": 12.4
    }
```

---

### 2. Ejecución Local con Uvicorn (Running Locally)

**Uvicorn** es un servidor web **ASGI** ultrarrápido escrito en Python. Para iniciar el servidor de desarrollo local con recarga automática (*live reload*), ejecutamos en la terminal:

```bash
uvicorn main:app --reload --port 8000
```

#### Desglose del Comando:
- `main`: Nombre del archivo Python (`main.py`).
- `app`: Variable que contiene la instancia `FastAPI()`.
- `--reload`: Habilita el reinicio automático al guardar modificaciones en el código.
- `--port 8000`: Especifica el puerto TCP de escucha.

---

### 3. Verificación de la API

Iniciado el servidor en `http://127.0.0.1:8000`, podemos probar la respuesta desde la consola mediante `curl` o `HTTPie`:

```bash
curl -X GET "http://127.0.0.1:8000/"
```

#### Respuesta JSON devuelta:
```json
{
  "mensaje": "¡Bienvenido a la API de Ciencia de Datos DataMaq!",
  "estado": "online",
  "version": "1.0.0"
}
```

---

### Resumen de la Lección
Has creado tu primera aplicación en FastAPI y la estás ejecutando localmente con Uvicorn. En la siguiente lección exploraremos cómo capturar y validar parámetros de solicitud.
