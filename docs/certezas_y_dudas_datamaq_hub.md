# Certezas y Dudas Estratégicas: Servidores FastMCP y Tracking Analítico (`datamaq-hub`)

> **Ámbito:** Integración de Google Ads, Google Analytics 4 (GA4), Microsoft Clarity y Model Context Protocol (MCP) en `datamaq-hub`.  
> **Fecha de Consolidación:** 2026-08-26 (Post-Lead JTEKT Automotive).  
> **Estado:** Documento Vivo (SSOT de Analítica & Telemetría).  

---

## 1. Certezas Consolidadas (Hechos Verificados)

1. **Topología de Cuentas y Credenciales:**
   - **Google Analytics 4 (Propiedad `533265197`):** Conectada y operativa mediante Service Account en GCP (`datamaq-ga4-key.json`). Proporciona desglose geográfico (Garín, Olivos, Buenos Aires), canales de origen (Direct, Organic, Referral), eventos de conversión nativos (`page_view`, `session_start`, `whatsapp_click`, `direct_contact`).
   - **Google Ads (Cuenta `405-777-8237`):** OAuth2 validado y Refresh Token operativo. Presupuesto diario controlado con límite de seguridad de **$1.500 ARS/día**. Campaña #1 actualmente en estado `PAUSED`.
   - **Microsoft Clarity (Proyecto `wx5hfvmv5y`):** Captura activa de mapas de calor y grabaciones en video de navegación de usuarios.

2. **Atribución de Tráfico B2B Industrial:**
   - El lead Tier 1 de **JTEKT Automotive** demostró que los compradores industriales combinan múltiples puntos de contacto:
     * Descubrimiento orgánico en Google / Enlace corporativo en LinkedIn (`l.wl.co`).
     * Acceso desde Zona Norte (Olivos / Garín / GBA Norte).
     * Contacto formal mediante **correo electrónico corporativo directo (`info@datamaq.com.ar`)** en lugar de formularios web o WhatsApp.
   - El Costo de Adquisición de Clientes (CAC) de este lead fue **$0 ARS** (tracción orgánica y autoridad de marca).

3. **Arquitectura de FastMCPs en `datamaq-hub`:**
   - Tres servidores dedicados construidos sobre `FastMCP`:
     * `scripts/mcp_google_ads_server.py`
     * `scripts/mcp_ga4_server.py`
     * `scripts/mcp_clarity_server.py`
   - Suite de pruebas automatizadas con tipado estricto (0 errores en Pyright).

---

## 2. Dudas, Limitaciones y Propuestas de Mejora para `datamaq-hub`

### Duda 1: Términos de Búsqueda Orgánicos Ocultos (`(not provided)`)
* **Problema:** En GA4, las palabras clave exactas que los usuarios escriben en el buscador de Google aparecen como `(not provided)` por políticas de privacidad de Google.
* **Propuesta de Mejora para `datamaq-hub`:**
  - Crear un nuevo gateway y servidor FastMCP para la **Google Search Console API** (`searchconsole.googleapis.com`).
  - Esto permitirá a los agentes auditar en tiempo real qué consultas (ej. *"tecnicatura ciencia de datos tigre"*, *"isft 199 inscripciones"*, *"mecatronica zona norte"*) generan impresiones y clics hacia `isftn199.com.ar`.

### Duda 2: Limitación de la API de Exportación de Microsoft Clarity
* **Problema:** El endpoint de la Clarity Data Export API (`/project-live-insights`) solo entrega métricas estadísticas agregadas (porcentaje de *rage clicks*, *dead clicks*, *scroll depth*, cantidad total de sesiones). La API REST **no entrega URLs individuales de video de grabación ni listados de sesiones**.
* **Solución Implementada & Recomendación:**
  - En `www-datamaq` se implementaron **Custom Tags** (`window.clarity("set", "lead_intent", ...)`).
  - En `datamaq-hub` o en los reportes de agentes, los asistentes deben proporcionar enlaces parametrizados directos a la consola web de Clarity:
    `https://clarity.microsoft.com/projects/view/wx5hfvmv5y/recordings?filter=lead_intent%3Aemail_click`

### Duda 3: Desacople del Motor de BD en `ApiCacheGateway`
* **Problema:** `ApiCacheGateway` en `datamaq-hub` intenta inicializar SQLAlchemy con dependencias asíncronas (`aiosqlite`) si la URL no es MySQL directa. En ejecuciones síncronas de scripts CLI sin MySQL local, puede fallar si falta el paquete `aiosqlite`.
* **Propuesta de Mejora para `datamaq-hub`:**
  - Robustecer el fallback en `ApiCacheGateway`: si `DATABASE_URL` no está definida o falla la conexión al motor, operar en modo *passthrough* (memoria o consulta directa a la API sin lanzar excepción).

### Duda 4: Alertas Proactivas en Background (Cron / Watchdog)
* **Problema:** Actualmente las consultas de gasto de Ads y métricas de GA4 en `datamaq-hub` son pasivas (solo cuando un agente o humano ejecuta el script).
* **Propuesta de Mejora para `datamaq-hub`:**
  - Implementar un job programado (cron o worker liviano) que consulte una vez al día el gasto de Google Ads y la tasa de rebote en GA4, y envíe un reporte ejecutivo automático al bot de Telegram de DataMaq.

---

## 3. Resumen de Gobernanza de Datos de Conversión y Contactos

| Tipo de Conversión | Canal de Captura | Destino de Alerta | SSOT Libreta de Contactos | Registro en DB | Atribución First-Touch |
|---|---|---|---|---|---|
| **Formulario Multi-Paso** | Web (`/contact`) | Telegram + Email + GA4 + Ads | **Roundcube** (`contacts` vCard 3.0 deduplicada) | MySQL (`datamaq_leads.leads`) | Sí (30 días localStorage) |
| **Clic en WhatsApp** | Web (`wa.me` / FAB) | Telegram + GA4 + Ads | *No aplica (sin identidad validada)* | MySQL (`datamaq_leads.leads`) | Sí (30 días localStorage) |
| **Clic en Email / Teléfono** | Web (`mailto:` / `tel:`) | Telegram + GA4 + Clarity | *No aplica (sin identidad validada)* | MySQL (`datamaq_leads.leads`) | Sí (30 días localStorage) |
| **Copia de Email / Tel** | Web (Portapapeles) | Telegram + GA4 + Clarity | *No aplica (sin identidad validada)* | MySQL (`datamaq_leads.leads`) | Sí (30 días localStorage) |
| **Envío Directo Outlook / Webmail** | Aspirante / Interesado | Buzón `isft199@gmail.com` | **Roundcube** (`contacts` manual / webmail) | Manual / Ingest Hub | Correlación analítica por IP/Geo/Hora |

---

## 4. Pipeline de Ingesta y Deduplicación en Datamaq Hub (`/api/v1/leads/ingest`)
1. **Deduplicación:** Antes de persistir, `datamaq-hub` busca si ya existe un contacto con el mismo correo electrónico o teléfono.
2. **Actualización Incremental:** Si el contacto existe, concatena la nueva consulta en el campo `notes` de la vCard 3.0 y actualiza la empresa/rol si estaban ausentes.
3. **Agenda Automática:** Agenda un recordatorio de seguimiento comercial (+1 día hábil a las 10:00 hs) en el calendario de Roundcube.

