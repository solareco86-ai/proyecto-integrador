# Unidad 6.4: Rúbricas de Evaluación — Criterios Explícitos de Acreditación en PP

**Curso:** Prácticas Profesionales - Proyecto Integrador (3er año)  
**Carga horaria:** 40 min (lectura de rúbricas y autoreflexión)  
**Objetivo:** Transparencia total sobre cómo se califica tu trabajo. Aquí está explícitamente.

---

## ¿Por Qué Rúbricas Públicas?

Según Wiggins & McTighe (Understanding by Design), los estudiantes merecen conocer **de antemano** cómo se evalúa su trabajo. Esto no es opcional; es pedagogía basada en evidencia.

> "Si la rúbrica es sorpresa el día del examen, no es evaluación formativa; es castigo."

Por eso publicamos estas rúbricas ahora: para que diseñes tu proyecto SAbiendo hacia dónde vas.

---

## Resumen de Notas

El curso tiene **3 notas parciales + 1 defensa oral**:

| Nota | Nombre | Peso | Cuándo |
|---|---|---|---|
| **N1** | Definición + Canvas + SRS | 25% | Fin semana 3 (Trayecto I) |
| **N2** | Progreso de Ejecución | 25% | Fin semana 12 (mitad Trayecto II) |
| **N3** | Testing + Documentación | 25% | Fin semana 15 (pre-defensa) |
| **N4** | Defensa Oral + Demo | 25% | Semana 16 |

**Nota final = (N1 + N2 + N3 + N4) / 4**

---

## Evaluación de Contribuciones en GitHub (aplica a N1, N2 y N3)

Se relevará la actividad del equipo en los repositorios indicados por la cátedra, mediante `gh` (commits, issues, pull requests, revisiones y comentarios). Se evalúa **qué aporta cada contribución**, no cuántas hay.

### 1. Atribución

1. **Registro previo:** cada estudiante informa su usuario de GitHub a la cátedra en la Semana 1. Solo se valora la actividad de usuarios registrados.
2. **Co-autoría:** los commits con `Co-Authored-By:` cuentan para todos los co-autores declarados.
3. **Asistentes de IA:** su uso está permitido si se declara (trailer `Co-Authored-By` o mención en la PR). Se evalúa el resultado y la comprensión del equipo, que se verifica en la defensa (N4).

### 2. Qué se valora en cada tipo de contribución

| Contribución | Se valora | Se penaliza |
|---|---|---|
| **Commits** | Un cambio lógico por commit; mensaje Conventional Commits que explica el *porqué*; el código pasa las validaciones locales (pre-push) | Mensajes vacíos o genéricos (`fix`, `wip`, `cambios`); mezclar funcionalidad, formato y dependencias; commits que rompen la build |
| **Issues abiertos** | Título concreto; contexto; criterios de aceptación verificables; referencia al ID del SRS (FR-xx, NFR-xx); cierre vinculado a un PR | Duplicados; títulos vagos; issues sin criterio verificable; issues creados solo para sumar actividad |
| **Comentarios** | Aportan información nueva: una decisión con su fundamento, evidencia (logs, métricas, capturas), una pregunta precisa o una alternativa | "+1", "ok", "gracias" repetidos; texto genérico o pegado sin adaptar al proyecto |
| **Pull requests** | Vinculado a un issue (`Fixes #n`); descripción con resumen y plan de pruebas; tamaño razonable; respuesta a cada revisión | PR sin descripción; PR que solo reformatea; merge sin revisión de un compañero |
| **Revisiones de código** | Comentarios sobre líneas concretas; sugerencias con justificación; aprobación o cambios solicitados fundamentados | Aprobaciones sin lectura; autorrevisión; comentarios sin contenido técnico |

### 3. Niveles de desempeño colaborativo

| Nivel | Descriptor |
|---|---|
| **Excelente (9-10)** | Contribuciones de calidad sostenidas en el tiempo; issues y revisiones que mejoran decisiones del equipo; el historial permite reconstruir el proceso |
| **Bueno (7-8)** | La mayoría de las contribuciones aporta valor; algunas carecen de contexto o de vínculo con issues |
| **Satisfactorio (5-6)** | Contribuciones correctas pero superficiales o concentradas en un solo tipo; varias sin descripción |
| **Insuficiente (0-4)** | Actividad mayormente sin contenido, o ausente |

### 4. Reglas anti-distorsión

1. Ningún número de contribuciones otorga puntaje por sí solo. Las cifras de referencia de las rúbricas son mínimos orientativos, no metas.
2. La actividad concentrada en la última semana se evalúa por contenido y se analiza en su cronología.
3. Contribuciones duplicadas o generadas en lote cuentan como una sola.
4. Cada nota de N1 a N3 se publica con un informe que enlaza (URL) cada contribución considerada, para que el estudiante pueda verificarla.

### 5. Revisión humana

Cualquier estudiante puede solicitar revisión de sus notas de N1 a N3 ante la cátedra dentro de los 7 días corridos desde su publicación. La cátedra puede modificar la nota con la misma evidencia.

### 6. Entregables grupales y mérito individual

Los entregables de N1 a N3 son del equipo. El **orden de mérito** es individual y se construye con las contribuciones de cada estudiante según los puntos 2 y 3.

---

## RÚBRICA 1: Canvas + SRS (N1 — 25%)

**Fecha límite:** Fin Trayecto I (semana 3, ~20 de abril)  
**Entrega:** Canvas + documento SRS en GitHub (Issue o PDF)  
**Evaluador:** Instructor

### 1.1 Lean Canvas (5 puntos)

```text
┌─────────────────────┬──────┬─────────┬────────┬────────────────┐
│ Criterio            │Excelente│Bueno  │Satisf.│Insuficiente   │
│                     │ (5)   │(4)    │(3)    │(1-2)           │
├─────────────────────┼──────┼─────────┼────────┼────────────────┤
│ 1. Problema         │Problem│Problem │Descri-│Ausente, vago   │
│ (¿Cuál es el        │ descr│descrito│be un  │o erróneo       │
│ problema real?)      │íto  │parcial-│proble-│                │
│                     │de 3+ │mente   │ma, no │                │
│                     │pain  │(falta  │es      │                │
│                     │points│1-2)    │claro  │                │
├─────────────────────┼──────┼─────────┼────────┼────────────────┤
│ 2. Solución         │Propue│Solución│Soluck │Ausente,        │
│ (¿Cómo la           │sta   │genérica│ión    │inviable        │
│ solucionas?)        │clara │o incom│parcial│                │
│                     │y via│pleta   │ o con │                │
│                     │ble  │(cubre  │riesgos│                │
│                     │(toca│1 técni-│altos  │                │
│                     │3+ te│ca)     │       │                │
│                     │cnica│        │       │                │
│                     │s)   │        │       │                │
├─────────────────────┼──────┼─────────┼────────┼────────────────┤
│ 3. Key Metrics      │3+ mé-│2 métri│1 métrica│Ausentes o      │
│ (¿Cómo mides        │tricas│cas    │vagaexo │no cuantificables│
│ éxito?)             │clara│claras  │         │                │
│                     │s y  │(falta  │        │                │
│                     │cuan-│una)    │        │                │
│                     │tifi-│        │        │                │
│                     │cadas│        │        │                │
├─────────────────────┼──────┼─────────┼────────┼────────────────┤
│ 4. Unfair Advantage │Ventaja│Explica│Explica│No identificada │
│ (¿Por qué vos y no  │clara:│ción   │ción   │o poco clara    │
│ otros?)             │acceso│parcial│débil  │                │
│ (OCR de drones      │único,│(falta │(no    │                │
│ expertise...)       │datos │contexo│es con│                │
│                     │, IP, │o      │vincente│                │
│                     │etc.) │caract.)│       │                │
├─────────────────────┼──────┼─────────┼────────┼────────────────┤
│ 5. MVP Scope        │MVP   │MVP     │MVP    │Scope vago,      │
│ (¿Qué entra en      │clara,│descri-│identif│ambicioso o sin  │
│ esta iteración?)    │limita│to pero│icado  │límites claros   │
│                     │do, 2-│sin    │pero   │                │
│                     │4     │límite │amplio │                │
│                     │semin│claro  │o difuso│                │
│                     │as   │        │       │                │
└─────────────────────┴──────┴─────────┴────────┴────────────────┘
```

**Puntaje Canvas: __ / 25 puntos** (suma de 5 criterios × 5)

---

### 1.2 SRS (Especificación de Requisitos) (20 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(20)  │(15) │(10) │(1-5)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Requisitos            │5+ FR │3-4  │2 FR │0-1 FR o     │
│ Funcionales (FR)         │clara│claras│vagos│no definidos │
│ (¿Qué debe hacer?)       │s,   │    │ o   │            │
│                          │prioriz│    │incom│            │
│                          │adas  │    │pleto│            │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Requisitos            │3+ NFR│2 NFR│1 NFR│Ausentes o  │
│ No-Funcionales (NFR)     │en   │(falta│(falta│no relevantes│
│ (performance, security)  │perf.│una) │2+)  │            │
│                          │, sec│    │     │            │
│                          │, esc│    │     │            │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Criterios de          │3+ AC │2 AC │1 AC │Ausentes o  │
│ Aceptación (AC)          │claros│claros│vago │ambiguos    │
│ (Definición de Listo)    │por FR│por  │por  │            │
│                          │    │FR   │FR   │            │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 4. Casos de Uso          │2+ UC│1 UC │UC  │Ausentes    │
│ (Flujos principales)     │con │descr│parcial│            │
│                          │actores│ito │      │            │
│                          │clara│    │     │            │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 5. Trazabilidad          │SRS  │SRS  │SRS  │Sin          │
│ (¿Cada FR se        │conecta│conecta│conecta│conexión a  │
│ conecta a Canvas?)       │a    │parcial│débil │objetivos   │
│                          │Canvas│mente │     │            │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje SRS: __ / 20 puntos**

**Nota N1 = (Canvas / 25 + SRS / 20) / 2 × 10**

---

## RÚBRICA 2: Progreso de Ejecución (N2 — 25%)

**Fecha límite:** Fin semana 12 (semana del 2 de junio)  
**Entrega:** Demostración en vivo de prototipo + estado del código  
**Evaluador:** Instructor + pares (si hay co-evaluación)

### 2.1 Avance Técnico (15 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(15)  │(12) │(8)  │(1-5)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Prototipo Funcional   │MVP  │MVP  │Prototipo│Idea en  │
│ (¿El software anda?)     │interactivo,│interactivo,│parcial│papel  │
│                          │todas│2/3  │(1/3 fea.│sin código  │
│                          │features│de MVP),│de MVP,│          │
│                          │de MVP       │pequeños│múltiples│        │
│                          │        │bugs │bugs   │        │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Integración Técnicas  │OCR+ │OCR+ │1-2 de│Ninguna      │
│ (¿Convergen las 3?)      │NLP+│NLP+│las 3│integración  │
│                          │ML  │ML  │técnicas│aún         │
│                          │funciona│parcial│integradas│        │
│                          │        │mente │       │        │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Commits Atómicos      │Un cambio por commit,│Mayoría atómica,     │Mezclados o mensajes │Ruido, cambios masivos│
│ (calidad, no cantidad)   │mensaje explica el   │mensajes claros      │pobres en varios     │o historial ilegible  │
│                          │porqué               │                     │                     │                      │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 4. Ramas, PRs e Issues   │PR con Fixes #n,     │PR con descripción   │PR sin vínculo a     │Sin PRs, o PRs sin    │
│ (colaboración)           │descripción y        │y revisión, algunas  │issues o sin revisión│contenido ni revisión │
│                          │revisión de un      │faltas               │                     │                      │
│                          │compañero            │                     │                     │                      │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Técnico: __ / 15 puntos**

### 2.2 Gestión Ágil (10 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(10)  │(7)  │(4)  │(0-2)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Sprint Planning       │2+ sprints│1-2 sprints│Sprints│Ausente│
│ (¿Planificación clara?)  │claros│claros pero│débiles│        │
│                          │con   │pequeños  │       │        │
│                          │historias│ajustes │       │        │
│                          │bien   │necesarios│       │        │
│                          │estimadas│       │       │        │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Adjustments/Deuda     │0-1   │2-3   │3+    │>5 ítems    │
│ Técnica (Riesgos)        │riesgos│riesgos│problemas│sobre   │
│                          │identif│identificados│no resuelt│
│                          │icados │resueltos│os, pila   │
│                          │y      │o en    │creciente│
│                          │resueltos│progreso│       │        │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Gestión: __ / 10 puntos**

**Nota N2 = (Técnico / 15 + Gestión / 10) / 2 × 10**

---

## RÚBRICA 3: Testing + Documentación (N3 — 25%)

**Fecha límite:** Fin semana 15 (pre-defensa, 1 semana antes de la defensa)  
**Entrega:** Código finalizado + reportes de test + documentación  
**Evaluador:** Instructor + automatización (coverage, linters)

### 3.1 Testing (15 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(15)  │(12) │(8)  │(1-5)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Cobertura de Tests    │>=85%│70-84│50-69│<50% o sin │
│ (Constraint Gauntlet)    │ con │ con │ con │tests      │
│                          │10+  │5-9  │2-4  │           │
│                          │tests│tests│tests│           │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Tests Unitarios       │3+ tipos│2 tipos│1 tipo│Ausentes   │
│ + Integración            │(unit, │(falta│(solo│           │
│                          │integration│uno) │unit OR│          │
│                          │, E2E)│     │integ│          │
│                          │todos  │     │ration│        │
│                          │pasan  │     │)     │           │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Ruff / Linters        │0 warnings│1-3 │4-10 │>10 errors │
│ (Calidad de código)      │ en full │warnings│warnings│or ignored│
│                          │análisis │       │       │          │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 4. Arquitectura Limpia   │Clean │Mayoría│Parcial│Mezclado  │
│ (Separación de capas)    │(domain│de    │(alguna│o sin     │
│                          │/app/ │capas │mezcla)│arquitectura│
│                          │infra)│clara │      │ clara     │
│                          │verificada│    │      │          │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Testing: __ / 15 puntos**

### 3.2 Documentación (10 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(10)  │(7)  │(4)  │(0-2)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. README Ejecutable     │Pasos │Pasos │Pasos │Ausente o   │
│ (¿Alguien puede         │claros│claros│parciales│no funciona│
│ replicar?)               │,    │con  │(falta│           │
│                          │verificado│pequeñas│screenshots│        │
│                          │en otra│fallas│o detalles│       │
│                          │máquina│     │        │           │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Informe Técnico       │20+   │10-19│5-9  │<5 páginas │
│ Final (Decisiones)       │páginas│págs.│págs.│o ausente  │
│                          │de    │que  │que  │           │
│                          │calidad│cubren│tocan│           │
│                          │, con │lo   │lo   │           │
│                          │diagr.│esencial│básico│         │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Docstrings / Comentar │Todos │80%+ │50%+ │<50% o sin │
│ (Código autodocumen.)    │los   │de   │de   │comentarios│
│                          │archivos│archs│archs│          │
│                          │tienen │tienen│tienen│         │
│                          │comentario│coment│coment│        │
│                          │claro  │ario  │ario │           │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Documentación: __ / 10 puntos**

**Nota N3 = (Testing / 15 + Documentación / 10) / 2 × 10**

---

## RÚBRICA 4: Defensa Oral + Demo (N4 — 25%)

**Fecha:** Semana 16 (últimas semanas de cursada)  
**Duración:** 20-30 minutos (presentación + preguntas + demo en vivo)  
**Evaluador:** Instructor + tribunal externo (si aplica)

### 4.1 Presentación Oral (12 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(12)  │(9)  │(6)  │(0-3)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Storytelling          │Narrativa│Narrativa│Narrativa│Confuso o│
│ (¿Cuentas bien?)         │clara, clara, parcial│sin      │
│                          │compelling,│con algunos│(saltos   │estructura│
│                          │ con moraleja│tangentes│lógicos)│         │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Manejo del Tiempo     │20-30 │20-30│18-32│<18 min o    │
│ (¿Respetas límite?)      │min  │min, │min, │>35 min     │
│                          │equilibrado│buen│algo│            │
│                          │        │ritmo│lento│            │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Uso de Visuals        │Slides│Slides│Slides│Mínimo o sin│
│ (Diapositivas/demoboard) │profesionales│legibles│básicos│diapositivas│
│                          │con   │con  │con  │            │
│                          │diagramas│algunos│errores│         │
│                          │y datos │diagramas│tipografía│     │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Presentación: __ / 12 puntos**

### 4.2 Demo + Q&A (13 puntos)

```text
┌──────────────────────────┬──────┬──────┬──────┬──────────────┐
│ Criterio                 │Excelente│Bueno│Satisf.│Insuf.    │
│                          │(13)  │(10) │(6)  │(0-3)       │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 1. Demo en Vivo          │Demo  │Demo │Demo │Demo no     │
│ (¿El software funciona?) │fluida│fluida│con  │funciona o  │
│                          │,todas│, 2/3│pequeños│multiples   │
│                          │features│features│bugs│problemas   │
│                          │de MVP│de MVP│ (frena│          │
│                          │        │    │historia)│         │
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 2. Responde Preguntas    │Responde│Responde│Responde│No       │
│ (¿Entiendes tu trabajo?) │clara, con│50%+ de│<50% de│responde │
│                          │profundidad│preguntas│preguntas│bien o  │
│                          │, cita│bien  │deficientemente│se     │
│                          │código│     │      │queda en     │
│                          │cuando necesario│ │superficie│
├──────────────────────────┼──────┼──────┼──────┼──────────────┤
│ 3. Reflexión Crítica     │Identif.│Identif.│Identif.│Sin crítica│
│ (Fortalezas/debilidades) │3+ debil│2 debil│1 debil│personal   │
│                          │idades,│idad o│idad o│           │
│                          │propone│mejora│sin   │           │
│                          │mejoras│futura│propuesta│        │
└──────────────────────────┴──────┴──────┴──────┴──────────────┘
```

**Puntaje Demo+Q&A: __ / 13 puntos**

**Nota N4 = (Presentación / 12 + Demo / 13) / 2 × 10**

---

## Nota Final

**Nota Curso = (N1 + N2 + N3 + N4) / 4**

### Criterios de Acreditación (aprobación)

- **Nota >= 70 (7.0):** Aprobado. Egresas.
- **Nota 50-69 (5.0-6.9):** Recurse una lección o haz actividad de recuperación.
- **Nota < 50 (< 5.0):** Recu rsa curso completo próxima cohorte.

---

## Notas Importantes

1. **No hay media ponderada selectiva.** Las 4 notas tienen igual peso.
2. **Si falta una nota, no egresas.** Todas son obligatorias.
3. **Las rúbricas son vivas.** El instructor puede ajustar criterios según contexto, pero solo **AUMENTANDO** expectativas, no disminuyéndolas.
4. **Feedback formativo:** Cada nota tiene retroalimentación escrita (no solo número).

---

## ¿Preguntas?

- 📧 Email: agustin-bustos@isftn199.com.ar
- 📍 Consultorio: Aula 12, martes 15:00-16:00 (previa coordinación)
- 💬 Slack (canal #proyecto-integrador): Respuesta en 24 horas
