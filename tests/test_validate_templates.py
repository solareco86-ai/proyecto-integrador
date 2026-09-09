"""Tests del validador estático de templates HTML (reglas R1 y R2)."""

from pathlib import Path

from scripts.validate_templates import validate_template_file


def _escribir(tmp_path: Path, contenido: str, nombre: str = "plantilla.html") -> Path:
    archivo = tmp_path / nombre
    archivo.write_text(contenido, encoding="utf-8")
    return archivo


def test_r1_detecta_jinja_en_atributo_style(tmp_path: Path) -> None:
    contenido = (
        "<div class=\"x\">\n  <span style=\"{{ 'display: none' if not loop.first else '' }}\">ok</span>\n</div>\n"
    )
    archivo = _escribir(tmp_path, contenido)

    errores = validate_template_file(archivo)

    assert len(errores) == 1
    assert str(archivo) in errores[0]
    assert ":2:" in errores[0]
    assert "style" in errores[0].lower()


def test_template_limpio_sin_errores(tmp_path: Path) -> None:
    contenido = (
        "<div class=\"panel {{ 'is-active' if loop.first else '' }}\">\n"
        "<style>\n.panel { display: block; }\n</style>\n"
        "</div>\n"
    )
    archivo = _escribir(tmp_path, contenido)

    assert validate_template_file(archivo) == []


def test_r2_detecta_llave_sin_cerrar_en_style(tmp_path: Path) -> None:
    contenido = "<style>\n.a { color: red;\n</style>\n"
    archivo = _escribir(tmp_path, contenido)

    errores = validate_template_file(archivo)

    assert len(errores) == 1
    assert ":1:" in errores[0]
    assert "style" in errores[0].lower()


def test_r2_tolera_css_legitimo_sin_falsos_positivos(tmp_path: Path) -> None:
    contenido = (
        '<div style="width: 33%;">\n'
        "<style>\n"
        ":root { --dm-bg: #000; }\n"
        "@media (max-width: 600px) { .a { color: red; } }\n"
        '.x::before { content: "{"; }\n'
        "</style>\n"
        "</div>\n"
    )
    archivo = _escribir(tmp_path, contenido)

    assert validate_template_file(archivo) == []


def test_r1_permite_jinja_en_custom_property(tmp_path: Path) -> None:
    contenido = '<nav class="c-home-dock" style="--dock-columns: {{ links|length }};">\n</nav>\n'
    archivo = _escribir(tmp_path, contenido)

    assert validate_template_file(archivo) == []


def test_r1_detecta_jinja_no_custom_property_en_style(tmp_path: Path) -> None:
    contenido = '<div style="color: {{ color }};"></div>\n'
    archivo = _escribir(tmp_path, contenido)

    errores = validate_template_file(archivo)

    assert len(errores) == 1
    assert ":1:" in errores[0]
    assert "style" in errores[0].lower()
