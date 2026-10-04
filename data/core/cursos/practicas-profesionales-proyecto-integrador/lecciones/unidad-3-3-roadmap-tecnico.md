# 3.3 Roadmap técnico: qué se implementa en qué orden

## Objetivo

Priorizar features técnicas para maximizar aprendizaje e integración rápida.

## Contenidos

### 1. Principios de Roadmap

- **MVP primero:** Funcionalidad básica antes que optimizaciones
- **Integración progresiva:** Módulos integrados en cada sprint
- **Testing en paralelo:** No dejar testing para el final
- **Documentación viva:** Actualizar conforme se implementa

### 2. Ejemplo: Proyecto Energético

```
Semana 1-2 (Sprint 0 - Setup):
  - Estructura Django/FastAPI
  - BD diseño inicial
  - Tests placeholder

Semana 3-4 (Sprint 1):
  - API lectura sensores (MQTT)
  - Almacenamiento en BD
  - Tests de API
  - Dashboard básico (estático)

Semana 5-6 (Sprint 2):
  - Visualización con Plotly
  - Alertas de anomalías
  - Tests de alertas

Semana 7-8 (Sprint 3):
  - OCR de facturas (3er año technique)
  - Comparación factura vs sensores

Semana 9-16:
  - ML para predicción (PAA)
  - NLP para bot (2do año)
  - Refinamientos
```

### 3. Ejemplo: Proyecto Institucional

```
Sprint 1-2:
  - Portal estático con carreras
  - API de datos
  - Búsqueda básica

Sprint 3-4:
  - Autenticación (JWT)
  - Dashboard de alumno
  - Tests

Sprint 5-6:
  - Bot básico (NLP, 2do año)

Sprint 7+:
  - Recomendador ML (PAA)
  - Análisis de trayectorias
```

## Actividad Práctica

Dibuja tu roadmap técnico:

```
Semana 1-2:  [Feature 1] [Feature 2]
Semana 3-4:  [Feature 3] [Integration]
Semana 5-6:  [Testing]  [Polish]
...
```

## Palabras clave

Roadmap, priorización, MVP, iteración, integración

