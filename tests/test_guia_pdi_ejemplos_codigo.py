"""Ejecuta los ejemplos de código de la lección 1.3 (transformaciones geométricas) de PDI.

La lección es la fuente de verdad: los bloques ```python se extraen del Markdown y
se ejecutan tal como están escritos, sin copiarlos acá. En cada bloque se verifica:

- que corre sin errores sobre la imagen de trabajo `cafe.png`;
- que cada `print` muestra lo que documenta su comentario (por ejemplo,
  `print("Reducida:", reducida.shape)  # (200, 300, 3)`);
- que cada imagen guardada con `cv2.imwrite` tiene el mismo tamaño que la imagen
  de resultado publicada en `static/media/cursos/pdi/` (misma base, en `.webp`).

OpenCV y NumPy no son dependencias del proyecto. Si no están instalados, las pruebas
se saltan e indican cómo instalarlos en un entorno aparte.
"""

import re
import shutil
from pathlib import Path
from types import ModuleType

import pytest

RAIZ: Path = Path(__file__).resolve().parent.parent
LECCION: Path = (
    RAIZ
    / "data"
    / "core"
    / "cursos"
    / "procesamiento-imagenes-python-opencv"
    / "lecciones"
    / "cap-1-3-transformaciones-geometricas-operaciones.md"
)
MEDIOS: Path = RAIZ / "static" / "media" / "cursos" / "pdi"
IMAGEN_TRABAJO: Path = MEDIOS / "cafe.png"
CANTIDAD_BLOQUES: int = 9

AYUDA_INSTALACION: str = (
    "OpenCV y NumPy no están instalados, y no son dependencias del proyecto. Para correr "
    "la comprobación de los ejemplos de la lección 1.3, instalalos en un entorno aparte: "
    "python3 -m venv /tmp/venv-pdi && /tmp/venv-pdi/bin/pip install "
    "'opencv-python-headless>=4.10.0' 'numpy>=1.26.0' "
    "-r requirements.txt -r requirements-dev.txt && /tmp/venv-pdi/bin/python -m pytest "
    "tests/test_guia_pdi_ejemplos_codigo.py"
)

PATRON_BLOQUE: re.Pattern[str] = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)
PATRON_IMWRITE: re.Pattern[str] = re.compile(r'cv2\.imwrite\("([^"]+)"')
PATRON_TUPLA: re.Pattern[str] = re.compile(r"^\(\d+(?:, \d+)*\)")


def _bloques_de_la_leccion() -> list[str]:
    return PATRON_BLOQUE.findall(LECCION.read_text(encoding="utf-8"))


def _salidas_documentadas(codigo: str) -> list[str]:
    """Devuelve la salida esperada de cada `print`, tomada de su comentario.

    El comentario puede estar en la misma línea (`print(...)  # salida`) o en la
    línea siguiente (`# salida`). Si empieza con una tupla, como
    `# (600, 400, 3): el ancho y el alto se intercambian`, se espera solo la tupla.
    """
    lineas: list[str] = codigo.splitlines()
    esperadas: list[str] = []
    for indice, linea in enumerate(lineas):
        if not linea.lstrip().startswith("print("):
            continue
        comentario: str = ""
        if "  # " in linea:
            comentario = linea.split("  # ", 1)[1]
        elif indice + 1 < len(lineas) and lineas[indice + 1].lstrip().startswith("# "):
            comentario = lineas[indice + 1].lstrip()[2:]
        assert comentario, f"El print no documenta su salida: {linea.strip()}"
        tupla: re.Match[str] | None = PATRON_TUPLA.match(comentario)
        esperadas.append(tupla.group(0) if tupla else comentario.strip())
    return esperadas


BLOQUES: list[str] = _bloques_de_la_leccion()


def _importar_opencv() -> ModuleType:
    pytest.importorskip("numpy", reason=AYUDA_INSTALACION)
    return pytest.importorskip("cv2", reason=AYUDA_INSTALACION)


def test_la_leccion_tiene_los_bloques_esperados() -> None:
    assert len(BLOQUES) == CANTIDAD_BLOQUES
    assert IMAGEN_TRABAJO.is_file()


@pytest.mark.parametrize("numero", range(1, len(BLOQUES) + 1), ids=lambda n: f"bloque-{n}")
def test_ejemplo_de_la_leccion_corre_y_coincide_con_lo_documentado(
    numero: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cv2: ModuleType = _importar_opencv()
    codigo: str = BLOQUES[numero - 1]
    esperadas: list[str] = _salidas_documentadas(codigo)
    assert esperadas, "El bloque no documenta ninguna salida para comprobar"

    shutil.copy(IMAGEN_TRABAJO, tmp_path / "cafe.png")
    monkeypatch.chdir(tmp_path)
    exec(compile(codigo, f"{LECCION.name} (bloque {numero})", "exec"), {"__name__": "__main__"})

    salidas: list[str] = capsys.readouterr().out.splitlines()
    assert len(salidas) == len(esperadas), salidas
    for salida, esperada in zip(salidas, esperadas, strict=True):
        if esperada.startswith("("):
            assert salida.endswith(esperada), f"{salida!r} no termina en {esperada!r}"
        else:
            assert salida == esperada

    for nombre in PATRON_IMWRITE.findall(codigo):
        generada: Path = tmp_path / nombre
        assert generada.is_file(), nombre
        publicada: Path = MEDIOS / f"{Path(nombre).stem}.webp"
        assert publicada.is_file(), f"Falta la imagen publicada {publicada.relative_to(RAIZ)}"
        forma_generada: tuple[int, ...] = cv2.imread(str(generada)).shape
        forma_publicada: tuple[int, ...] = cv2.imread(str(publicada)).shape
        assert forma_generada == forma_publicada, f"{nombre}: {forma_generada} != {forma_publicada}"
