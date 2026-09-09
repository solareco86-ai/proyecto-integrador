# Spec — Consola de Navegador Limpia (DX 2.0)

## 1. Objetivo y Contexto

Reducir el ruido en la consola del navegador **emitido por nuestro propio código**
y garantizar que el HTML se sirva siempre fresco (eliminando errores CSP residuales
por cache viejo), **sin perder captura de datos de analítica**.

### Decisiones de negocio (aprobadas por el usuario)

1. **Logger con gating por entorno.** Los niveles verbosos (`debug`, `info`) quedan
   silenciados en producción; `warn` y `error` siempre pasan (señal de diagnóstico).
2. **Warnings de terceros bloqueados (ETP) con dedupe por sesión.** Un único aviso
   por vendor (gtag/clarity) por sesión, en lugar de uno por cada carga de página.
3. **Cache-Control de HTML a `no-cache, must-revalidate`.** Elimina de raíz el HTML
   viejo (beacon de Cloudflare) servido hasta 24 h por CDN/proxy.
4. **Telemetría de bloqueo de terceros.** Emitir un evento `tp:blocked` (CustomEvent
   + push a `dataLayer`) para medir qué porcentaje de visitas tiene ETP bloqueando
   Clarity/GTAG.

### Alcance

- Crear `static/js/modules/logger.js` y migrar los 26 `console.*` de producción.
- Dedupe por sesión en `ThirdPartyScriptsManager.js` + emisión de `tp:blocked`.
- Cambiar `HTML_CACHE_CONTROL` en `src/infrastructure/settings/config.py`.
- Actualizar/crear tests de privacidad frontend y de cache.

### Fuera de alcance

- Warnings del navegador (Firefox ETP, uBlock, Brave): "Protección de rastreo…",
  cookies `_ga_*` "dominio no válido". Son del cliente, no accionables desde el sitio.
- Modificar dominios GA4 / Ads / Clarity / Bing, política de consentimiento o `cookie_domain`.
- Crear un endpoint backend de ingesta de eventos: la medición de `tp:blocked` se
  resuelve vía `dataLayer`/GA4 (los mismos canales de telemetría ya existentes).
- `preview-telemetry.js`: ya vive tras `{% if config.DEBUG %}` (`base.html:20-22`),
  no se sirve en producción.

## 2. Dominio & Puertos

Cambio exclusivamente en **infraestructura** y **frontend**. No se introducen
entidades, value objects ni puertos en `domain/`.

- `logger.js` es un módulo ES puro sin estado (salvo lectura de `APP_CONFIG.debug`).

## 3. Casos de Uso & Contratos

### 3.1 `logger.js` (nuevo)

```js
debug(...args)  // no-op salvo APP_CONFIG.debug === true
info(...args)   // no-op salvo APP_CONFIG.debug === true
warn(...args)   // siempre emite console.warn
error(...args)  // siempre emite console.error
```

- `isDebugEnabled()` lee `window.APP_CONFIG?.debug === true` dentro de `try/catch`
  (degradación segura: ante ausencia de `APP_CONFIG` se asume producción → silencio).

### 3.2 Dedupe por sesión (`ThirdPartyScriptsManager.js`)

- Helper `markVendorWarned(vendor)` / `hasVendorWarned(vendor)` usando
  `sessionStorage` con clave `tp:warned:<vendor>`.
- Si `sessionStorage` falla (modo privado), fallback a variable en memoria (dedupe
  por página). Nunca se pierde el primer aviso.
- Aplicado a los `onerror` de GTAG y Clarity.

### 3.3 Telemetría de bloqueo (`tp:blocked`)

- En `onerror` de GTAG/Clarity: `window.dispatchEvent(new CustomEvent('tp:blocked',
  { detail: { vendor } }))` con `vendor ∈ {'gtag', 'clarity'}`.
- Listener propio: `window.dataLayer?.push({ event: 'third_party_blocked',
  third_party_vendor: vendor })` (visible en GA4/GTM cuando éstos cargan).

### 3.4 Cache-Control de HTML

- `config.HTML_CACHE_CONTROL` pasa a `"no-cache, must-revalidate"`.
- Nota técnica: no se añade ETag custom porque Starlette no provee `ETagMiddleware`
  y un validador propio introduciría riesgo de streaming/gzip. `no-cache` sin
  validador fuerza re-fetch completo (correcto y aceptable para un sitio pequeño);
  el objetivo (HTML siempre fresco) se cumple al 100 %.

## 4. Matriz de Pruebas (RED Suite)

```gherkin
Feature: Consola limpia y HTML fresco
  Scenario: Navegador en producción ejecuta la aplicación
    Given APP_CONFIG.debug es false
    Then logger.debug y logger.info no emiten salida
    And logger.warn y logger.error sí emiten

  Scenario: Script de terceros bloqueado por ETP
    Given el onerror de GTAG/Clarity se dispara
    Then se emite el primer logger.warn del vendor
    And las siguientes cargas en la misma sesión no repiten el aviso
    And se despacha CustomEvent 'tp:blocked'

  Scenario: Auditor inspecciona el código
    Given los módulos de producción
    Then ningún módulo llama console.debug ni console.info directamente
    And FormManager no usa console.info

  Scenario: Navegador carga una página HTML
    Given config.DEBUG es false
    Then Cache-Control contiene no-cache y must-revalidate
```

### Contratos de tests

| Archivo | Test | Contrato |
|---|---|---|
| `tests/test_privacidad_frontend.py` | `test_modulos_sin_console_debug` | `"console.debug"` ausente en `ThirdPartyScriptsManager.js` y `DirectContactTracker.js` |
| 〃 | `test_form_manager_sin_console_info` | `"console.info"` ausente en `FormManager.js` |
| 〃 | `test_third_party_manager_emite_tp_blocked` | `"tp:blocked"` presente en `ThirdPartyScriptsManager.js` |
| 〃 | `test_third_party_manager_dedupe_sesion` | `"sessionStorage"` y `"tp:warned:"` presentes |
| `tests/test_logger_frontend.py` (nuevo) | `test_logger_gating_debug_info` | `logger.js` contiene guard `APP_CONFIG?.debug === true` para `debug`/`info` |
| 〃 | `test_logger_warn_error_siempre` | `logger.js` emite `console.warn`/`console.error` sin guard |
| `tests/test_seo.py` | `test_cache_control_html_no_cache` | `"no-cache"` y `"must-revalidate"` presentes; `"public"` ausente |

## 5. Criterios del Gauntlet

| Etapa | Comando | Criterio |
|---|---|---|
| Estilo | `ruff check src/ tests/ scripts/` | 0 errores |
| Tipado Python | `pyright` | 0 diagnósticos |
| Tipado JS | `npm run typecheck:js` | 0 errores |
| Tests | `pytest --cov=src --cov-fail-under=85 tests/ -q` | 100% aprobados, cobertura ≥ 85 % |
| Arquitectura | `python3 scripts/verify_architecture.py` | Capas respetadas |
| Plantillas | `python3 scripts/validate_templates.py` | R1 no afectada |
| Integridad | `__init__.py` de 0 bytes | Sin re-exportaciones |
