#!/bin/bash
set -e

# Cargar configuración desde .env.deploy si existe. Si no, se espera que las
# variables estén definidas como entorno (por ejemplo, en GitHub Actions).
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
fi

# Validaciones mínimas
if [ -z "$DEPLOY_SSH_HOST" ] || [ -z "$DEPLOY_SSH_PORT" ] || [ -z "$DEPLOY_SSH_USER" ] || [ -z "$DEPLOY_REMOTE_DIR" ] || [ -z "$DEPLOY_SERVICE_NAME" ]; then
    echo "Error: faltan variables de configuración del deploy."
    echo "Definilas en scripts/.env.deploy o como variables de entorno:"
    echo "  DEPLOY_SSH_HOST, DEPLOY_SSH_PORT, DEPLOY_SSH_USER, DEPLOY_REMOTE_DIR, DEPLOY_SERVICE_NAME"
    exit 1
fi

if [ "$DEPLOY_SSH_USER" = "root" ]; then
    echo "Error: no se permite desplegar como root. Usá un usuario dedicado."
    exit 1
fi

# Guard: prohibido ejecutar el deploy desde el propio VPS. Si DEPLOY_SSH_HOST
# coincide con el hostname o con alguna IP local, el ssh intentaría conectarse a
# sí mismo (auto-SSH), fallando por "Host key verification failed" o generando
# artefactos. El despliegue debe correr desde CI (CD Deploy) o máquina local.
LOCAL_NAMES="$(hostname 2>/dev/null || true) $(hostname -f 2>/dev/null || true) $(hostname -I 2>/dev/null || true)"
case " $LOCAL_NAMES " in
    *" $DEPLOY_SSH_HOST "*)
        echo "Error: no ejecutar deploy-server.sh dentro del VPS."
        echo "El host destino ($DEPLOY_SSH_HOST) coincide con este equipo."
        echo "Usá el workflow 'CD Deploy' de GitHub Actions."
        exit 1
        ;;
esac

# Función de log local
log() { echo "[$(date +"%Y-%m-%dT%H:%M:%S")] $1"; }

log "Iniciando despliegue de Datamaq en $DEPLOY_SSH_HOST..."

# Ejecutamos los comandos remotos. Usamos un heredoc entre comillas simples y
# pasamos las variables necesarias como entorno al proceso bash remoto. Esto
# evita expansiones locales indeseadas y permite usar variables de forma segura
# dentro del bloque remoto (por ejemplo, el commit previo para rollback).
ssh -T -p "$DEPLOY_SSH_PORT" "$DEPLOY_SSH_USER@$DEPLOY_SSH_HOST" \
    DEPLOY_REMOTE_DIR="$DEPLOY_REMOTE_DIR" \
    DEPLOY_SERVICE_NAME="$DEPLOY_SERVICE_NAME" \
    bash <<'EOF'
    set -e

    echo "==> Cambiando a $DEPLOY_REMOTE_DIR"
    cd "$DEPLOY_REMOTE_DIR" || { echo "Error: no se pudo entrar a $DEPLOY_REMOTE_DIR"; exit 1; }

    echo "==> Guardando commit actual para posible rollback..."
    PREVIOUS_COMMIT=$(git rev-parse HEAD)

    echo "==> Verificando permisos de escritura sobre el repositorio git..."
    NOT_WRITABLE=$(find .git -maxdepth 2 ! -writable 2>/dev/null | head -1)
    if [ -n "$NOT_WRITABLE" ]; then
        echo "ERROR: Sin permiso de escritura en '$NOT_WRITABLE'."
        echo "Corregí el ownership del repositorio en el VPS:"
        echo "  sudo chown -R <usuario_despliegue>:<grupo> $DEPLOY_REMOTE_DIR"
        exit 1
    fi

    echo "==> Actualizando código..."
    git pull --ff-only

    echo "==> Instalando dependencias..."
    ./.venv/bin/pip install -r requirements.txt

    echo "==> Reiniciando servicio $DEPLOY_SERVICE_NAME..."
    sudo systemctl restart "$DEPLOY_SERVICE_NAME"

    echo "==> Verificando salud del servicio vía HTTP..."
    HEALTH_URL="http://localhost:8000/"
    MAX_WAIT=30
    INTERVAL=2
    ATTEMPTS=$((MAX_WAIT / INTERVAL))
    HEALTH_OK=false

    for i in $(seq 1 "$ATTEMPTS"); do
        sleep "$INTERVAL"
        HTTP_STATUS=$(./.venv/bin/python3 -c "import urllib.request; print(urllib.request.urlopen('$HEALTH_URL', timeout=5).status)" 2>/dev/null || echo "000")
        if [[ "$HTTP_STATUS" == "200" ]]; then
            HEALTH_OK=true
            echo "Health-check OK (HTTP 200) en el intento $i."
            break
        fi
        echo "Intento $i/$ATTEMPTS: servicio no responde con HTTP 200 (status: $HTTP_STATUS). Reintentando..."
    done

    if [ "$HEALTH_OK" != true ]; then
        echo "ERROR: El health-check falló después de ${MAX_WAIT}s. Ejecutando rollback a $PREVIOUS_COMMIT..."
        git reset --hard "$PREVIOUS_COMMIT"
        echo "==> Reiniciando servicio $DEPLOY_SERVICE_NAME con versión anterior..."
        sudo systemctl restart "$DEPLOY_SERVICE_NAME"
        echo "ERROR: Deploy fallido. Rollback ejecutado."
        exit 1
    fi

    echo "==> Verificando estado del servicio..."
    sudo systemctl is-active "$DEPLOY_SERVICE_NAME"
EOF

if [ $? -eq 0 ]; then
    log "Despliegue exitoso."
else
    log "ERROR: El despliegue falló."
    exit 1
fi

# Purga la caché de Cloudflare tras un despliegue exitoso. No bloqueante si las
# credenciales (CF_API_TOKEN/CF_ZONE_ID) no están definidas; en CI provienen de
# los secrets de GitHub Actions.
log "Purgando caché de Cloudflare..."
python3 scripts/purge_cloudflare.py
