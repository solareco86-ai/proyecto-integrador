# Acceso al entorno dev (`dev.isftn199.com.ar`)

## Objetivo y contexto

El subdominio `dev.isftn199.com.ar` expone el entorno de integración (`develop`)
en el VPS (`isftn199-dev.service`, `127.0.0.1:8004`) detrás de Cloudflare
(modo Flexible, registro `dev` proxied).

Problema: el acceso debía restringirse con Cloudflare Access, pero el rol de
cuenta del responsable técnico **no** tiene el permiso "Access: Apps and
Policies". Mientras no se habilite, el subdominio queda público (`200` sin
autenticación).

Solución de contingencia (este cambio): guardia en el origen nginx con
**Basic Auth** + **allow-list de rangos Cloudflare**, manteniendo
`X-Robots-Tag: noindex`. Se reemplazará por Cloudflare Access cuando el rol lo
permita (seguimiento en el issue #22).

## Superficies afectadas

| Superficie | Recurso | Cambio |
|---|---|---|
| nginx (vhost dev) | `deploy/dev/dev.isftn199.com.ar.conf` | `include` allow-list + `auth_basic` + IP real desde `CF-Connecting-IP` |
| Provisión | `deploy/dev/provision-dev.sh` | genera `/etc/nginx/.htpasswd-dev` y `/etc/nginx/snippets/cloudflare-allow.conf` (idempotente) |
| Plantilla | `deploy/dev/cloudflare-allow.conf` | fallback estático de rangos CF si no hay red |
| Docs | `docs/ops.md` §2.4 | documentar guardia y rotación de credencial |

## Matriz de pruebas (BDD)

| Escenario | Precondición | Esperado |
|---|---|---|
| Petición local sin credencial | `curl -H 'Host: dev.isftn199.com.ar' -H 'X-Forwarded-Proto: https' http://127.0.0.1/` | `401` + `WWW-Authenticate: Basic` |
| Petición local con credencial válida | idem con `-u dev:<pass>` | `200` + `X-Robots-Tag: noindex` |
| Fuente no Cloudflare (IP ajena) | petición directa a `168.181.184.103:80` | `403` |
| Cliente HTTP genuino (sin `X-Forwarded-Proto`) | `curl` HTTP plano | `301` a `https://...` |
| Edge Cloudflare | `curl -sI https://dev.isftn199.com.ar` | `401` (o `302` a Access cuando se habilite) |
| App saludable | `curl http://127.0.0.1:8004/` | `200` |

## Criterios del Gauntlet

- `nginx -t` sin errores antes de `systemctl reload nginx` (ya lo valida `provision-dev.sh`).
- Provisión idempotente: no pisa `/etc/nginx/.htpasswd-dev` ni `.env` existentes.
- No se versionan secretos: el hash htpasswd vive solo en el VPS.
- Verificación post-aplicación: los 6 escenarios de la matriz.
