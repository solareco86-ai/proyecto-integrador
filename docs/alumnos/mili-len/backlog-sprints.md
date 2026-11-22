# Backlog, sprints y riesgos – Milagros Lencina

**Alumna:** Lencina Milagros (`@mili-len`).  
**Entrega:** N2 – Progreso de ejecución (gestión ágil).  
**Fecha de corte:** 22/11/2026.  
**Base:** requisitos del [SRS](https://github.com/solareco86-ai/proyecto-integrador/blob/alumno/mili-len/n1-definicion/docs/alumnos/mili-len/srs-proyecto-institucional.md) y alcance del [Lean Canvas](https://github.com/solareco86-ai/proyecto-integrador/blob/alumno/mili-len/n1-definicion/docs/alumnos/mili-len/canvas-lean-proyecto-institucional.md), ambos en revisión en el PR #113. También incluye las tareas que me asignó la cátedra.

---

## 1. Criterios

- **Story points:** escala de Fibonacci (1, 2, 3, 5, 8), que estima **complejidad relativa**. No son horas trabajadas.
- **Prioridad:** MoSCoW (Must, Should, Could, Won't), igual que en el SRS.
- **Estados:** *Hecho* (con evidencia enlazada), *En revisión* (PR abierto), *En progreso*, *Pendiente*, *Bloqueado* (depende de algo externo) y *Futuro*.
- **Alcance:** el backlog tiene 12 historias, todas vinculadas a un requisito del SRS o a una tarea asignada. El Trayecto I sugiere entre 20 y 30 historias para un proyecto completo de equipo. No agregué historias sin respaldo para llegar a esa cifra.

---

## 2. Product backlog

| ID | Historia de usuario | Requisito | SP | Prioridad | Sprint | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| HU-01 | Como **aspirante**, quiero que el sitio aparezca correctamente en los buscadores, para encontrar la oferta del instituto. | RF-06 | 5 | Must | S0 | Hecho (equipo, con aporte propio) | Commit `5d54353` (datos estructurados y `robots.txt`); `tests/test_seo.py` |
| HU-02 | Como **aspirante que consulta un asistente de IA**, quiero que la información del instituto sea legible por esos sistemas, para recibir respuestas correctas. | RF-07 | 3 | Should | S0 | Hecho | Commit `5d54353` (`llms.txt`, `llms-full.txt`, `tests/test_llms_txt.py`) |
| HU-03 | Como **equipo**, queremos un Lean Canvas y un SRS del proyecto, para acordar el problema, el alcance y los requisitos. | Todos | 5 | Must | S0 | En revisión | PR #113 |
| HU-04 | Como **estudiante de PDI**, quiero ejemplos de escalado, recorte y rotación con una imagen real y un ejercicio, para aprender transformaciones geométricas. | Tarea de la cátedra (#101) | 5 | Must | S1 | En revisión | PR #114 |
| HU-05 | Como **docente**, quiero que revise el PR del compañero asignado en la épica #98, para asegurar la calidad de la guía. | Tarea de la cátedra (#98) | 2 | Must | S1 | Bloqueado | Depende de que se abra el PR del #100 |
| HU-06 | Como **equipo**, queremos revisiones técnicas de los PRs abiertos, para detectar errores antes de integrar. | RNF-04 | 3 | Should | S1 | Hecho | Revisiones en los PR #90 y #97 (22/11/2026) |
| HU-07 | Como **equipo**, queremos una línea base de PageSpeed para `/`, `/carreras` y `/contact`, para saber si se cumple la meta de ≥ 80. | RNF-01, RF-08 | 2 | Should | S1 | Bloqueado | La API de PageSpeed devolvió 429 (cuota agotada). Ver `evidencias-n2.md` |
| HU-08 | Como **equipo**, queremos una línea base de impresiones e indexación en Search Console, para medir la visibilidad orgánica. | RF-08 | 2 | Should | S2 | Bloqueado | No tengo acceso a la propiedad de Search Console |
| HU-09 | Como **secretaría**, quiero conocer la cantidad mensual de consultas, para evaluar si el formulario cumple su objetivo. | RF-08, RF-04 | 3 | Should | S2 | Pendiente | Requiere definir quién consulta los leads en producción |
| HU-10 | Como **equipo**, queremos un monitor externo sobre el endpoint de salud, para verificar la disponibilidad ≥ 99 %. | RNF-02 | 3 | Should | S2 | Bloqueado | Depende de la decisión del Issue #86 sobre qué endpoint usa el monitor |
| HU-11 | Como **aspirante con celular**, quiero que las páginas principales se vean bien en pantallas chicas, para consultar desde cualquier dispositivo. | RNF-05 | 2 | Should | S2 | Pendiente | Revisión manual en 360 px y 1280 px, a documentar con capturas |
| HU-12 | Como **alumna**, quiero preparar la demo y las evidencias de N2, para defender mi aporte con datos verificables. | – | 3 | Must | S1 | En progreso | `evidencias-n2.md` (este PR) |
| – | Campañas SEM | RF-09 | – | Won't | – | Futuro | Requiere presupuesto y autorización institucional |

**Total planificado (sin S0):** 25 SP. S1 suma 15 SP y S2 suma 10 SP.

### Criterios de aceptación

**HU-04 – Guía 1.3 (Issue #101)**
1. La lección incluye ejemplos de escalado, recorte y rotación ejecutables.
2. Cada ejemplo muestra una imagen real con el antes y el después.
3. Hay un ejercicio de cierre, resuelto.
4. El PR tiene `Closes #101` y revisión de @LucasR1404.

**HU-05 – Revisión del PR del #100**
1. Se verifica que el código corre.
2. Se verifica que hay imagen real con el antes y el después.
3. Se dejan comentarios en líneas concretas.

**HU-06 – Revisiones técnicas**
1. Cada revisión indica qué se ejecutó y con qué resultado.
2. Los problemas encontrados se fundamentan con evidencia, como mediciones o líneas de código.
3. No se aprueba sin haber verificado.

**HU-07 – Línea base de PageSpeed**
1. Se registran fecha, URL, dispositivo (móvil y escritorio) y las cuatro puntuaciones.
2. Se adjunta captura o JSON del informe.
3. Se compara con la meta del RNF-01.

**HU-08 – Línea base de Search Console**
1. Se registran impresiones, clics y URLs indexadas de los últimos 28 días, con fecha de corte.
2. Se informa cuántas de las URLs del sitemap están indexadas.

**HU-09 – Consultas mensuales**
1. Hay un procedimiento escrito para contar los leads por mes sin exponer datos personales.
2. Se registra el primer valor medido.

**HU-10 – Monitor de disponibilidad**
1. El monitor consulta el endpoint acordado en el #86 cada 5 minutos o menos.
2. Hay un reporte mensual de disponibilidad.

**HU-11 – Revisión de diseño adaptable**
1. Hay capturas de `/`, `/carreras` y `/contact` en 360 px y 1280 px.
2. No hay scroll horizontal.
3. El formulario se puede usar con teclado.

**HU-12 – Demo y evidencias**
1. El guion de la demo se basa solo en funcionalidades verificadas.
2. Las evidencias tienen enlaces a PRs, commits y revisiones.
3. Se distingue el aporte propio del aporte del equipo.

---

## 3. Roadmap de sprints

| Sprint | Período (propuesto) | Objetivo | Historias | SP |
|---|---|---|---|---|
| **S0** (retrospectivo) | 09/09 – 22/11/2026 | Trabajo ya realizado: SEO/GEO y definición del proyecto. | HU-01, HU-02, HU-03 | 13 |
| **S1** | 23/11 – 06/12/2026 | Cerrar la tarea de la cátedra, sumar revisiones y tomar la primera medición. | HU-04, HU-05, HU-06, HU-07, HU-12 | 15 |
| **S2** | 07/12 – 20/12/2026 | Completar la medición de métricas (RF-08) y los RNF pendientes. | HU-08, HU-09, HU-10, HU-11 | 10 |

Las fechas de S1 y S2 son una propuesta. El calendario oficial de la materia todavía tiene inconsistencias abiertas (Issue #40).

### Dependencias

```text
HU-03 (Canvas + SRS) ──► define las metas que miden HU-07, HU-08, HU-09, HU-10 y HU-11
HU-04 (PR #114) ──► revisión de @LucasR1404 ──► revisión final del docente
HU-05 ◄── requiere que se abra el PR del Issue #100
HU-07 ◄── requiere una clave de la API de PageSpeed o una medición manual en pagespeed.web.dev
HU-08 ◄── requiere acceso a la propiedad de Search Console
HU-09 ◄── requiere que un responsable con acceso a producción consulte los leads
HU-10 ◄── requiere la decisión del Issue #86 (qué endpoint consulta el monitor)
HU-12 ◄── reúne la evidencia de HU-04 a HU-11
```

---

## 4. Registro de riesgos

Escalas: **probabilidad** e **impacto** en Baja, Media o Alta. El **nivel** combina ambos valores.

| ID | Riesgo | Prob. | Impacto | Nivel | Mitigación | Evidencia o Issue | Estado |
|---|---|---|---|---|---|---|---|
| R-01 | El dominio `isftn199.com.ar` está registrado a nombre de una alumna. Si no se renueva o no se transfiere, el sitio y todas las métricas se pierden. | Media | Alta | **Alto** | Transferir la titularidad a la institución o documentar la renovación. Es una decisión de la cátedra y la dirección. | Issue #32 | Abierto (fuera de mi control) |
| R-02 | Hay dos versiones de la rúbrica N2: la de `develop` (cantidad) y la del PR #41 (calidad). Se puede planificar contra criterios que no se usen. | Alta | Media | **Alto** | Seguir la regla común (calidad sobre cantidad) y consultar a la cátedra. | Issue #40, PR #41, consulta del 22/11/2026 | Abierto (consulta realizada) |
| R-03 | El criterio "Integración OCR + NLP + ML" no aplica de forma directa a un sitio institucional. | Alta | Media | **Alto** | Pedir a la cátedra un criterio equivalente. No agregar técnicas artificiales. Ver `analisis-rubrica-n2.md`. | Issue #40 (consulta del 22/11/2026) | Abierto (consulta realizada) |
| R-04 | No hay línea base de PageSpeed: la API anónima devolvió 429 y en este equipo no hay Chrome ni Lighthouse. | Alta | Media | **Alto** | Medir a mano en pagespeed.web.dev o usar una clave de API. Mientras tanto se registraron tiempos de respuesta reales con curl. | `evidencias-n2.md` §4 | Abierto |
| R-05 | No tengo acceso a Search Console, así que no puedo medir impresiones ni indexación (RF-08). | Alta | Media | **Alto** | Pedir acceso de lectura a quien administra la propiedad. | `evidencias-n2.md` §4 | Abierto |
| R-06 | `Closes #101` no cierra el issue al integrar en `develop`, porque GitHub solo cierra issues cuando el PR se integra a la rama por defecto (`main`). | Alta | Baja | Medio | Cerrar a mano o al promover a `main`, según lo que defina la cátedra. | PR #114 (sin issue vinculado como de cierre), Issue #40 | Abierto (consulta realizada) |
| R-07 | `tests/test_seo.py::test_ready_endpoint` necesita MySQL y falla en entornos sin base de datos. Puede bloquear el pre-push o confundir los resultados. | Alta | Baja | Medio | Reemplazarla por pruebas con dobles, como las del PR #90. | Revisión en el PR #90, Issue #86 | Abierto (reportado) |
| R-08 | En mi clon local no está instalado el hook `pre-push`, ni el entorno `.venv` que usa. Podría subir cambios sin pasar las validaciones. | Media | Media | Medio | Correr manualmente la batería del pre-push antes de cada PR (registrado en cada PR) y configurar `.venv` para instalar el hook. | `evidencias-n2.md` §5 | Mitigado parcialmente |
| R-09 | Pyright 1.1.414 informa 68 errores ya existentes en `develop` (`tests/test_seo.py`, `scripts/audit_seo.py` y otros). Si el pre-push usa esa versión, la etapa de tipado falla. | Media | Media | Medio | Verificar que mis cambios no sumen errores (mismo total con y sin ellos) e informar a la cátedra. | `evidencias-n2.md` §5 | Abierto (mis PRs no suman errores) |
| R-10 | La revisión entre pares depende de los tiempos de los compañeros (@LucasR1404 para el #114; el PR del #100 todavía no existe). | Media | Media | Medio | Abrir los PRs con anticipación y avisar en el PR. | PR #114, épica #98 | Abierto |

Ningún riesgo figura como *Resuelto*, porque ninguno tiene todavía evidencia de resolución.
