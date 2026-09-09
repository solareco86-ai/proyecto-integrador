"""Generador del partial de CSS crítico (templates/partials/critical_css.html).

Lee la fuente real ``static/css/src/critical.css``, resuelve inline sus imports
relativos (``@import "./tokens.css";``) y emite el partial HTML autocontenido.

El partial generado es un artefacto de build: no editar a mano.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_IMPORT_RE = re.compile(r'^@import\s+["\']([^"\']+)["\']\s*;?\s*$', re.MULTILINE)
_CHARSET_RE = re.compile(r'^@charset\s+["\'][^"\']+["\']\s*;?\s*$', re.MULTILINE)

_SRC_DIR = Path("static") / "css" / "src"
_PARTIAL = Path("templates") / "partials" / "critical_css.html"


def resolve_imports(css: str, base_dir: Path) -> str:
    """Resuelve inline los ``@import`` relativos (``./`` o ``../``) de forma recursiva.

    Los imports no relativos (p. ej. ``tailwindcss``) se dejan intactos.
    Lanza :class:`ValueError` ante imports circulares.
    """

    def _resolver(contenido: str, directorio: Path, pila: set[Path]) -> str:
        def _reemplazar(match: re.Match[str]) -> str:
            objetivo = match.group(1)
            if not (objetivo.startswith("./") or objetivo.startswith("../")):
                return match.group(0)
            destino = (directorio / objetivo).resolve()
            if destino in pila:
                raise ValueError(f"Import circular detectado: {destino}")
            pila.add(destino)
            texto = destino.read_text(encoding="utf-8")
            texto = _CHARSET_RE.sub("", texto)
            resuelto = _resolver(texto, destino.parent, pila)
            pila.discard(destino)
            return resuelto

        return _IMPORT_RE.sub(_reemplazar, contenido)

    return _resolver(css, base_dir, set())


def build_critical_css(project_root: Path) -> str:
    """Genera el contenido completo del partial (``<style>`` incluido)."""
    fuente = project_root / _SRC_DIR / "critical.css"
    css = fuente.read_text(encoding="utf-8")
    css = resolve_imports(css, fuente.parent).strip()
    return "<style>\n" + css + "\n</style>\n"


def main() -> int:
    """CLI: regenera ``templates/partials/critical_css.html``. Retorna 0 si ok, 1 si error."""
    raiz = Path(__file__).resolve().parent.parent
    destino = raiz / _PARTIAL
    try:
        contenido = build_critical_css(raiz)
    except (OSError, ValueError) as exc:
        print(f"❌ ERROR generando critical_css.html: {exc}", file=sys.stderr)
        return 1
    destino.write_text(contenido, encoding="utf-8")
    print(f"✅ Partial generado: {destino.relative_to(raiz)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
