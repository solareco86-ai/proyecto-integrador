# Especificación de Requerimientos de Software (SRS) — ISFT N° 199

> **Proyecto:** Instituto Superior de Formación Técnica N° 199 (`isftn199.com.ar`)  
> **Estado:** Documento Vivo (Living SSOT)  
> **Ámbito:** Portal institucional, catálogo de tecnicaturas superiores, campus virtual (LMS), admisiones y requerimientos funcionales/no funcionales.

---

## 1. Contexto Institucional y Misión Educativa

### 1.1 Identidad y Dependencia
El **Instituto Superior de Formación Técnica N° 199 de Tigre** es una institución educativa pública de nivel superior técnico dependiente de la Dirección General de Cultura y Educación (DGCyE) de la Provincia de Buenos Aires (Región Educativa 6).

* **Sede Operativa:** Maestra Celina Voena 1750, El Talar, Partido de Tigre, Provincia de Buenos Aires.
* **Turno de Cursada:** Vespertino oficial (18:00 a 22:30 hs), permitiendo compatibilizar los estudios superiores con la actividad laboral.
* **Propósito:** Brindar formación técnica superior pública, gratuita y de excelencia, orientada a las demandas productivas y tecnológicas de Tigre y la Zona Norte del Gran Buenos Aires.

### 1.2 Principio de Educación Pública y Gratuidad Total
* La formación es **100% pública y gratuita de por vida**. No se cobran matrículas, cuotas, derechos de examen ni ningún tipo de arancel.
* Todos los títulos otorgados son oficiales de nivel superior técnico con **validez nacional** y planes de estudio de 3 años de duración aprobados por resoluciones de la DGCyE.
* Las rutas históricas de naturaleza comercial (`/pricing`, `/planes`) cuentan con redirecciones permanentes (HTTP 301) hacia el catálogo académico oficial (`/carreras`).

---

## 2. Oferta Académica Oficial (Catálogo de Tecnicaturas)

La institución ofrece 6 tecnicaturas superiores diseñadas en articulación directa con el entorno socio-productivo:

1. **Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial (Res. 423/24):** Formación en programación Python, pipelines de datos, machine learning, deep learning y gobierno ético del dato.
2. **Tecnicatura Superior en Mecatrónica (Res. 423/24):** Integración de mecánica, electrónica industrial, robótica, automatización y control programable (PLC).
3. **Tecnicatura Superior en Logística (Res. 423/24):** Gestión integral de suministros, centros de almacenamiento, distribución física y comercio exterior.
4. **Tecnicatura Superior en Higiene y Seguridad en el Trabajo (Res. 423/24):** Prevención de riesgos laborales, ergonomía, auditoría de seguridad y normativa SRT.
5. **Tecnicatura Superior en Administración de Recursos Humanos (Res. 423/24):** Gestión del talento humano, relaciones laborales, liquidación de haberes y clima organizacional.
6. **Tecnicatura Superior en Servicios Gastronómicos y Turismo (Res. 423/24):** Gestión hotelera, hospitalidad, gastronomía regional y planificación turística sustentable.

---

## 3. Requerimientos Funcionales del Sistema Web (RF)

* **RF-01 (Portal Institucional / Home):** Renderizado SSR del portal principal con secciones informativas: Hero de educación pública, pilares pedagógicos, catálogo de tecnicaturas, pasos de preinscripción, cuerpo docente, vinculación socio-productiva, preguntas frecuentes y formulario de orientación.
* **RF-02 (Catálogo y Detalle de Carreras `/carreras` y `/carreras/{slug}`):** 
  - Vista general con filtros temáticos y badges oficiales.
  - Páginas de detalle por carrera con resolución ministerial, perfil profesional del egresado, materias destacadas, campo ocupacional y llamado a la acción para preinscripción.
* **RF-03 (Campus Virtual y Aulas Técnicas `/cursos`):**
  - Sistema LMS integrado con módulos formativos, materias y talleres prácticos (Python, FastAPI, Sistemas Operativos, Electrónica).
  - Renderizado server-side de lecciones en Markdown con resaltado de sintaxis (Pygments).
* **RF-04 (Orientación al Aspirante y Preinscripción `/contact` y `#ingreso`):** Formulario multi-paso interactivo con validación Pydantic para capturar consultas de aspirantes (nombre, contacto, tecnicatura de interés, situación de estudios secundarios) y despacho seguro a Secretaría.
* **RF-05 (Redirecciones Permanentes 301):** Redirección 301 de URLs obsoletas (`/pricing`, `/planes`) hacia `/carreras`, y de `/inscripciones` hacia `/carreras#requisitos`.
* **RF-06 (Sitemap Dinámico y SEO Educativo):** Generación automática de `sitemap.xml` incorporando todas las carreras oficiales, URLs canónicas con protocolo HTTPS y metadatos educativos estructurados (Schema.org).

---

## 4. Requerimientos No Funcionales (RNF)

* **RNF-01 (Arquitectura Limpia & DDD):** Separación estricta de capas (`domain`, `application`, `adapters`, `infrastructure`). La capa `domain` tiene cero dependencias externas.
* **RNF-02 (Performance & Core Web Vitals):** Inyección de Critical CSS inline (<14KB) para carga instantánea above-the-fold, lazy-loading de assets y preflight de Tailwind v4 en bundle asíncrono.
* **RNF-03 (Tipado Estricto):** 100% del código en `src/`, `scripts/` y `tests/` verificado con `pyright` (0 errores), y código JavaScript en `static/js/` tipado con JSDoc validado con `npm run typecheck:js` (0 errores LSP).
* **RNF-04 (Cobertura de Pruebas):** Suite automatizada de pruebas unitarias y de integración con `pytest` manteniendo cobertura >= 85%.
* **RNF-05 (Observabilidad y Seguridad):** Middleware de `X-Request-ID`, registro de logs estructurados con tiempo de respuesta, headers de seguridad HTTP y protección de datos conforme a la normativa vigente.
