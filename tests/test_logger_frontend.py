"""Tests unitarios del módulo de logging con gating por entorno (logger.js)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOGGER_JS = REPO_ROOT / "static/js/modules/logger.js"


def _read_logger() -> str:
    return LOGGER_JS.read_text(encoding="utf-8")


def test_logger_expone_niveles() -> None:
    """El logger debe exportar los cuatro niveles de logging."""
    contenido = _read_logger()
    for nivel in ("debug", "info", "warn", "error"):
        assert f"export const {nivel}" in contenido


def test_logger_gating_debug_info() -> None:
    """debug e info deben silenciarse en producción (gate por APP_CONFIG.debug)."""
    contenido = _read_logger()
    assert "APP_CONFIG?.debug === true" in contenido
    assert "isDebugEnabled()" in contenido
    assert "console.debug(...args)" in contenido
    assert "console.info(...args)" in contenido


def test_logger_warn_error_siempre() -> None:
    """warn y error deben emitir siempre (señal de diagnóstico no silenciable)."""
    contenido = _read_logger()
    assert "console.warn(...args)" in contenido
    assert "console.error(...args)" in contenido
