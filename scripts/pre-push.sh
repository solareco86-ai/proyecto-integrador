#!/bin/bash
# pre-push.sh — Hook de git previo al push (Gatekeeper local inteligente)
#
# Valida localmente el 100% de los requisitos del CI antes de enviar código:
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .github/).
# 2. Frescura de CSS crítico y bundle Tailwind.
# 3. Esquemas YAML y reglas de plantillas HTML.
# 4. Clean Architecture & DDD.
# 5. Linter ruff (estilo e imports).
# 6. Verificación estática de tipos estricta (Pyright).
# 7. Tests unitarios e integración con cobertura mínima del 85%.
set -euo pipefail

# Detectar si solo hay cambios en documentación (docs, *.md, .agents, .github)
CHANGED=$(git diff --cached --name-only | grep -E '\\.(md|txt)$|^docs/|^\\.agents/|^\\.github/' || true)

if [[ -z "$CHANGED" ]]; then
  echo "⚡ Solo cambios en documentación – ejecutando quality gate en modo fast"
  ./scripts/quality_gate.sh --fast
else
  echo "🔧 Cambios de código detectados – ejecutando quality gate completo"
  ./scripts/quality_gate.sh
fi

exit 0
# pre-push.sh — Hook de git previo al push (Gatekeeper local inteligente)
#
# Valida localmente el 100% de los requisitos del CI antes de enviar código:
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .gitignore).
# 2. Frescura de CSS crítico y bundle Tailwind.
# 3. Esquemas YAML y reglas de plantillas HTML.
# 4. Clean Architecture & DDD.
# 5. Linter ruff (estilo e imports).
# 6. Verificación estática de tipos estricta (Pyright).
# 7. Tests unitarios e integración con cobertura mínima del 85%.
set -euo pipefail

# Detectar si solo hay cambios en documentación (docs, *.md, .agents, .github)
CHANGED=$(git diff --cached --name-only | grep -E '\\.(md|txt)$|^docs/|^\\.agents/|^\\.github/' || true)

if [[ -z "$CHANGED" ]]; then
  echo "⚡ Solo cambios en documentación – ejecutando quality gate en modo fast"
  ./scripts/quality_gate.sh --fast
else
  echo "🔧 Cambios de código detectados – ejecutando quality gate completo"
  ./scripts/quality_gate.sh
fi

exit 0

# pre-push.sh — Hook de git previo al push (Gatekeeper local inteligente)
#
# Valida localmente el 100% de los requisitos del CI antes de enviar código:
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .gitignore).
# 2. Frescura de CSS crítico y bundle Tailwind.
# 3. Esquemas YAML y reglas de plantillas HTML.
# 4. Clean Architecture & DDD.
# 5. Linter ruff (estilo e imports).
# 6. Verificación estática de tipos estricta (Pyright).
# 7. Tests unitarios e integración con cobertura mínima del 85%.
set -euo pipefail

# Detectar si solo hay cambios en documentación (docs, *.md, .agents, .github)
CHANGED=$(git diff --cached --name-only | grep -E '\\.(md|txt)$|^docs/|^\\.agents/|^\\.github/' || true)

if [[ -z "$CHANGED" ]]; then
  echo "⚡ Solo cambios en documentación – ejecutando quality gate en modo fast"
  ./scripts/quality_gate.sh --fast
else
  echo "🔧 Cambios de código detectados – ejecutando quality gate completo"
  ./scripts/quality_gate.sh
fi

# pre-push.sh — Hook de git previo al push (Gatekeeper local inteligente)
#
# Valida localmente el 100% de los requisitos del CI antes de enviar código:
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .gitignore).
# 2. Frescura de CSS crítico y bundle Tailwind.
# 3. Esquemas YAML y reglas de plantillas HTML.
# 4. Clean Architecture & DDD.
# 5. Linter ruff (estilo e imports).
# 6. Verificación estática de tipos estricta (Pyright).
# 7. Tests unitarios e integración con cobertura mínima del 85%.

set -euo pipefail

# Detectar si solo hay cambios en documentación (docs, *.md, .agents, .github)
CHANGED=$(git diff --cached --name-only | grep -E '\\.(md|txt)$|^docs/|^\\.agents/|^\\.github/' || true)

if [[ -z "$CHANGED" ]]; then
  echo "⚡ Solo cambios en documentación – ejecutando quality gate en modo fast"
  ./scripts/quality_gate.sh --fast
else
  echo "🔧 Cambios de código detectados – ejecutando quality gate completo"
  ./scripts/quality_gate.sh
fi

# pre-push.sh — Hook de git previo al push (Gatekeeper local inteligente)
#
# Valida localmente el 100% de los requisitos del CI antes de enviar código:
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .gitignore).
# 2. Frescura de CSS crítico y bundle Tailwind.
# 3. Esquemas YAML y reglas de plantillas HTML.
# 4. Clean Architecture & DDD.
# 5. Linter ruff (estilo e imports).
# 6. Verificación estática de tipos estricta (Pyright).
# 7. Tests unitarios e integración con cobertura mínima del 85%.

set -e

start_time=$(date +%s)

# 0. Detección inteligente de archivos modificados (Paridad con paths-ignore de GitHub Actions)
changed_files=""
if [ ! -t 0 ]; then
    # Invocado como hook pre-push de git (recibe refs por stdin)
    while read -r local_ref local_sha remote_ref remote_sha; do
        if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
            continue
        fi
        if [ "$remote_sha" = "0000000000000000000000000000000000000000" ]; then
            if git rev-parse --verify origin/main &>/dev/null; then
                diff_files=$(git diff --name-only origin/main "$local_sha" 2>/dev/null || git diff-tree --no-commit-id --name-only -r "$local_sha" 2>/dev/null)
            else
                diff_files=$(git diff-tree --no-commit-id --name-only -r "$local_sha" 2>/dev/null)
            fi
        else
            diff_files=$(git diff --name-only "$remote_sha" "$local_sha" 2>/dev/null || true)
        fi
        changed_files="$changed_files $diff_files"
    done
else
    # Invocación manual desde terminal
    upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "origin/main")
    if git rev-parse --verify "$upstream" &>/dev/null; then
        changed_files=$(git diff --name-only "$upstream"..HEAD 2>/dev/null || true)
    fi
fi

# Si se pudieron determinar los archivos modificados
if [ -n "$(echo "$changed_files" | tr -d '[:space:]')" ]; then
    code_changes=false
    for file in $changed_files; do
        case "$file" in
            docs/*|*.md|.agents/*|.gitignore)
                ;;
            *)
                code_changes=true
                break
                ;;
        esac
    done

    if [ "$code_changes" = false ]; then
        echo "⚡ [Pre-push] Solo se detectaron cambios en documentación y metadatos (*.md, docs/, .agents/, .gitignore)."
        echo "⏩ Omitiendo suite pesada de validación (coincide con paths-ignore de GitHub Actions CD)."
        exit 0
    fi
fi

echo "🚀 [Pre-push] Validando calidad local antes del push..."

# 1. Selección de ejecutable Python
if [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
elif [ -f "./venv/bin/python" ]; then
    PYTHON="./venv/bin/python"
else
    PYTHON="python3"
fi

export PYTHONPATH=$PYTHONPATH:.

# 2. Regeneración y frescura de CSS crítico
echo "==> [1/7] Validando CSS crítico..."
$PYTHON scripts/build_critical_css.py

if ! git diff --exit-code templates/partials/critical_css.html &> /dev/null; then
    echo "❌ ERROR: templates/partials/critical_css.html está desactualizado respecto a los fuentes."
    echo "👉 Ejecutá 'python3 scripts/build_critical_css.py', agregalo ('git add templates/partials/critical_css.html') y reintentá."
    exit 1
fi
echo "✅ CSS crítico validado."

# 3. Compilación de CSS con Tailwind
if command -v npm &> /dev/null; then
    echo "==> [2/7] Compilando CSS con npm..."
    npm run build:css &> /dev/null
    
    if ! git diff --exit-code static/css/index.css &> /dev/null; then
        echo "❌ ERROR: static/css/index.css está desactualizado respecto a los fuentes."
        echo "👉 Ejecutá 'npm run build:css', agregalo ('git add static/css/index.css') y reintentá."
        exit 1
    fi
    echo "✅ Bundle CSS validado."
else
    echo "⚠️ npm no encontrado. Se omite validación de CSS."
fi

# 4. Validar esquemas YAML y plantillas HTML
echo "==> [3/7] Validando esquemas YAML y templates HTML..."
if ! $PYTHON scripts/validate_content.py; then
    echo "❌ ERROR: Auditoría de esquemas YAML fallida."
    exit 1
fi

if ! $PYTHON scripts/validate_templates.py; then
    echo "❌ ERROR: Auditoría de templates HTML fallida."
    exit 1
fi
echo "✅ Contenido YAML y templates HTML válidos."

# 5. Validar Clean Architecture
echo "==> [4/7] Verificando Clean Architecture & DDD..."
if ! $PYTHON scripts/verify_architecture.py; then
    echo "❌ ERROR: Violación de Clean Architecture o DDD."
    exit 1
fi
echo "✅ Arquitectura verificada."

# 6. Linter (ruff)
echo "==> [5/7] Verificando linter (ruff)..."
if command -v ruff &> /dev/null || [ -f "venv/bin/ruff" ]; then
    RUFF_BIN="ruff"
    [ -f "venv/bin/ruff" ] && RUFF_BIN="venv/bin/ruff"
    
    if ! $RUFF_BIN check src/ tests/ scripts/; then
        echo "❌ ERROR: Falló ruff check."
        echo "👉 Ejecutá '$RUFF_BIN check --fix src/ tests/ scripts/' para corregir automáticamente."
        exit 1
    fi
    echo "✅ Linter ruff aprobado (0 errores)."
else
    echo "⚠️ ruff no encontrado en el entorno."
fi

# 7. Tipado estricto (pyright)
echo "==> [6/7] Verificando tipos con pyright..."
if command -v pyright &> /dev/null || [ -f "node_modules/.bin/pyright" ]; then
    PYRIGHT_BIN="pyright"
    [ -f "node_modules/.bin/pyright" ] && PYRIGHT_BIN="node_modules/.bin/pyright"
    
    if ! $PYRIGHT_BIN; then
        echo "❌ ERROR: Existen errores de tipado estricto con pyright."
        exit 1
    fi
    echo "✅ Tipado estricto pyright aprobado (0 errores)."
else
    echo "⚠️ pyright no encontrado en el entorno."
fi

# 8. Tests unitarios con cobertura >= 85%
echo "==> [7/7] Ejecutando tests unitarios y cobertura (pytest)..."
if ! $PYTHON -m pytest --cov=src --cov-fail-under=85 tests/ -q; then
    echo "❌ ERROR: Fallaron las pruebas unitarias o la cobertura es < 85%."
    exit 1
fi
echo "✅ Tests y cobertura aprobados (>= 85%)."

end_time=$(date +%s)
duration=$((end_time - start_time))
echo "🎉 [Pre-push] Validación integral exitosa en ${duration}s. Procediendo con el push."
exit 0
