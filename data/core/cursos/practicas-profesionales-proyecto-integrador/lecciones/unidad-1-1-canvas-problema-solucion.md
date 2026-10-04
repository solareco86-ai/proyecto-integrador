# 1.1 Canvas: Problem, Solution, Key Metrics

## Objetivo

Definir el problema del proyecto de forma clara, la solución propuesta, y cómo mediremos éxito.

## Referencia

**Spec:** Business Model Canvas (BMC) es parte del proceso de gobernanza.
Ref: https://github.com/datamaq-automation/spec

## Contenidos

### 1. Problema (Problem)

¿Cuál es el problema que resuelve este proyecto?

**Proyecto Energético (energy-ml):**
- **Problema:** Institutos no conocen patrones de consumo eléctrico en tiempo real. Facturas llegan después. No hay visibilidad de cargas anómalas.
- **Impacto:** Costos innecesarios, no hay optimización, sorpresas en facturas.

**Proyecto Institucional (web):**
- **Problema:** Alumnos no saben qué carrera elegir, qué materias cursar, cómo es el plan de estudios. Consultas manuales saturan secretaría.
- **Impacto:** Alumnos desorientados, retenciones, saturación administrativa.

### 2. Solución (Solution)

¿Cómo resolvemos el problema?

**Proyecto Energético:**
- Sistema de monitoreo en tiempo real (sensores MQTT)
- Predicción de consumo (ML, PAA)
- Dashboard (visualización)
- Bot conversacional (NLP, 2do año) para consultas

**Proyecto Institucional:**
- Portal centralizado con información de carreras
- Bot de atención (NLP, 2do año)
- Recomendador de carreras (ML, PAA)
- Análisis de trayectorias (datos)

### 3. Key Metrics

¿Cómo sabemos que la solución funciona?

**Proyecto Energético:**
- Visibilidad de consumo en tiempo real (latencia < 5 min)
- Precisión de predicción (RMSE < 10% del consumo promedio)
- Adopción del bot (% de consultas resueltas)
- Reducción de costos (ahorro estimado al optimizar)

**Proyecto Institucional:**
- Tiempo de respuesta a consultas (antes: 2-3 días; ahora: < 1 min)
- Satisfacción de alumnos (NPS > 70)
- Tasa de ingreso a carrera elegida (% de retención)

## Actividad Práctica

Llenar la sección **Problem + Solution + Key Metrics** del Canvas:

```yaml
# Canvas - Tu Proyecto

Problem:
  - Qué molesta hoy
  - A quién
  - Impacto

Solution:
  - Cómo lo resolvemos
  - Tecnologías que usamos
  - Enfoque

Key Metrics:
  - ¿Cómo medimos éxito?
  - Números concretos
  - Timeline de medición
```

## Palabras clave

Canvas, problema, solución, métricas, valor, impacto

## Referencias

- https://leanstack.com/lean-canvas (formato oficial)
- spec § Business Model Canvas
