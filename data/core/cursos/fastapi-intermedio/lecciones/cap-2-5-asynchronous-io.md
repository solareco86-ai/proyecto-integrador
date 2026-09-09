### 2.5 Entrada/Salida Asíncrona (Asynchronous I/O)

La **Entrada/Salida Asíncrona (Async I/O)** es el modelo de ejecución no bloqueante que le otorga a **FastAPI** su velocidad y capacidad para atender miles de peticiones concurrentes en un único hilo de procesador.

---

### 1. Concepto de I/O No Bloqueante vs Bloqueante

- **I/O Bloqueante (WSGI)**: El hilo de ejecución se detiene por completo esperando la respuesta de la base de datos o de la red externa, dejando la CPU ociosa.
- **I/O No Bloqueante (ASGI)**: Mientras se espera la respuesta de red o disco, el **Event Loop** (bucle de eventos) cede el control a otra petición entrante, logrando un alto grado de concurrencia.

---

### 2. `async def`, `await` y el Event Loop (`asyncio`)

- **`async def`**: Declara una función asíncrona (*corrutina*). Al invocarla, retorna un objeto *coroutine* sin ejecutarla inmediatamente.
- **`await`**: Pausa la corrutina actual y cede la ejecución de vuelta al Event Loop hasta que la tarea pendiente finalice.

```python
import asyncio
from fastapi import FastAPI

app = FastAPI(title="API Asíncrona")

# Simulación de consulta a base de datos asíncrona
async def consultar_base_datos_async(query_id: str) -> dict:
    # asyncio.sleep cede la ejecución al Event Loop sin bloquear el proceso
    await asyncio.sleep(0.1)
    return {"query_id": query_id, "status": "OK"}

@app.get("/reporte/{query_id}")
async def get_reporte(query_id: str):
    resultado = await consultar_base_datos_async(query_id)
    return {"data": resultado}
```

---

### 3. Tareas I/O-Bound vs CPU-Bound en FastAPI

> **Regla de Arquitectura**:
> 1. Utilizá `async def` cuando invoques operaciones I/O no bloqueantes (ej. `httpx`, `asyncpg`, `aioredis`).
> 2. Utilizá `def` síncrono estándar cuando ejecutes código intensivo de CPU (ej. procesamiento numérico con `numpy`, inferencia de Machine Learning con `scikit-learn` o `pandas`). FastAPI ejecutará automáticamente las funciones `def` en un **ThreadPool secundario** para no congelar el Event Loop principal.

---

### Resumen de la Lección
Async I/O permite construir servidores web con alto rendimiento mediante `async def` y `await`, dejando que el Event Loop procese múltiples peticiones de I/O concurrentemente.
