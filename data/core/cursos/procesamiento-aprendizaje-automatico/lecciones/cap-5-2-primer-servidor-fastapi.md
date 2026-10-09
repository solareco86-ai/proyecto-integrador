# Guía de Laboratorio — Lección 5.2: Servidor FastAPI con Uvicorn: Estructura Modular y Documentación Swagger UI

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 5:** De Script de Consola a Servicio Web con FastAPI sobre `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 5.1 (Protocolo HTTP y JSON).

---

## 1. ¿Por Qué FastAPI para Servicios de Machine Learning?

En el ecosistema de Python existen múltiples frameworks web (como Flask o Django). Sin embargo, en el ámbito de la Ciencia de Datos y el Aprendizaje Automático moderno, **FastAPI** se ha convertido en el estándar indiscutido de la industria debido a tres pilares fundamentales:

1. **Rendimiento Asíncrono de Nivel Superior:** Construido sobre **Starlette** y el servidor ASGI **Uvicorn**, ofrece un rendimiento a la par de frameworks en NodeJS y Go, ideal para soportar miles de consultas de inferencia por segundo.
2. **Aprovechamiento del Tipado Estándar de Python:** Utiliza las anotaciones de tipo nativas de Python (`str`, `int`, `float`, `list[float]`) para realizar validaciones automáticas, autocompletado en el editor y prevención de errores en tiempo de ejecución.
3. **Documentación Interactiva Automática (OpenAPI / Swagger):** Sin necesidad de escribir una sola línea de HTML o configuración adicional, FastAPI genera una interfaz web interactiva donde cualquier cliente o ingeniero puede probar los endpoints en vivo.

---

## 2. Estructura de Directorios en `energy-ml`

Nos ubicamos en el repositorio de trabajo:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Para mantener la separación de responsabilidades y la arquitectura limpia, organizamos los componentes de la API dentro del paquete `src/api/`:

```text
energy-ml/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py          # Punto de entrada de la aplicación FastAPI
│   │   └── routes.py        # Definición modular de endpoints
│   ├── pipeline.py          # Pipeline de datos desarrollado en capítulos 1 y 2
│   └── modelo.py            # Lógica de inferencia y cálculo
├── tests/
│   └── test_api.py          # Pruebas automatizadas de la API
└── requirements.txt
```

---

## 3. Construcción del Servidor en `src/api/main.py`

Crearemos el punto de entrada de la API web para el servicio de telemetría de `energy-ml`:

```python
"""Punto de entrada del servicio web de inferencia para energy-ml."""

from fastapi import FastAPI
from typing import Any

app = FastAPI(
    title="Energy-ML API — ISFT N° 199",
    description="Servicio web de telemetría e inferencia de consumo eléctrico en tiempo real.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", tags=["Información"])
def ruta_raiz() -> dict[str, str]:
    """Endpoint de bienvenida e información institucional."""
    return {
        "plataforma": "Energy-ML Gateway",
        "institucion": "ISFT N° 199 — Tigre",
        "estado": "operativo",
        "documentacion": "/docs"
    }

@app.get("/health", tags=["Monitoreo"])
def verificar_salud() -> dict[str, Any]:
    """Healthcheck para monitoreo de infraestructura y balanceadores de carga."""
    return {
        "status": "healthy",
        "subestacion": "Planta Industrial Tigre",
        "red_activa": True
    }
```

---

## 4. Puesta en Marcha con Uvicorn en Modo Recarga Automática

El framework FastAPI requiere un servidor compatible con la especificación ASGI. Utilizaremos **Uvicorn**:

```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

### Explicación de los Parámetros:
* `src.api.main:app`: Indica el archivo (`src/api/main.py`) y la variable (`app`) que contiene la instancia de FastAPI.
* `--reload`: Activa la recarga en caliente (*hot reload*). Si modificas y guardas el código de cualquier archivo `.py`, el servidor se reiniciará automáticamente.
* `--port 8000`: Puerto de red local en el que escuchará peticiones.

---

## 5. Exploración de la Documentación Interactiva Swagger UI

Abre tu navegador web e ingresa a:

```text
http://127.0.0.1:8000/docs
```

Verás la interfaz interactiva de **Swagger UI**:
1. Haz clic en el endpoint `GET /health`.
2. Pulsa el botón **"Try it out"** y luego **"Execute"**.
3. Observa la respuesta HTTP con código **`200 OK`** y el cuerpo JSON devuelto por el servidor:

```json
{
  "status": "healthy",
  "subestacion": "Planta Industrial Tigre",
  "red_activa": true
}
```

También puedes acceder a la documentación alternativa formateada según el estándar **ReDoc** en:
```text
http://127.0.0.1:8000/redoc
```

---

## 6. Verificación Automatizada con curl desde otra Terminal

Abre una segunda pestaña de terminal Bash y realiza una petición directa con la herramienta de consola `curl`:

```bash
curl -i http://127.0.0.1:8000/health
```

Observarás los encabezados HTTP emitidos por Uvicorn (`HTTP/1.1 200 OK`, `content-type: application/json`) seguidos por la respuesta estructurada.

---

## 7. Conclusión

Has levantado con éxito tu primer servidor de aplicaciones asíncrono con **FastAPI** y comprobado el poder de la documentación autogenerada en **Swagger UI**.

En la siguiente lección, utilizaremos **OpenCode** para construir nuestro endpoint principal de inferencia (`POST /api/v1/predict/consumo`), aplicando validación estricta de datos con esquemas **Pydantic**.
