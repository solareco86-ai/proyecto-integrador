#!/usr/bin/env bash
#
# pre-push.sh — Hook de git previo al push (CI local obligatorio)
#
# Ejecuta el 100% de las validaciones de calidad localmente en CPU ($0 Tokens):
# 1. Detección rápida: Omite la suite pesada si solo se modificaron docs (*.md, docs/, .agents/, .gitignore).
# 2. Frescura de CSS crítico (build_critical_css.py).
# 3. Compilación de CSS con Tailwind y validación de diff.
# 4. Esquemas YAML (validate_content.py) y plantillas HTML (validate_templates.py).
# 5. Clean Architecture & DDD (verify_architecture.py).
# 6. Linter ruff (src/, tests/, scripts/).
# 7. Tipado estricto Python con Pyright.
# 8. Tipado estricto JavaScript con TypeScript LSP (npm run typecheck:js).
# 9. Tests unitarios e integración con cobertura mínima del 85% (pytest).
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

start_time=$(date +%s)

# 0. Detección inteligente de archivos modificados (Paridad con paths-ignore de CD)
changed_files=""
if [ ! -t 0 ]; then
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
    upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "origin/main")
    if git rev-parse --verify "$upstream" &>/dev/null; then
        changed_files=$(git diff --name-only "$upstream"..HEAD 2>/dev/null || true)
    fi
fi

if [ -n "$(echo "$changed_files" | tr -d "[:space:]")" ]; then
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
        echo "⏩ Omitiendo suite pesada de validación."
        exit 0
    fi
fi

echo "=================================================="
echo "🚀 [Pre-push] Validando calidad local de CI (CPU $0 tokens)..."
echo "=================================================="

if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
    export PATH="$ROOT_DIR/.venv/bin:$PATH"
elif [ -d "venv" ]; then
    PYTHON="venv/bin/python"
    export PATH="$ROOT_DIR/venv/bin:$PATH"
else
    PYTHON="python3"
fi

export PYTHONPATH=".:${PYTHONPATH:-}"

echo "==> [1/9] Validando CSS crítico..."
$PYTHON scripts/build_critical_css.py
if ! git diff --exit-code templates/partials/critical_css.html &> /dev/null; then
    echo "❌ ERROR: templates/partials/critical_css.html está desactualizado respecto a los fuentes."
    echo "👉 Ejecutá '$PYTHON scripts/build_critical_css.py' y agregalo con 'git add'."
    exit 1
fi
echo "✅ CSS crítico validado."

echo "==> [2/9] Validando compilación CSS (Tailwind)..."
if command -v npm &> /dev/null; then
    npm run build:css &> /dev/null
    if ! git diff --exit-code static/css/index.css &> /dev/null; then
        echo "❌ ERROR: static/css/index.css está desactualizado respecto a los fuentes."
        echo "👉 Ejecutá 'npm run build:css' y agregalo con 'git add'."
        exit 1
    fi
    echo "✅ Bundle CSS validado."
else
    echo "⚠️ npm no encontrado en el sistema. Se omite paso CSS."
fi

echo "==> [3/9] Validando contenidos YAML..."
if ! $PYTHON scripts/validate_content.py; then
    echo "❌ ERROR: Auditoría de contenidos YAML fallida."
    exit 1
fi
echo "✅ Contenidos YAML validados."

echo "==> [4/9] Validando templates HTML..."
if ! $PYTHON scripts/validate_templates.py; then
    echo "❌ ERROR: Auditoría de templates HTML fallida."
    exit 1
fi
echo "✅ Templates HTML conformes."

echo "==> [5/9] Verificando Clean Architecture & DDD..."
if ! $PYTHON scripts/verify_architecture.py; then
    echo "❌ ERROR: Violación de reglas de arquitectura limpia."
    exit 1
fi
echo "✅ Arquitectura Limpia verificada (100%)."

echo "==> [6/9] Verificando estilo y lint con ruff..."
if command -v ruff &> /dev/null; then
    RUFF_BIN="ruff"
else
    RUFF_BIN="$PYTHON -m ruff"
fi

if ! $RUFF_BIN check src/ tests/ scripts/; then
    echo "❌ ERROR: Falló ruff check."
    echo "👉 Ejecutá '$RUFF_BIN check --fix src/ tests/ scripts/' para auto-reparar."
    exit 1
fi
echo "✅ Linter ruff aprobado (0 errores)."

echo "==> [7/9] Verificando tipos Python con pyright..."
if command -v pyright &> /dev/null; then
    PYRIGHT_BIN="pyright"
else
    PYRIGHT_BIN="$PYTHON -m pyright"
fi

if ! $PYRIGHT_BIN; then
    echo "❌ ERROR: Errores de tipado estricto detectados por pyright."
    exit 1
fi
echo "✅ Pyright aprobado (0 diagnósticos)."

echo "==> [8/9] Verificando tipos JavaScript con tsc..."
if command -v npm &> /dev/null; then
    if ! npm run typecheck:js; then
        echo "❌ ERROR: Errores de tipado JavaScript detectados."
        exit 1
    fi
    echo "✅ JavaScript typecheck aprobado (0 errores)."
else
    echo "⚠️ npm no encontrado. Se omite typecheck JS."
fi

echo "==> [9/9] Ejecutando suite de pruebas con cobertura (pytest)..."
if ! $PYTHON -m pytest --cov=src --cov-fail-under=85 tests/ -q; then
    echo "❌ ERROR: Fallaron las pruebas o la cobertura es inferior al 85%."
    exit 1
fi
echo "✅ Suite de tests aprobada con cobertura >= 85%."

end_time=$(date +%s)
duration=$((end_time - start_time))
echo "=================================================="
echo "🎉 [Pre-push] Validación local de CI exitosa en ${duration}s. Push autorizado."
echo "=================================================="
exit 0
