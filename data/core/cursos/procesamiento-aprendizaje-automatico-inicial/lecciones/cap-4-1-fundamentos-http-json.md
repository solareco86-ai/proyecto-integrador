# Guía de Laboratorio: Capítulo 4 - De Script de Consola a Servicio Web con FastAPI

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel 0 — Nivelación)  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  
**Nivel:** Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  

---

## 1. Objetivos y Conceptos Clave

### Objetivos de Aprendizaje
* Comprender la arquitectura de una API Web, el funcionamiento del protocolo HTTP, la diferencia entre métodos GET y POST, y el uso de JSON como formato de intercambio de datos.
* Construir y desplegar un servicio web interactivo con **FastAPI** y servidor **Uvicorn**.
* Utilizar la interfaz de documentación interactiva Swagger (`/docs`) para probar endpoints.
* Desarrollar un endpoint tipado (`POST /operar`) con el soporte del asistente **OpenCode**.
* Analizar la transición conceptual entre la programación basada en reglas manuales (`if/else`) y la toma de decisiones basada en datos/ejemplos.

### Conceptos Clave
* **API Web & HTTP:** Interfaz que permite la comunicación cliente-servidor mediante peticiones HTTP (`GET` para lectura/consulta sin efectos secundarios, `POST` para creación o procesamiento con carga útil).
* **JSON (JavaScript Object Notation):** Estructura liviana y universal de datos basada en pares clave-valor y colecciones ordenadas.
* **FastAPI + Uvicorn:** Framework asíncrono moderno en Python basado en OpenAPI/JSON Schema y servidor ASGI de alto rendimiento.
* **Reglas vs. Datos:** Diferencia crítica entre codificar lógica condicional fija (`if x > 10`) frente a delegar la decisión a patrones observados en datos de ejemplo.

---

## 2. Preparación del Entorno

Asegúrate de tener activo tu entorno virtual (`venv`) creado en los capítulos anteriores:

```bash
# Activar el entorno virtual
source venv/bin/activate

# Instalar FastAPI y Uvicorn
pip install "fastapi[standard]" uvicorn
```

Verifica la estructura inicial de tu proyecto:
```text
laboratorio-capitulo-4/
├── .env
├── .gitignore
├── venv/
└── main.py
```
