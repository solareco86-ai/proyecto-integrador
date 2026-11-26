"""Pruebas de scripts/optimizar_imagenes.py.

Trabajan sobre imágenes generadas en una carpeta temporal: nunca tocan static/.
"""

from pathlib import Path

import pytest
from PIL import Image

from scripts import optimizar_imagenes as opt


def _foto(ruta: Path, ancho: int, alto: int) -> Path:
    """Imagen con mucho detalle (ruido), que en PNG pesa bastante más que en WebP."""
    Image.effect_noise((ancho, alto), 60).convert("RGB").save(ruta)
    return ruta


def _plana(ruta: Path) -> Path:
    """Imagen de un solo color: en PNG pesa casi nada y el WebP no la achica."""
    Image.new("RGB", (8, 8), (20, 40, 60)).save(ruta)
    return ruta


@pytest.mark.parametrize(
    ("ancho", "alto", "ancho_max", "esperado"),
    [
        (800, 600, 1600, (800, 600)),  # ya entra: no se toca
        (3200, 1800, 1600, (1600, 900)),  # se achica a la mitad
        (1601, 1000, 1600, (1600, 999)),  # se redondea el alto
        (5000, 1, 1000, (1000, 1)),  # nunca queda en 0 px
    ],
)
def test_nuevo_tamano_conserva_la_proporcion(ancho: int, alto: int, ancho_max: int, esperado: tuple[int, int]) -> None:
    assert opt.nuevo_tamano(ancho, alto, ancho_max) == esperado


def test_nuevo_tamano_rechaza_un_ancho_maximo_invalido() -> None:
    with pytest.raises(ValueError):
        opt.nuevo_tamano(100, 100, 0)


def test_sin_aplicar_no_escribe_nada(tmp_path: Path) -> None:
    origen: Path = _foto(tmp_path / "foto.png", 400, 300)

    resultado = opt.procesar(origen, ancho_max=1600, calidad=85, aplicar=False)

    assert resultado.accion == "convertir"
    assert resultado.ahorro > 0
    assert not (tmp_path / "foto.webp").exists()


def test_con_aplicar_achica_y_convierte_a_webp(tmp_path: Path) -> None:
    origen: Path = _foto(tmp_path / "grande.png", 2000, 1000)

    resultado = opt.procesar(origen, ancho_max=1000, calidad=85, aplicar=True)

    assert resultado.accion == "convertir"
    assert resultado.motivo == "achicada y convertida"
    with Image.open(tmp_path / "grande.webp") as webp:
        assert webp.format == "WEBP"
        assert webp.size == (1000, 500)
    assert origen.exists(), "el original no se borra"


def test_no_convierte_si_el_webp_pesa_mas(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    origen: Path = _plana(tmp_path / "plana.png")

    # Simula un WebP más pesado que el original, como pasa con algunos PNG de pocos colores.
    def webp_pesado(imagen: Image.Image, calidad: int) -> bytes:
        return b"x" * (origen.stat().st_size + 1)

    monkeypatch.setattr(opt, "codificar_webp", webp_pesado)

    resultado = opt.procesar(origen, ancho_max=1600, calidad=85, aplicar=True)

    assert resultado.accion == "omitir"
    assert resultado.motivo == "el WebP no pesa menos"
    assert not (tmp_path / "plana.webp").exists()


def test_no_pisa_un_webp_que_ya_existe(tmp_path: Path) -> None:
    origen: Path = _foto(tmp_path / "logo.png", 400, 300)
    (tmp_path / "logo.webp").write_bytes(b"version anterior")

    resultado = opt.procesar(origen, ancho_max=1600, calidad=85, aplicar=True)

    assert resultado.accion == "omitir"
    assert (tmp_path / "logo.webp").read_bytes() == b"version anterior"


def test_un_webp_de_buen_tamano_se_deja_como_esta(tmp_path: Path) -> None:
    origen: Path = tmp_path / "og.webp"
    Image.effect_noise((1200, 630), 60).convert("RGB").save(origen, format="WEBP")

    resultado = opt.procesar(origen, ancho_max=1600, calidad=85, aplicar=True)

    assert resultado.accion == "omitir"
    assert resultado.motivo == "ya es WebP y tiene buen tamaño"


def test_un_webp_demasiado_ancho_se_reemplaza_achicado(tmp_path: Path) -> None:
    origen: Path = tmp_path / "ancha.webp"
    Image.effect_noise((3200, 1600), 60).convert("RGB").save(origen, format="WEBP", quality=100)

    resultado = opt.procesar(origen, ancho_max=1600, calidad=80, aplicar=True)

    assert resultado.accion == "convertir"
    with Image.open(origen) as webp:
        assert webp.size == (1600, 800)


def test_conserva_la_transparencia(tmp_path: Path) -> None:
    origen: Path = tmp_path / "icono.png"
    con_alfa = Image.effect_noise((300, 300), 60).convert("RGBA")
    con_alfa.putalpha(128)
    con_alfa.save(origen)

    opt.procesar(origen, ancho_max=1600, calidad=85, aplicar=True)

    with Image.open(tmp_path / "icono.webp") as webp:
        assert webp.mode == "RGBA"


def test_buscar_imagenes_filtra_extensiones_y_excluidos(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    _plana(tmp_path / "a.png")
    _plana(tmp_path / "sub" / "b.jpg")
    _plana(tmp_path / "favicon.png")
    (tmp_path / "notas.txt").write_text("no es imagen", encoding="utf-8")

    encontradas = opt.buscar_imagenes([tmp_path, tmp_path / "a.png"])

    assert [p.name for p in encontradas] == ["a.png", "b.jpg"]


def test_buscar_referencias_encuentra_donde_se_usa_la_imagen(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    (tmp_path / "templates").mkdir()
    (tmp_path / "data" / "leccion.md").write_text("![x](/static/img/foto.png)", encoding="utf-8")
    (tmp_path / "templates" / "otra.html").write_text("<p>sin imagen</p>", encoding="utf-8")

    assert opt.buscar_referencias("foto.png", raiz=tmp_path) == [tmp_path / "data" / "leccion.md"]


def test_main_muestra_el_informe_con_el_ahorro(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _foto(tmp_path / "foto.png", 400, 300)
    Image.effect_noise((300, 200), 60).convert("RGB").save(tmp_path / "og.webp", format="WEBP")
    monkeypatch.setattr(opt, "RAIZ", tmp_path)

    assert opt.main([str(tmp_path)]) == 0

    salida: str = capsys.readouterr().out
    assert "CONVERTIR  foto.png  400×300" in salida
    assert "omitir     og.webp" in salida
    assert "2 imágenes revisadas. Se guardarían 1 en WebP" in salida
    assert "--aplicar" in salida
    assert not (tmp_path / "foto.webp").exists()


@pytest.mark.parametrize("argumentos", [["--calidad", "0"], ["--calidad", "101"], ["--ancho-max", "0"]])
def test_main_rechaza_parametros_invalidos(argumentos: list[str]) -> None:
    with pytest.raises(SystemExit):
        opt.main(argumentos)
