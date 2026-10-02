# Guía de Laboratorio: Capítulo 4 - De Script de Consola a Servicio Web con FastAPI

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  

---

## 3. Ejercicio 4.1: Hola Mundo en FastAPI y Servidor Uvicorn

En este ejercicio aprenderás a levantar un servidor HTTP asíncrono con FastAPI y explorar la documentación interactiva Swagger.

### 1. Creación de la Aplicación en `main.py`
Crea el archivo `main.py` con una ruta básica `GET /`:

```python
from fastapi import FastAPI

app = FastAPI(
    title="API Inicial de Aprendizaje Automático",
    description="Servicio web inicial para la transición de scripts a APIs.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {
        "mensaje": "Bienvenido al servicio web de Nivelación",
        "estado": "activo",
        "doc": "/docs"
    }
```

### 2. Ejecución con Uvicorn en Modo Recarga Automática
Inicia el servidor con Uvicorn en modo recarga automática (*auto-reload*):

```bash
uvicorn main:app --reload --port 8000
```

### 3. Exploración de la Documentación Interactiva (Swagger UI)
Abre tu navegador web en:
```text
http://127.0.0.1:8000/docs
```
FastAPI genera de forma nativa la especificación OpenAPI con una interfaz visual donde podés probar el endpoint `GET /` haciendo clic en **"Try it out"** y luego en **"Execute"**.
