"""Pruebas RED de limpieza de assets legacy de la página /monitoreo."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_legacy_assets_removed():
    """Los assets de la página /monitoreo ya no deben existir."""
    assert not (REPO_ROOT / "templates" / "monitoreo.html").exists()
    assert not (REPO_ROOT / "static" / "js" / "modules" / "telemetry_dashboard.js").exists()
    assert not (REPO_ROOT / "static" / "css" / "telemetry.css").exists()


@pytest.mark.parametrize(
    "needle",
    [
        "telemetry_dashboard.js",
        "telemetry.css",
        'href="/monitoreo"',
    ],
)
def test_no_residual_references(needle: str):
    """Ningún archivo de templates/, src/ o data/ debe referenciar los assets legacy ni /monitoreo."""
    for base in ("templates", "src", "data"):
        for path in (REPO_ROOT / base).rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in (".html", ".py", ".yaml", ".yml", ".md"):
                continue
            content = path.read_text(encoding="utf-8")
            assert needle not in content, f"Referencia residual '{needle}' en {path}"
