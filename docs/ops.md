# Manual de Operaciones, Infraestructura y Despliegue en VPS (Ops Runbook) — ISFT N° 199

> **Proyecto:** Instituto Superior de Formación Técnica N° 199 (`isftn199.com.ar`)  
> **Estado:** Documento Vivo (Living SSOT)  
> **Ámbito:** Servidor de producción DonWeb, coexistencia de repositorios en `/var/www/`, despliegues seguros, seguridad Linux, watchdogs y gestión de incidentes.

---

## 1. Topología del Servidor de Producción (VPS DonWeb)

* **Proveedor:** DonWeb Cloud VPS Linux (CentOS / RHEL 8 / Linux 4.18 kernel en `vps-5685053-x.dattaweb.com`).
* **Usuario Dedicado del Servicio:** `datamaq` (sin privilegios root, propietario del código y los logs).
* **Servidor Web / Reverse Proxy:** Nginx con certificados SSL TLS 1.3 gestionados por Certbot (Let's Encrypt) y `proxy_protocol`.
* **Bases de Datos MySQL:**
  - **`datamaq_leads`**: Almacén inmutable de auditoría de consultas y preinscripciones de `www-datamaq` (`DATABASE_URL`).
  - **`roundcube`**: Base de datos de Webmail corporativo y libreta de contactos (`roundcube.contacts` en formato vCard 3.0).
  - **`datamaq_hub`**: Base de datos de herramientas internas, conciliación y estado operativo.
  - **`datamaq_telemetry`**: Almacén de series temporales y telemetría de hardware.

### Coexistencia de Servicios en `/var/www/`

| Directorio VPS | Servicio / Proceso | Puerto Local | Dominio Público | Repositorio GitHub |
|---|---|---|---|---|
| **`/var/www/www-datamaq`** | `datamaq.service` (FastAPI / Uvicorn SSR) | `127.0.0.1:8001` | `https://isftn199.com.ar` | `solareco86-ai/proyecto-integrador` |
| **`/var/www/app-datamaq`** | Nginx SPA (Dashboard & Telemetría) | Estático | `https://app.datamaq.com.ar` | Aplicación SPA |
| **`/var/www/datamaq-telemetry`** | Backend IoT / WebSockets / Ingesta | `127.0.0.1:8885` | `https://api.datamaq.com.ar` | Backend Telemetría |
| **`/var/www/datamaq-hub`** | `datamaq-hub.service` (FastAPI + FastMCP) | `127.0.0.1:8013` | Uso interno / Webhooks | Servidores FastMCP |

---

## 2. Protocolo Oficial de Despliegue (`deploy-server.sh`)

### ⚠️ Regla de Oro Inviolable (§6 AGENTS.md)
> **PROHIBIDO EJECUTAR COMANDOS GIT COMO `root` EN EL VPS:**  
> Cualquier comando `git pull`, `git fetch` o `git status` ejecutado como `root` cambia los permisos de `.git/index` y `.git/FETCH_HEAD`, bloqueando el despliegue automático y dejando el repositorio en estado de error de permisos.

### 2.1 Procedimiento de Despliegue Oficial (CI/CD Automatizado)
El flujo principal de despliegue opera automáticamente mediante **GitHub Actions (`.github/workflows/deploy.yml`)**:
1. Tras aprobar los cambios, el usuario autoriza el `git push origin main`.
2. El hook local pre-push valida los 7 pasos de calidad (CSS, templates, Clean Architecture, ruff, pyright, pytest).
3. GitHub Actions ejecuta la suite completa de tests de integración e invoca `./scripts/deploy-server.sh` de forma segura vía SSH hacia el VPS DonWeb.

### 2.2 Procedimientos de Despliegue de Contingencia (Manual)
En caso de requerir un despliegue manual directo:

```bash
# Método A: Ejecución mediante script de deploy directo vía SSH (con autorización)
./scripts/deploy-server.sh

# Método B: Ejecución manual directa en VPS asumiendo el usuario dedicado
sudo -u datamaq git pull --ff-only
sudo -u datamaq /var/www/www-datamaq/.venv/bin/pip install -r requirements.txt
sudo systemctl restart datamaq.service
```

### 2.3 Política de Autorización de Despliegue
Cualquier modificación que impacte en producción debe ser autorizada por el usuario al aprobar el `git push` a `main` o al autorizar la ejecución directa del script de contingencia. Queda prohibido el despliegue manual autónomo por parte del asistente de IA sin confirmación previa.

---

## 3. Servicios en Segundo Plano y Watchdogs

### 3.1 Watchdog de Captura de Leads (`scripts/watchdog_leads.py`)
* Monitorea la integridad de los leads registrados en MySQL / SQLite.
* Envía alertas instantáneas ante nuevos prospectos vía Telegram Bot y Email corporativo.
* Ejecutado como servicio systemd (`datamaq-watchdog.service`) o cron job del usuario `datamaq`.

### 3.2 Backup y Respaldo de Base de Datos
* Backup periódico automatizado de la base de datos MySQL (`datamaq_leads`, `roundcube`, `datamaq_hub`) hacia almacenamiento cifrado.
* Rotación de logs de aplicación y Nginx mediante `logrotate`.

### 3.3 Gestión y Deduplicación de Contactos en Roundcube
* **Libreta Canónica:** Ubicada en la tabla `roundcube.contacts` bajo la cuenta institucional `isft199@gmail.com` (`user_id=1`).
* **Formato vCard 3.0:** Cada registro contiene `name`, `email`, `phone`, `organization` y `notes` con el histórico de consultas.
* **Integración Webhook:** `www-datamaq` despacha consultas a `datamaq-hub.service` (`http://127.0.0.1:8013/api/v1/leads/ingest`), que resuelve la deduplicación y actualiza la libreta de Roundcube.


---

## 4. Gestión de Incidentes y Rollback

### 4.1 Recuperación de Permisos en caso de error de Git/Root
Si accidentalmente se ejecutó un comando como `root` y el deploy falla con error `Permission denied`, ejecutar:

```bash
sudo chown -R datamaq:datamaq /var/www/www-datamaq
sudo -u datamaq git status
```

### 4.2 Verificación de Salud del Servidor (Healthchecks)
* **Endpoint de Liveness:** `GET https://isftn199.com.ar/healthz` (200 OK).
* **Endpoint de Readiness:** `GET https://isftn199.com.ar/ready` (Verifica acceso a base de datos: `db_accessible: true`).
* **Logs en Vivo:** `sudo journalctl -u datamaq.service -f -n 50`.
