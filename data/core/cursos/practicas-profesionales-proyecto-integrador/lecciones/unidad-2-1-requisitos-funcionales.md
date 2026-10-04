# 2.1 Requisitos Funcionales (FR): ¿Qué debe hacer el sistema?

## Objetivo

Escribir especificación clara de QUÉ debe hacer el sistema. Ref: **spec § Especificación de Requisitos**

## Referencia

Ver especificación completa: https://github.com/datamaq-automation/spec/blob/main/backend/srs-spec-backend-fastapi.md

## Contenidos

### 1. Formato de FR

```
FR-XX: [Nombre]
Descripción: [Qué hace]
Actores: [Quién/es invocan]
Precondiciones: [Qué debe ser verdad antes]
Flujo normal: [Pasos 1, 2, 3...]
Flujo alternativo: [Excepciones]
Postcondiciones: [Qué cambia después]
Prioridad: Alta / Media / Baja
```

### 2. Ejemplo: Proyecto Energético

```
FR-01: Lectura de telemetría de sensores
Descripción: Sistema recibe datos de consumo (kW, V, A) cada 5 minutos
Actores: Sensor MQTT, Sistema central
Precondiciones: Sensor está conectado y transmitiendo
Flujo normal:
  1. Sensor envía JSON: {timestamp, power_kw, voltage_v, current_a}
  2. Sistema recibe y valida
  3. Almacena en BD
Flujo alternativo: Si sensor offline > 1h, alertar
Postcondiciones: Dato disponible en API REST
Prioridad: Alta
```

### 3. Ejemplo: Proyecto Institucional

```
FR-02: Listado de carreras disponibles
Descripción: Alumno puede ver todas las carreras ofertadas
Actores: Alumno, Portal web
Precondiciones: Alumno autenticado (o público)
Flujo normal:
  1. GET /api/carreras
  2. Sistema retorna lista con: nombre, duración, requisitos
  3. Mostrar en UI
Prioridad: Alta
```

## Actividad Práctica

Escribir 5-10 FR de tu proyecto. Usar template arriba.

## Palabras clave

Requisitos funcionales, especificación, casos de uso, FR

## Referencias

- spec § Especificación de Requisitos
- https://en.wikipedia.org/wiki/Functional_requirement

