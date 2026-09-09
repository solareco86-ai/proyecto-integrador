#!/usr/bin/env bash
set -euo pipefail

# Helper para medir tiempo de cada paso
_time_step() {
  local description="$1"
  shift
  echo "▶️  $description"
  local start=$(date +%s)
  "$@"
  local end=$(date +%s)
  echo "✅ $description ($(($end - $start))s)"
}

# Flags
FAST=false
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --fast) FAST=true; shift;;
    *) shift;;
  esac
done

# Selección del ejecutable Python
if [ -f ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
  export PATH="$(pwd)/.venv/bin:$PATH"
elif [ -f "venv/bin/python" ]; then
  PYTHON="venv/bin/python"
  export PATH="$(pwd)/venv/bin:$PATH"
elif [ -f "./venv/bin/python" ]; then
  PYTHON="./venv/bin/python"
  export PATH="$(pwd)/venv/bin:$PATH"
else
  PYTHON="python3"
fi
: "${PYTHONPATH:=.}"; export PYTHONPATH

# 1️⃣ CSS crítico (solo en modo full)
if ! $FAST; then
  _time_step "Generar CSS crítico" python3 scripts/build_critical_css.py
  _time_step "Verificar diff CSS crítico" git diff --quiet templates/partials/critical_css.html || { echo "Error: CSS crítico modificado"; exit 1; }
fi

# 2️⃣ Compilación Tailwind (solo en modo full)
if ! $FAST; then
  _time_step "Compilar Tailwind CSS" npm run build:css
  _time_step "Verificar diff CSS compilado" git diff --quiet static/css/index.css || { echo "Error: CSS compilado modificado"; exit 1; }
fi

# 3️⃣ Validar YAML
_time_step "Validar contenidos YAML" python3 scripts/validate_content.py

# 4️⃣ Validar templates Jinja
_time_step "Validar templates" python3 scripts/validate_templates.py

# 5️⃣ Verificar Clean Architecture (solo en modo full)
if ! $FAST; then
  _time_step "Verificar Clean Architecture" python3 scripts/verify_architecture.py
fi

# 6️⃣ Linter ruff
_time_step "Lint con ruff" ruff check src/ tests/ scripts/

# 7️⃣ Pyright (tipado estricto)
_time_step "Chequeo de tipado con pyright" pyright

# 8️⃣ Tests unitarios con cobertura (solo en modo full)
if ! $FAST; then
  _time_step "Ejecutar pruebas con cobertura" pytest --cov=src --cov-fail-under=85
else
  echo "⚡ Modo fast: se omitieron tests y cobertura"
fi

echo "🎉 Quality gate completado exitosamente"
