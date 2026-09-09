"""Tests del generador del partial de CSS crítico (build_critical_css)."""

from pathlib import Path

from scripts.build_critical_css import build_critical_css

RAIZ = Path(__file__).resolve().parent.parent
PARTIAL = RAIZ / "templates" / "partials" / "critical_css.html"
CRITICAL = RAIZ / "static" / "css" / "src" / "critical.css"


def test_b1_genera_wrapper_style() -> None:
    contenido = build_critical_css(RAIZ)

    assert contenido.startswith("<style>\n")
    assert contenido.rstrip().endswith("</style>")
    assert ":root" in contenido


def test_b2_partial_autocontenido_sin_import() -> None:
    contenido = build_critical_css(RAIZ)

    assert "@import" not in contenido
    assert "--dm-bg-0:" in contenido


def test_b3_build_idempotente() -> None:
    assert build_critical_css(RAIZ) == build_critical_css(RAIZ)


def test_b4_sincronizado_con_partial_commiteado() -> None:
    assert build_critical_css(RAIZ) == PARTIAL.read_text(encoding="utf-8")


def test_b5_critical_no_define_root_propio() -> None:
    fuente = CRITICAL.read_text(encoding="utf-8")

    assert ":root" not in fuente
