#!/bin/bash
# Provisión idempotente del entorno dev (https://dev.isftn199.com.ar) en el VPS.
#
# Se ejecuta UNA vez como root en el VPS, desde un checkout que contenga este
# directorio (p. ej. tras `sudo -u datamaq git fetch` de la rama develop):
#
#   sudo bash deploy/dev/provision-dev.sh
#
# Crea: checkout de la rama de integración, venv, .env propio (BD SQLite propia
# en data/leads.db del checkout dev, sin credenciales de producción), servicio
# systemd en 127.0.0.1:8004, regla sudoers de deploy, vhost nginx con guardia
# de acceso (Basic Auth + allow-list Cloudflare) y snippet de rangos Cloudflare.
# Los comandos git se ejecutan SIEMPRE como `datamaq` (ver AGENTS.md §6).
set -euo pipefail

DEV_DIR="/var/www/proyecto-integrador-dev"
BRANCH="${DEV_BRANCH:-develop}"
REPO_URL="${REPO_URL:-https://github.com/solareco86-ai/proyecto-integrador.git}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_USER="isftn199"
DEPLOY_USER="datamaq"

log() { echo "[provision-dev] $1"; }

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: ejecutar como root (sudo)." >&2
    exit 1
fi

log "1/9 Checkout de '$BRANCH' en $DEV_DIR"
if [ ! -d "$DEV_DIR/.git" ]; then
    install -d -o "$DEPLOY_USER" -g "$DEPLOY_USER" -m 755 "$DEV_DIR"
    sudo -u "$DEPLOY_USER" git clone --branch "$BRANCH" "$REPO_URL" "$DEV_DIR"
else
    log "    ya existe, se omite el clone"
fi

log "2/9 Entorno virtual y dependencias"
if [ ! -x "$DEV_DIR/.venv/bin/python3" ]; then
    sudo -u "$DEPLOY_USER" python3 -m venv "$DEV_DIR/.venv"
fi
sudo -u "$DEPLOY_USER" "$DEV_DIR/.venv/bin/pip" install -r "$DEV_DIR/requirements.txt"

log "3/9 Archivo .env propio (sin secretos de producción)"
if [ ! -f "$DEV_DIR/.env" ]; then
    SECRET="$("$DEV_DIR/.venv/bin/python3" -c 'import secrets; print(secrets.token_urlsafe(48))')"
    umask 077
    cat > "$DEV_DIR/.env" <<ENV
BASE_URL=https://dev.isftn199.com.ar
DEBUG=False
WHATSAPP_ENABLED=false
DATABASE_URL=sqlite+aiosqlite:///data/leads.db
SECRET_KEY=$SECRET
SESSION_COOKIE_NAME=isft199_dev_session
ENV
    # Igual que producción: la app (usuario isftn199) lee el .env vía load_dotenv().
    chown "$DEPLOY_USER:$APP_USER" "$DEV_DIR/.env"
    chmod 640 "$DEV_DIR/.env"
else
    log "    .env ya existe, no se toca"
fi

log "4/9 Permisos de data/ (la app escribe solo su SQLite)"
chgrp "$APP_USER" "$DEV_DIR/data"
chmod 2775 "$DEV_DIR/data"

log "5/9 Servicio systemd"
install -m 644 "$SRC_DIR/isftn199-dev.service" /etc/systemd/system/isftn199-dev.service
systemctl daemon-reload
systemctl enable --now isftn199-dev.service

log "6/9 Regla sudoers de deploy (validada con visudo)"
TMP_SUDOERS="$(mktemp)"
install -m 440 "$SRC_DIR/sudoers-isftn199-dev" "$TMP_SUDOERS"
visudo -cf "$TMP_SUDOERS"
install -m 440 -o root -g root "$TMP_SUDOERS" /etc/sudoers.d/datamaq-deploy-isftn199-dev
rm -f "$TMP_SUDOERS"

log "7/9 Guardia de acceso dev: htpasswd (idempotente)"
HTPASSWD=/etc/nginx/.htpasswd-dev
if [ ! -f "$HTPASSWD" ]; then
    PASS="${DEV_BASIC_AUTH_PASS:-$(openssl rand -base64 18)}"
    printf '%s:%s\n' "${DEV_BASIC_AUTH_USER:-dev}" "$(openssl passwd -apr1 "$PASS")" > "$HTPASSWD"
    chmod 640 "$HTPASSWD"
    log "    Credencial generada: usuario=${DEV_BASIC_AUTH_USER:-dev} password=$PASS (guardar; no se repite)"
else
    log "    $HTPASSWD ya existe, no se toca"
fi

log "8/9 Rangos Cloudflare (allow-list de origen)"
install -d /etc/nginx/snippets
SNIP=/etc/nginx/snippets/cloudflare-allow.conf
if curl -fsS https://www.cloudflare.com/ips-v4 > /tmp/cf-v4.txt 2>/dev/null \
   && curl -fsS https://www.cloudflare.com/ips-v6 > /tmp/cf-v6.txt 2>/dev/null; then
    {
        echo "allow 127.0.0.1;"
        echo "allow ::1;"
        sed 's/^/allow /;s/$/;/' /tmp/cf-v4.txt
        sed 's/^/allow /;s/$/;/' /tmp/cf-v6.txt
        echo "deny all;"
    } > "$SNIP"
    rm -f /tmp/cf-v4.txt /tmp/cf-v6.txt
    log "    rangos actualizados desde cloudflare.com"
else
    install -m 644 "$SRC_DIR/cloudflare-allow.conf" "$SNIP"
    rm -f /tmp/cf-v4.txt /tmp/cf-v6.txt
    log "    sin red: se usa la plantilla versionada (revisar rangos)"
fi

log "9/9 Vhost nginx (se recarga solo si 'nginx -t' pasa)"
install -m 644 "$SRC_DIR/dev.isftn199.com.ar.conf" /etc/nginx/conf.d/dev.isftn199.com.ar.conf
if nginx -t; then
    systemctl reload nginx
else
    echo "ERROR: nginx -t falló; se quita el vhost nuevo para no dejar nginx roto." >&2
    rm -f /etc/nginx/conf.d/dev.isftn199.com.ar.conf
    exit 1
fi

log "Listo. Verificación local:"
sleep 3
curl -s -o /dev/null -w "  app (127.0.0.1:8004): HTTP %{http_code}\n" http://127.0.0.1:8004/ || true
curl -s -o /dev/null -w "  nginx (Host dev): HTTP %{http_code}\n" -H "Host: dev.isftn199.com.ar" -H "X-Forwarded-Proto: https" http://127.0.0.1/ || true
