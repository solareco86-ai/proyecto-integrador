# Spec — Cache Busting Robusto Frontend (F1+F2+F3)

## 1. Objetivo y Contexto

Eliminar el servicio de **assets JS/CSS viejos cacheados en el CDN (Cloudflare) y en
el navegador** que sobreviven a un deploy, rompiendo el comportamiento del frontend.

### Problema confirmado (evidencia de producción)

- El HTML se sirve fresco (`cf-cache-status: DYNAMIC`, sin beacon), pero los
  **módulos internos importados relativamente** (`app.js` → `./modules/*.js`) se
  sirven desde el edge del CDN con `age` acumulado y `immutable, max-age=604800`.
- Cloudflare **sí distingue query strings** en la cache key (`?v=x` → `MISS`,
  sin query → `HIT`). Por lo tanto, versionar con `?v=` funciona, **siempre que la
  versión se propague a todos los recursos** y que la versión refleje el contenido real.
- El código actual versiona solo los *entry points* (`app.js`, `css/index.css`,
  `CourseManager.js`) con `?v={{ static_version() }}`, pero:
  1. `static_version()` es un **git SHA cacheado al boot** (`dependencies.py`): si el
     proceso no se reinicia, la versión no cambia aunque cambie el contenido.
  2. Los **imports relativos internos no llevan `?v=`** y se sirven con `immutable`
     por 7 días → el navegador y el CDN ejecutan código viejo (raíz del bug reportado:
     `ThirdPartyScriptsManager.js:50` con código anterior al refactor).

### Decisiones de diseño (aprobadas por el usuario)

1. **F1 — Versión por contenido:** `static_version()` pasa de git SHA cacheado al
   boot a un **hash SHA-256 del árbol `static/`**, memoizado con **TTL de 60 s**
   (no cache eterno). Un cambio de archivo se refleja sin reiniciar el proceso.
2. **F2 — Cache-Control diferenciado:** los recursos servidos **con `?v=`** mantienen
   `immutable` (URL estable por contenido → seguro); los **sin query** (módulos
   internos, assets) bajan a `public, max-age=3600` con revalidación 304 vía
   ETag/Last-Modified de Starlette (barata).
3. **F3 — Purga de Cloudflare en el deploy:** script `scripts/purge_cloudflare.py`
   (stdlib) que purga la caché del edge tras cada deploy, con credenciales en
   `CF_API_TOKEN` / `CF_ZONE_ID` (`.env` local / secrets de GitHub Actions).

### Alcance

- `src/infrastructure/fastapi/dependencies.py`: `CachedStaticFiles` (F2) y
  `static_version()` (F1).
- `src/infrastructure/settings/config.py`: `STATIC_MODULE_MAX_AGE`.
- `scripts/purge_cloudflare.py` (nuevo), `scripts/deploy-server.sh`, `.env.example`,
  `.github/workflows/deploy.yml`.
- Tests: `tests/test_static_cache.py`, `tests/test_purge_cloudflare.py`.

### Fuera de alcance

- Reescribir los imports relativos para embeder `?v=` (estrategia A descartada).
- Bundle único con esbuild (estrategia C descartada).
- Warnings de navegador (ETP Firefox, cookies `_ga_*`): del cliente, no accionables.
- Cambiar la política de consentimiento, dominios de analítica o `cookie_domain`.

## 2. Dominio & Puertos

Cambio exclusivamente en **infraestructura** y **scripts de deploy**. No se
introducen entidades, value objects ni puertos en `domain/`.

## 3. Casos de Uso & Contratos

### 3.1 `static_version()` por contenido (F1)

- `_hash_static_tree()` recorre `config.STATIC_DIR` (`os.walk`, directorios y
  archivos ordenados) y acumula en un `sha256` la **ruta relativa** + **bytes** de
  cada archivo. Retorna `hexdigest()[:12]`.
- Archivo ilegible (`OSError`): se omite sin abortar.
- `get_static_version()`:
  - En `DEBUG`: devuelve `str(int(time.time()))` en cada llamada (sin caché).
  - En producción: memoiza `(momento_monotónico, hash)` y recalcula solo si
    transcurrieron más de 60 s (`_STATIC_VERSION_TTL_SECONDS`).
  - Si el hasheo lanza excepción: `logger.warning` + fallback a timestamp.

### 3.2 Cache-Control diferenciado (F2)

`CachedStaticFiles.get_response` decide según `scope.get("query_string")`:

| Condición | Cache-Control |
|---|---|
| `config.DEBUG` | `no-cache, no-store, must-revalidate` |
| query presente (`?v=`) | `public, max-age={STATIC_CACHE_SECONDS}, immutable` |
| sin query | `public, max-age={STATIC_MODULE_MAX_AGE}` (3600) |

- Sin `immutable` en recursos sin versión: el navegador revalida (304 vía ETag)
  y el CDN no los congela 7 días.

### 3.3 Purga de Cloudflare (F3)

- `scripts/purge_cloudflare.py` lee `CF_API_TOKEN` y `CF_ZONE_ID` del entorno
  (cargador `.env` stdlib `_load_env_file()`, sin dependencias externas para
  correr en el runner de CI), y hace `POST /zones/{zone}/purge_cache` con
  `{"purge_everything": true}`.
- Semántica de salida:
  - Faltan credenciales → `warning` a stderr y **exit 0** (deploy local no bloqueante).
  - API `success: true` → exit 0.
  - API con error (HTTP/red) o `success: false` → error a stderr y **exit 1**
    (señala purga manual pendiente; el código ya está desplegado).
- `deploy-server.sh` invoca `python3 scripts/purge_cloudflare.py` **tras** el bloque
  de deploy/health-check (en el runner, no dentro del heredoc SSH).
- `deploy.yml` pasa `CF_API_TOKEN` / `CF_ZONE_ID` como `env` al step Deploy.

## 4. Matriz de Pruebas (RED Suite)

```gherkin
Feature: Cache busting robusto de frontend
  Scenario: Navegador pide un entry point versionado
    Given producción (DEBUG=false) y la URL lleva ?v=
    Then Cache-Control incluye immutable y max-age de STATIC_CACHE_SECONDS

  Scenario: Navegador pide un módulo interno sin versión
    Given producción y la URL no lleva query
    Then Cache-Control NO incluye immutable
    And incluye max-age de STATIC_MODULE_MAX_AGE (3600)

  Scenario: Se calcula la versión de cache-busting
    Given producción
    Then la versión es estable dentro del TTL de 60 s
    And cambia cuando el hash del contenido cambia
    And en DEBUG es un timestamp por llamada

  Scenario: El hasheo del árbol static falla parcialmente
    Given un archivo ilegible durante el walk
    Then el hasheo no aborta y devuelve un digest válido

  Scenario: Script de purga sin credenciales
    Given CF_API_TOKEN o CF_ZONE_ID ausentes
    Then se omite la purga y el proceso sale 0 sin HTTP

  Scenario: Script de purga con credenciales válidas
    Given credenciales presentes y API success=true
    Then el proceso sale 0 y envía purge_everything=true

  Scenario: Script de purga con API en error
    Given credenciales presentes y API responde error
    Then el proceso sale 1
```

### Contratos de tests

| Archivo | Test | Contrato |
|---|---|---|
| `tests/test_static_cache.py` | `test_static_con_query_lleva_immutable` | `immutable` + `max-age=STATIC_CACHE_SECONDS` en `/static/*?v=` |
| 〃 | `test_static_sin_query_sin_immutable` | sin `immutable` + `max-age=STATIC_MODULE_MAX_AGE` en `/static/*` |
| 〃 | `test_static_version_estable_dentro_del_ttl` | dos llamadas → mismo valor |
| 〃 | `test_static_version_cambia_con_contenido` | hash distinto tras TTL expirado |
| 〃 | `test_static_version_debug_usa_timestamp` | `DEBUG=true` → string numérica |
| 〃 | `test_static_version_fallback_ante_error` | hash lanza excepción → timestamp |
| 〃 | `test_hash_static_tree_ignora_archivo_ilegible` | `OSError` en `open` no aborta |
| `tests/test_purge_cloudflare.py` | `test_purge_sin_vars_omite_y_sale_cero` | exit 0, sin `urlopen` |
| 〃 | `test_purge_exitosa_sale_cero` | exit 0, payload `purge_everything` |
| 〃 | `test_purge_http_error_sale_uno` | `HTTPError` → exit 1 |
| 〃 | `test_purge_api_success_false_sale_uno` | `success:false` → exit 1 |

## 5. Criterios del Gauntlet

| Etapa | Comando | Criterio |
|---|---|---|
| Estilo | `ruff check .` + `ruff format --check .` | 0 errores |
| Tipado Python | `pyright` | 0 diagnósticos (incluye `scripts/purge_cloudflare.py`) |
| Tipado JS | `npm run typecheck:js` | 0 errores |
| Tests | `pytest --cov=src --cov-fail-under=85 tests/ -q` | 100% aprobados, cobertura ≥ 85 % |
| Arquitectura | `python3 scripts/verify_architecture.py` | Capas respetadas |
| Plantillas | `python3 scripts/validate_templates.py` | R1 no afectada |
