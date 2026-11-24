"""Ejecuta los ejemplos de código de la lección 2.2 (histogramas, Otsu y bordes) de PDI.

La lección es la fuente de verdad: los bloques ```python se extraen del Markdown y
se ejecutan tal como están escritos, sin copiarlos acá. En cada bloque se verifica:

- que corre sin errores sobre las imágenes de trabajo (`retina.jpg`, `monedas.png`
  y `texto.png`);
- que cada `print` muestra lo que documenta su comentario
  (por ejemplo, `print("Umbral de Otsu:", umbral)  # Umbral de Otsu: 107.0`);
- que cada imagen que guarda (`cv2.imwrite` o `savefig`) está publicada en
  `static/media/cursos/pdi/` (misma base, en `.webp`) y, si la genera OpenCV, con
  el mismo tamaño.

OpenCV, NumPy y Matplotlib no son dependencias del proyecto. Si no están instalados,
las pruebas se saltan e indican cómo instalarlos en un entorno aparte.
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
    / "cap-2-2-histogramas-umbralizacion-bordes-canny.md"
)
MEDIOS: Path = RAIZ / "static" / "media" / "cursos" / "pdi"
IMAGENES_DE_TRABAJO: list[str] = ["retina.jpg", "monedas.png", "texto.png"]
CANTIDAD_BLOQUES: int = 8

AYUDA_INSTALACION: str = (
    "OpenCV, NumPy y Matplotlib no están instalados, y no son dependencias del proyecto. "
    "Para correr los ejemplos de la lección 2.2, instalalos en un entorno aparte: "
    "python3 -m venv /tmp/venv-pdi && /tmp/venv-pdi/bin/pip install "
    "'opencv-python-headless>=4.10.0' 'numpy>=1.26.0' 'matplotlib>=3.9.0' "
    "-r requirements.txt -r requirements-dev.txt && /tmp/venv-pdi/bin/python -m pytest "
    "tests/test_guia_pdi_histogramas_ejemplos.py"
)

PATRON_BLOQUE: re.Pattern[str] = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)
PATRON_IMWRITE: re.Pattern[str] = re.compile(r'cv2\.imwrite\("([^"]+)"')
PATRON_SAVEFIG: re.Pattern[str] = re.compile(r'\.savefig\("([^"]+)"')
PATRON_TUPLA: re.Pattern[str] = re.compile(r"^\(\d+(?:, \d+)*\)")


def _bloques_de_la_leccion() -> list[str]:
    return PATRON_BLOQUE.findall(LECCION.read_text(encoding="utf-8"))


def _salidas_documentadas(codigo: str) -> list[str]:
    """Devuelve la salida esperada de cada `print`, tomada de su comentario.

    El comentario va en la misma línea: `print(...)  # salida`. Si es una tupla,
    como `# (600, 600)`, se espera que la salida termine en esa tupla.
    """
    esperadas: list[str] = []
    for linea in codigo.splitlines():
        if not linea.lstrip().startswith("print("):
            continue
        assert "  # " in linea, f"El print no documenta su salida: {linea.strip()}"
        comentario: str = linea.split("  # ", 1)[1].strip()
        tupla: re.Match[str] | None = PATRON_TUPLA.match(comentario)
        esperadas.append(tupla.group(0) if tupla else comentario)
    return esperadas


BLOQUES: list[str] = _bloques_de_la_leccion()


def _importar_librerias() -> ModuleType:
    pytest.importorskip("numpy", reason=AYUDA_INSTALACION)
    matplotlib: ModuleType = pytest.importorskip("matplotlib", reason=AYUDA_INSTALACION)
    matplotlib.use("Agg")  # sin ventana: las figuras solo se guardan
    return pytest.importorskip("cv2", reason=AYUDA_INSTALACION)


def test_la_leccion_tiene_los_bloques_y_las_imagenes_de_trabajo() -> None:
    assert len(BLOQUES) == CANTIDAD_BLOQUES
    for nombre in IMAGENES_DE_TRABAJO:
        assert (MEDIOS / nombre).is_file(), nombre


def test_cada_print_documenta_su_salida() -> None:
    for numero, codigo in enumerate(BLOQUES, start=1):
        assert _salidas_documentadas(codigo), f"El bloque {numero} no documenta ninguna salida"


@pytest.mark.parametrize("numero", range(1, len(BLOQUES) + 1), ids=lambda n: f"bloque-{n}")
def test_ejemplo_de_la_leccion_corre_y_coincide_con_lo_documentado(
    numero: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cv2: ModuleType = _importar_librerias()
    codigo: str = BLOQUES[numero - 1]
    esperadas: list[str] = _salidas_documentadas(codigo)

    for nombre in IMAGENES_DE_TRABAJO:
        shutil.copy(MEDIOS / nombre, tmp_path / nombre)
    monkeypatch.chdir(tmp_path)
    exec(compile(codigo, f"{LECCION.name} (bloque {numero})", "exec"), {"__name__": "__main__"})

    salidas: list[str] = capsys.readouterr().out.splitlines()
    assert len(salidas) == len(esperadas), salidas
    for salida, esperada in zip(salidas, esperadas, strict=True):
        if esperada.startswith("("):
            assert salida.endswith(esperada), f"{salida!r} no termina en {esperada!r}"
        else:
            assert salida == esperada

    for nombre in PATRON_IMWRITE.findall(codigo) + PATRON_SAVEFIG.findall(codigo):
        generada: Path = tmp_path / nombre
        assert generada.is_file(), nombre
        publicada: Path = MEDIOS / f"{Path(nombre).stem}.webp"
        assert publicada.is_file(), f"Falta la imagen publicada {publicada.relative_to(RAIZ)}"
        if nombre in PATRON_IMWRITE.findall(codigo):
            forma_generada: tuple[int, ...] = cv2.imread(str(generada)).shape
            forma_publicada: tuple[int, ...] = cv2.imread(str(publicada)).shape
            assert forma_generada == forma_publicada, f"{nombre}: {forma_generada} != {forma_publicada}"
