# Análisis de la rúbrica N2 – vigente y propuesta

**Alumna:** Lencina Milagros (`@mili-len`).  
**Fecha de corte:** 22/11/2026.  
**Fuentes:**
- **Rúbrica vigente:** `data/core/cursos/practicas-profesionales-proyecto-integrador/lecciones/unidad-6-criterios-evaluacion-rubrica.md`, igual en `develop` y en `main`.
- **Propuesta:** PR #41 (rama `docs/curso-pp-contribuciones-github`).
- **Contexto:** Issue #40.

---

## 1. Qué está vigente

La rúbrica N2 publicada en `develop` y en `main` se compone de dos partes:

| Parte | Criterio | Excelente | Bueno | Satisfactorio | Insuficiente |
|---|---|---|---|---|---|
| 2.1 Técnico (15) | 1. Prototipo funcional | MVP interactivo con todas sus funciones | MVP con 2/3 de las funciones, bugs menores | Prototipo parcial (1/3 del MVP) | Idea en papel |
| 2.1 Técnico | 2. Integración de técnicas | OCR + NLP + ML funcionando | OCR + NLP + ML parcial | 1 o 2 de las 3 técnicas | Ninguna |
| 2.1 Técnico | 3. Commits atómicos | 10+ commits claros | 5 a 9 | 2 a 4 con mensajes vagos | 0 o 1, historial desordenado |
| 2.1 Técnico | 4. Ramas y PRs | 3+ PRs con revisión de código | 2 PRs con revisión | 1 PR sin revisión | Sin PRs |
| 2.2 Gestión (10) | 1. Sprint planning | 2+ sprints con historias bien estimadas | 1 o 2 sprints con ajustes | Sprints débiles | Ausente |
| 2.2 Gestión | 2. Ajustes y deuda técnica (riesgos) | 0 o 1 riesgos identificados y resueltos | 2 o 3 resueltos o en progreso | 3+ sin resolver | Más de 5 acumulados |

**Fórmula:** Nota N2 = (Técnico / 15 + Gestión / 10) / 2 × 10.

**También vigente:** la sección "Evaluación de Contribuciones en GitHub" de `develop` establece tres reglas:

1. Commits atómicos con mensaje que explique qué cambia y por qué.
2. La calidad pesa más que la cantidad, y el ruido se penaliza.
3. Las notas de N1 a N3 arman un orden de mérito.

## 2. Qué es propuesta pendiente (PR #41)

El PR #41 está abierto desde el 14/10/2026, sin revisiones ni merge, y su rama está desfasada de `develop`. Propone:

| Tema | Vigente (`develop`) | Propuesta (PR #41) |
|---|---|---|
| Criterio 3 | "10+ commits claros" | "Un cambio por commit; el mensaje explica el porqué" (calidad, no cantidad) |
| Criterio 4 | "3+ PR con code review" | "Ramas, PRs e Issues": PR con `Fixes #n`, descripción y revisión de un compañero |
| Contribuciones | Tres reglas generales | Tabla de qué se valora y qué se penaliza en commits, issues, comentarios, PRs y revisiones; niveles de 0 a 10; reglas contra la distorsión ("ningún número otorga puntaje por sí solo"); revisión humana en 7 días; mérito individual sobre entregables grupales |
| Uso de IA | No se menciona | Permitido si se declara (`Co-Authored-By` o mención en el PR) |

**Lo que no cambia:** los criterios 1 y 2 (prototipo e integración de técnicas) y toda la parte de Gestión.

## 3. Diferencias que afectan a N2

1. **Cantidad o calidad.** Con la rúbrica vigente, la cantidad de commits y de PRs define el nivel. Con la propuesta, se mira el contenido. Mi plan sigue la regla común a las dos: **commits atómicos con el porqué y PRs con descripción, revisión y plan de pruebas**, sin agregar commits para sumar.
2. **Vínculo con issues.** La propuesta exige `Fixes #n`. El PR #114 cumple (`Closes #101`). El PR #113 (N1) no tiene un issue asociado.
3. **Declaración del uso de IA.** Mis commits incluyen el trailer `Co-Authored-By`, así que cumplo la regla propuesta si se aprueba.
4. **Cierre automático.** GitHub solo cierra un issue con `Closes #n` cuando el PR se integra a la rama por defecto (`main`). Como los PRs de alumnos van a `develop`, el #101 no se cerrará solo al integrar el #114.

## 4. El criterio "Integración de técnicas (OCR + NLP + ML)"

**Qué pide:** que converjan reconocimiento óptico de caracteres, procesamiento de lenguaje natural y aprendizaje automático en el prototipo.

**Por qué puede no corresponder a mi proyecto:**

- El problema que define el Lean Canvas es la dispersión de la información institucional, la dificultad de contacto y la baja visibilidad en buscadores. Ninguno se resuelve con OCR, NLP o ML.
- El SRS no tiene requisitos que usen esas técnicas, y en `src/` no hay funcionalidades de OCR, NLP ni ML (verificado en el repositorio).
- La rúbrica pone como ejemplo de ventaja "OCR de drones", un proyecto de otra naturaleza. En cambio, la unidad 1.3 del curso describe un "Proyecto Institucional" cuyo MVP (listado de carreras, requisitos de ingreso, búsqueda simple y formulario de contacto) no incluye OCR, NLP ni ML.
- Agregar una técnica solo para cumplir la rúbrica contradice el SRS ("no inventar funcionalidades") y el criterio de valor real de la sección de contribuciones.

**Qué sí existe relacionado:** el aporte GEO (`llms.txt` y `llms-full.txt`) prepara el contenido para que lo interpreten sistemas basados en modelos de lenguaje, pero no implementa NLP dentro del sistema. Lo cuento como contexto, no como cumplimiento del criterio.

**Posible extensión futura (no planificada ni implementada):** clasificar automáticamente las consultas del formulario por tema con NLP. Solo tendría sentido si la secretaría lo necesita y si se cuenta con datos reales. Queda como idea para consultar, no como compromiso.

## 5. Consulta a la cátedra

Publiqué la consulta en el Issue #40 el 22/11/2026: https://github.com/solareco86-ai/proyecto-integrador/issues/40#issuecomment-7082435808

Preguntas:

1. ¿N2 se evalúa con la tabla de `develop` (cantidades) o con la del PR #41 (calidad)?
2. ¿Cómo se aplica "Integración de técnicas (OCR + NLP + ML)" a proyectos que no las usan? ¿Se reemplaza, se pondera distinto o cada proyecto justifica su técnica?
3. Como `Closes #n` no cierra issues al integrar en `develop`, ¿los sub-issues de la épica #98 se cierran a mano o al promover a `main`?

**Estado:** sin respuesta a la fecha de corte.
