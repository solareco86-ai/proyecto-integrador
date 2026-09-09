# Roadmap, Certezas y Backlog de Decisiones (TODO) — ISFT N° 199

> **Proyecto:** Instituto Superior de Formación Técnica N° 199 (`isftn199.com.ar`)  
> **Estado:** Documento Vivo (Living SSOT)  
> **Ámbito:** Registro de certezas consolidadas, catálogo de carreras y roadmap de desarrollo.

---

## 1. Registro de Certezas Consolidadas (Aprobadas por el Titular)

| Ítem | Tema | Definición Vigente |
|---|---|---|
| **C-01** | **SaaS Cloud $0** | Plataforma de telemetría web 100% gratuita ($0 de por vida) como vitrina abierta. |
| **C-02** | **Descuentos y Stacking** | 10% OFF Banco Provincia + 15% OFF Vitrina Pública **100% acumulables hasta un 25% OFF total**. |
| **C-03** | **Provisión de Hardware** | Compra directa del cliente a Powermeter SAS a precio de lista; DataMaq factura mano de obra e ingeniería. |
| **C-04** | **Relevamiento Inicial Deducible** | Visita preliminar con costo de diagnóstico/viáticos ($55.000 ARS) **deducible al 100%** de la factura de obra si se aprueba la cotización. |
| **C-05** | **Moneda Base y Mantenimiento** | Valores nominales en **Pesos Argentinos (ARS)** con actualización periódica manual en YAML. |
| **C-06** | **Desglose Modular de Obra (WBS 5a)** | Instalación descompuesta en 5 sub-ítems: (a) Viáticos por CP/km, (b) Instalación estándar con corte garantizado, (c) Adicional térmica, (d) Adicional acondicionamiento tablero, (e) Configuración y puesta en marcha cloud. |
| **C-07** | **Switch Booleano de Precios** | Variable `show_public_prices: false` por defecto para renderizar `"A cotizar"` / `"A convenir"` hasta autorización expresa. |
| **C-08** | **Financiamiento Fintech** | Financiación en cuotas productivas con **Pactar Digital** (pagarés digitales sin ticket mínimo). |
| **C-09** | **Ciclo PRO 60d + Free Bifurcado** | 60 días PRO por instalación/consultoría (no acumulables). Al vencer: Monitoreo Privado Básico (default) o Vitrina Pública Anonimizada ($0 de por vida). |
| **C-10** | **Federación de Cuentas Google & FastMCP** | Cuenta técnica `agustin.deoz@gmail.com` (MCC `131-878-0733`) federada como Administrador de la cuenta comercial `contacto.datamaq@gmail.com` (`405-777-8237`), gobernando la suite FastMCP (Ads, GA4, Clarity) con tope de $1.500 ARS/día. |
| **C-11** | **Honorario Cerrado 5b (Cierre P-05)** | Consultoría energética y auditoría bajo honorario profesional cerrado con visita deducible al 100% ($55.000 ARS). Se descarta el *Success Fee* para evitar disputas de línea de base y cobranza diferida. |
| **C-12** | **Escalonamiento Tarifario 5b (Cierre P-06)** | Tarifario base escalonado por categoría de suministro de Edenor: T2 Pequeñas Demandas ($350.000 ARS), T3 Baja Tensión ($650.000 ARS), T3 Media Tensión / Trafo Propio ($850.000 ARS), con 50% de bonificación en acometidas adicionales. |
| **C-13** | **Visualización Híbrida Enriquecida (Cierre P-07)** | Exposición cuando `show_public_prices: true` en formato híbrido: Precio de Lista + Sub-badge de cuotas con Pactar Digital + Banner 25% OFF acumulable (BAPRO + Vitrina) + Desglose modular WBS (a, b, c, d, e) colapsable. |
| **C-14** | **Prioridad Docente & Filtro Asíncrono** | La docencia universitaria es la fuente segura de ingresos y el pilar de autoridad técnica; el tiempo del titular se protege operando la captación mediante filtro asíncrono previo (auditoría documental de factura de Edenor en PDF por WhatsApp en <3 min), derivando clientes de bajo margen a la web gratuita y aceptando solo proyectos de alto ticket coordinados en días sin clases. |
| **C-15** | **Roundcube SSOT de Contactos & Deduplicación** | La libreta de contactos de Roundcube (`roundcube.contacts` en MySQL) es la Fuente Única de Verdad de clientes y prospectos de DataMaq. Toda captura de formulario ejecuta deduplicación por email/teléfono antes de persistir, mientras que los eventos CTA notifican a Telegram sin generar contactos incompletos ni spam por email. |
| **C-16** | **Portal Oficial ISFT N° 199** | Migración canónica hacia `isftn199.com.ar` como portal institucional oficial y campus virtual del Instituto Superior de Formación Técnica N° 199 de Tigre (DGCyE, Pcia. de Buenos Aires). |
| **C-17** | **Educación Superior Pública y Gratuita** | Toda la propuesta académica es 100% gratuita. Prohibido cobrar matrículas o aranceles; redirección 301 de `/pricing` y `/planes` hacia `/carreras`. |
| **C-18** | **Catálogo de 6 Tecnicaturas Superiores** | Oferta formativa oficial de 3 años con validez nacional: Ciencia de Datos e IA, Mecatrónica, Logística, Higiene y Seguridad, Recursos Humanos y Servicios Gastronómicos y Turismo (SSOT `data/content/carreras.yaml`). |
| **C-19** | **Campus Virtual LMS Integrado** | Aulas técnicas y talleres integrados en `/cursos` con material de cátedra, lecciones Markdown con resaltado de código y repositorios abiertos. |
| **C-20** | **Cursada Vespertina y Admisión Abierta** | Cursada de 18:00 a 22:30 hs en sede El Talar (Maestra Celina Voena 1750), admisión con título secundario o constancia de trámite. |

---

## 2. Registro de Decisiones de Pricing Resueltas

Todas las decisiones del backlog de pricing han sido formalmente analizadas, resueltas y aprobadas como Certezas:
* ✅ **[P-05] Resuelto $\rightarrow$ [C-11]:** Honorario profesional técnico cerrado predecible.
* ✅ **[P-06] Resuelto $\rightarrow$ [C-12]:** Tarifario escalonado por categoría regulatoria T2, T3 BT y T3 MT.
* ✅ **[P-07] Resuelto $\rightarrow$ [C-13]:** Formato visual híbrido con financiamiento fintech y desglose WBS.

---

## 3. Roadmap Técnico y Tareas Pendientes

- [x] **T-01:** Implementar `pricing_structure.yaml` con los 5 sub-ítems WBS y el switch `show_public_prices: false`.
- [x] **T-02:** Diseñar `PricingService` y `PresupuestoCalculadoDTO` en `src/application/`.
- [x] **T-03:** Añadir pruebas unitarias para el switch, WBS, viáticos y cálculo de descuentos (`test_pricing_engine.py`).
- [x] **T-04:** Auditoría en vivo en VPS DonWeb y habilitación de orígenes de Google Ads en CSP (`test_csp_headers.py`).
- [x] **T-05:** Consolidación de la Tétrada del Ecosistema (`www-datamaq`, `app-datamaq`, `datamaq-telemetry`, `datamaq-hub`) en suite documental.
- [x] **T-06:** Suite FastMCP para analítica en vivo (`google-ads`, `google-analytics`, `microsoft-clarity`) y tests unitarios.
- [x] **T-07:** Flujo OAuth2 de Google Ads, vinculación MCC/Cliente y presentación de solicitud de Acceso Básico con PDF oficial.
- [x] **T-08:** Auditoría cruzada en vivo de adquisición SEM (Google Ads) y comportamiento UX (Clarity) con agentes autónomos (446 tests passing).
- [x] **T-09:** Refactorización de `FormManager.js` (eliminación de dead clicks en stepper, botón Volver en pasos 2/3, sincronización animada de progreso y depuración de código huérfano).
- [x] **T-10:** Carga y estructuración de la Super-Lista Maestra de 8 bloques de palabras clave negativas en Google Ads (`data/ads/`).
- [ ] **T-11:** Seguimiento de aprobación de *Basic Access* en Google Ads API Center para habilitar streaming de métricas en vivo.
- [x] **T-12:** Optimización de Core Web Vitals en imágenes (recompresión WebP, `fetchpriority="high"`, contención de layout y eliminación de huérfanos).
- [x] **T-13:** Investigación Estratégica Integral con Gemini Deep Research (persistencia de informe en `docs/informe_estrategico_gemini_2026.md`, validación matemática de Payback y formalización de 3 líneas remotas: Tele-Peritaje $150k, Capacitaciones $450k y Retainer Insights $85k-$150k/mes).
- [x] **T-14:** Conexión en vivo de Google Analytics 4 FastMCP con Service Account (`533265197`), segmentación de tráfico (`commercial` vs `academic`), tracking nativo `gtag` de conversiones (`whatsapp_click`, `generate_lead`) y selector de catálogo de materias en `/cursos` (`?view=all`).
- [x] **T-15:** Consolidación de la gobernanza de métricas de `datamaq-hub`, validación del aislamiento de indexación de LMS e inyección de datos de campaña para WhatsApp (442 tests de integración activos pasando en suite).
- [x] **T-16:** Arquitectura de contactos en Roundcube como SSOT sin duplicados, backup inmutable en MySQL, notificaciones de email y Telegram para formularios y eventos de CTA, y actualización exhaustiva de toda la documentación.
- [x] **T-17:** Cache busting robusto frontend (F1: hash SHA-256 del árbol estático en `?v=`, F2: Cache-Control diferenciado con/sin query, F3: purga Cloudflare) — implementado, desplegado y verificado (`max-age` acotado sin `immutable` en módulos internos).
- [x] **T-18:** Fix de `scripts/purge_cloudflare.py` a stdlib puro (sin `python-dotenv` en el runner de CI) — deploy verde.
- [ ] **T-19:** Desactivar Web Analytics en Cloudflare (zona `datamaq.com.ar` → Analytics & Logs → Web Analytics) para eliminar el beacon `static.cloudflareinsights.com` bloqueado por CSP.
- [ ] **T-20:** Agregar secrets `CF_API_TOKEN` y `CF_ZONE_ID` (`97a5266edc3168950db5707cdec5cec9`) en GitHub Actions para habilitar la purga automática post-deploy.
- [ ] **T-21:** Limpiar cookies de `datamaq.com.ar` en el navegador (residuo del GA ID anterior `_ga_4Y7WLJ1740` que genera advertencias de consola).
- [x] **T-22:** Estructurar el catálogo institucional `data/content/carreras.yaml` con las 6 tecnicaturas oficiales y resoluciones DGCyE.
- [x] **T-23:** Implementar arquitectura de dominio y aplicación para Carreras (`Carrera` entity, `CarreraModel` DTO, métodos en `DataService`, router `carreras_routes.py` y plantillas `carreras.html` y `carrera_detail.html`).
- [x] **T-24:** Configurar redirección permanente 301 de rutas de pricing/planes (`/pricing`, `/planes`) hacia `/carreras`.
- [x] **T-25:** Actualizar identidad visual, branding institucional, SEO y navegación general (`brand.yaml`, `footer.yaml`, `seo.yaml`, `home_sections.yaml`).
- [x] **T-26:** Actualizar la suite documental y de agentes (`AGENTS.md`, `docs/srs.md`, `docs/specs.md`, `docs/todo.md`) reflejando la misión educativa pública y gratuita del ISFT N° 199.


