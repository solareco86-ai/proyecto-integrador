# SRS-SPECS: Portal Institucional y Campus Virtual — Single Source of Truth (SSOT)

> **Documento:** `docs/srs-portal-isftn199.md`  
> **Versión:** `1.0.0`  
> **Estado:** `Borrador en Revisión`  
> **Fecha:** `2026-09-09`  
> **Institución:** Instituto Superior de Formación Técnica N° 199 (Tigre, Pcia. de Buenos Aires)  
> **Repositorio:** `solareco86-ai/proyecto-integrador`  

---

## 1. Contexto Estratégico & Propuesta de Valor

### 1.1. Foco Estratégico & Alcance
* **Misión Institucional:** Plataforma digital oficial y aula virtual para la educación superior técnico-profesional pública y gratuita dependiente de la DGCyE (Provincia de Buenos Aires, Región 6).
* **Público Objetivo (Personas):**
  * **Aspirante / Estudiante:** Consulta de tecnicaturas superiores, requisitos de ingreso, cursadas, talleres prácticos en el campus y material interactivo.
  * **Docente / Cátedra:** Publicación de contenidos de clases en Markdown estructurado, laboratorios de código y evaluaciones.
  * **Secretaría / Coordinación:** Gestión de consultas de postulantes (leads), trazabilidad de aspirantes y canales de contacto directo.
* **Alcance Geográfico & Modalidad:** Sede en Maestra Celina Voena 1750, El Talar (Tigre). Formación presencial vespertina con soporte digital del campus virtual en `/cursos`.
* **Fuera de Alcance:** Cobro de matrículas o aranceles (educación 100% pública y gratuita). Pasarelas de pago no aplicables.

### 1.2. Pilares de Valor de la Solución
| Pilar | Enfoque | Implementación en este Sistema |
| :--- | :--- | :--- |
| **1. Entorno Educativo & Activos** | 6 Tecnicaturas Superiores (Ciencia de Datos e IA, Mecatrónica, Logística, Higiene y Seguridad, RRHH, Servicios Gastronómicos y Turismo). | Catálogo oficial desacoplado en `data/content/carreras.yaml` y campus técnico en `data/core/cursos/`. |
| **2. Arquitectura de Software** | Rendimiento web de alta velocidad, SEO optimizado y mantenibilidad estricta. | Arquitectura Hexagonal / DDD en Python con FastAPI + Jinja2 SSR, Tailwind CSS v4 y datos estáticos YAML/Markdown. |
| **3. Impacto Comunitario** | Acceso universal a la formación superior técnica y vinculación socio-productiva en Zona Norte. | Cero barreras arancelarias, diseño responsivo móvil accesible y orientación directa vía WhatsApp y formularios. |

---

## 2. Modelo de Negocio Social & Gobernanza

### 2.1. Matriz de Gobernanza Institucional
* **Alianzas Clave:** DGCyE PBA, empresas e industrias del Parque Industrial de Tigre y Zona Norte del GBA.
* **Actividades Clave:** Difusión de oferta académica, inscripción y orientación de ingresantes, dictado de cátedras técnicas y prácticas profesionalizantes.
* **Recursos Clave:** Repositorio institucional auditado con herramientas AST, contenidos curriculares abiertos y despliegue continuo automatizado en VPS.
* **Canales Oficiales:** Portal web (`isftn199.com.ar`), correo institucional (`isft199@gmail.com`), WhatsApp de secretaría (+54 11 5629 7160).

---

## 3. Requisitos del Sistema (SRS)

### 3.1. Requisitos Funcionales (FR)
* **FR-01 (Catálogo Académico):** Presentación de planes de estudio oficiales, perfiles profesionales y materias de las 6 tecnicaturas desde `data/content/carreras.yaml`.
* **FR-02 (Campus Virtual / LMS Desacoplado):** Módulo `/cursos` con soporte para lecciones modulares en Markdown con syntax highlighting y cuestionarios de autoevaluación interactivos (quizzes).
* **FR-03 (Captura de Aspirantes / Leads):** Formularios con validación en servidor (Pydantic DTOs), protección anti-spam por Honeypot, almacenamiento persistente (MySQL/SQLAlchemy) y despacho de notificaciones (Email, Telegram).
* **FR-04 (SEO y Metadatos Semánticos):** Generación dinámica de `sitemap.xml`, `robots.txt`, `llms.txt`, etiquetas OpenGraph y esquemas JSON-LD (EducationalOrganization, Course, BreadcrumbList).
* **FR-05 (Redirecciones Canónicas):** Mapeo de rutas históricas (`/pricing`, `/planes`) hacia `/carreras` con códigos HTTP 301.

### 3.2. Requisitos No Funcionales (NFR) & Guantelete de Calidad
* **NFR-01 (Arquitectura Limpia & DDD):**
  * `src/domain`: Capa pura usando únicamente estándar Python (`dataclass`, `typing`, `abc`). Cero dependencias externas (prohibido Pydantic, FastAPI o bases de datos).
  * `src/application`: Use Cases, DTOs de validación con Pydantic y servicios de aplicación.
  * `src/adapters`: Presenters desacoplados.
  * `src/infrastructure`: Rutas FastAPI (Thin Controllers), persistencia e integraciones externas.
* **NFR-02 (Auditoría AST Determinística):** Cumplimiento innegociable de:
  * `scripts/verify_architecture.py` (capas, thin controllers, imports relativos prohibidos, detección de credenciales en código).
  * `tests/test_god_components.py` (control estricto sobre clases y funciones sobredimensionadas).
  * `tests/test_clean_design.py` (prevención de código muerto y sobreingeniería).
* **NFR-03 (Cobertura de Pruebas):** Cobertura global de código ejecutada en Pytest requerida estrictamente en `>= 85%`.
* **NFR-04 (Tipado Estricto):** Cero diagnósticos pendientes en Pyright (`pyright src/`) y TypeScript LSP (`tsc --noEmit`).

---

## 4. Convenciones de Desarrollo y Despliegue

### 4.1. Estrategia de Ramas (Git Flow Institucional)
* `main`: Rama de producción vinculada al VPS. Protegida con Pull Requests requeridas. Despliegue automático vía GitHub Actions.
* `develop`: Rama base de desarrollo e integración colaborativa.
* `alumno/<nombre>/<tarea>`: Ramas personales de trabajo para estudiantes y docentes colaboradores.

### 4.2. Flujo de Control de Cambios
1. Todo cambio se verifica localmente en CPU ($0 tokens) mediante el hook `pre-push.sh`.
2. Las revisiones de PRs hacia `develop` las conduce la Alumna Referente (`solareco86-ai`) o el Profesor (`datamaq-automation`).
3. La promoción de `develop` a `main` es coordinada por el Profesor previo release a producción.
