# 2.3 Criterios de aceptación y casos de uso

## Objetivo

Definir **CUÁNDO** consideramos que un requisito está "listo" y mapear interacciones usuario-sistema.

## Contenidos

### 1. Criterios de Aceptación (AC)

```yaml
# Formato

FR-01: [Nombre]
Criterios de Aceptación:
  - DADO que [precondición]
    CUANDO [acción]
    ENTONCES [resultado esperado]
```

### 2. Ejemplo: Proyecto Energético

```
FR-01: Lectura de sensores

AC1:
  DADO que el sensor está activo
  CUANDO envía telemetría cada 5 minutos
  ENTONCES la BD recibe y almacena el dato en < 100ms

AC2:
  DADO que llegó un dato de sensor
  CUANDO power_kw está fuera de rango [0, 100]
  ENTONCES se marca como outlier y se loguea

AC3:
  DADO que no recibimos dato en 1 hora
  CUANDO intentamos leer datos
  ENTONCES retornamos error HTTP 503 "Sensor offline"
```

### 3. Casos de Uso (Use Case)

```
Caso de Uso: Revisar consumo del día
Actor Principal: Gerente de Infraestructura
Precondiciones: Gerente autenticado

Flujo Normal:
  1. Gerente ingresa al dashboard
  2. Ve gráfico de consumo últimas 24h
  3. Identifica pico a las 15:00
  4. Hace clic para detalles
  5. Sistema muestra: hora, equipo activo, kW consumidos

Flujo Alternativo (Datos faltantes):
  6. Si hay gap > 1h, mostrar "Sensor offline"
  7. Sugerir revisar conexión

Postcondición: Gerente tiene visibilidad de consumo
```

### 4. Ejemplo: Proyecto Institucional

```
Caso de Uso: Alumno consulta plan de carrera

Actor: Alumno ingresante

Flujo:
  1. Abre portal
  2. Ve listado de carreras
  3. Selecciona "Ciencia de Datos"
  4. Ve: plan de estudios, requisitos, docentes, duración
  5. Puede hacer clic en materia para más info
  6. Completa inscripción

Criterios:
  - DADO que la carrera existe
    CUANDO el alumno hace clic
    ENTONCES ve plan completo en < 1s
```

## Actividad Práctica

Para cada FR, escribir 2-3 criterios de aceptación.
Para los 3 casos más importantes, detallar flujo de caso de uso.

## Palabras clave

Criterios de aceptación, casos de uso, Gherkin (Given-When-Then), BDD

## Referencias

- https://www.bddbooks.com/resources/get-examples (formato Gherkin)
- spec § Use Cases

