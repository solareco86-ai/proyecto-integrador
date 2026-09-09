#!/usr/bin/env python
"""Validador estático de templates HTML.

Reglas:
- R1: prohíbe expresiones Jinja (``{{`` / ``{%``) dentro del valor de atributos ``style="..."``,
  salvo cuando el valor es una declaración de CSS custom property (``--nombre: <valor>``).
- R2: verifica el balance de llaves ``{``/``}`` en bloques ``<style>`` embebidos,
  ignorando strings y comentarios CSS.

Uso:
    python scripts/validate_templates.py [--templates-dir templates]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_STYLE_JINJA_RE = re.compile(r"""style\s*=\s*["']([^"']*?)(?:\{\{|\{%)""")
_STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)


def _linea_del_match(contenido: str, pos: int) -> int:
    """Devuelve el número de línea (1-indexado) en el que cae la posición dada."""
    return contenido[:pos].count("\n") + 1


def _balance_llaves(css: str) -> int:
    """Devuelve el balance neto de llaves, ignorando strings y comentarios CSS."""
    balance = 0
    i = 0
    n = len(css)
    in_string: str | None = None
    while i < n:
        ch = css[i]
        nxt = css[i + 1] if i + 1 < n else ""
        if in_string is not None:
            if ch == "\\":
                i += 2
                continue
            if ch == in_string:
                in_string = None
            i += 1
            continue
        if ch == "/" and nxt == "*":
            fin = css.find("*/", i + 2)
            i = n if fin == -1 else fin + 2
            continue
        if ch in ('"', "'"):
            in_string = ch
            i += 1
            continue
        if ch == "{":
            balance += 1
        elif ch == "}":
            balance -= 1
        i += 1
    return balance


def validate_template_file(path: Path) -> list[str]:
    """Devuelve la lista de errores (``archivo:línea: mensaje``) de un template."""
    contenido = path.read_text(encoding="utf-8")
    errores: list[str] = []

    for match in _STYLE_JINJA_RE.finditer(contenido):
        prefijo = match.group(1).strip()
        if prefijo.startswith("--"):
            continue
        linea = _linea_del_match(contenido, match.start())
        errores.append(
            f"{path}:{linea}: Expresión Jinja en atributo style: "
            "mover la lógica a una clase CSS (definirla en critical_css.html)"
        )

    for match in _STYLE_BLOCK_RE.finditer(contenido):
        if _balance_llaves(match.group(1)) != 0:
            linea = _linea_del_match(contenido, match.start())
            errores.append(
                f"{path}:{linea}: Llaves desbalanceadas en bloque <style>: se espera un cierre o sobra una llave"
            )

    return errores


def validate_tree(root: Path) -> list[str]:
    """Recorre un árbol en busca de ``*.html`` y concatena los errores de cada archivo."""
    errores: list[str] = []
    for archivo in sorted(root.rglob("*.html")):
        if archivo.is_file():
            errores.extend(validate_template_file(archivo))
    return errores


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida reglas de diseño y sintaxis de templates HTML (Jinja en style, balance CSS)."
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Directorio raíz de templates (default: 'templates').",
    )
    args = parser.parse_args()

    errores = validate_tree(Path(args.templates_dir))

    if errores:
        for error in errores:
            print(error, file=sys.stderr)
        print(f"❌ {len(errores)} defecto(s) en templates.", file=sys.stderr)
        return 1

    print("✅ Templates HTML válidos (sin Jinja en style, CSS balanceado).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
