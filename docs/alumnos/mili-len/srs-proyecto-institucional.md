# SRS – Proyecto Web Institucional ISFT N.º 199

**Documento:** Especificación de Requisitos de Software (SRS).  
**Proyecto:** Desarrollo y posicionamiento del sitio web institucional del ISFT N.º 199.  
**Responsable:** Lencina Milagros.  
**Entrega:** N1 – Definición + Canvas + SRS.  
**Versión:** 1.0  
**Documento relacionado:** [Lean Canvas del proyecto](canvas-lean-proyecto-institucional.md).  
**Base:** este SRS toma y acota los requisitos ya definidos en [docs/srs.md](../../srs.md) y [docs/srs-portal-isftn199.md](../../srs-portal-isftn199.md), enfocándolos en el MVP definido en el Lean Canvas.

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requisitos funcionales y no funcionales del sitio web institucional del ISFT N.º 199 (`https://isftn199.com.ar`) para el alcance MVP definido en el Lean Canvas. Sirve como referencia para planificar, implementar, probar y evaluar el proyecto dentro del Proyecto Integrador.

### 1.2 Convenciones de estado

Cada requisito indica su estado según lo verificado en el repositorio a la fecha de esta entrega:

| Estado | Significado |
|---|---|
| **Implementado** | Existe en el código (`src/`, `templates/`, `static/`) y está cubierto por pruebas automatizadas que pasan. |
| **Parcial** | Existe una parte en el código, pero falta completar o medir algo para darlo por cumplido. |
| **Pendiente** | Forma parte del MVP, pero todavía no está implementado o no fue verificado. |
| **Futuro** | Propuesta para etapas posteriores; no forma parte del MVP. |

### 1.3 Prioridad

Se usa la escala MoSCoW: **Must** (imprescindible para el MVP), **Should** (importante, pero el MVP funciona sin él), **Could** (deseable) y **Won't** (fuera de esta iteración).

---

## 2. Alcance del sistema

El sistema es el portal web institucional del ISFT N.º 199. Su objetivo es centralizar la información institucional y académica, facilitar las consultas de aspirantes y mejorar la visibilidad del instituto en buscadores tradicionales y en sistemas de inteligencia artificial (SEO y GEO).

**Incluido en el MVP** (alineado con la sección 8 del Lean Canvas):

- Página principal con información institucional.
- Catálogo y detalle de las seis tecnicaturas superiores.
- Requisitos de ingreso.
- Acceso al campus virtual de cursos (`/cursos`).
- Formulario de consulta con validación y registro.
- SEO técnico: sitemap, robots.txt, metadatos y datos estructurados.
- GEO: recursos legibles por sistemas de IA (`llms.txt`).
- Diseño adaptable a móviles y escritorio.

**Fuera del alcance del MVP:**

- Sistema completo de inscripción académica.
- Campañas SEM permanentes.
- Implementación completa de un sistema administrativo propio.
- Cobro de matrículas, aranceles o cuotas. La educación es 100 % pública y gratuita, y este punto es una restricción del sistema, no una funcionalidad postergada.

**Límite temporal:** una iteración de 4 semanas dentro del período de implementación del Proyecto Integrador, según el Lean Canvas.

---

## 3. Usuarios y contexto

### 3.1 Contexto

El ISFT N.º 199 es un instituto público de nivel superior técnico que depende de la DGCyE de la Provincia de Buenos Aires (Región 6). Su sede está en Maestra Celina Voena 1750, El Talar (Tigre), con cursada vespertina de 18:00 a 22:30 hs. Ofrece seis tecnicaturas superiores de tres años, con títulos oficiales de validez nacional.

### 3.2 Usuarios

| Usuario | Necesidad principal | Prioridad |
|---|---|---|
| **Aspirante** | Conocer las carreras y los requisitos de ingreso, y enviar una consulta. | Principal |
| **Estudiante actual** | Acceder a información institucional y a los cursos del campus virtual. | Secundaria |
| **Docente / personal institucional** | Contar con información oficial centralizada y actualizada. | Secundaria |
| **Secretaría** | Recibir las consultas de aspirantes de forma ordenada. | Secundaria |
| **Empresas y organizaciones** | Conocer la oferta formativa y la vinculación con el sector productivo. | Secundaria |
| **Buscadores y sistemas de IA** (actor no humano) | Rastrear, indexar e interpretar correctamente el contenido del sitio. | Principal para SEO/GEO |

---

## 4. Requisitos funcionales

### RF-01 – Página principal institucional

**Prioridad:** Must · **Estado:** Implementado

El sistema debe mostrar en `/` una página principal con la información institucional: presentación del instituto, oferta académica, pasos de ingreso y acceso al formulario de consulta.

**Criterios de aceptación:**

1. Al solicitar `GET /`, el servidor responde con código 200 y contenido HTML renderizado en el servidor.
2. La página tiene un único `<h1>` y las etiquetas `<title>` y `meta description` completas.
3. La página incluye enlaces visibles hacia `/carreras` y hacia el formulario de consulta.
4. Los textos de la página provienen de los archivos de `data/` y no están escritos en el código ni en la plantilla.

**Evidencia:** `src/infrastructure/fastapi/routes/main_routes.py`, `tests/test_home_institucional.py`, `tests/test_seo.py`.

### RF-02 – Catálogo y detalle de carreras

**Prioridad:** Must · **Estado:** Implementado

El sistema debe listar las seis tecnicaturas en `/carreras` y ofrecer una página de detalle para cada una en `/carreras/{slug}`, con datos tomados de `data/content/carreras.yaml`.

**Criterios de aceptación:**

1. `GET /carreras` responde 200 y muestra las seis tecnicaturas definidas en `data/content/carreras.yaml`.
2. `GET /carreras/{slug}` responde 200 para cada carrera existente y 404 para un slug inexistente.
3. Cada página de detalle muestra la información curricular cargada en el YAML (descripción, perfil y materias) sin datos inventados.
4. Todas las páginas de carreras aparecen en `sitemap.xml`.

**Evidencia:** `src/infrastructure/fastapi/routes/carreras_routes.py`, `tests/test_carreras.py`.

### RF-03 – Requisitos de ingreso

**Prioridad:** Must · **Estado:** Implementado

El sistema debe informar los requisitos de ingreso (título secundario completo o en trámite y documentación de legajo) en una sección identificable del catálogo.

**Criterios de aceptación:**

1. La página `/carreras` contiene una sección con el ancla `#requisitos`.
2. La ruta histórica `/inscripciones` redirige con código 301 a `/carreras#requisitos`.
3. Los requisitos mostrados coinciden con los definidos en los datos institucionales y no incluyen costos ni aranceles.

**Evidencia:** `templates/carreras.html` (sección `id="requisitos"`), `carreras_routes.py` (redirección de `/inscripciones`).

### RF-04 – Formulario de consulta para aspirantes

**Prioridad:** Must · **Estado:** Implementado

El sistema debe permitir que un aspirante envíe una consulta desde `/contact` o desde la sección de ingreso. La consulta se valida en el servidor, se registra y se notifica a la institución.

**Criterios de aceptación:**

1. El envío a `POST /api/v1/contact` con nombre válido y al menos un medio de contacto (email o teléfono) responde 201 y devuelve un identificador de la consulta.
2. Un envío con nombre vacío, nombre demasiado corto o sin email ni teléfono es rechazado con un error de validación, y no se registra la consulta.
3. Si el campo honeypot anti-spam llega completo, la consulta se descarta en silencio, sin registrarse.
4. El formulario muestra en el navegador los campos obligatorios y valida cada paso antes de avanzar.
5. Una consulta válida se guarda mediante el repositorio de leads y se intenta notificar a la institución. Si falla la notificación, la respuesta indica `partial_success` en lugar de perder la consulta.

**Evidencia:** `src/infrastructure/fastapi/routes/contact_routes.py`, `src/application/dtos/lead_dto.py`, `tests/test_contact_form_validation.py`, `tests/test_contact_form_honeypot.py`, `tests/test_lead_repository_engine.py`.

### RF-05 – Acceso a cursos del campus virtual

**Prioridad:** Should · **Estado:** Implementado

El sistema debe permitir consultar los cursos y lecciones del campus virtual en `/cursos`, con contenido tomado de `data/core/cursos/`.

**Criterios de aceptación:**

1. `GET /cursos` responde 200 y lista los cursos publicados.
2. `GET /cursos/{curso}/{leccion}` muestra la lección en HTML generado desde su archivo Markdown.
3. Los cursos publicados aparecen en `sitemap.xml`.

**Evidencia:** `src/infrastructure/fastapi/routes/course_routes.py`, `tests/test_cursos.py`.

### RF-06 – SEO técnico

**Prioridad:** Must · **Estado:** Implementado

El sistema debe exponer los elementos técnicos necesarios para que los buscadores rastreen e indexen el sitio correctamente.

**Criterios de aceptación:**

1. `GET /sitemap.xml` responde con un sitemap válido que incluye la página principal, las carreras, los cursos y la página de contacto, y excluye las rutas ocultas.
2. `GET /robots.txt` responde con las reglas de rastreo, bloquea `/api/` y declara la ubicación del sitemap.
3. Las páginas principales incluyen datos estructurados JSON-LD válidos (`EducationalOrganization`, `Course`, `BreadcrumbList`).
4. Las páginas de error 404 incluyen `noindex`.
5. Las rutas históricas comerciales (`/pricing`, `/planes`) redirigen con 301 a `/carreras`, y las variantes `www`, `http` y con barra final redirigen a la URL canónica.

**Evidencia:** `main_routes.py`, `static/robots.txt`, `tests/test_seo.py`, `tests/test_additional_routes.py`, `tests/test_canonical_redirects.py`, `tests/test_coverage_gap.py`, `tests/test_paginas_comerciales_retiradas.py`.

### RF-07 – GEO: información legible por sistemas de IA

**Prioridad:** Should · **Estado:** Implementado

El sistema debe ofrecer recursos que faciliten la interpretación de la información institucional por motores generativos y asistentes de IA.

**Criterios de aceptación:**

1. `GET /llms.txt` y `GET /llms-full.txt` responden 200 con texto plano que resume la institución y su oferta académica.
2. `robots.txt` permite el acceso de los bots de IA declarados (por ejemplo, `GPTBot`).
3. La información de `llms.txt` coincide con los datos oficiales de `data/` (seis tecnicaturas y gratuidad), sin contenido inventado.

**Evidencia:** `main_routes.py`, `static/robots.txt`, `tests/test_llms_txt.py`.

### RF-08 – Medición de métricas clave

**Prioridad:** Should · **Estado:** Parcial

El sistema debe permitir medir las métricas clave del Lean Canvas: visibilidad orgánica, indexación, consultas recibidas y disponibilidad.

**Criterios de aceptación:**

1. El sitio queda verificado en Google Search Console. *Hecho:* existe la ruta del archivo de verificación en `main_routes.py`.
2. Se registra una línea base inicial de impresiones orgánicas y de URLs indexadas. *Pendiente.*
3. Se obtiene la cantidad mensual de consultas a partir de los leads registrados (RF-04). *Pendiente:* falta definir el procedimiento de consulta del registro.
4. El sitio expone endpoints de salud (`/healthz`) que un monitor externo de disponibilidad pueda consultar. *Hecho:* el endpoint existe. *Pendiente:* configurar un monitor externo.

**Evidencia:** `main_routes.py` (`/healthz`, `/metrics`, archivo de verificación de Google).

### RF-09 – Campañas SEM

**Prioridad:** Won't (esta iteración) · **Estado:** Futuro

Evaluar campañas publicitarias en buscadores, sujetas a la disponibilidad de presupuesto y a la autorización institucional.

**Criterios de aceptación (para una etapa futura):**

1. Existe autorización institucional documentada antes de lanzar cualquier campaña.
2. Las campañas dirigen a páginas existentes del catálogo (`/carreras` o `/contact`).
3. Los resultados se comparan con la línea base orgánica definida en RF-08.

---

## 5. Requisitos no funcionales

| ID | Categoría | Requisito | Criterio de verificación | Estado |
|---|---|---|---|---|
| **RNF-01** | Rendimiento | Las páginas principales deben cargar rápido en móviles. Se incluye CSS crítico inline y los recursos no críticos se cargan de forma diferida. | Puntuación ≥ 80 en Google PageSpeed Insights (móvil) para `/`, `/carreras` y `/contact`. | CSS crítico implementado (`scripts/build_critical_css.py`). Medición en PageSpeed: **pendiente**. |
| **RNF-02** | Disponibilidad | El sitio debe estar disponible al menos el 99 % del tiempo mensual. | Monitor externo sobre `/healthz` con reporte mensual. | Endpoint implementado. Monitoreo: **pendiente**. |
| **RNF-03** | Seguridad | El sitio debe servir solo por HTTPS, enviar cabeceras de seguridad (incluida CSP), proteger los formularios contra spam y no exponer credenciales en el código. | Tests de cabeceras, CSP, honeypot y CSRF en verde; `scripts/verify_architecture.py` sin hallazgos. | Implementado (`tests/test_seo.py`, `tests/test_csp_headers.py`, `tests/test_csrf.py`, `tests/test_contact_form_honeypot.py`). |
| **RNF-04** | Mantenibilidad | Respetar la arquitectura en capas (`domain`, `application`, `adapters`, `infrastructure`). El contenido vive en `data/` y no en el código. | `scripts/verify_architecture.py` sin errores, cobertura de pruebas ≥ 85 % y Pyright sin errores. | Implementado como regla del repositorio (`AGENTS.md`). |
| **RNF-05** | Usabilidad y adaptabilidad | El sitio debe poder usarse en móviles y escritorio, con formularios accesibles por teclado y campos obligatorios señalados. | Revisión manual en anchos de 360 px y 1280 px; atributos `required` verificados por tests. | Diseño adaptable implementado con Tailwind. Revisión manual documentada: **pendiente**. |
| **RNF-06** | Privacidad | Los datos personales de las consultas solo se usan para responder al aspirante y no se publican. | Los datos se guardan en el servidor y los logs no registran el contenido personal (solo registran si cada campo está presente). | Implementado en `contact_routes.py` (los logs solo indican si cada campo está presente). |

---

## 6. Casos de uso

### UC-01 – Aspirante consulta una carrera y envía una consulta

- **Actor principal:** aspirante.
- **Actor secundario:** Secretaría, que recibe la notificación.
- **Precondición:** el sitio está disponible.
- **Requisitos relacionados:** RF-01, RF-02, RF-03, RF-04.

**Flujo principal:**

1. El aspirante ingresa a la página principal desde un buscador o un enlace.
2. Accede a `/carreras` y elige una tecnicatura.
3. Lee el detalle de la carrera y los requisitos de ingreso (`#requisitos`).
4. Abre el formulario de consulta y completa su nombre, email o teléfono, la carrera de interés y un comentario.
5. El formulario valida cada paso y el aspirante envía la consulta.
6. El sistema valida los datos en el servidor, registra la consulta y notifica a la institución.
7. El sistema muestra al aspirante la confirmación del envío.

**Flujos alternativos:**

- **4a.** El aspirante no indica email ni teléfono: el formulario muestra el mensaje de validación y no permite avanzar.
- **6a.** Falla el envío de la notificación: la consulta queda registrada igualmente y la respuesta indica `partial_success`.
- **6b.** El envío proviene de un bot (honeypot completo): el sistema lo descarta sin registrarlo.

**Postcondición:** la consulta queda registrada y la institución puede responderla.

### UC-02 – Buscador o sistema de IA indexa el sitio

- **Actor principal:** rastreador de buscador (por ejemplo, Googlebot) o bot de IA (por ejemplo, GPTBot).
- **Precondición:** el sitio está publicado en `https://isftn199.com.ar`.
- **Requisitos relacionados:** RF-06, RF-07, RF-08.

**Flujo principal:**

1. El rastreador solicita `/robots.txt` y obtiene las reglas de acceso y la ubicación del sitemap.
2. Solicita `/sitemap.xml` y obtiene las URLs canónicas de la página principal, las carreras, los cursos y la página de contacto.
3. Recorre cada URL y lee el contenido HTML junto con los datos estructurados JSON-LD.
4. En el caso de un sistema de IA, consulta además `/llms.txt` para obtener un resumen institucional.
5. Las páginas quedan indexadas y la institución verifica el resultado en Google Search Console.

**Flujos alternativos:**

- **2a.** El rastreador accede a una URL no canónica (`www`, `http` o con barra final): el sistema responde 301 a la URL canónica.
- **3a.** El rastreador accede a una URL inexistente: el sistema responde 404 con `noindex`.

**Postcondición:** las páginas institucionales pueden aparecer en resultados de búsqueda y en respuestas de asistentes de IA.

### UC-03 – Estudiante consulta una lección del campus virtual

- **Actor principal:** estudiante.
- **Requisitos relacionados:** RF-05.

**Flujo principal:**

1. El estudiante ingresa a `/cursos`.
2. Elige un curso y luego una lección.
3. El sistema muestra la lección generada desde Markdown, con resaltado de código.

**Flujo alternativo:**

- **2a.** El curso o la lección no existen: el sistema responde 404.

---

## 7. Trazabilidad con el Lean Canvas

| Requisito | Problema del Canvas que atiende (sección 1) | Elemento de la solución (sección 4) | Métrica clave (sección 6) | En el MVP (sección 8) |
|---|---|---|---|---|
| RF-01 Página principal | Información institucional dispersa | Consultar información general | Visibilidad orgánica | Sí |
| RF-02 Carreras | Falta de claridad sobre carreras y cursos | Acceder a carreras y propuestas educativas | Visibilidad orgánica, indexación | Sí |
| RF-03 Requisitos de ingreso | Información dispersa para aspirantes | Acceder a información de carreras | Consultas recibidas | Sí |
| RF-04 Formulario de consulta | Dificultad para contactar a la institución | Formularios de consulta | Consultas recibidas | Sí |
| RF-05 Cursos | Falta de claridad sobre cursos | Consultar cursos y capacitaciones | Indexación | Sí |
| RF-06 SEO técnico | Baja visibilidad en buscadores | SEO, sitemap, robots.txt, datos estructurados | Indexación, visibilidad orgánica | Sí |
| RF-07 GEO | Baja visibilidad en buscadores y en IA | Estrategias GEO | Visibilidad orgánica | Sí |
| RF-08 Medición | Todos (permite verificar si se resuelven) | Evaluación del funcionamiento | Todas las métricas | Sí (parcial) |
| RF-09 SEM | Baja visibilidad en buscadores | Evaluar campañas SEM | Visibilidad (pago) | No (futuro) |
| RNF-01 Rendimiento | Baja visibilidad (la velocidad influye en el posicionamiento) | Mejoras SEO | Rendimiento (PageSpeed ≥ 80) | Sí |
| RNF-02 Disponibilidad | Dificultad para acceder a la información | Sitio accesible | Disponibilidad ≥ 99 % | Sí |

Todas las métricas clave del Lean Canvas tienen al menos un requisito que las hace medibles.

---

## 8. Restricciones, tecnologías y estado actual

### 8.1 Restricciones

- **Gratuidad:** no se pueden publicar precios, matrículas ni aranceles. Las rutas comerciales antiguas redirigen al catálogo.
- **Veracidad:** el sitio no puede mostrar títulos, materias ni resoluciones que no estén en `data/content/carreras.yaml`.
- **Contenido desacoplado:** los textos y catálogos se cargan en `data/` (YAML y Markdown), nunca en el código Python ni en las plantillas.
- **Arquitectura:** se respeta la arquitectura en capas definida en `AGENTS.md`. La capa de dominio no usa dependencias externas.
- **Calidad:** todo cambio debe pasar las pruebas (`pytest` con cobertura ≥ 85 %), Pyright, el chequeo de tipos de JavaScript y la verificación de arquitectura antes de publicarse.
- **SEM:** depende de presupuesto y de autorización institucional.

### 8.2 Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python, FastAPI, renderizado en servidor con Jinja2 |
| Validación | Pydantic (DTOs en `src/application/dtos/`) |
| Persistencia | SQLAlchemy y MySQL (registro de consultas) |
| Frontend | HTML, Tailwind CSS v4, JavaScript tipado con JSDoc |
| Contenido | Archivos YAML y Markdown en `data/` |
| Calidad | pytest, Pyright, Ruff y `scripts/verify_architecture.py` |
| Control de versiones | Git y GitHub (ramas `alumno/<usuario>/<tarea>` hacia `develop`) |
| Despliegue | VPS con GitHub Actions desde `main` |

### 8.3 Estado actual

| Funcionalidad | Estado |
|---|---|
| Página principal, catálogo de carreras y requisitos de ingreso | Implementado |
| Formulario de consulta con validación, honeypot y registro | Implementado |
| Campus virtual de cursos | Implementado |
| Sitemap, robots.txt, JSON-LD, URLs canónicas y redirecciones 301 | Implementado |
| `llms.txt` y acceso para bots de IA | Implementado |
| Verificación en Google Search Console | Parcial (el archivo de verificación existe; falta la línea base) |
| Monitoreo de disponibilidad y medición en PageSpeed | Pendiente |
| Revisión manual de diseño adaptable | Pendiente |
| Campañas SEM | Futuro |
| Sistema completo de inscripción académica | Futuro (fuera del MVP) |

Los estados "Implementado" se basan en el código del repositorio y en la ejecución local de las pruebas relacionadas (`tests/test_seo.py`, `test_carreras.py`, `test_cursos.py`, `test_contact_form_validation.py`, `test_contact_form_honeypot.py`, `test_llms_txt.py`, `test_canonical_redirects.py`, `test_additional_routes.py`, entre otras). En esa ejecución, la única prueba que falló fue `test_ready_endpoint`, porque necesita una base de datos que no estaba disponible en el entorno local. No corresponde a un requisito de este SRS.

---

## 9. Consideraciones finales

Este SRS traduce el Lean Canvas en requisitos verificables. Las métricas son objetivos propuestos y no resultados alcanzados. Los requisitos en estado "Parcial", "Pendiente" o "Futuro" se completarán en las siguientes iteraciones, y este documento se actualizará a medida que se obtengan mediciones reales.
