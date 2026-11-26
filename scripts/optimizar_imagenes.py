"""Redimensiona las imágenes del sitio y las convierte a WebP.

Recorre las carpetas indicadas (por defecto, `static/`) y, para cada PNG, JPG o
WebP:

1. Si es más ancha que `--ancho-max`, la achica conservando la proporción.
2. La codifica en WebP con `--calidad`.
3. Solo la propone si el WebP pesa menos que el original: un PNG de pocos
   colores puede pesar menos que su versión WebP.

Por defecto **no escribe nada**: muestra el informe con lo que haría y cuánto se
ahorra. Con `--aplicar` guarda cada `.webp` al lado de su original; una imagen que
ya es WebP pero supera el ancho máximo se reemplaza por su versión achicada.
Los originales no se borran, porque antes hay que actualizar las referencias: el
informe lista en qué archivos de `templates/`, `data/` y `static/` aparece cada imagen.

Uso:
    python3 scripts/optimizar_imagenes.py                 # informe de static/
    python3 scripts/optimizar_imagenes.py static/img --ancho-max 1280
    python3 scripts/optimizar_imagenes.py static/img --aplicar
"""

import argparse
import io
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

RAIZ: Path = Path(__file__).resolve().parent.parent
EXTENSIONES: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp"})
# El favicon tiene que seguir en PNG: no todos los navegadores aceptan WebP ahí.
EXCLUIR_POR_DEFECTO: tuple[str, ...] = ("favicon", "node_modules")
CARPETAS_CON_REFERENCIAS: tuple[str, ...] = ("templates", "data", "static/css", "static/js")
SUFIJOS_CON_REFERENCIAS: frozenset[str] = frozenset({".html", ".md", ".yaml", ".yml", ".css", ".js", ".txt"})


@dataclass(frozen=True)
class Resultado:
    """Lo que el script decidió para una imagen."""

    origen: Path
    destino: Path
    ancho: int
    alto: int
    nuevo_ancho: int
    nuevo_alto: int
    bytes_antes: int
    bytes_despues: int
    accion: str  # "convertir" u "omitir"
    motivo: str

    @property
    def ahorro(self) -> int:
        return self.bytes_antes - self.bytes_despues if self.accion == "convertir" else 0


def nuevo_tamano(ancho: int, alto: int, ancho_max: int) -> tuple[int, int]:
    """Tamaño final: igual si entra en `ancho_max`; si no, achicado con la misma proporción."""
    if ancho_max <= 0:
        raise ValueError("ancho_max tiene que ser mayor que 0")
    if ancho <= ancho_max:
        return ancho, alto
    return ancho_max, max(1, round(alto * ancho_max / ancho))


def buscar_imagenes(rutas: Iterable[Path], excluir: Sequence[str] = EXCLUIR_POR_DEFECTO) -> list[Path]:
    """Imágenes a revisar, ordenadas y sin repetir. Acepta archivos y carpetas."""
    encontradas: set[Path] = set()
    for ruta in rutas:
        candidatas: Iterable[Path] = [ruta] if ruta.is_file() else ruta.rglob("*")
        for candidata in candidatas:
            if not candidata.is_file() or candidata.suffix.lower() not in EXTENSIONES:
                continue
            if any(patron in part for part in candidata.parts for patron in excluir):
                continue
            encontradas.add(candidata)
    return sorted(encontradas)


def codificar_webp(imagen: Image.Image, calidad: int) -> bytes:
    """Codifica en WebP en memoria. Conserva la transparencia si la imagen la tiene."""
    tiene_alfa: bool = imagen.mode in {"RGBA", "LA"} or (imagen.mode == "P" and "transparency" in imagen.info)
    modo: str = "RGBA" if tiene_alfa else "RGB"
    salida = io.BytesIO()
    imagen.convert(modo).save(salida, format="WEBP", quality=calidad, method=6)
    return salida.getvalue()


def procesar(origen: Path, ancho_max: int, calidad: int, aplicar: bool) -> Resultado:
    """Decide qué hacer con una imagen y, si `aplicar`, guarda el WebP."""
    destino: Path = origen.with_suffix(".webp")
    bytes_antes: int = origen.stat().st_size
    with Image.open(origen) as abierta:
        abierta.load()
        ancho, alto = abierta.size
        nuevo_ancho, nuevo_alto = nuevo_tamano(ancho, alto, ancho_max)
        es_webp: bool = origen.suffix.lower() == ".webp"

        if es_webp and (nuevo_ancho, nuevo_alto) == (ancho, alto):
            return Resultado(
                origen,
                destino,
                ancho,
                alto,
                ancho,
                alto,
                bytes_antes,
                bytes_antes,
                "omitir",
                "ya es WebP y tiene buen tamaño",
            )

        imagen: Image.Image = abierta
        if (nuevo_ancho, nuevo_alto) != (ancho, alto):
            imagen = abierta.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        datos: bytes = codificar_webp(imagen, calidad)

    if len(datos) >= bytes_antes:
        return Resultado(
            origen,
            destino,
            ancho,
            alto,
            nuevo_ancho,
            nuevo_alto,
            bytes_antes,
            len(datos),
            "omitir",
            "el WebP no pesa menos",
        )
    if destino.exists() and not es_webp:
        return Resultado(
            origen,
            destino,
            ancho,
            alto,
            nuevo_ancho,
            nuevo_alto,
            bytes_antes,
            len(datos),
            "omitir",
            f"ya existe {destino.name}",
        )
    if aplicar:
        destino.write_bytes(datos)
    motivo: str = "achicada y convertida" if (nuevo_ancho, nuevo_alto) != (ancho, alto) else "convertida"
    return Resultado(
        origen, destino, ancho, alto, nuevo_ancho, nuevo_alto, bytes_antes, len(datos), "convertir", motivo
    )


def buscar_referencias(nombre: str, raiz: Path | None = None) -> list[Path]:
    """Archivos de texto del sitio que mencionan `nombre` (por ejemplo, `slide_04.png`)."""
    raiz = raiz or RAIZ
    encontrados: list[Path] = []
    for carpeta in CARPETAS_CON_REFERENCIAS:
        base: Path = raiz / carpeta
        if not base.is_dir():
            continue
        for archivo in sorted(base.rglob("*")):
            if archivo.is_file() and archivo.suffix.lower() in SUFIJOS_CON_REFERENCIAS:
                if nombre in archivo.read_text(encoding="utf-8", errors="ignore"):
                    encontrados.append(archivo)
    return encontrados


def kb(cantidad: int) -> str:
    return f"{cantidad / 1024:,.0f} KB".replace(",", ".")


def informe(resultados: Sequence[Resultado], aplicar: bool, raiz: Path | None = None) -> str:
    """Texto del informe: una línea por imagen y el total ahorrado."""
    raiz = raiz or RAIZ
    lineas: list[str] = []
    for r in resultados:
        try:
            ruta: str = str(r.origen.relative_to(raiz))
        except ValueError:
            ruta = str(r.origen)
        tamano: str = f"{r.ancho}×{r.alto}"
        if (r.nuevo_ancho, r.nuevo_alto) != (r.ancho, r.alto):
            tamano += f" → {r.nuevo_ancho}×{r.nuevo_alto}"
        if r.accion == "convertir":
            lineas.append(f"CONVERTIR  {ruta}  {tamano}  {kb(r.bytes_antes)} → {kb(r.bytes_despues)}")
            referencias: list[Path] = buscar_referencias(r.origen.name, raiz)
            for ref in referencias:
                lineas.append(f"           usada en {ref.relative_to(raiz)}")
        else:
            lineas.append(f"omitir     {ruta}  {tamano}  {kb(r.bytes_antes)}  ({r.motivo})")
    convertidas: list[Resultado] = [r for r in resultados if r.accion == "convertir"]
    antes: int = sum(r.bytes_antes for r in convertidas)
    ahorro: int = sum(r.ahorro for r in convertidas)
    porcentaje: float = 100 * ahorro / antes if antes else 0.0
    verbo: str = "Se guardaron" if aplicar else "Se guardarían"
    lineas.append("")
    lineas.append(
        f"{len(resultados)} imágenes revisadas. {verbo} {len(convertidas)} en WebP: "
        f"{kb(antes)} → {kb(antes - ahorro)} (ahorro de {kb(ahorro)}, {porcentaje:.0f} %)."
    )
    if not aplicar and convertidas:
        lineas.append("Para escribir los archivos, volvé a correrlo con --aplicar.")
    return "\n".join(lineas)


def main(argumentos: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Redimensiona las imágenes del sitio y las convierte a WebP.")
    parser.add_argument(
        "rutas",
        nargs="*",
        type=Path,
        default=None,
        help="carpetas o archivos a revisar (por defecto, static/)",
    )
    parser.add_argument("--ancho-max", type=int, default=1600, help="ancho máximo en píxeles (por defecto, 1600)")
    parser.add_argument("--calidad", type=int, default=85, help="calidad WebP de 1 a 100 (por defecto, 85)")
    parser.add_argument("--aplicar", action="store_true", help="escribe los .webp; sin esto solo muestra el informe")
    args = parser.parse_args(argumentos)

    if not 1 <= args.calidad <= 100:
        parser.error("--calidad tiene que estar entre 1 y 100")
    if args.ancho_max <= 0:
        parser.error("--ancho-max tiene que ser mayor que 0")

    imagenes: list[Path] = buscar_imagenes(args.rutas or [RAIZ / "static"])
    resultados: list[Resultado] = [procesar(ruta, args.ancho_max, args.calidad, args.aplicar) for ruta in imagenes]
    print(informe(resultados, args.aplicar))
    return 0


if __name__ == "__main__":
    sys.exit(main())
