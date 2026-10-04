# 7.1 Informe Técnico Final: Estructura, Metodología y Decisiones

## Objetivo

Documentar el proyecto de forma profesional. El informe es el **registro permanente** de qué se hizo, cómo, por qué, y qué se aprendió. Audiencia: docentes, stakeholders reales, futuros desarrolladores.

## Referencia

**spec § 5.4:** Documentación y Trazabilidad

**Plan Oficial § Referenciales:** Coherencia entre hipótesis, metodología, datos y conclusiones

## Contenidos

### 1. Estructura del Informe (10-15 págs)

```
1. Portada (1 pág)
   └─ Título, autores, fecha, institución

2. Resumen Ejecutivo (1 pág)
   └─ Qué es el proyecto, por qué importa, resultados clave
   └─ Dirigido a: PO, stakeholders (sin detalles técnicos)

3. Índice (0.5 pág)

4. Introducción y Contexto (1-2 págs)
   ├─ Problema inicial
   ├─ Stakeholders
   ├─ Requisitos
   └─ Alcance (qué entra, qué NO)

5. Metodología (2 págs)
   ├─ Spec-Driven Development (SDD)
   ├─ Agile / Scrum (2 sprints de 2 semanas)
   ├─ Equipo y roles
   └─ Herramientas (GitHub, pytest, Pyright, spec)

6. Arquitectura y Diseño (2-3 págs)
   ├─ Diagrama de 4 capas (Clean Architecture)
   ├─ Decisiones tecnológicas (por qué X no Y)
   ├─ Integración de técnicas (OCR+NLP+ML)
   └─ Diagramas de flujo de datos

7. Implementación (2-3 págs)
   ├─ Hitos principales por sprint
   ├─ Desafíos encontrados
   ├─ Soluciones aplicadas
   └─ Commits y PRs relevantes (resumen)

8. Testing y Validación (1-2 págs)
   ├─ Cobertura de tests (porcentaje)
   ├─ Constraint Gauntlet (11 validaciones, status)
   ├─ UAT (aceptación de stakeholders)
   └─ Gaps conocidos y plan

9. Resultados y Demostraciones (1-2 págs)
   ├─ Screenshots/videos del sistema funcionando
   ├─ Métricas (velocidad, latencia, uptime)
   ├─ Casos de uso cubiertos
   └─ Comparación: requisitos vs entrega

10. Lecciones Aprendidas (1-2 págs)
    ├─ Qué salió bien
    ├─ Qué fue difícil
    ├─ Cómo se resolvió
    ├─ Transferencia al futuro
    └─ Responsabilidad social / limitaciones

11. Conclusiones (0.5 pág)
    └─ Resumen ejecutivo de lo aprendido

12. Apéndices (opcional)
    ├─ Código clave (snippets)
    ├─ Logs de tests
    ├─ Traceability matrix completa
    └─ Referencias a spec
```

### 2. Resumen Ejecutivo (Clave)

**Debe poder leerse en 5 minutos y entender TODO.**

```markdown
# Resumen Ejecutivo

## Problema
Instituto energético no tiene visibilidad de consumo eléctrico en tiempo real. 
Facturas llegan mensualmente, sorpresas de costos. No hay forma de detectar 
anomalías o máquinas con fugas.

## Solución
Sistema de monitoreo en tiempo real:
- Sensores MQTT capturan consumo c/5 min
- Dashboard muestra consumo actual vs promedio
- Alertas si consumo > 20% del promedio
- Predicción ML de consumo futuro

## Metodología
Spec-Driven Development (SDD): 
- 2 sprints de 2 semanas
- 64 horas de cursada
- Equipo de 3 estudiantes
- Testing exhaustivo (Constraint Gauntlet)

## Resultados
✅ Requisitos: 6 FR, 3 NFR. 5/6 implementados (1 en roadmap)
✅ Testing: 87% cobertura, 11/11 validaciones de Constraint Gauntlet
✅ UAT: Operador aprobó deployment (con feedback para mejoras)

## Impacto
Instituto ganará visibilidad para optimizar consumo. Costo estimado de 
herramienta comercial: $50k/año. Nuestro MVP: gratuito, código abierto.

## Próximos Pasos
1. Monitoreo en producción (6 meses)
2. Agregar análisis de subcircuitos (Sprint 3)
3. Optimizar latencia (<1s, actualmente 1.2s)
```

### 3. Metodología (Descripción en Informe)

```markdown
# 4. Metodología

## 4.1 Spec-Driven Development (SDD)

El proyecto fue guiado por un documento de especificación (spec) que define:
- 4 capas de arquitectura (Clean Architecture)
- 11 validaciones arquitectónicas automatizadas (Constraint Gauntlet)
- 85% cobertura mínima de tests
- Tipado estricto (Pyright 0 errores, TypeScript LSP)

### Beneficio de SDD
Sin SDD, código crecería sin dirección. Con SDD, cada decisión 
está justificada y verificable.

## 4.2 Agile / Scrum

**Sprint 1 (Semanas 10-11):** Lectura MQTT + Dashboard
- Planning: Lunes 18:00
- Dailys: Miércoles, Viernes
- Review + Retro: Viernes 19:00-21:00
- Velocidad: 13 story points

**Sprint 2 (Semanas 12-13):** Modelo ML + Anomalías
- Planning: Lunes 18:00
- Dailys: Miércoles, Viernes
- Review + Retro: Viernes 19:00-21:00
- Velocidad: 12 story points

### Cambios Detectados en Campo
Semana 9, visita a institución energética:
- Datos vienen de factura, NO de sensores ya instalados
- Requisito original sobre "sensores IoT" → cambió a "data ingestion flexible"
- Impacto: Redefinimos Backlog en +20% de alcance real

## 4.3 Equipo y Roles

- **Product Owner (Docente):** Priorización, stakeholder liaison
- **Scrum Master (Dev1):** Facilitación, remoción de blockers
- **Dev Team (Dev2, Dev3):** Implementación, testing

### Principios de Colaboración
- Código review obligatorio (mín 1 aprobador)
- Commits atómicos (revertibles individualmente)
- Clima institucional: género, inclusión, horizontalidad (Unidad 5A.3)
- Daily standup: máximo 5 min por persona

## 4.4 Herramientas

- **Lenguaje:** Python 3.10+
- **Framework:** FastAPI
- **BD:** PostgreSQL
- **Testing:** pytest (86% cobertura)
- **Type Checking:** Pyright (0 errores)
- **Linting:** ruff
- **VCS:** GitHub
- **CI/CD:** GitHub Actions (pre-push hook)
- **Spec:** https://github.com/datamaq-automation/spec
```

### 4. Arquitectura (Diagramas en Informe)

```markdown
# 6. Arquitectura y Diseño

## 6.1 Las 4 Capas (Clean Architecture)

```
┌────────────────────────────────┐
│   FastAPI Routes / REST API    │  Infrastructure Layer
├────────────────────────────────┤
│   Application Services / DTOs  │  Application Layer
├────────────────────────────────┤
│   Domain Entities / Logic      │  Domain Layer
├────────────────────────────────┤
│   DB / External APIs           │  Infrastructure Layer
└────────────────────────────────┘
```

## 6.2 Decisiones Clave

| Decisión | Alternativa | Justificación |
|----------|-------------|---------------|
| FastAPI | Django | Async/await nativa, OpenAPI automático |
| PostgreSQL | MongoDB | Datos estructurados, transacciones ACID |
| pytest | unittest | Mejor sintaxis, fixtures, plugins |
| Pyright | mypy | Faster, strict mode nativo, IDE integration |

## 6.3 Flujo de Datos (Energy-ML)

```
Sensores MQTT
    ↓
[Lectura + Validación]
    ↓
[Normalización a % promedio]
    ↓
[ML: Predicción de consumo]
    ↓
[Comparación: Real vs Predicción]
    ↓
[Decisión: ¿Anomalía?]
    ├─ SÍ → Alerta en dashboard
    └─ NO → Log normal
```
```

### 5. Lecciones Aprendidas (Sección Crítica)

```markdown
# 10. Lecciones Aprendidas

## 10.1 Qué Salió Bien ✅

### Clean Architecture + Testing
Implementar de entrada las 4 capas + tests hizo que:
- Refactors fueran seguros (tests siguen pasando)
- Bugs se detectaran ANTES de integración
- Código fuera legible para próximos mantenedores

**Aprendizaje:** Inversión inicial en arquitectura paga dividendos.

### Agile Iterativo
2 sprints cortos permitieron:
- Feedback temprano de PO (no sorpresas al final)
- Adaptación cuando descubrimos dato en campo (Semana 9)
- Momentum del equipo (commitments realizables)

**Aprendizaje:** 2 semanas es sweet spot. Sprints más largos generan drift.

## 10.2 Qué Fue Difícil 😅

### Integración OCR + NLP + ML
Conectar 3 técnicas complejas fue desafiante:
- Problema: Formato de output de OCR vs input esperado de NLP
- Solución: DTO intermediario con validación
- Tiempo: 2 días de debugging

**Aprendizaje:** Testing de integración ANTES de integración completa.

### Latencia en NFR
Req: < 1 segundo. Medida: 1.2 segundos.
- Causa: Query de histórico hacía full scan
- Solución: Índice en BD
- Impacto: Fuera de Sprint 2, ir a roadmap

**Aprendizaje:** NFR deben testearse temprano. Optimización es iterativa.

## 10.3 Responsabilidad Social y Limitaciones

### Datos Sensibles
Consumo eléctrico es información sensible:
- Privacidad: ¿Quién ve los datos?
- Seguridad: ¿Están encriptados?
- Gobernanza: ¿Cuánto se guarda?

**Decisión:** Solo personal autorizado ve dashboard. Datos encriptados en reposo.

### Sesgo en Recomendador ML
(Si usara recomendador de carrera en Portal):
- ¿El modelo discrimina por género, origen?
- ¿Perpetúa estereotipos?

**Decisión:** Auditar modelo con dataset diverso. Documentar limitaciones.

### Sostenibilidad
"¿Quién mantiene esto en 2 años?"
- Código tiene deuda técnica (optimizaciones pospuestas)
- Documentación es punto de partida, no final
- Dependencias externas pueden volverse obsoletas

**Decisión:** Documentar roadmap de mantenimiento. Código abierto → community.

## 10.4 Transferencia al Futuro

Para próximos proyectos:
1. **Arquitectura Primero:** No esperes a Sprint 2 para refactor
2. **Testing Temprano:** TDD desde Día 1
3. **Campo Temprano:** Semana 9 era tarde; hubiera sido mejor Semana 6
4. **NFR Medibles:** "Rápido" ≠ "< 1s". Especifica números.
5. **Clima Institucional:** No es "extra". Equipo sano = código sano.
```

## Actividad Práctica

1. **Estructura tu informe (Semana 15):**
   - 10-15 páginas, máximo
   - Secciones clave: Resumen, Metodología, Arquitectura, Lecciones
   - Máx 3 páginas por sección (foco)

2. **Documentar en `TECHNICAL_REPORT.md` o `.pdf`:**
   - Markdown o Word → PDF para compartir
   - Incluir índice, figuras numeradas
   - Apéndices para código/logs

3. **Validar contra:**
   - ¿Cubre todos los requisitos SRS?
   - ¿Justifica decisiones arquitectónicas?
   - ¿Reconoce limitaciones y roadmap?

## Palabras clave

Technical Report, Methodology, Architecture Documentation, Lessons Learned, Social Responsibility, Sustainability

## Referencias

- spec § 5.4 (Documentación)
- IEEE Standard 1028 (Software Reviews and Audits)
- Plan Oficial § Referenciales
