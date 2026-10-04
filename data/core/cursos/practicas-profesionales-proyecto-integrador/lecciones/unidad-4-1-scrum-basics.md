# 4.1 Agile y Scrum: Sprints, Ceremonies y Artefactos

## Objetivo

Comprender la filosofía Agile y el framework Scrum. Dominar los roles (Product Owner, Scrum Master, Equipo), artefactos (Product Backlog, Sprint Backlog, Increment) y ceremonies (Planning, Daily Standup, Review, Retrospective).

## Referencia

**Plan Oficial:** § Gestión de Proyectos (métodos ágiles, planeamiento iterativo)

**spec:** § Gobernanza (ceremonias, reportes, sprints de 2 semanas)

## Contenidos

### 1. Filosofía Agile

El Manifesto Agile (2001) propone 4 valores y 12 principios centrados en:
- **Personas e interacciones** sobre procesos y herramientas
- **Software funcionando** sobre documentación exhaustiva
- **Responder a cambios** sobre seguir un plan
- **Colaboración** sobre negociación de contratos

En educación técnica, Agile es vital porque: proyectos reales tienen cambios (feedback de stakeholders, descubrimientos técnicos, eventos inesperados). Agile enseña a convivir con incertidumbre, no a evitarla.

**Agile vs Waterfall:**
- **Waterfall:** Planifica todo, ejecuta linealmente, valida al final. Riesgo: si requisitos estaban mal, proyecto falla.
- **Agile:** Planifica iterativamente, ejecuta en ciclos cortos (sprints), valida cada sprint. Riesgo: menor porque se detectan problemas temprano.

Para este proyecto: usamos **Agile** porque tenemos 2 casos reales (energy-ml, portal ISFT) y feedback real de stakeholders.

### 2. Scrum Framework

Scrum es una implementación de Agile. Define:

#### Roles

1. **Product Owner (PO):** Docente + stakeholders reales
   - Define qué se construye (prioridades)
   - Negocia cambios de requisitos
   - Acepta o rechaza trabajo completado

2. **Scrum Master (SM):** Facilitador del proceso
   - Facilita ceremonies (sin decidir)
   - Remueve bloqueadores
   - Protege equipo de interrupciones

3. **Development Team:** 2-3 estudiantes
   - Estima trabajo (story points)
   - Ejecuta tareas
   - Produce incremento de software

#### Artefactos

1. **Product Backlog:** Lista ordenada de todo lo que "estaría bien tener"
   - Ejemplo: "Como alumno quiero ver carreras disponibles", "Como operador quiero alertas de consumo alto"
   - Priorizado: must-have primero, nice-to-have después

2. **Sprint Backlog:** Items del Product Backlog seleccionados para este sprint
   - Ej: Sprint 1 = 12 story points de work. Sprint 2 = 10 story points.

3. **Increment:** Trabajo completado en el sprint
   - Debe ser "potentially releasable" (aunque no lo releaseemos)

#### Ceremonies (Eventos Scrum)

1. **Sprint Planning (2h):** Seleccionar work para sprint
   - PO presenta prioridades
   - Team estima capacidad
   - Outcome: Sprint Backlog + Sprint Goal

2. **Daily Standup (15 min, cada lunes/miércoles/viernes):** Sync diaria
   - ¿Qué hice ayer?
   - ¿Qué hago hoy?
   - ¿Hay bloqueadores?

3. **Sprint Review (1h, viernes):** Demo de work completado
   - Team muestra qué funcionó
   - PO acepta o pide ajustes
   - Feedback para refinement

4. **Sprint Retrospective (1h, viernes después de Review):** Reflexión
   - ¿Qué salió bien?
   - ¿Qué se puede mejorar?
   - 1-2 acciones concretas para próximo sprint

5. **Product Backlog Refinement (1h, antes de planning):** Preparar backlog
   - Dividir historias grandes en pequeñas
   - Estimar story points
   - Aclarar criterios de aceptación

### 3. Sprint Cycle de 2 Semanas

Para este proyecto, cada sprint es **2 semanas laborales**:

```
SEMANA 1 (Lunes - Viernes)
├─ Lunes: Sprint Planning (2h)
│  ├─ PO presenta prioridades
│  ├─ Team estima qué cabe
│  └─ Documentar Sprint Goal + Backlog
├─ Miércoles: Daily Standup #1 (15 min)
│  └─ Quick sync (ya deberían estar codificando)
└─ Viernes: Daily Standup #2 (15 min)

SEMANA 2 (Lunes - Viernes)
├─ Lunes: Daily Standup #3 (15 min)
├─ Miércoles: Daily Standup #4 (15 min)
└─ Viernes (Ceremonia de cierre)
   ├─ Sprint Review (1h): Demo
   └─ Sprint Retro (1h): Reflexión
```

**Ejemplos de Sprint Goal:**
- Sprint 1: "Tener arquitectura limpia + OCR integrando con pipeline de datos"
- Sprint 2: "Integrar NLP + ML, tests >= 85%, documentación inicial"

### 4. Métricas Clave

1. **Velocity:** Promedio de story points completados por sprint
   - Sprint 1: planeamos 12 puntos, completamos 10 = velocity = 10
   - Sprint 2: planeamos 10 puntos, completamos 10 = velocity = 10
   - Promedio velocity = 10 puntos/sprint

2. **Burn-down Chart:** Gráfico de "work remaining" vs tiempo
   - Eje X: días del sprint
   - Eje Y: story points restantes
   - Línea ideal: desciende linealmente
   - Línea real: desciende, sube si hay cambios, desciende de nuevo

3. **Burn-up Chart:** Contrario al burn-down
   - Eje Y: puntos completados (ascendente)
   - Útil para ver progreso acumulativo

4. **Sprint Goal:** Objetivo cualitativo del sprint
   - No solo "completar puntos"; es "lograr esto específico"
   - Ej: "Sprint 1: Validar que OCR + NLP pueden hablar vía DTOs"

## Actividad Práctica

1. **Definir Sprint 0:** ¿Cómo será nuestro ciclo? ¿Lunes Planning? ¿Standups lunes/miércoles/viernes?
2. **Asignar roles:** Quién es PO (docente), SM (estudiante), Dev Team (resto).
3. **Documentar en `SPRINT_PLAN.md`:**
   ```markdown
   # Sprint 0: Definición del Ciclo

   ## Roles
   - Product Owner: [Docente]
   - Scrum Master: [Estudiante 1]
   - Dev Team: [Estudiante 2, 3]

   ## Ceremony Schedule
   - **Sprint Planning:** Lunes 18:00-20:00
   - **Daily Standup:** Lunes, Miércoles, Viernes 18:15 (15 min)
   - **Sprint Review:** Viernes 19:00-20:00
   - **Sprint Retro:** Viernes 20:00-21:00

   ## Sprint Duration
   - 2 semanas (14 días)
   - Start: [Fecha]
   - End: [Fecha]

   ## Metrics
   - Target velocity: [Estimado story points/sprint]
   - Target burn-down: [Lineal]
   ```

## Palabras clave

Agile, Scrum, Sprint, Standup, Backlog, Velocity, Increment, Ceremony, Framework

## Referencias

- https://scrumguides.org/ (Scrum Guide 2020, oficial)
- Mountain Goat Software: https://www.mountaingoatsoftware.com/
- spec § Gobernanza (ceremonias, reportes)
- Plan Oficial § Gestión de Proyectos
