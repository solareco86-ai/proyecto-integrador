# 5B.1 Sprint Planning: Cómo Estructurar el Sprint

## Objetivo

Ejecutar Sprint Planning ceremony. Seleccionar User Stories para el sprint. Definir Sprint Goal y Backlog. Comenzar ejecución con ritual claro.

## Referencia

**Unidad 4.1:** Scrum Framework, ceremonies

**spec:** § Gobernanza (ceremonias, reportes)

## Contenidos

### 1. Sprint Planning Ceremony (2 horas)

Se ejecuta al inicio de cada sprint (lunes de semana 1).

**Participantes:**
- Product Owner (Docente) 
- Scrum Master (Estudiante facilitador)
- Dev Team (Resto de estudiantes)

**Duración total:** 120 min
- 30 min: PO presenta prioridades + preguntas
- 60 min: Team estima capacidad + selecciona historias
- 30 min: Documentación de Sprint Backlog

**Facilitación (Scrum Master):**
- Mantiene agenda en tiempo
- Asegura que todos entienden historias
- Guía estimación sin decisiones ("Chicos, ¿cuántos puntos?")

**Output:**
- Sprint Backlog documentado
- Sprint Goal claro
- Asignación de tareas (quién hace qué)

### 2. Fase 1: PO Presenta Prioridades (30 min)

PO (docente) toma las historias de Product Backlog (priorizado en Unidad 4.3) y dice:

**Ejemplo Energy-ML:**
```
PO: "Chicos, para Sprint 1, tenemos estas prioridades:

1. MUST: US-02 (Integración MQTT) - 8 puntos
   "Necesitamos datos reales. Sin esto, no hay nada."

2. MUST: US-01 (Dashboard) - 5 puntos
   "Operador quiere ver consumo en tiempo real. Depende de US-02."

3. SHOULD: US-05 (Exportar CSV) - 5 puntos
   "Si cabe. Operador lo pidió, pero no es crítico."

Preguntas?
"
```

**Preguntas del Team:**
- "¿US-02 incluye logeo de errores?" (PO aclara)
- "¿Dashboard debe soportar X?" (PO define scope)
- "¿Hay datos de ejemplo?" (PO los proporciona)

**Resultado:** Team entiende qué se busca, por qué, alcance.

### 3. Fase 2: Team Estima Capacidad y Selecciona (60 min)

Team hace Planning Poker (Unidad 4.2). La pregunta es: **"¿Cuántos puntos caben en 2 semanas?"**

**Supuesto:** Velocity estimada = 10 pt/sprint (de 4.3).

**Cálculo:**
```
PO propone: US-02 (8) + US-01 (5) + US-05 (5) = 18 puntos total
Team estima: Podemos hacer 12-14 puntos realistically

Negociación:
└─ US-02 (8) + US-01 (5) = 13 puntos ✅ Entra
└─ US-05 (5) = 18 puntos ❌ No entra, posponer a Sprint 2
```

**Resultado:** Sprint 1 Backlog = US-02 + US-01 (13 pt)

### 4. Sprint Goal (Cualitativo, NO solo puntos)

**NO es:** "Completar 13 puntos"

**SÍ es:** Una frase que resume la intención

**Ejemplos Energy-ML:**
```
"Tener datos en tiempo real fluyendo desde sensores MQTT hasta dashboard"
"Demostrar que sensores pueden comunicar con sistema central"
```

**Ejemplos Portal:**
```
"Setup básico: login funcional + listar carreras"
"Validar arquitectura con primera funcionalidad operacional"
```

**Uso:** En retrospectiva, preguntamos: "¿Logramos el Sprint Goal?" (SÍ/NO más importante que "¿completamos 13 pt?")

### 5. Fase 3: Documentación de Sprint Backlog

Se documenta en `SPRINT_1_BACKLOG.md`:

```markdown
# Sprint 1 Backlog
**Semana:** 10-11 (Octubre 2026)
**Sprint Goal:** Tener datos en tiempo real fluyendo desde sensores MQTT hasta dashboard

## Seleccionadas (Total: 13 pt)

| US-ID | Descripción | Puntos | Asignado a | Dependencias |
|-------|-------------|--------|-----------|--------------|
| US-02 | Integración sensores MQTT | 8 | Dev1, Dev2 | Ninguna |
| US-01 | Dashboard tiempo real | 5 | Dev2, Dev3 | US-02 |

## Pospuestas a Sprint 2
- US-05 (Exportar CSV) - 5 pt
- US-03 (Entrenar modelo) - 13 pt
- [otras]

## Definición de "Done"
Una historia está done cuando:
- [ ] Código mergeado a main
- [ ] Tests pasen (>= 85% cobertura)
- [ ] Code review aprobado
- [ ] Documentada (docstring, README si aplica)
- [ ] Demo funciona sin errores

## Ritmo de Sprint
- **Lunes 18:00-19:00:** Daily Standup (aunque es primer día, rapido setup)
- **Miércoles 18:15-18:30:** Daily Standup #2
- **Viernes 18:15-18:30:** Daily Standup #3
- **Viernes 19:00-20:00:** Sprint Review + Retrospective

## Métricas Esperadas
- Velocity estimada: 13 pt
- Burn-down esperado: lineal (3pt/día aprox)
- Riesgo: US-02 depende de acceso a sensores (verif. viernes)
```

### 6. Asignación de Tareas

Cada historia puede tener subtareas. Ejemplo:

```markdown
## US-02: Integración MQTT (8 pt)

### Subtareas (facilitan tracking)
- [ ] Setup broker MQTT local (Dev1, est. 2 pt)
  - Instalar mosquitto (1h)
  - Publicar mensaje de test (1h)

- [ ] Conectar aplicación a broker (Dev1, Dev2, est. 3 pt)
  - Librería paho-mqtt (1h)
  - Parsear JSON (2h)

- [ ] Validación y logging (Dev2, est. 2 pt)
  - Validar datos (1h)
  - Logger estructurado (1h)

- [ ] Tests (Dev1, est. 1 pt)
  - Mock del broker
```

**Ventaja:** Si alguien termina antes, puede ayudar en siguiente subtarea. No espera a todo el otro para "siguiente tarea".

### 7. Kick-off (30 min, después de planning)

Antes de que se vayan:

1. **Verificación de blockers:** 
   - "¿Alguien no tiene acceso a repo?" → Resolver ahora
   - "¿Necesitamos lab/servidor?" → Verificar disponible

2. **Setup técnico:**
   - Crear ramas en Git: `git checkout -b feat/mqtt-integration`
   - Crear tarea en project (si usan GitHub projects, Jira, etc.)

3. **Expectativas claras:**
   - "Commiteamos diariamente (mín 1 commit/persona/día)"
   - "PRs se reviewan en 24h"
   - "Si bloqueado, comunicar en Slack/standup. No esperes"

## Actividad Práctica

1. **Ejecutar Sprint 1 Planning (Semana 10, Lunes 18:00-20:00):**
   - Preparar: Product Backlog priorizado (de Unidad 4.3)
   - Facilitador (SM) prepara agenda (2h)
   - Ejecutar con equipo

2. **Documentar `SPRINT_1_BACKLOG.md`:**
   ```markdown
   # Sprint 1 Backlog: [Tu Proyecto]
   
   **Sprint Goal:** [1 frase]
   **Dates:** Semana 10-11
   **Velocity Target:** 12 pt
   
   ## Selected Stories
   [Tabla]
   
   ## Definition of Done
   [Checklist]
   
   ## Schedule
   [Standup times, review/retro times]
   ```

3. **Asignación clara:**
   - Quien hace qué
   - Dependencias mapeadas
   - Bloqueadores identificados

4. **Kick-off checklist:**
   - [ ] Repo branches creadas
   - [ ] Acceso verificado (BD, servidores, librerías)
   - [ ] Equipos saben qué hacer
   - [ ] Timeline realista

## Palabras clave

Sprint Planning, Sprint Goal, Product Backlog, Sprint Backlog, Estimation, Subtasks, Definition of Done

## Referencias

- Unidad 4.1 (Scrum ceremonies)
- Unidad 4.3 (Product Backlog)
- Scrum Guide 2020
