#!/usr/bin/env bash
#
# CI.sh — Pipeline de auditoría completa e integración continua para datamaq.com.ar
#
# Corre validaciones de CSS, contenido YAML, linter (ruff), tests unitarios con cobertura,
# smoke tests de componentes, auditorías con Playwright (responsive/usabilidad/SEO),
# barrido de términos prohibidos y prueba E2E de leads.
#
# Uso: bash scripts/CI.sh

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

start_time=$(date +%s)

PASS=0
FAIL=0
SKIP=0

green() { echo -e "\033[32m$1\033[0m"; }
red()   { echo -e "\033[31m$1\033[0m"; }
yellow(){ echo -e "\033[33m$1\033[0m"; }

check() {
    local label="$1" cmd="$2" critical="${3:-true}"
    echo -n "[....] $label "
    if eval "$cmd" > /tmp/ci-check.log 2>&1; then
        green "PASS"
        PASS=$((PASS + 1))
        return 0
    else
        if [ "$critical" = "false" ]; then
            yellow "SKIP (no crítico)"
            SKIP=$((SKIP + 1))
            return 0
        fi
        red "FAIL"
        echo "  ── salida ────────────────────────"
        head -15 /tmp/ci-check.log
        echo "  ──────────────────────────────────"
        FAIL=$((FAIL + 1))
        return 1
    fi
}

echo "=================================================="
echo "🚀 Auditoría Completa CI :: datamaq.com.ar"
echo "=================================================="

PYTHON_BIN="python3"
if [ -x "./venv/bin/python" ]; then
    PYTHON_BIN="./venv/bin/python"
fi

export PYTHONPATH="${PYTHONPATH:-}:."

# 1. Compilación y frescura de CSS
check "Compilación CSS (npm)" "npm run build:css && git diff --exit-code static/css/index.css" false

# 1b. Frescura del CSS crítico (partial generado)
check "CSS crítico (build_critical_css.py)" "$PYTHON_BIN scripts/build_critical_css.py && git diff --exit-code templates/partials/critical_css.html"

# 2. Validación de contenido YAML/Markdown
check "Validación YAML (validate_content.py)" "$PYTHON_BIN scripts/validate_content.py"

# 2b. Validación de reglas de diseño de templates HTML
check "Templates HTML (validate_templates.py)" "$PYTHON_BIN scripts/validate_templates.py"

# 2c. Verificación estática de Clean Architecture & DDD
check "Arquitectura Limpia (verify_architecture.py)" "$PYTHON_BIN scripts/verify_architecture.py"

# 3. Barrido de términos prohibidos
check "Términos prohibidos" 'grep -rin --include="*.yaml" --include="*.html" --include="*.md" \
  -e "vaca muerta" -e "yacimiento" -e "cuenca neuquina" -e "neuquén capital" \
  data/ templates/ | grep -v "data/config/redirects.yaml" | grep -v "docs/" | grep -v "AGENTS.md"; test $? -ne 0'

# 4. Linter ruff
check "Linter (ruff check)" "$PYTHON_BIN -m ruff check src/ tests/ || ruff check src/ tests/"

# 5. Tests unitarios e integración con cobertura
check "Pytest (cobertura >=85%)" "$PYTHON_BIN -m pytest --cov=src --cov-report=term-missing --cov-fail-under=85 tests/"

# 6. E2E test de captación de leads
check "E2E Lead test (test_lead_e2e.py)" "$PYTHON_BIN scripts/test_lead_e2e.py"

# 7. Auditorías con servidor activo (Components preview, Playwright responsive y SEO)
SERVER_PID=""
PORT=8008
cleanup_server() {
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup_server EXIT INT TERM

echo "==> Levantando servidor temporal en http://127.0.0.1:$PORT para auditorías HTTP/Playwright..."
$PYTHON_BIN -m uvicorn src.infrastructure.fastapi.app:app --host 127.0.0.1 --port $PORT --no-access-log > /dev/null 2>&1 &
SERVER_PID=$!

server_ready=false
for i in $(seq 1 15); do
    if curl -s "http://127.0.0.1:$PORT/health" &> /dev/null || curl -s "http://127.0.0.1:$PORT/" &> /dev/null; then
        server_ready=true
        break
    fi
    sleep 1
done

if [ "$server_ready" = true ]; then
    check "Componentes preview (audit_components.py)" "$PYTHON_BIN scripts/audit_components.py --base-url http://127.0.0.1:$PORT --skip-chrome"
    check "Auditoría Responsive (Playwright)" "$PYTHON_BIN scripts/audit_responsive.py --base-url http://127.0.0.1:$PORT" false
    check "Auditoría SEO (Playwright)" "$PYTHON_BIN scripts/audit_seo.py --base-url http://127.0.0.1:$PORT" false
else
    yellow "⚠️ No se pudo levantar servidor en puerto $PORT. Omitiendo auditorías HTTP/Playwright."
fi

cleanup_server
trap - EXIT INT TERM

end_time=$(date +%s)
duration=$((end_time - start_time))

echo ""
echo "───────────────────────────────"
echo "Resultado: $PASS pasaron, $SKIP saltados/opcionales, $FAIL fallaron (tiempo: ${duration}s)"
if [ "$FAIL" -gt 0 ]; then
    red "❌ CI FAILED"
    exit 1
else
    green "✅ CI PASSED"
    exit 0
fi

