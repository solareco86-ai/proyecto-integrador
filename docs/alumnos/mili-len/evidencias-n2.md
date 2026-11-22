# Evidencias N2 – Milagros Lencina

**Alumna:** Lencina Milagros (`@mili-len`).  
**Entrega:** N2 – Progreso de ejecución.  
**Fecha de corte:** 22/11/2026.  
**Documentos relacionados:** [Backlog, sprints y riesgos](backlog-sprints.md) · [Análisis de la rúbrica N2](analisis-rubrica-n2.md).

Este documento reúne solo evidencias verificables: cada dato tiene un enlace, un hash de commit o un comando que lo reproduce.

---

## 1. Pull Requests propios

| PR | Título | Base | Estado | Vínculo | Revisión |
|---|---|---|---|---|---|
| [#114](https://github.com/solareco86-ai/proyecto-integrador/pull/114) | feat(pdi): ampliar guía 1.3 de transformaciones geométricas con imagen real | `develop` | Abierto | `Closes #101` | Solicitada a @LucasR1404 (según el Issue #101) |
| [#113](https://github.com/solareco86-ai/proyecto-integrador/pull/113) | docs(n1): Lean Canvas del proyecto institucional | `develop` | Abierto | Entrega N1 | Solicitada a @datamaq-automation |
| PR de N2 (este documento) | docs(n2): planificación, riesgos, análisis de rúbrica y evidencias | `develop` | Abierto | – | – |

La rama `alumno/mili-len/seo-geo-sem` **no pasó por un PR**: se integró a `develop` con un merge directo (`fb7bb10`, 11/09/2026). Lo aclaro para no presentarlo como PR revisado.

## 2. Commits relevantes

| Commit | Rama | Descripción |
|---|---|---|
| `5d54353` | `alumno/mili-len/seo-geo-sem` (integrada a `develop`) | SEO/GEO: datos estructurados, `llms.txt`, `llms-full.txt`, `robots.txt` y palabras clave negativas para SEM. **No es atómico:** mezcla 7 archivos de temas distintos. |
| `8edd14f` | `alumno/mili-len/guia-1-3-transformaciones` | Guía 1.3 de PDI: ejemplos de escalado, recorte y rotación con imagen real (CC0) y ejercicio de cierre. |
| `db1dfe9` | `alumno/mili-len/guia-1-3-transformaciones` | Prueba automática de la lección 1.3 y control de enlaces a `static/` en todas las lecciones. |
| `e0d39b2` | `alumno/mili-len/n2-planificacion-evidencias` | Backlog, roadmap de sprints y registro de riesgos. |
| `c6ee814` | `alumno/mili-len/n2-planificacion-evidencias` | Análisis de la rúbrica vigente frente a la propuesta del PR #41. |
| `fd314df`, `c4302ba`, `298b127`, `5b7f197` | `alumno/mili-len/n1-definicion` | Entrega N1: Canvas, SRS y reflexión sobre oportunidades de ingreso. |

## 3. Issues trabajados

| Issue | Rol | Estado | Evidencia |
|---|---|---|---|
| [#101](https://github.com/solareco86-ai/proyecto-integrador/issues/101) – Guía 1.3, transformaciones geométricas | Responsable | Abierto, con PR en revisión | PR #114 |
| [#98](https://github.com/solareco86-ai/proyecto-integrador/issues/98) – Épica de la guía de PDI | Revisora del PR del #100 | Pendiente | El PR del #100 todavía no existe |
| [#40](https://github.com/solareco86-ai/proyecto-integrador/issues/40) – Decisiones de la evaluación | Consulta técnica | Sin respuesta | [Comentario del 22/11/2026](https://github.com/solareco86-ai/proyecto-integrador/issues/40#issuecomment-7082435808) |

## 4. Revisiones de código a compañeros

| PR | Fecha | Tipo | Contenido |
|---|---|---|---|
| [#97](https://github.com/solareco86-ai/proyecto-integrador/pull/97#pullrequestreview-6013372813) – Asignación de aulas | 22/11/2026 | Comentarios, 3 en líneas concretas | Ejecuté las 29 pruebas (pasan). Medí que el algoritmo nuevo crece de forma exponencial: 16 comisiones con 6 aulas tardaron 58,4 s. El horario 18:30–21:40 está fijo en el dominio y contradice el turno oficial de 18:00 a 22:30. No aprobé. |
| [#90](https://github.com/solareco86-ai/proyecto-integrador/pull/90#pullrequestreview-6013338143) – Pruebas de `healthz` y `ready` | 22/11/2026 | Comentarios, 1 en línea concreta | Ejecuté las 4 pruebas en la rama del PR y sobre el `develop` actual. Pyright y Ruff sin errores. Señalé la prueba duplicada que depende de MySQL y la exposición de `str(e)` en `/ready`. |
| #85 – Promover `develop` a producción | 19/11/2026 | Aprobación con comentario | Verificación del curso en DEV (5 secciones y 11 lecciones). |
| #61 – Textos de ingreso y contacto | 31/10/2026 | Aprobación con comentario | Coherencia de los textos con lo solicitado. |
| #60 – Reversión del curso de Fundamentos | 31/10/2026 | Aprobación con comentario | Breve. |
| #55 – Identidad visual institucional | 28/10/2026 | Aprobación con comentario | Breve. |
| #53 – Actualización de `certifi` | 28/10/2026 | Aprobación con comentario | Breve. |

Las revisiones del #90 y el #97 son las primeras con comentarios en líneas concretas y mediciones propias. Las anteriores son aprobaciones con un comentario general.

## 5. Pruebas y validaciones ejecutadas

Ejecutadas el 22/11/2026 en un entorno virtual temporal (Python 3, dependencias de `requirements.txt` y `requirements-dev.txt`), sobre la rama del PR #114:

| Validación | Resultado |
|---|---|
| `pytest --cov=src --cov-fail-under=85 tests/` | 1070 aprobadas, 1 fallida, cobertura del 88,47 %. Falla `test_seo.py::test_ready_endpoint`, que necesita MySQL (riesgo R-07). |
| `tests/test_guia_pdi_transformaciones.py` y `tests/test_cursos.py` | 56 aprobadas |
| Los 9 bloques de código de la lección 1.3, ejecutados sobre `cafe.png` | 9 de 9 sin errores; los tamaños impresos coinciden con el texto |
| `scripts/validate_content.py` | Sin errores |
| `scripts/validate_templates.py` | Sin errores |
| `scripts/verify_architecture.py` | PASS |
| `ruff check src/ tests/ scripts/` | Sin errores |
| `pyright` 1.1.414 (`src/ scripts/ tests/`) | 68 errores, **los mismos con y sin mis cambios**; todos son previos y están en otros archivos (riesgo R-09). 0 errores en los archivos nuevos. |

El hook `pre-push` no está instalado en mi clon (riesgo R-08), así que ejecuté a mano las mismas etapas.

## 6. Métricas

### 6.1 PageSpeed Insights: no se pudo medir

| Fecha | URL | Dispositivo | Resultado |
|---|---|---|---|
| 22/11/2026 13:43 (UTC−3) | `/`, `/carreras`, `/contact` | Móvil | La API respondió **HTTP 429**: cuota diaria agotada para consultas sin clave. Volví a intentar más tarde con el mismo resultado. |

En este equipo no hay Chrome ni Node, así que tampoco pude correr Lighthouse en local. **No hay puntuaciones de PageSpeed registradas.**

**Cómo obtenerlas:**
1. Abrir https://pagespeed.web.dev en un navegador.
2. Analizar `https://isftn199.com.ar/`, `https://isftn199.com.ar/carreras` y `https://isftn199.com.ar/contact`.
3. Registrar para móvil y escritorio las puntuaciones de Rendimiento, Accesibilidad, Prácticas recomendadas y SEO, junto con LCP, CLS y TBT, la fecha y una captura.
4. Comparar con la meta del RNF-01 (≥ 80 en móvil).

### 6.2 Mediciones complementarias con curl (no reemplazan a PageSpeed)

Tomadas el 22/11/2026 a las 13:44 (UTC−3), con 5 solicitudes por URL desde la conexión de este equipo y con `Accept-Encoding: gzip, br`. Miden la respuesta del servidor, no la experiencia de carga en el navegador.

| URL | HTTP | Tiempo hasta el primer byte, 5 muestras (s) | HTML comprimido / sin comprimir | Compresión |
|---|---|---|---|---|
| `/` | 200 ×5 | 0,442 · 0,176 · 0,159 · 0,154 · 0,167 | ≈12,2 KB / 55,7 KB | Brotli |
| `/carreras` | 200 ×5 | 0,185 · 0,199 · 0,184 · 0,184 · 0,180 | ≈11,4 KB / 53,4 KB | Brotli |
| `/contact` | 200 ×5 | 0,220 · 0,188 · 0,194 · 0,166 · 0,185 | ≈12,6 KB / 56,2 KB | Brotli |

Otros datos verificados el mismo día:
- `/healthz` → 200.
- `/ready` → 200, con `{"status":"ok","checks":{"db_accessible":true}}`.
- `/llms.txt` → 200.
- `/sitemap.xml` → 200, con **36 URLs** (`<loc>`).
- El servidor responde detrás de Cloudflare.

### 6.3 Google Search Console: sin acceso

No tengo acceso a la propiedad de Search Console del sitio y no usé credenciales ajenas. **No hay métricas de impresiones ni de indexación registradas.** Para obtenerlas hace falta que quien administra la propiedad me dé acceso de lectura (riesgo R-05, historia HU-08).

## 7. Qué puedo demostrar

### En producción (`https://isftn199.com.ar`)

| Funcionalidad | URL | Autoría |
|---|---|---|
| Página principal y catálogo de carreras | `/`, `/carreras` | Equipo |
| Formulario de consulta | `/contact` | Equipo |
| `robots.txt` con acceso para bots de IA | `/robots.txt` | Equipo, con aporte propio (`5d54353`) |
| Resumen para sistemas de IA | `/llms.txt`, `/llms-full.txt` | Aporte propio (`5d54353`) |
| Datos estructurados JSON-LD | Código fuente de `/` (`EducationalOrganization`) | Equipo, con aporte propio (`5d54353`) |
| Sitemap | `/sitemap.xml` | Equipo |

### En local, desde la rama del PR #114 (todavía no está en producción)

| Funcionalidad | URL local | Autoría |
|---|---|---|
| Lección 1.3 con imágenes de antes y después y ejercicio de cierre | `http://127.0.0.1:8001/cursos/procesamiento-imagenes-python-opencv/transformaciones-geometricas-operaciones` | Propia |

Lo verifiqué el 22/11/2026: la lección responde 200 en local y muestra sus 9 imágenes.

## 8. Guion de la demostración (unos 10 minutos)

1. **Contexto (1 min):** el problema del Canvas (información dispersa y baja visibilidad) y el MVP del SRS.
2. **Recorrido del aspirante, UC-01 (2 min):** abrir `https://isftn199.com.ar/`, ir a `/carreras`, entrar a una carrera, ver `#requisitos` y abrir `/contact`. Aclarar que estas funciones son del equipo.
3. **Mi aporte SEO/GEO, UC-02 (2 min):**
   - abrir `/robots.txt` y mostrar que permite a `GPTBot` y declara el sitemap;
   - abrir `/llms.txt`;
   - mostrar el JSON-LD con "Ver código fuente" en `/`;
   - mostrar `/sitemap.xml`.

   Explicar el commit `5d54353` y reconocer que no fue atómico.
4. **Guía 1.3 de PDI (3 min):** en la rama `alumno/mili-len/guia-1-3-transformaciones`:
   - levantar la app con `python run.py` (puerto 8001 por defecto);
   - abrir la lección;
   - recorrer escalado (con la comparación de interpolaciones), recorte (con la zona marcada), rotación con y sin pérdida de esquinas, y el ejercicio de cierre;
   - correr un bloque de código en vivo sobre `cafe.png`;
   - correr `pytest tests/test_guia_pdi_transformaciones.py`.
5. **Colaboración (1 min):** mostrar el PR #114 (`Closes #101`, revisión solicitada) y las revisiones del #97 (medición del algoritmo exponencial) y del #90.
6. **Gestión (1 min):** el backlog con sus estados reales, el registro de riesgos y la consulta al docente en el #40.

**Si falla internet:** la parte local (paso 4) funciona sin conexión.

## 9. Aporte propio y aporte del equipo

| Aporte propio | Aporte del equipo (no lo presento como propio) |
|---|---|
| SEO/GEO del commit `5d54353` | Arquitectura del sistema, rutas FastAPI, formulario de consulta y su persistencia |
| Guía 1.3 de PDI y su prueba automatizada (PR #114) | Catálogo de carreras, campus virtual y panel de autoridades |
| Canvas, SRS y reflexión de ingreso (PR #113) | Pipeline de despliegue, CSP, monitoreo e infraestructura |
| Revisiones de los PR #53, #55, #60, #61, #85, #90 y #97 | El resto de los commits del repositorio |
| Backlog, riesgos, análisis de la rúbrica y estas evidencias | |

**Sobre el uso de IA:** usé un asistente de IA en estas tareas, y está declarado con el trailer `Co-Authored-By` en cada commit. En la defensa tengo que poder explicar cada decisión: las convenciones de coordenadas, por qué `INTER_AREA`, el cálculo del lienzo para rotar sin perder las esquinas, y la medición y la causa del crecimiento exponencial en el PR #97.
