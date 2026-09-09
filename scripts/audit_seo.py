#!/usr/bin/env python3
"""
Auditoría SEO e imágenes con Playwright.

Verifica en páginas reales del sitio:
- Tags HTML y meta tags esenciales (title, description, canonical, OG).
- Estructura de encabezados (h1 único y orden lógico).
- Imágenes con alt y dimensiones explícitas (width/height) para evitar CLS.

Requiere Playwright instalado:
    source venv/bin/activate
    pip install -r requirements-dev.txt
    playwright install chromium

Uso:
    python3 scripts/audit_seo.py
    python3 scripts/audit_seo.py --base-url http://localhost:8000
    python3 scripts/audit_seo.py --seo-warnings
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Any, cast

from playwright.sync_api import sync_playwright

# Rutas principales del sitio que se auditan por defecto.
DEFAULT_ROUTES: list[str] = [
    "/",
    "/contact",
    "/cursos",
    "/casos",
    "/terminos-y-condiciones",
]


@dataclass
class RouteResult:
    route: str
    url: str
    seo_issues: list[dict[str, Any]] = cast(list[dict[str, Any]], field(default_factory=list))
    image_issues: list[dict[str, Any]] = cast(list[dict[str, Any]], field(default_factory=list))

    @property
    def has_failures(self) -> bool:
        return bool(self.seo_issues or self.image_issues)


def check_heading_order(headings: list[dict[str, str]]) -> list[str]:
    """Detecta saltos inválidos en la jerarquía de encabezados."""
    issues: list[str] = []
    levels = [int(h["level"]) for h in headings]
    for i in range(1, len(levels)):
        prev = levels[i - 1]
        curr = levels[i]
        if curr > prev + 1:
            issues.append(f"Salto de h{prev} a h{curr} en '{headings[i]['text']}'")
    return issues


def audit_route(base_url: str, route: str) -> RouteResult:
    """Audita SEO e imágenes de una ruta real del sitio."""
    url = f"{base_url.rstrip('/')}{route}"
    result = RouteResult(route=route, url=url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 667},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=15000)

        data = page.evaluate("""
            () => {
                const html = document.documentElement;
                const title = document.querySelector('title');
                const description = document.querySelector('meta[name="description"]');
                const canonical = document.querySelector('link[rel="canonical"]');
                const ogTitle = document.querySelector('meta[property="og:title"]');
                const ogDescription = document.querySelector('meta[property="og:description"]');
                const ogImage = document.querySelector('meta[property="og:image"]');

                const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
                    level: parseInt(h.tagName.substring(1)),
                    text: h.textContent.trim().substring(0, 40)
                }));

                const images = Array.from(document.querySelectorAll('img')).map(img => ({
                    src: (img.getAttribute('src') || '').substring(0, 60),
                    alt: img.hasAttribute('alt'),
                    altValue: img.getAttribute('alt') || '',
                    width: img.hasAttribute('width'),
                    height: img.hasAttribute('height'),
                    ariaHidden: img.getAttribute('aria-hidden') === 'true',
                    role: img.getAttribute('role') || '',
                    widthValue: img.getAttribute('width'),
                    heightValue: img.getAttribute('height')
                }));

                return {
                    lang: html.getAttribute('lang') || '',
                    title: title ? title.textContent.trim() : '',
                    description: description ? description.getAttribute('content') || '' : '',
                    canonical: canonical ? canonical.getAttribute('href') || '' : '',
                    ogTitle: ogTitle ? ogTitle.getAttribute('content') || '' : '',
                    ogDescription: ogDescription ? ogDescription.getAttribute('content') || '' : '',
                    ogImage: ogImage ? ogImage.getAttribute('content') || '' : '',
                    headings,
                    images
                };
            }
        """)

        browser.close()

    # SEO checks
    if not data["lang"]:
        result.seo_issues.append({"type": "lang", "message": "Falta atributo lang en <html>"})
    if not data["title"]:
        result.seo_issues.append({"type": "title", "message": "Falta <title> o está vacío"})
    if not data["description"]:
        result.seo_issues.append({"type": "description", "message": 'Falta <meta name="description"> o está vacío'})
    if not data["canonical"]:
        result.seo_issues.append({"type": "canonical", "message": 'Falta <link rel="canonical"> o href vacío'})
    if not data["ogTitle"]:
        result.seo_issues.append({"type": "og:title", "message": 'Falta <meta property="og:title">'})
    if not data["ogDescription"]:
        result.seo_issues.append({"type": "og:description", "message": 'Falta <meta property="og:description">'})
    if not data["ogImage"]:
        result.seo_issues.append({"type": "og:image", "message": 'Falta <meta property="og:image">'})

    h1_count = sum(1 for h in data["headings"] if h["level"] == 1)
    if h1_count == 0:
        result.seo_issues.append({"type": "h1", "message": "No hay <h1> en la página"})
    elif h1_count > 1:
        result.seo_issues.append({"type": "h1", "message": f"Hay {h1_count} <h1>; debe haber exactamente 1"})

    for issue_text in check_heading_order(data["headings"]):
        result.seo_issues.append({"type": "headings", "message": issue_text})

    # Image checks
    for img in data["images"]:
        is_decorative = img["ariaHidden"] or img["role"] == "presentation"
        if not img["alt"] and not is_decorative:
            result.image_issues.append(
                {
                    "type": "alt",
                    "src": img["src"],
                    "message": "<img> sin atributo alt",
                }
            )
        if img["alt"] and img["altValue"] == "" and not is_decorative:
            result.image_issues.append(
                {
                    "type": "alt-empty",
                    "src": img["src"],
                    "message": "alt vacío sin aria-hidden='true' ni role='presentation'",
                }
            )
        if not img["width"] or not img["height"]:
            result.image_issues.append(
                {
                    "type": "dimensions",
                    "src": img["src"],
                    "message": "<img> sin width/height explícitos (riesgo de CLS)",
                }
            )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría SEO e imágenes con Playwright")
    parser.add_argument("--base-url", default="http://localhost:8000", help="URL base del servidor")
    parser.add_argument(
        "--routes",
        nargs="+",
        default=DEFAULT_ROUTES,
        help="Rutas a auditar (default: / /contact /cursos /casos /terminos-y-condiciones)",
    )
    parser.add_argument(
        "--seo-warnings",
        action="store_true",
        help="Reporta hallazgos SEO e imágenes sin contarlos como fallas (modo impacto)",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("Auditoría SEO e imágenes con Playwright")
    print(f"Rutas: {len(args.routes)} | Modo: {'warnings' if args.seo_warnings else 'estricto'}")
    print("=" * 70)

    total_seo_issues = 0
    total_image_issues = 0
    route_failures = 0
    results: list[RouteResult] = []

    for route in args.routes:
        print(f"\n🔍 {route}")
        try:
            result = audit_route(args.base_url, route)
        except Exception as exc:  # noqa: BLE001
            print(f"   ❌ Error al auditar {route}: {exc}")
            route_failures += 1
            continue

        results.append(result)

        for issue in result.seo_issues:
            total_seo_issues += 1
            label = "⚠️" if args.seo_warnings else "❌"
            print(f"   {label} [{issue['type']}] {issue['message']}")

        for issue in result.image_issues:
            total_image_issues += 1
            label = "⚠️" if args.seo_warnings else "❌"
            print(f"   {label} [{issue['type']}] {issue['src']}: {issue['message']}")

        if result.seo_issues or result.image_issues:
            if not args.seo_warnings:
                route_failures += 1
                print(f"   ❌ {route} tiene fallas")
            else:
                print(f"   ⚠️ {route} tiene warnings")
        else:
            print("   ✅ SEO e imágenes correctos")

    print("\n" + "=" * 70)
    print("Resumen:")
    print(f"   Rutas auditadas: {len(args.routes)}")
    print(f"   Problemas SEO: {total_seo_issues}")
    print(f"   Problemas de imágenes: {total_image_issues}")
    print(f"   Rutas con fallas: {route_failures}")

    if route_failures == 0:
        print("   ✅ Auditoría SEO superada")
        return 0
    print("   ❌ Se detectaron problemas de SEO o imágenes")
    return 1


if __name__ == "__main__":
    sys.exit(main())
