# 4.3 Product Backlog Priorizado y Roadmap de Sprints

## Objetivo

Priorizar User Stories con MoSCoW. Mapear dependencias. Estimar realistically cuántos sprints necesitamos. Diseñar 2 sprints de 2 semanas c/u.

## Referencia

**spec:** § Product Backlog & Roadmap

**Plan Oficial:** § Métodos PERT/CPM, Diagrama de Gantt

## Contenidos

### 1. Priorización con MoSCoW

MoSCoW es una técnica simple: cada historia es Must, Should, Could o Won't.

**M - Must Have (MVP, no se negocia):**
- Requisitos mínimos para que el proyecto sea válido
- Ej: Energy-ML MUST: lectura de sensores + alertas. Sin eso, no es útil.
- Ej: Portal MUST: listar carreras + login. Sin eso, no sirve.
- **No se negocia.** Si cabe en 2 sprints, lo hacemos. Si no, hay problema.

**S - Should Have (Nice-to-have, importante pero flexible):**
- Mejora de UX, optimizaciones, reportes
- Ej: Energy-ML SHOULD: exportar CSV. Sin eso, funciona, pero menos cómodo.
- Ej: Portal SHOULD: recomendador de carrera. Sin eso, funciona, pero menos inteligente.
- **Negociable.** Si falta tiempo, pueden posponer al "futuro".

**C - Could Have (Future, low priority):**
- Roadmap post-proyecto
- Ej: Integración con Telegram, API abierta, ML de clustering
- Ej: App móvil, exportar a PDF, analítica de comportamiento

**W - Won't Have (Out of scope, decisión explícita):**
- Cosas que NO vamos a hacer (aunque alguien lo pida)
- Ej: Energy-ML WON'T: Simulación de futuros escenarios climáticos (es otro proyecto)
- Ej: Portal WON'T: Venta de cursos online (la educación es pública)
- **Importante:** Decir NO explícitamente evita surpresas.

### 2. Ejemplo: Product Backlog Priorizado (energy-ml)

```markdown
# Product Backlog - energy-ml (Priorizado)

## MUST HAVE (MVP - Sprint 1 + Sprint 2)
1. US-01: Ver consumo real en dashboard (5 pt) - Sprint 1
2. US-02: Integrar sensores MQTT (8 pt) - Sprint 1
3. US-03: Entrenar modelo predicción (13 pt) - Sprint 2
4. US-04: Detectar anomalías (8 pt) - Sprint 2

**Total MUST:** 34 pt
**Sprints necesarios:** 34 / 12 (velocity esperada) = ~3 sprints
**Problema:** Tenemos solo 2 sprints (semanas 10-13)
**Solución:** Reducir US-03 de 13 a "hacer versión simple" (8 pt)

## SHOULD HAVE (Si sobra tiempo)
5. US-05: Exportar reportes CSV (5 pt)
6. US-06: Historial de alertas (5 pt)

## COULD HAVE (Roadmap futuro)
7. US-07: Integración con Telegram notifications
8. US-08: ML de clustering de patrones horarios

## WON'T HAVE (Explícitamente NO hacemos)
- Simulación climática
- Integración con smart meters de empresa distribuidora
- App móvil nativa
```

### 3. Mapear Dependencias (Critical Path)

No todas las historias son independientes. Algunas dependen de otras.

**Ejemplo (energy-ml):**
```
US-01 (Dashboard) depende de US-02 (MQTT)
├─ Sin sensores MQTT, no hay datos
└─ Sin datos, dashboard está vacío

US-04 (Anomalías) depende de US-03 (Modelo)
├─ Sin modelo entrenado, no puedo predecir
└─ Sin predicción, no puedo comparar vs real

US-03 (Modelo) depende de US-02 (MQTT)
├─ Sin datos de sensores, no entreno
```

**Diagrama simplificado (PERT):**
```
Sprint 1: US-02 (MQTT) → US-01 (Dashboard)
Sprint 2: US-03 (Modelo) → US-04 (Anomalías)
         (paralelo)

Ruta crítica: US-02 → US-03 → US-04
Eso determina duración mínima.
```

**Regla:** Historias sin dependencias van primero.

### 4. Estimación de Velocity

**Velocity = promedio de puntos completados por sprint.**

En Unidad 4.1 sabemos que cada sprint es 2 semanas, equipo de 2-3 personas, 4h/semana en clase + estudio.

**Estimación conservadora:**
- Equipo dedicado 100%: 15-20 pt/sprint
- Equipo part-time (4h clase + estudio): 8-12 pt/sprint
- Nuestro caso: **Asumir 10 pt/sprint** (conservador, hay sorpresas)

**Cálculo de sprints necesarios:**
```
Total MUST points: 34 (o 26 si simplificamos US-03)
Velocity esperada: 10 pt/sprint
Sprints necesarios: 34 / 10 = 3.4 sprints

Pero tenemos solo 2 sprints (semanas 10-13).
Solución: 2 sprints × 10 pt = 20 pt de MUST.

¿Qué entra?
Sprint 1: US-02 (8) + US-01 (5) = 13 pt (excedera 10, pero Setup es importante)
Sprint 2: US-03-simple (8) + US-04-simple (5) = 13 pt

Total: 26 pt en 2 sprints = velocity 13 pt/sprint (optimista, pero posible).
```

### 5. Roadmap de 2 Sprints

**Estructura visual:**
```
SEMANAS 9-16 (Trayecto II)

Semana 9: Integración Estratégica (5A) - NO código
├─ 5A.1: Integración de técnicas
├─ 5A.2: Trabajo en campo
├─ 5A.3: Clima institucional
└─ 5A.4: Post-procesamiento

Semana 10-11: SPRINT 1 (5B.1)
├─ L: Planning
├─ Mi/V: Standups
├─ V: Review + Retro
└─ Entregables: US-02 (MQTT) + US-01 (Dashboard)

Semana 12-13: SPRINT 2 (5B.2)
├─ L: Planning (refinar backlog)
├─ Mi/V: Standups
├─ V: Review + Retro
└─ Entregables: US-03 (Modelo simple) + US-04 (Anomalías)

Semana 14-15: TESTING & DOCUMENTACIÓN (Unidad 6-7)
├─ Constraint Gauntlet (11 validaciones)
├─ Tests >= 85% cobertura
└─ Documentación (informe, README, slides)

Semana 16: DEFENSA (Unidad 8)
└─ Presentación oral + Q&A + Reflexión
```

### 6. Capacity Planning: ¿Es Realista?

**Preguntas clave:**
- ¿Equipo de 2 o 3 personas? (2 = menos hand-holding, 3 = más colaboración)
- ¿Hay otras materias en paralelo? (pueden competir por tiempo)
- ¿Algún miembro tiene responsabilidades externas? (cuidado, enfermedad, trabajo)
- ¿Tenemos laboratorio disponible? (acceso a repo, servidores, datos)

**Buffer para sorpresas:**
- Asumimos 10 pt/sprint, pero planeamos 12 pt (20% buffer).
- Si alcanzamos 12 pt en Sprint 1, ajustamos velocity a 12 pt/sprint para Sprint 2.
- Si caemos a 8 pt, reconocemos que tenemos menos capacidad y replanificamos.

### 7. Producto Incremental (no "todo al final")

**NO hacemos esto:**
```
Semana 10-13: Código
Semana 14-15: Testing
Semana 16: Defensa
Problema: Si testing encuentra bugs en Semana 14, poco tiempo para arreglarse.
```

**Hacemos esto:**
```
Semana 10-11 (Sprint 1): Code + tests de esa funcionalidad
Semana 12-13 (Sprint 2): Code + tests de esa funcionalidad
Semana 14-15: Testing EXHAUSTIVO de todo + documentación
Semana 16: Defensa
Ventaja: bugs se descubren temprano. Testing final es validación, no "sorpresas".
```

## Actividad Práctica

1. **Priorizar con MoSCoW:**
   ```markdown
   # Product Backlog - [tu proyecto]

   ## MUST HAVE
   - US-XX: [historia] (X pt)
   - US-YY: [historia] (Y pt)
   ...
   **Total:** ZZ pt

   ## SHOULD HAVE
   ...

   ## COULD HAVE
   ...

   ## WON'T HAVE
   ...
   ```

2. **Mapear dependencias:** Dibujar o listar qué US depende de cuál.

3. **Diseñar 2 sprints:**
   ```markdown
   # Sprint Planning

   ## Sprint 1 (Semanas 10-11)
   **Velocity esperada:** 12 pt
   **Sprint Goal:** [Objetivo cualitativo]
   
   | US-ID | Descripción | Pt | Owner |
   |-------|-------------|----|----|
   | US-XX | [historia] | 8 | Dev1 |
   | US-YY | [historia] | 5 | Dev2 |
   **Total:** 13 pt (excedera 1 pt, pero OK)

   ## Sprint 2 (Semanas 12-13)
   **Velocity esperada:** 12 pt
   **Sprint Goal:** [Objetivo cualitativo]
   ...
   ```

4. **Documentar en `PRODUCT_BACKLOG.md`:** Backlog completo + roadmap visual.

## Palabras clave

MoSCoW, Priorización, Dependencias, Ruta crítica, Velocity, Capacity, Incremental
