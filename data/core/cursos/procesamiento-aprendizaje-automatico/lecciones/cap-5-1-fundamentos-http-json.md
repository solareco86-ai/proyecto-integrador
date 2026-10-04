# Guía de Laboratorio — Lección 5.1: Protocolo HTTP, Métodos GET/POST y JSON como Contrato de Datos en energy-ml

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 5:** De Script de Consola a Servicio Web con FastAPI sobre `energy-ml`  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado los Capítulos 1 al 4 (Terminal Bash, Git sobre `energy-ml`, Asistentes Estudiantiles y Ecosistema Avanzado de IA Agéntica).

---

## 1. De la Terminal al Servidor de Producción

En los capítulos anteriores aprendiste a explorar repositorios, auditar código con Git y colaborar con agentes de IA (OpenCode, Antigravity CLI, Claude Code y Aider) para depurar scripts utilitarios en `energy-ml`.

Sin embargo, en el mundo profesional de la Ciencia de Datos e Inteligencia Artificial, un script de Python aislado que solo corre cuando un desarrollador escribe `python script.py` en su terminal no puede alimentar tableros de control en tiempo real, ni procesar lecturas de miles de medidores inteligentes de una red eléctrica.

Para que nuestros modelos y algoritmos generen valor operativo continuo, debemos exponerlos como un **Servicio Web (Web API)** accesible a través de la red mediante el **Protocolo HTTP**.

---

## 2. Fundamentos de la Arquitectura Cliente-Servidor y Protocolo HTTP

El protocolo HTTP (*Hypertext Transfer Protocol*) es el estándar universal que rige la comunicación en internet. Opera bajo el modelo **Petición-Respuesta (Request-Response)** y es un protocolo **sin estado (*stateless*)**, lo que significa que el servidor procesa cada petición de forma independiente sin necesidad de recordar peticiones pasadas.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA CLIENTE - SERVIDOR HTTP                 │
├────────────────────────────────────────────────────────────────────────┤
│  Cliente (Medidor Smart / Sensor IoT / Dashboard)                      │
│       │                                                                │
│       ├─── Petición HTTP (Método + URL + Headers + Payload JSON) ────►│
│       │                                                                │
│  Servidor FastAPI (energy-ml en ejecución con Uvicorn)                 │
│       │                                                                │
│       ◄─── Respuesta HTTP (Código de Estado + Headers + Body JSON) ────┤
└────────────────────────────────────────────────────────────────────────┘
```

### Métodos HTTP Esenciales

1. **`GET` (Lectura y Consulta):**
   - **Propósito:** Solicitar datos o consultar el estado de un recurso sin modificar nada en el servidor (*idempotente* y seguro).
   - **En `energy-ml`:** Consultar el estado operativo del servicio (`GET /health`), obtener la versión del modelo en producción o solicitar el historial de consumo de un medidor.
   - **Cuerpo:** Habitualmente no lleva cuerpo (*body*); los parámetros viajan en la URL (*query parameters* o *path parameters*).
2. **`POST` (Creación y Procesamiento):**
   - **Propósito:** Enviar un paquete de información complejo al servidor para que sea procesado, validado o almacenado.
   - **En `energy-ml`:** Enviar lecturas de telemetría de alta frecuencia (`POST /api/v1/predict/consumo`) para que el algoritmo calcule la estimación de demanda o detecte anomalías eléctricas.
   - **Cuerpo:** Transporta una carga útil (*payload*) estructurada, típicamente en formato **JSON**.

---

## 3. JSON como Contrato Universal de Datos

**JSON** (*JavaScript Object Notation*) es el formato de intercambio de datos por excelencia en arquitecturas web modernas. Es liviano, legible tanto por humanos como por máquinas, e independiente del lenguaje de programación.

### Tipos de Datos Primitivos en JSON

```text
┌───────────────┬──────────────────────────┬─────────────────────────────┐
│ Tipo en JSON  │ Equivalente en Python    │ Ejemplo en energy-ml        │
├───────────────┼──────────────────────────┼─────────────────────────────┤
│ String        │ str                      │ "sensor-subestacion-norte"  │
│ Number        │ int o float              │ 220.5 (Voltios), 15 (Amps)  │
│ Boolean       │ bool (True / False)      │ true (activo), false        │
│ Array         │ list                     │ [220.1, 220.4, 219.8]       │
│ Object        │ dict                     │ {"potencia_w": 3300.0}      │
│ null          │ None                     │ null                        │
└───────────────┴──────────────────────────┴─────────────────────────────┘
```

### El Contrato de Telemetría Eléctrica en `energy-ml`

En nuestra plataforma de eficiencia energética `energy-ml`, los sensores transmiten paquetes de telemetría con este contrato de datos:

```json
{
  "sensor_id": "MED-TALAR-0199",
  "timestamp": "2026-10-03T22:00:00Z",
  "voltaje_v": 221.4,
  "corriente_a": 14.8,
  "potencia_activa_w": 3276.7,
  "factor_potencia": 0.95,
  "fase": "R"
}
```

---

## 4. Laboratorio Práctico: Serialización y Deserialización en Python

Nos posicionamos en el entorno virtual de trabajo:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Iniciamos una sesión interactiva de Python para experimentar con el módulo nativo `json`:

```python
import json

# 1. Definimos un diccionario con datos de un medidor eléctrico
medicion_local = {
    "sensor_id": "MED-TALAR-0199",
    "voltaje_v": 220.0,
    "corriente_a": 10.5,
    "potencia_activa_w": 2310.0,
    "alerta": False
}

# 2. SERIALIZACIÓN (dumps: de objeto Python a cadena JSON)
json_string = json.dumps(medicion_local, indent=2)
print("Formato JSON listo para viajar por la red:")
print(json_string)

# 3. DESERIALIZACIÓN (loads: de cadena JSON a diccionario Python)
datos_recibidos = json.loads(json_string)
print("\nRecuperado en Python:")
print(f"Sensor: {datos_recibidos['sensor_id']} | Potencia: {datos_recibidos['potencia_activa_w']} W")
```

---

## 5. Códigos de Estado HTTP: Comunicación de Éxito y Errores

Cuando un cliente envía una petición a nuestra API en `energy-ml`, el servidor responde obligatoriamente con un código numérico de 3 dígitos:

* **Familia 2xx (Éxito):**
  * `200 OK`: La petición fue procesada con éxito y se retorna la predicción o dato solicitado.
  * `201 Created`: Un nuevo registro de telemetría fue persistido exitosamente.
* **Familia 4xx (Error del Cliente):**
  * `400 Bad Request`: La petición tiene una sintaxis JSON inválida o parámetros corruptos.
  * `404 Not Found`: El endpoint o sensor solicitado no existe.
  * `422 Unprocessable Entity`: El JSON es sintácticamente válido pero no cumple las reglas de validación de tipos.
* **Familia 5xx (Error del Servidor):**
  * `500 Internal Server Error`: Ocurrió una excepción no controlada en el código Python del backend.

---

## 6. Conclusión

Has comprendido la base sobre la que opera cualquier servicio web moderno: el flujo **Cliente-Servidor**, los métodos **GET** y **POST**, el intercambio riguroso en **JSON** y los códigos de respuesta **HTTP**.

En la siguiente lección, montaremos nuestra primera aplicación con **FastAPI y Uvicorn** en `energy-ml` y exploraremos la documentación interactiva autogenerada en Swagger UI.
