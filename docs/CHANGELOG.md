# Registro Histórico de Cambios e Hitos (CHANGELOG) — ISFT N° 199

Este documento consolida cronológicamente las decisiones estratégicas, refactorizaciones arquitectónicas y evoluciones del portal institucional y campus virtual del **Instituto Superior de Formación Técnica N° 199** (`isftn199.com.ar`).

## [2026-09-03] — Migración Integral hacia Portal Institucional y Campus Virtual ISFT N° 199

* **Catálogo Académico Oficial (`data/content/carreras.yaml`):**
  * Incorporación de las 6 tecnicaturas superiores oficiales de 3 años con validez nacional: *Ciencia de Datos e IA*, *Mecatrónica*, *Logística*, *Higiene y Seguridad en el Trabajo*, *Administración de Recursos Humanos* y *Servicios Gastronómicos y Turismo*.
  * Mallas curriculares, perfiles profesionales del egresado, resoluciones DGCyE y campo ocupacional.
* **Arquitectura Hexagonal & DDD en `src/`:**
  * Nueva entidad pura `@dataclass Carrera` en `src/domain/content/entities.py`.
  * DTOs Pydantic `CarreraModel` y `CarrerasContainerModel` en `src/application/dtos/content_dto.py`.
  * Métodos `get_carreras()` y `get_carrera_by_slug()` en `DataService`.
  * Router `carreras_routes.py` con endpoints `/carreras`, `/carreras/{carrera_slug}` e `/inscripciones`.
  * Inyección dinámica de carreras en `index()` y en `sitemap.xml`.
* **Redirecciones Permanentes 301 de Rutas Comerciales:**
  * `/pricing` y `/planes` redirigen con código HTTP 301 directamente al catálogo académico `/carreras`.
  * `/inscripciones` redirige con 301 a `/carreras#requisitos`.
* **Vistas, Plantillas y UX Educativa (`templates/`):**
  * `templates/carreras.html`: Catálogo con filtros temáticos, badges y guía de requisitos de ingreso.
  * `templates/carrera_detail.html`: Ficha curricular detallada con perfil del egresado y CTA de preinscripción.
  * `templates/partials/components/header.html`: Identidad ISFT N° 199, navegación a Carreras, Campus Virtual, Ingreso y Contacto con ícono de birrete universitario (`mortarboard-fill`).
* **Configuración, SEO y Datos Institucionales:**
  * Canónica oficial `https://isftn199.com.ar` en `seo.yaml`.
  * Identidad de sede en El Talar, Tigre (Maestra Celina Voena 1750), turno vespertino (18:00 a 22:30 hs) y contacto `isft199@gmail.com` en `brand.yaml`.
  * Pasos de inscripción con título secundario, cuerpo docente y FAQs académicas en `home_sections.yaml`.
* **Suite Documental y de Gobernanza:**
  * Actualización integral de `AGENTS.md`, `docs/srs.md`, `docs/specs.md`, `docs/todo.md` y `README.md`.
* **Control de Calidad:**
  * 529 tests pasando en `pytest` (100%), 0 errores en `pyright`, 0 errores en TypeScript LSP y 100% Clean Architecture verificada.

---

## [2026-08-28] — DX Consola: Eliminación de Cloudflare Insights, CSP Declarativa y Reportes de Violación

* **Eliminación de Cloudflare Web Analytics (`beacon.min.js`):**
  * Removido el `<script>` estático incondicional de `templates/partials/head.html`, que se cargaba antes del consentimiento y generaba errores CORS en navegadores con protección de rastreo (ETP, uBlock, Brave Shields).
  * GA4 + Google Ads + Microsoft Clarity siguen cubriendo la analítica bajo consentimiento fail-closed.
  * Removidos `https://static.cloudflareinsights.com` y `https://cloudflareinsights.com` de las directivas `script-src` y `connect-src` de la CSP.
* **Refactorización de la CSP a builder declarativo:**
  * Nuevo módulo `src/infrastructure/fastapi/csp.py` con `_CSP_DIRECTIVES: dict[str, list[str]]` y `build_csp(telemetry_hosts)`.
  * Sustituye el string monolítico de ~1100 caracteres en `middleware.py`, mejorando legibilidad, mantenibilidad y testabilidad por directiva.
* **Reportes de violación CSP conectados:**
  * Añadida la directiva `report-uri /csp-report` a la CSP en modo enforcement.
  * El endpoint `POST /csp-report` ahora loguea el reporte a nivel `warning` (truncado a 4 KB) manteniendo la respuesta `204 No Content`.
* **Control de Calidad:**
  * Nuevos tests unitarios en `tests/test_csp_builder.py` y contratos de regresión en `tests/test_csp_headers.py` y `tests/test_privacidad_frontend.py`.

---

## [2026-08-28] — Corrección Integral de CSP, Endpoint /csp-report, Desacoplamiento y Observabilidad

* **Observabilidad de Despliegues y Versionado (Commit SHA):**
  * Inyección automática del hash SHA corto del commit actual (`GIT_COMMIT_SHA` vía variable de entorno o `git rev-parse --short HEAD`).
  * Visualización sutil de la versión de despliegue en el pie de página (`templates/partials/components/footer.html`) y en la cabecera HTTP de respuesta `X-Commit-SHA`.
* **Content-Security-Policy (CSP) Completa y Robusta:**
  * Ampliación de orígenes autorizados en `src/infrastructure/fastapi/middleware.py` para Google Ads (`ad.doubleclick.net`, `googleads.g.doubleclick.net`, `google.com.ar`, `*.google.com`, `*.google.com.ar`), Google Analytics 4 (`analytics.google.com`, `*.google-analytics.com`), Microsoft Clarity (`scripts.clarity.ms`, `c.clarity.ms`, `*.clarity.ms`), Bing (`c.bing.com`, `*.bing.com`) y Cloudflare Web Analytics (`static.cloudflareinsights.com`, `cloudflareinsights.com`).
  * Creación del endpoint `POST /csp-report` en `src/infrastructure/fastapi/routes/main_routes.py` respondiendo `204 No Content` para recibir reportes de navegadores limpiamente sin errores 405.
  * Desactivación de la cabecera Report-Only obsoleta en `/etc/nginx/conf.d/security-headers-common.conf` de la VPS DonWeb.
* **Optimización de Cookies en Frontend:**
  * Configuración explícita de `cookie_domain: 'auto'` y `cookie_flags: 'SameSite=Lax;Secure'` en `ThirdPartyScriptsManager.js` para suprimir advertencias de dominio de cookies en navegadores con ETP.
* **Centralización de Configuración de `middleware.py` en `config.py`:**
  * Parametrización de rate limiting (`RATE_LIMIT_WINDOW_SECONDS`, `RATE_LIMIT_MAX_REQUESTS`), directivas de caché (`HTML_CACHE_CONTROL`) y cabeceras HSTS (`HSTS_HEADER`).
  * Inyección dinámica de `TELEMETRY_API_URL` y `TELEMETRY_WS_URL` en `connect-src` de la CSP.
  * Limpieza de imports ubicando `from src.infrastructure.settings import config` en la cabecera del archivo.
* **Desacoplamiento Total de Valores Hardcodeados en `*.py`:**
  * Reemplazo de URLs y dominios literales en `sitemap.xml`, gateways de notificación (`ga4_measurement_gateway.py`, `email_notification_gateway.py`) por `config.BASE_URL`.
  * Reemplazo de email corporativo de fallback en `contact_routes.py` y `telegram_notification_gateway.py` por `config.NOTIFICATION_EMAIL`.
  * Reemplazo de cadenas `" | DataMaq"` en `seo_routes.py`, `industry_routes.py` y `landing_routes.py` por `brand_data['brandName']` y metadatos dinámicos de `landings.yaml`.
* **Control de Calidad:**
  * 485 pruebas unitarias pasadas (100%), 88.87% de cobertura, 0 errores en Pyright y Typecheck JS.

---

## [2026-08-28] — Arquitectura de Contactos Roundcube SSOT, Deduplicación y Notificaciones Duales

* **Roundcube como Fuente Única de Verdad (SSOT):**
  * Definición canónica de la libreta de contactos en MySQL (`roundcube.contacts` bajo la cuenta `info@datamaq.com.ar` con vCard 3.0).
  * Regla estricta de no duplicación: deduplicación por email y teléfono con enriquecimiento incremental de historial de notas ante múltiples consultas.
* **Separación de Flujos de Notificación y Respaldo:**
  * **Formularios completados (`/contact`, landings):** Cuádruple acción integrada: (1) Upsert en Roundcube contacts, (2) Respaldo inmutable en `datamaq_leads.leads` (MySQL), (3) Despacho de email estructurado vía SMTP a `info@datamaq.com.ar`, (4) Alerta en tiempo real en Telegram con enlace directo a WhatsApp.
  * **Eventos de interacción con CTAs (WhatsApp Flotante, Click/Copia de Mail o Teléfono):** Despacho instantáneo a Telegram con contexto de navegación y atribución en base de datos, aislando el buzón de correo de spam y la libreta de Roundcube de contactos vacíos.
* **Consolidación de Certeza C-15 & Suite Documental:**
  * Formalización de la Certeza **C-15** en `docs/todo.md` y actualización exhaustiva de `README.md`, `AGENTS.md`, `docs/specs.md`, `docs/srs.md`, `docs/ops.md`, `docs/certezas_y_dudas_datamaq_hub.md` y `.agents/canvas/*.md`.

---

## [2026-08-25] — Integración de Métricas Centralizadas, Gobernanza Canvas y Verificación de Calidad


* **Conexión y Métricas Centralizadas con `datamaq-hub`:**
  * Configuración del acceso a Microsoft Clarity, Google Ads y Google Analytics desde el repositorio hermano en `../datamaq-hub`.
* **Gobernanza Canvas & Auditoría de Subagentes:**
  * Despliegue de tres subagentes especializados (Bloque 2: Segmentos, Bloque 3: Canales, Bloque 9: Costos) para validar la consistencia de segmentación (PyMEs GBA Norte), conversión analítica del LMS, y estabilidad financiera (OPEX ultraliviano y break-even).
  * Confirmación de la exclusión activa de los cursos académicos (ISFT 199) de la indexación SEO (`noindex, nofollow`) y exclusión automática en `sitemap.xml`.
* **Control de Calidad Automatizado y de Tipos:**
  * Validación de la suite completa de pruebas unitarias y de integración: **442 tests pasados (100% de éxito)**.
  * Verificación estática con **0 errores** en Pyright (tipos de Python) y `tsc -p jsconfig.json --noEmit` (tipos de JavaScript).
  * Validación de arquitectura limpia hexagonal/DDD al 100% mediante `scripts/verify_architecture.py`.

---

## [2026-08-24] — Consolidación de Certezas C-11 a C-14, Tipado Estricto Frontend y Prompt Maestro de Deep Research

* **Analítica Web, Tracking Nativo y Activación FastMCP GA4:**
  * Activación y validación en vivo del servidor FastMCP de Google Analytics 4 (`scripts/mcp_ga4_server.py`) conectado con la propiedad `533265197` vía Service Account (`ga4-analytics-reader@datamaq-505320.iam.gserviceaccount.com`).
  * Implementación de segmentación analítica en FastMCP (`segment='all'`, `'commercial'`, `'academic'`) aislando el embudo industrial/PyME del tráfico educativo de los alumnos.
  * Disparo nativo de eventos de conversión en frontend (`static/js/app.js` y `static/js/modules/FormManager.js`) mediante `window.gtag('event', 'whatsapp_click', ...)` y `window.gtag('event', 'generate_lead', ...)` con `transport_type: 'beacon'`.
* **Catálogo de Cursos LMS y Navegación Académica:**
  * Incorporación del selector de visualización en `templates/cursos/list.html` conmutando entre cursos públicos destacados (`/cursos`) y el catálogo completo de las 13 materias académicas para alumnos (`/cursos?view=all`).
* **Estrategia Comercial, Docencia y Certezas de Negocio (C-11 a C-14):**
  * Consolidación de **C-11**: Consultoría 5b bajo honorario profesional cerrado predecible (+10% a +30% sobre mercado) con visita deducible al 100% ($35.000 ARS), descartando el *Success Fee*.
  * Consolidación de **C-12**: Escala tarifaria de consultoría por categoría de suministro de Edenor (T2: $140.000 ARS; T3 BT: $220.000 ARS; T3 MT: $340.000 ARS; 50% desc. en acometidas adicionales).
  * Consolidación de **C-13**: Visualización híbrida de catálogo (Precio de lista + cuotas Pactar Digital + 25% OFF stacking + WBS modular colapsable).
  * Consolidación de **C-14**: Prioridad a la docencia universitaria (ISFT 199) y captación mediante filtro asíncrono previo (auditoría documental de facturas por WhatsApp/PDF en <3 min) para no canibalizar horas de clase y captar solo proyectos de alto ticket.
* **Calidad y Tipado Estricto Frontend (JSDoc + `npm run typecheck:js`):**
  * Creación de `jsconfig.json` canónico (`moduleResolution: "bundler"`, `checkJs: true`, target `ES2022`) y declaraciones ambientales en `static/js/globals.d.ts` para tipar la interfaz global `Window` (`APP_CONFIG`, `dataLayer`, `gtag`, `clarity`).
  * Contratos centrales con `@typedef` en `static/js/types.js` espejando fielmente los DTOs de Pydantic de backend.
  * Incorporación del script `npm run typecheck:js` (`tsc -p jsconfig.json --noEmit`) en `package.json` para validación estricta de tipos de JavaScript con 0 errores y paridad 100% con el Language Server del IDE.
* **Rendimiento Web y Core Web Vitals (Tarea T-12):**
  * Recompresión y optimización dimensional a `(1200x630)` de `static/media/cursos/og-instalaciones-aplicaciones-energia.webp` reduciendo su peso.
  * Inyección de directiva `fetchpriority="high"` en la imagen hero de `templates/cursos/detail.html` para maximizar LCP.
  * Depuración de almacenamiento eliminando imagen huérfana de 644 KB en `static/media/`.
* **Adquisición SEM y Palabras Clave Negativas (Tarea T-10):**
  * Creación del script extractor `scripts/export_negative_keywords.py` y generación de la Super-Lista Maestra de 119 términos negativos en 8 bloques temáticos (`data/ads/negative_keywords_clean.txt` y `data/ads/negative_keywords_editor.csv`).
* **Investigación Estratégica & Inteligencia B2B (Tarea T-13):**
  * Creación y ejecución del Master Prompt en `docs/prompt_investigacion_profunda_gemini.md` estructurado en 5 ejes estratégicos para ser procesado con Gemini Deep Research / Advanced.
  * Publicación del informe ejecutivo integral en `docs/informe_estrategico_gemini_2026.md` validando el modelo de "Faro de Autoridad", el Payback de 16 a 60 días bajo la Res. ENRE 544/2024, el embudo asíncrono de facturas PDF en 3 min y la formalización de 3 líneas de ingresos remotos (Tele-Peritaje $95k, Capacitaciones Virtuales $250k y Retainer Insights $45k-$80k/mes).

---

## [2026-08-23] — Formalización de la Tríada del Ecosistema, Motor WBS de Pricing y CSP para Google Ads

* **Ecosistema Tecnológico de 3 Repositorios:**
  * Formalización y documentación de la tríada de repositorios desacoplados con sus rutas absolutas en local (`/home/agustin/proyectos_software/...`), VPS DonWeb (`/var/www/...`) y GitHub (`git@github.com:datamaq-automation/...`):
    - `www-datamaq`: Web comercial, SEO local, pricing, captura de leads y LMS (FastAPI + Jinja2 SSR, puerto `8001`).
    - `app-datamaq`: Dashboard SPA de telemetría y vitrina pública en tiempo real (`https://app.datamaq.com.ar`).
    - `datamaq-telemetry`: Backend IoT de series temporales, streaming WebSockets e ingesta de hardware Powermeter (puerto `8885`, `https://api.datamaq.com.ar`).
* **Pricing & Motor de Cálculo WBS (Certezas C-06 a C-09):**
  * Definición e implementación de `pricing_structure.yaml` con desglose modular de obra en 5 sub-ítems (viáticos por CP/km, instalación estándar, adicional térmica, acondicionamiento de tablero y configuración cloud).
  * Creación del servicio de aplicación `PricingService` y `PresupuestoCalculadoDTO` con lógica de cálculo de viáticos y stacking de descuentos (10% BAPRO + 15% Vitrina = hasta 25% OFF).
  * Consolidación de la **Certeza C-09**: 60 días de Versión PRO incluidos con cada obra/consultoría (2 ciclos de Edenor) y bifurcación Free posterior ($0 de por vida en Monitoreo Privado Básico o Vitrina Pública Anonimizada).
* **Seguridad, Diagnóstico de VPS y Google Ads:**
  * Auditoría en vivo del servidor VPS DonWeb (`vps-5685053-x.dattaweb.com`) verificando estado activo de `datamaq.service`, persistencia MySQL y presencia de variables de entorno `.env` de producción.
  * Corrección de la cabecera `Content-Security-Policy` en `src/infrastructure/fastapi/middleware.py` para habilitar dominios oficiales de balizas y conversiones de Google Ads (`googleadservices.com`, `googleads.g.doubleclick.net`, `google.com`, `stats.g.doubleclick.net`).
  * Creación de suite de pruebas unitarias `tests/test_csp_headers.py` validando cabeceras de seguridad.
* **Suite de Servidores FastMCP & Analítica en Tiempo Real:**
  * Creación y publicación de 3 servidores FastMCP dedicados en `scripts/`:
    - `mcp_google_ads_server.py`: Control de presupuesto diario ($1.500 ARS/día), auditoría de CPC, rendimiento de campañas y detección de palabras clave negativas.
    - `mcp_ga4_server.py`: Consulta de páginas más visitadas, fuentes de tráfico, conversiones y tráfico local en GBA Norte vía Google Analytics Data API v1beta.
    - `mcp_clarity_server.py`: Métricas de UX en vivo (rage clicks, dead clicks, scroll depth y enlaces directos a grabaciones y heatmaps).
  * Flujo de autenticación OAuth2 para Google Ads resuelto mediante `scripts/auth_google_ads.py` y Google OAuth 2.0 Playground, persistiendo `GOOGLE_ADS_REFRESH_TOKEN` en `.env`.
  * Vinculación y federación de cuentas Google Ads completada: `agustin.deoz@gmail.com` (MCC `131-878-0733`) configurada como Administradora de la cuenta comercial `contacto.datamaq@gmail.com` (`405-777-8237`).
  * Presentación formal de la solicitud de **Acceso Básico (Basic Access)** ante Google Ads API con documento técnico de arquitectura generado en PDF (`docs/DataMaq_Google_Ads_API_Tool_Documentation.pdf`).
  * **Auditoría Cruzada de Subagentes FastMCP:** Ejecución en vivo de subagentes paralelos auditando la API de Microsoft Clarity, la cuenta de Google Ads y la telemetría web. Detección heurística de mejoras UX en el stepper de `FormManager.js` y consolidación de la Super-Lista Maestra de Negativas de 8 bloques para blindaje presupuestario B2B.
  * Incorporación de suite de tests unitarios (`tests/test_mcp_clarity.py`, `tests/test_mcp_ga4.py`, `tests/test_mcp_google_ads.py`) alcanzando **446 tests automatizados pasando (100%)** con 0 errores de tipado estricto (Pyright).
* **Armonización Documental SSOT:**
  * Desduplicación masiva y compresión de archivos Markdown (`README.md`, `specs.md`, `ops.md`, `todo.md`), eliminando ambigüedades y delimitando responsabilidades únicas por documento.
  * Consolidación de la **Certeza C-10** (Gobernanza de Cuentas Google & FastMCP) y expansión del roadmap técnico (tareas T-08 a T-12) en `docs/todo.md`.
  * Creación y actualización de manual de gobernanza analítica (posteriormente unificado y migrado a `datamaq-hub` y [`docs/certezas_y_dudas_datamaq_hub.md`](certezas_y_dudas_datamaq_hub.md)).
  * Publicación y blindaje de la ficha técnica oficial de campañas SEM (centralizada en `datamaq-hub` con lista de 119 negativas en `data/ads/`).

---

## [2026-08-20] — Consolidación de Pricing, Packaging por Dolor y Reestructuración Documental
* **Pricing & Negocio:**
  * Consolidación del Trinomio de Valor ("Máquinas + Datos + Dinero").
  * Packaging por dolor: *Pack Cero Multas* (SmartPlus), *Pack Control de Picos* (Automate) y *Pack Fábrica 4.0* (Gateway).
  * Formalización de beneficios acumulables: 10% BAPRO + 15% Vitrina Pública = **hasta 25% OFF total**.
  * Esquema de compra directa de hardware a Powermeter SAS + mano de obra e ingeniería de DataMaq.
  * Visita de relevamiento inicial con diagnóstico 100% deducible de la obra.
  * Anclaje de retorno de inversión: amortización típica estimada en **30 a 60 días**.
* **Arquitectura Documental (El Cuarteto Canónico):**
  * Unificación y sustitución de más de 25 archivos fragmentados por 4 documentos vivos:
    - `docs/srs.md`: Requisitos del sistema, propuesta de valor y catálogo comercial.
    - `docs/specs.md`: Arquitectura Hexagonal/DDD, Critical CSS y testing.
    - `docs/ops.md`: Manual de operaciones en VPS DonWeb y protocolos de deploy.
    - `docs/todo.md`: Registro de certezas consolidadas y backlog de dudas abiertas.

---

## [2026-08-19] — Sistema de Observabilidad y Métricas
* Middleware de trazabilidad `X-Request-ID` (`req_<uuid>`) inyectado en logs y respuestas.
* Logging estructurado de peticiones con cálculo de duración en milisegundos.
* Endpoints de salud: `/healthz` (liveness) y `/ready` (readiness con chequeo de BD y filesystem).

---

## [2026-08-17] — Desacoplamiento de SPA y Nueva Página Canónica de Pricing
* Creación de la página canónica `/pricing` con SEO independiente y macro reutilizable de tarjetas.
* Redirección permanente 301 del alias `/planes` hacia `/pricing`.
* Desacoplamiento total de la SPA de telemetría viva apuntando al subdominio `https://app.datamaq.com.ar`.

---

## [2026-08-15] — Consolidación Territorial en GBA Norte (Pivot AMBA)
* Enfoque comercial y operativo 100% centrado en el corredor industrial de Zona Norte del GBA (Garín, Pilar, Escobar, Tigre, Campana, San Martín).
* Descarte formal de hipótesis de prospección en Oil & Gas / Vaca Muerta en favor de la cercanía operativa y velocidad de respuesta en planta.
* Integración del ecosistema fintech de **Pactar Digital** (pagarés digitales sin ticket mínimo) y convenios con **Banco Provincia**.

---

## [2026-08-14] — Optimización de Performance: Critical CSS & Tailwind v4
* Estrategia de CSS crítico inline (<14KB) para carga instantánea above-the-fold sin bloqueo de renderizado.
* Compilación asíncrona de Tailwind CSS v4 (`static/css/index.css`) con prefijo `tw:`.
* Script de validación de sintaxis de plantillas (`scripts/validate_templates.py` - Regla R1).

---

## [2026-08-10] — Auditoría Integral de Arquitectura y Refactorización Hexagonal
* Implementación estricta de Arquitectura Limpia / Hexagonal y Domain-Driven Design (DDD).
* Aislamiento de la capa `src/domain` con cero dependencias externas (dataclasses estándar).
* Tipado estricto en todo el repositorio con **Pyright** (0 errores, 0 warnings).
* Script de verificación arquitectónica automatizada (`scripts/verify_architecture.py`).
* Incidente de deploy resuelto: lección aprendida de permisos en VPS (*prohibido correr git como root*).
