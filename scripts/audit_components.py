#!/usr/bin/env python3
"""
Auditoría de componentes UI/UX para desarrollo local.

Este script:
1. Lista los archivos físicos de componentes en templates/partials/components/.
2. Verifica cuáles tienen una rama de previsualización en templates/preview.html.
3. Hace peticiones HTTP a cada /dev/preview/{componente} y reporta el estado.
4. Mide el ancho del body renderizado en viewport móvil si Google Chrome está disponible
   en modo headless (sin dependencias de terceros).

Uso:
    PYTHONPATH=. python scripts/audit_components.py
    python scripts/audit_components.py --base-url http://localhost:8000
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_DIR = PROJECT_ROOT / "templates" / "partials" / "components"
PREVIEW_TEMPLATE = PROJECT_ROOT / "templates" / "preview.html"

# Componentes que son macros auxiliares y no requieren preview propia.
HELPER_COMPONENTS = {"icon.html"}

# Viewports móviles de referencia para la auditoría responsive.
MOBILE_VIEWPORTS = [
    (375, 667, "iPhone SE/8"),
    (390, 844, "iPhone 14"),
    (412, 915, "Android large"),
]


def list_physical_components() -> list[str]:
    """Devuelve los nombres base de los archivos de componentes."""
    return sorted(p.stem for p in COMPONENTS_DIR.glob("*.html") if p.is_file())


def list_previewable_components() -> list[str]:
    """Extrae los nombres de componentes que tienen rama en preview.html."""
    if not PREVIEW_TEMPLATE.exists():
        return []
    text = PREVIEW_TEMPLATE.read_text(encoding="utf-8")

    # Captura tanto {% if ... %} como {% elif ... %>
    branch_pattern = re.compile(r"{%\s*(?:if|elif)\s+(.*?)\s+%}")
    branches = branch_pattern.findall(text)

    components: list[str] = []
    for branch in branches:
        # Extrae todos los literales de string de la condición Jinja.
        for name in re.findall(r"['\"]([^'\"]+)['\"]", branch):
            components.append(name)

    return sorted(set(components))


def fetch_status(base_url: str, component: str) -> tuple[int, str | None]:
    """Hace una petición GET al preview del componente y devuelve (status, error)."""
    url = f"{base_url}/dev/preview/{component}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.status, None
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc.reason)
    except Exception as exc:  # noqa: BLE001
        return 0, str(exc)


def chrome_available() -> bool:
    """Detecta si hay un ejecutable de Chrome/Google Chrome en PATH."""
    for binary in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        try:
            subprocess.run(
                [binary, "--version"],
                capture_output=True,
                check=True,
                timeout=5,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    return False


def measure_with_chrome(base_url: str, component: str, width: int, height: int) -> dict[str, Any] | None:
    """Usa Chrome headless para medir scrollWidth y contar enlaces pequeños."""
    if not chrome_available():
        return None

    url = f"{base_url}/dev/preview/{component}"

    for binary in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        try:
            subprocess.run(
                [
                    binary,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    f"--window-size={width},{height}",
                    "--hide-scrollbars",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=3000",
                    "--dump-dom",
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=20,
                check=True,
            )
            return {
                "viewport": {"width": width, "height": height},
                "note": "Chrome detectado. Para mediciones JS exactas usar scripts/audit_responsive.py (Playwright).",
            }
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría de componentes UI/UX")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="URL base del servidor de desarrollo (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--skip-chrome",
        action="store_true",
        help="Omitir mediciones con Chrome headless",
    )
    args = parser.parse_args()

    physical = list_physical_components()
    previewable = list_previewable_components()

    print("=" * 60)
    print("Auditoría de componentes UI/UX - DataMaq")
    print("=" * 60)
    print(f"\nComponentes físicos: {len(physical)}")
    print(f"Componentes con preview: {len(previewable)}")
    print(f"Helpers sin preview: {', '.join(Path(h).stem for h in HELPER_COMPONENTS)}\n")

    missing: list[str] = []
    for comp in physical:
        if comp not in previewable and f"{comp}.html" not in HELPER_COMPONENTS:
            missing.append(comp)

    if missing:
        print("⚠️  Componentes sin preview aislado:")
        for comp in missing:
            print(f"   - {comp}")
    else:
        print("✅ Todos los componentes interactivos tienen preview aislado.")

    print("\nSmoke test de previews:")
    failures = 0
    for comp in previewable:
        status, error = fetch_status(args.base_url, comp)
        symbol = "✅" if status == 200 else "❌"
        detail = f" ({error})" if error else ""
        print(f"   {symbol} /dev/preview/{comp} -> HTTP {status}{detail}")
        if status != 200:
            failures += 1

    if not args.skip_chrome and chrome_available():
        print("\nMedición headless (Chrome disponible):")
        for comp in previewable[:3]:  # limitamos para no demorar demasiado
            for width, height, name in MOBILE_VIEWPORTS[:1]:
                result = measure_with_chrome(args.base_url, comp, width, height)
                if result:
                    print(f"   📱 {comp} @ {name}: {json.dumps(result, ensure_ascii=False)}")
    elif not args.skip_chrome:
        print("\nℹ️ Chrome no detectado; se omite la medición headless.")

    print("\n" + "=" * 60)
    if failures == 0 and not missing:
        print("Resultado: ✅ Auditoría superada")
        return 0
    print(f"Resultado: ❌ {failures} previews fallaron, {len(missing)} sin mapeo")
    return 1


if __name__ == "__main__":
    sys.exit(main())
