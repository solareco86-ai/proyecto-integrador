# Spec — Mejora de DX en Consola del Navegador (Reducción de Ruido de Terceros)

## 1. Objetivo y Contexto

Reducir el ruido en la consola del navegador producido por rastreadores de terceros
bloqueados por protecciones del lado del cliente (Firefox ETP, uBlock, Brave Shields).

La causa raíz es el beacon de **Cloudflare Insights** (`beacon.min.js`) cargado de forma
incondicional en `head.html`, lo que viola la lógica fail-closed de `CookieManager.js` y
genera errores CORS en navegadores con protección de rastreo. La CSP es un string monolítico
de ~1100 caracteres difícil de auditar, y el endpoint `/csp-report` está muerto (no conectado
a la CSP ni loguea violaciones).

### Decisiones de negocio (aprobadas por el usuario)

1. **Eliminar Cloudflare Insights de raíz.** GA4 + Google Ads + Microsoft Clarity cubren la
   analítica con consentimiento. Eliminar el beacon resuelve el error CORS de raíz.
2. **Mantener `cookie_domain: "auto"`.** gtag.js resuelve los ccTLD de dos niveles (`.com.ar`)
   vía Public Suffix List; el ruido restante proviene de bloqueadores, no del dominio.
3. **Refactorizar la CSP a un builder declarativo** con diccionario de directivas.
4. **Conectar `report-uri` y activar el logging** de violaciones en `/csp-report`.

### Alcance

- Eliminar el beacon de Cloudflare de `head.html` y sus dominios de la CSP.
- Extraer la CSP a un módulo `src/infrastructure/fastapi/csp.py` con `build_csp()`.
- Añadir `report-uri /csp-report` a la CSP en modo enforcement.
- Loguear (warning) los reportes de violación en el endpoint `/csp-report`.

### Fuera de alcance

- Modificar dominios de GA4 / Ads / Clarity / Bing.
- Cambiar la política de consentimiento o el `cookie_domain`.
- Cambiar datos de contenido, pricing o plantillas más allá de `head.html`.

## 2. Dominio & Puertos

Este cambio opera exclusivamente en la capa de **infraestructura** y en el **frontend**.
No se introducen entidades, value objects ni puertos nuevos en `domain/`.

- `build_csp()` es una **función pura** (sin estado, sin I/O) que pertenece a
  `src/infrastructure/fastapi/csp.py` y no importa de ninguna otra capa.

## 3. Casos de Uso & DTOs

### 3.1 `build_csp(telemetry_hosts: tuple[str, ...] = ()) -> str`

Construye el header `Content-Security-Policy` desde el diccionario declarativo
`_CSP_DIRECTIVES: dict[str, list[str]]`.

- Recorre el dict en orden de inserción (determinista).
- Para `connect-src`, concatena `telemetry_hosts` al final de la lista base.
- Formatea cada directiva como `directiva origen1 origen2 ...` y une con `"; "`.

### 3.2 Endpoint `POST /csp-report`

- Lee el body crudo (`await request.body()`).
- Decodifica con `errors="replace"` y loguea `warning` truncado a 4096 caracteres.
- Responde siempre `204 No Content`.

## 4. Matriz de Pruebas (RED Suite)

```gherkin
Feature: Consola limpia y CSP auditable
  Scenario: Navegador con bloqueador visita el sitio
    Given el head no contiene beacon.min.js
    Then no se dispara request a static.cloudflareinsights.com
    And la consola no muestra error CORS de Cloudflare

  Scenario: Auditor inspecciona la CSP
    Given build_csp() con hosts de telemetría
    Then la política incluye report-uri /csp-report
    And no incluye dominios de cloudflareinsights.com

  Scenario: Navegador reporta una violación CSP
    Given la página se sirve con report-uri /csp-report
    When el navegador POSTea un reporte a /csp-report
    Then el servidor responde 204
    And registra un warning con el detalle de la violación
```

### Contratos de tests

| Archivo | Test | Contrato |
|---|---|---|
| `tests/test_csp_builder.py` | `test_build_csp_incluye_directivas_requeridas` | Todas las directivas presentes |
| 〃 | `test_build_csp_sin_cloudflare` | `"cloudflareinsights.com" not in csp` |
| 〃 | `test_build_csp_report_uri_conectado` | `"report-uri /csp-report" in csp` |
| 〃 | `test_build_csp_inyecta_telemetria` | Hosts API+WS en `connect-src` |
| 〃 | `test_build_csp_determinista` | Mismo input → mismo output |
| 〃 | `test_build_csp_conserva_dominios_ads_clarity` | Dominios de Ads/Clarity/Bing presentes |
| 〃 | `test_build_csp_sin_telemetria_sin_espacios` | Sin espacios duplicados ni trailing space |
| `tests/test_csp_headers.py` | `test_csp_headers_en_respuestas_html` | Sin asserts Cloudflare; con `report-uri` |
| 〃 | `test_csp_report_endpoint_loguea` | POST → 204 + warning con el reporte |
| `tests/test_privacidad_frontend.py` | `test_head_sin_beacon_cloudflare` | `"beacon.min.js" not in head.html` |
| 〃 | `test_third_party_manager_sin_cloudflare` | `"cloudflare" not in ThirdPartyScriptsManager.js` |

## 5. Criterios del Gauntlet

| Etapa | Comando | Criterio |
|---|---|---|
| Estilo | `ruff check src/ tests/ scripts/` | 0 errores |
| Tipado | `pyright` | 0 diagnósticos |
| Tests | `pytest --cov=src --cov-fail-under=85 tests/ -q` | 100% aprobados, cobertura ≥ 85% |
| Arquitectura | `python3 scripts/verify_architecture.py` | Capas respetadas |
| Plantillas | `python3 scripts/validate_templates.py` | R1 no afectada |
| Frontend | `npm run typecheck:js` | 0 errores |
| Integridad | `__init__.py` de 0 bytes | Sin re-exportaciones |
