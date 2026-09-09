# Especificaciones Técnicas y Arquitectura del Sistema — ISFT N° 199

> **Proyecto:** Instituto Superior de Formación Técnica N° 199 (`isftn199.com.ar`)  
> **Estado:** Documento Vivo (Living SSOT)  
> **Ámbito:** Arquitectura de software, capas Hexagonal/DDD, catálogo de carreras, campus virtual (LMS), frontend, observabilidad y testing.

---

## 1. Arquitectura de Software: Hexagonal / Limpia & DDD

El código fuente en `src/` sigue estrictamente el patrón de Arquitectura Hexagonal (Ports & Adapters) con Domain-Driven Design (DDD), garantizando el desacoplamiento entre las entidades pedagógicas/institucionales y los frameworks web:

```
src/
├── domain/                      # ENTIDADES Y VALUE OBJECTS PURAS (Python estándar @dataclass)
│   ├── common/                  # Value Objects comunes y excepciones de dominio puro.
│   ├── content/                 # Entidades del catálogo: Carrera, Secciones Institucionales.
│   ├── leads/                   # Entidades de aspirantes, consultas académicas y preinscripciones.
│   ├── lms/                     # Entidades de cursos, materias, lecciones y evaluaciones.
│   └── repositories/            # Interfaces/puertos abstractos de persistencia (LeadRepository).
├── application/                 # CASOS DE USO, SERVICIOS DE APLICACIÓN Y DTOs (Pydantic)
│   ├── data_service.py          # Servicio de acceso a datos estructurados (carreras, cursos, YAML, Markdown).
│   ├── dtos/                    # Modelos de validación Pydantic (CarreraModel, content, seo, course).
│   ├── gateways/                # Interfaces de salida (NotificationGateway, EmailGateway).
│   ├── mappers/                 # Mappers bidireccionales entre entidades y DTOs/modelos.
│   └── use_cases/               # Casos de uso de negocio orquestados (SubmitLeadUseCase).
├── adapters/                    # ADAPTADORES AGNOSTICOS DE FRAMEWORK
│   └── presenters/              # Presenters para transformar datos en estructuras de renderizado.
└── infrastructure/              # INFRAESTRUCTURA, FRAMEWORKS, PERSISTENCIA Y MIDDLEWARE
    ├── fastapi/                 # Inicialización de FastAPI, middleware (RequestId, CSP, Cache), dependencias.
    │   ├── routes/              # Endpoints HTTP limpios (carreras, course, contact, main, seo).
    │   └── utils/               # Utilidades web (generación de URLs canónicas y SEO).
    ├── gateways/                # Adaptadores de notificación (EmailGateway, TelegramGateway).
    ├── persistence/             # Persistencia en base de datos SQLAlchemy/MySQL y SQLite fallback.
    └── settings/                # Configuración de entorno y logging estructurado (config.py).
```

### 1.1 Reglas de Dependencia Inviolables
* **`domain`:** Cero dependencias externas (prohibido Pydantic, FastAPI, SQLAlchemy en domain).
* **`application`:** Solo depende de `domain` y librerías de soporte (Pydantic, PyYAML).
* **`adapters`:** Transforma datos entre capas sin acoplarse a FastAPI.
* **`infrastructure`:** Implementa los puertos de `application` y conecta con FastAPI, MySQL o SMTP.
* **Endpoints HTTP:** No contienen lógica de negocio ni de persistencia; delegan siempre en servicios de aplicación.
* **Verificación automatizada:** `python3 scripts/verify_architecture.py`.

---

## 2. Ecosistema de la Plataforma Digital ISFT N° 199

El sistema opera como una plataforma integral de comunicación académica y pedagogía digital:

| Componente | Rol en el Ecosistema | Ruta / Endpoint | Tecnología |
|---|---|---|---|
| **Portal Institucional** | Comunicación institucional, oferta académica, ingreso y contacto | `/`, `/carreras`, `/contact` | FastAPI SSR + Jinja2 + Tailwind v4 |
| **Catálogo de Carreras** | Fichas curriculares, perfiles profesionales y mallas de 3 años | `/carreras`, `/carreras/{slug}` | Datos YAML (`data/content/carreras.yaml`) |
| **Campus Virtual (LMS)** | Aulas técnicas, material didáctico y lecciones interactivas | `/cursos`, `/cursos/{curso_slug}` | Markdown estructurado (`data/core/cursos/`) |
| **Preinscripción & Consultas** | Captura y seguimiento de aspirantes a tecnicaturas | `#ingreso`, `POST /api/v1/contact` | Pydantic DTOs + MySQL/SQLite + Email/Telegram |

---

## 3. Frontend, Renderizado y Performance

### 3.1 Motor de Plantillas Jinja2 y Componentes
* Las plantillas en `templates/` siguen un esquema modular de componentes y macros en `templates/partials/components/`:
  - `planes.html`: Macro reutilizable `planes(data, phone, catalog, show_header)` para home y pricing.
  - `header.html` y `footer.html`: Layout global con enlaces y branding.
  - `contact_section.html` y `contact_form.html`: Formulario multi-paso con captura de UTMs y `gclid`.
  - `faq_item.html`: Acordeón accesible.
* **Regla R1 (Estricta):** Prohibido Jinja dentro de atributos `style="..."` excepto para CSS custom properties (`style="--nombre: {{ dato }}"`). Validado con `python3 scripts/validate_templates.py`.

### 3.2 Estrategia de CSS Crítico (Critical CSS) & Tailwind v4
* **Above-the-fold Instantáneo:** El CSS crítico reside en `static/css/src/critical.css` y `tokens.css`, inyectándose inline en `<head>` vía `templates/partials/critical_css.html` (<14KB).
* **Bundle Asíncrono:** Tailwind CSS v4 con `@import "tailwindcss" prefix(tw);` se compila a `static/css/index.css` y se carga de forma diferida.
* **Regeneración de CSS Crítico:** `python3 scripts/build_critical_css.py` o `npm run build:css`.

---

## 4. Observabilidad, Seguridad y Testing

### 4.1 Middleware, Seguridad HTTP y Google Ads
* **X-Request-ID:** Genera un identificador único `req_<uuid>` por petición y lo inyecta en los headers de respuesta y en los logs estructurados.
* **Content-Security-Policy (CSP):** Configurado en `security_headers_middleware` con lista blanca estricta para telemetría, analytics y balizas de conversión de Google Ads (`googleadservices.com`, `googleads.g.doubleclick.net`, `google.com`, `stats.g.doubleclick.net`, `clarity.ms`).
* **Logs Estructurados:** Registro con timestamp, método, ruta, status code y tiempo de procesamiento en ms.

### 4.2 Tipado Estricto (Pyright & TypeScript LSP)
* Todo el código Python en `src/`, `scripts/` y `tests/` cuenta con type annotations completas verificadas con `pyright` (0 errores).
* Queda prohibida la inicialización de colecciones sin tipo explícito (`items: list[str] = []`).
* Todo el código JavaScript en `static/js/` está tipado con JSDoc y gobernado por `jsconfig.json` y `globals.d.ts`, validado mediante `npm run typecheck:js` (0 errores LSP).

### 4.3 Suite de Pruebas Automatizadas (pytest)
* Pruebas unitarias, de integración y de endpoints con `pytest` y `pytest-asyncio` utilizando `httpx.AsyncClient` sobre la app real con datos YAML.
* Ejecución y cobertura mínima obligatoria: `>= 85%` (ver comandos en [README.md §4](file:///home/agustin/proyectos_software/www-datamaq/README.md#L53-L70)).

### 4.4 Suite de Servidores FastMCP para Agentes de IA
* Los servidores FastMCP de analítica y auditoría en tiempo real se encuentran centralizados en el repositorio **`datamaq-hub`**:
  - `mcp_google_ads_server.py`: Auditoría de gasto diario ($1.500 ARS/día), CPC, campañas y search terms.
  - `mcp_ga4_server.py`: Reporte de visitas por URL, fuentes de tráfico, geolocalización en GBA Norte y conversiones.
  - `mcp_clarity_server.py`: Análisis de fricción de UX en vivo (rage clicks, dead clicks, heatmaps y grabaciones).
* Manual y especificación completa: [`docs/certezas_y_dudas_datamaq_hub.md`](certezas_y_dudas_datamaq_hub.md).

---

## 5. Arquitectura del Subsistema de Leads y Contactos (Roundcube SSOT)

### 5.1 Flujo de Formularios Completos (`POST /api/v1/contact`)
1. **SSOT (Libreta de Contactos y Consultas):**
   - Los datos del contacto se unifican en `roundcube.contacts` en MySQL para la cuenta `isft199@gmail.com`.
   - **Deduplicación:** Se busca coincidencia por `email` o teléfono antes de la persistencia. Si ya existe, se actualiza la vCard 3.0 (`name`, `email`, `phone`, `organization`, `note`) concatenando el nuevo mensaje para preservar el historial del aspirante.
2. **Respaldo Inmutable (MySQL `datamaq_leads`):**
   - Transacción atómica en `LeadRepositorySQL` que persiste la entidad `Lead` con todos los parámetros analíticos (`utm_source`, `utm_medium`, `utm_campaign`, `gclid`, `page_location`, `user_agent`, timestamp).
3. **Despacho por Correo Electrónico (SMTP):**
   - Notificación estructurada enviada al buzón institucional `isft199@gmail.com`.
4. **Alerta en Telegram:**
   - Mensaje con formato enriquecido en Telegram Bot API con botón de enlace directo a chat de WhatsApp (`wa.me/...`).

### 5.2 Flujo de Eventos de Interacción en CTAs (`/api/v1/events/*`)
1. **Eventos Soportados:** `whatsapp-click` (botón flotante / inline) y `direct-contact` (`email_click`, `email_copy`, `phone_click`, `phone_copy`).
2. **Despacho Inmediato a Telegram:** Formato conciso indicando página, campaña UTM, elemento interactuado y tipo de dispositivo.
3. **Aislamiento de Buzón y Contactos:** No se despachan correos electrónicos ni se insertan contactos incompletos en Roundcube para mantener limpios ambos canales.
4. **Registro Analítico:** Inserción ligera en `datamaq_leads.leads` (`lead_source="whatsapp_cta"` o `lead_source="direct_contact_..."`) para atribución First-Touch.

