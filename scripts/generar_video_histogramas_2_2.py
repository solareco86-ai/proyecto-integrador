"""Genera el video «Histogramas, brillo y contraste» de la lección 2.2 del curso de PDI.

Es un video sin voz, con textos en pantalla y música de fondo. Cada escena muestra
una técnica sobre una imagen real y su histograma: qué es un histograma, brillo,
contraste, ecualización, CLAHE y umbral de Otsu.

Usa solo Pillow y ffmpeg. Las imágenes salen de `static/media/cursos/pdi/`: la
retina y las monedas de trabajo, y los resultados de la ecualización, CLAHE y Otsu
que ya publicó la lección, para que el video muestre exactamente lo mismo que el
texto. La música también se genera acá (acordes suaves sintetizados), así no
depende de ninguna pista con derechos de autor.

Uso (desde la raíz del repositorio):
    python3 scripts/generar_video_histogramas_2_2.py
"""

import math
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ: Path = Path(__file__).resolve().parent.parent
MEDIOS: Path = RAIZ / "static" / "media" / "cursos" / "pdi"
SALIDA_VIDEO: Path = MEDIOS / "video-histogramas-brillo-contraste.mp4"
SALIDA_PORTADA: Path = MEDIOS / "video-histogramas-brillo-contraste.webp"

ANCHO: int = 1280
ALTO: int = 720
FPS: int = 24
MUESTREO: int = 32000  # Hz del audio

FONDO: tuple[int, int, int] = (15, 23, 42)
PANEL: tuple[int, int, int] = (30, 41, 59)
TINTA: tuple[int, int, int] = (241, 245, 249)
TINTA_SUAVE: tuple[int, int, int] = (148, 163, 184)
ACENTO: tuple[int, int, int] = (56, 189, 248)
ROJO: tuple[int, int, int] = (248, 113, 113)

FUENTES: dict[str, list[str]] = {
    "titulo": [
        "/usr/share/fonts/google-noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "texto": ["/usr/share/fonts/google-noto/NotoSans-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "codigo": [
        "/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
}

Fuente = ImageFont.FreeTypeFont | ImageFont.ImageFont


def fuente(tipo: str, tamano: int) -> Fuente:
    for ruta in FUENTES[tipo]:
        if Path(ruta).is_file():
            return ImageFont.truetype(ruta, tamano)
    return ImageFont.load_default(tamano)


# ---------------------------------------------------------------- imágenes


def recortar_panel(ruta: Path, indice: int, cantidad: int) -> Image.Image:
    """Uno de los paneles de una imagen armada con hconcat (original | resultado | ...)."""
    with Image.open(ruta) as compuesta:
        ancho_panel: int = compuesta.width // cantidad
        return compuesta.convert("L").crop((indice * ancho_panel, 0, (indice + 1) * ancho_panel, compuesta.height))


def mascara_ojo(retina: Image.Image) -> Image.Image:
    """Píxeles del ojo: el fondo de la foto va de 0 a 15, el ojo empieza más arriba."""
    return binarizar(retina, 15)


def binarizar(imagen: Image.Image, umbral: float) -> Image.Image:
    """Blanco (255) donde el tono supera el umbral; negro (0) en el resto."""
    return imagen.point([255 if v > umbral else 0 for v in range(256)])


def ajustar(imagen: Image.Image, mascara: Image.Image, alfa: float, beta: float, centro: float) -> Image.Image:
    """Contraste (alfa) y brillo (beta) alrededor de `centro`, solo dentro de la máscara."""
    tabla: list[int] = [max(0, min(255, round(alfa * (v - centro) + centro + beta))) for v in range(256)]
    ajustada: Image.Image = imagen.point(tabla)
    return Image.composite(ajustada, imagen, mascara)


def histograma(imagen: Image.Image, mascara: Image.Image | None = None) -> list[int]:
    return imagen.histogram(mask=mascara)


# ---------------------------------------------------------------- dibujo


@dataclass(frozen=True)
class Caja:
    x: int
    y: int
    ancho: int
    alto: int


def dibujar_histograma(
    lienzo: Image.Image,
    caja: Caja,
    valores: list[int],
    tope: float,
    progreso: float = 1.0,
    umbral: float | None = None,
    titulo: str = "",
) -> None:
    """Histograma con eje de 0 a 255. `progreso` < 1 lo dibuja solo hasta ese tramo."""
    d = ImageDraw.Draw(lienzo)
    d.rounded_rectangle((caja.x, caja.y, caja.x + caja.ancho, caja.y + caja.alto), radius=12, fill=PANEL)
    margen: int = 24
    x0, x1 = caja.x + margen, caja.x + caja.ancho - margen
    y0, y1 = caja.y + margen + (26 if titulo else 0), caja.y + caja.alto - 40
    if titulo:
        d.text((x0, caja.y + 14), titulo, font=fuente("texto", 20), fill=TINTA_SUAVE)
    hasta: int = max(1, round(256 * progreso))
    puntos: list[tuple[float, float]] = [(x0, y1)]
    for nivel in range(hasta):
        x: float = x0 + (x1 - x0) * nivel / 255
        y: float = y1 - (y1 - y0) * min(1.0, valores[nivel] / tope)
        puntos.append((x, y))
    puntos.append((x0 + (x1 - x0) * (hasta - 1) / 255, y1))
    d.polygon(puntos, fill=(56, 189, 248, 255))
    d.line(puntos[1:-1], fill=TINTA, width=2)
    d.line((x0, y1, x1, y1), fill=TINTA_SUAVE, width=2)
    chica = fuente("texto", 18)
    for nivel, rotulo in ((0, "0 negro"), (128, "128"), (255, "255 blanco")):
        x = x0 + (x1 - x0) * nivel / 255
        ancho_txt: float = d.textlength(rotulo, font=chica)
        tx: float = min(max(x - ancho_txt / 2, x0), x1 - ancho_txt)
        d.text((tx, y1 + 8), rotulo, font=chica, fill=TINTA_SUAVE)
    if umbral is not None:
        xu: float = x0 + (x1 - x0) * umbral / 255
        for y in range(round(y0), round(y1), 14):
            d.line((xu, y, xu, min(y + 8, y1)), fill=ROJO, width=3)
        d.text((xu + 8, y0), f"umbral {round(umbral)}", font=fuente("titulo", 20), fill=ROJO)


def pegar(lienzo: Image.Image, imagen: Image.Image, caja: Caja, rotulo: str = "") -> None:
    """Pega la imagen centrada en la caja, sin deformarla, con un rótulo debajo."""
    copia: Image.Image = imagen.convert("RGB")
    alto_disp: int = caja.alto - (34 if rotulo else 0)
    copia.thumbnail((caja.ancho, alto_disp), Image.Resampling.LANCZOS)
    x: int = caja.x + (caja.ancho - copia.width) // 2
    lienzo.paste(copia, (x, caja.y + (alto_disp - copia.height) // 2))
    if rotulo:
        d = ImageDraw.Draw(lienzo)
        f = fuente("titulo", 22)
        d.text(
            (caja.x + (caja.ancho - d.textlength(rotulo, font=f)) / 2, caja.y + alto_disp + 6),
            rotulo,
            font=f,
            fill=TINTA,
        )


def partir_lineas(texto: str, f: Fuente, ancho: int, d: ImageDraw.ImageDraw) -> list[str]:
    lineas: list[str] = []
    actual: str = ""
    for palabra in texto.split():
        prueba: str = f"{actual} {palabra}".strip()
        if d.textlength(prueba, font=f) <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def leyenda(lienzo: Image.Image, titulo: str, texto: str, codigo: str = "", opacidad: float = 1.0) -> None:
    """Banda inferior: el nombre de la técnica, la explicación y, si hay, la línea de código."""
    d = ImageDraw.Draw(lienzo)
    alto_banda: int = 170
    d.rectangle((0, ALTO - alto_banda, ANCHO, ALTO), fill=(2, 6, 23))
    d.rectangle((0, ALTO - alto_banda, 8, ALTO), fill=ACENTO)
    d.text((40, ALTO - alto_banda + 16), titulo, font=fuente("titulo", 30), fill=ACENTO)
    cuerpo = fuente("texto", 25)
    color: tuple[int, int, int] = tuple(
        round(c * opacidad + f * (1 - opacidad)) for c, f in zip(TINTA, (2, 6, 23), strict=True)
    )  # type: ignore[assignment]
    y: int = ALTO - alto_banda + 60
    for linea in partir_lineas(texto, cuerpo, ANCHO - 80, d)[:2]:
        d.text((40, y), linea, font=cuerpo, fill=color)
        y += 34
    if codigo:
        f = fuente("codigo", 21)
        ancho_codigo: float = d.textlength(codigo, font=f)
        d.rounded_rectangle((ANCHO - ancho_codigo - 64, 24, ANCHO - 24, 66), radius=8, fill=(2, 6, 23))
        d.text((ANCHO - ancho_codigo - 44, 32), codigo, font=f, fill=(190, 242, 100))


def insignia(lienzo: Image.Image, texto: str, x: int, y: int) -> None:
    d = ImageDraw.Draw(lienzo)
    f = fuente("titulo", 28)
    ancho: float = d.textlength(texto, font=f)
    d.rounded_rectangle((x, y, x + ancho + 32, y + 48), radius=24, fill=ACENTO)
    d.text((x + 16, y + 6), texto, font=f, fill=FONDO)


def lienzo_vacio() -> Image.Image:
    return Image.new("RGB", (ANCHO, ALTO), FONDO)


def suave(t: float) -> float:
    """Curva 0→1 sin saltos (para animaciones)."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def texto_en(tiempo: float, tramos: list[tuple[float, str]]) -> tuple[str, float]:
    """Texto que corresponde a `tiempo` y su opacidad (aparece en 0,4 s)."""
    actual: tuple[float, str] = tramos[0]
    for tramo in tramos:
        if tiempo >= tramo[0]:
            actual = tramo
    return actual[1], suave((tiempo - actual[0]) / 0.4)


# ---------------------------------------------------------------- escenas


@dataclass(frozen=True)
class Escena:
    duracion: float
    cuadro: Callable[[float], Image.Image]


def construir_escenas() -> list[Escena]:
    with Image.open(MEDIOS / "retina.jpg") as abierta:
        retina: Image.Image = abierta.convert("L")
    with Image.open(MEDIOS / "monedas.png") as abierta:
        monedas: Image.Image = abierta.convert("L")
    ojo: Image.Image = mascara_ojo(retina)
    hist_retina: list[int] = histograma(retina, ojo)
    tope_retina: float = max(hist_retina) * 1.15
    centro: float = sum(n * v for n, v in enumerate(hist_retina)) / sum(hist_retina)

    original_eq: Image.Image = recortar_panel(MEDIOS / "retina-ecualizada.webp", 0, 2)
    ecualizada: Image.Image = recortar_panel(MEDIOS / "retina-ecualizada.webp", 1, 2)
    global_eq: Image.Image = recortar_panel(MEDIOS / "retina-clahe.webp", 1, 3)
    clahe: Image.Image = recortar_panel(MEDIOS / "retina-clahe.webp", 2, 3)
    otsu: Image.Image = recortar_panel(MEDIOS / "monedas-umbral.webp", 2, 3)
    hist_monedas: list[int] = histograma(monedas)

    izquierda = Caja(40, 40, 520, 480)
    derecha = Caja(600, 84, 640, 436)

    def titulo(t: float) -> Image.Image:
        lienzo = lienzo_vacio()
        d = ImageDraw.Draw(lienzo)
        d.text((80, 200), "Histogramas, brillo y contraste", font=fuente("titulo", 64), fill=TINTA)
        d.text(
            (80, 300),
            "Técnicas de Procesamiento Digital de Imágenes · Lección 2.2",
            font=fuente("texto", 30),
            fill=TINTA_SUAVE,
        )
        d.rectangle((80, 370, 80 + 400 * suave(t / 1.5), 376), fill=ACENTO)
        d.text((80, 410), "ISFT N° 199 · Ciencia de Datos e IA", font=fuente("texto", 26), fill=TINTA_SUAVE)
        return lienzo

    def que_es(t: float) -> Image.Image:
        lienzo = lienzo_vacio()
        pegar(lienzo, retina, izquierda, "Retina (foto real)")
        dibujar_histograma(
            lienzo,
            derecha,
            hist_retina,
            tope_retina,
            progreso=suave(t / 4),
            titulo="Cantidad de píxeles de cada tono (solo el ojo)",
        )
        texto, op = texto_en(
            t,
            [
                (0, "Cuenta cuántos píxeles hay de cada tono de gris, del 0 (negro) al 255 (blanco)."),
                (5.5, "En esta retina casi todos los tonos están amontonados en el medio: por eso se ve apagada."),
            ],
        )
        leyenda(lienzo, "¿Qué es un histograma?", texto, "cv2.calcHist(...)", op)
        return lienzo

    def brillo(t: float) -> Image.Image:
        beta: float = 75 * math.sin(2 * math.pi * max(0.0, t - 1) / 11)
        ajustada = ajustar(retina, ojo, 1.0, beta, centro)
        lienzo = lienzo_vacio()
        pegar(lienzo, ajustada, izquierda)
        dibujar_histograma(lienzo, derecha, histograma(ajustada, ojo), tope_retina, titulo="Histograma del ojo")
        insignia(lienzo, f"brillo {round(beta):+d}", 60, 50)
        texto, op = texto_en(
            t,
            [
                (0, "Subir el brillo suma el mismo valor a todos los píxeles; bajarlo, lo resta."),
                (6, "El histograma se corre entero hacia un lado, pero no cambia de forma: el contraste sigue igual."),
            ],
        )
        leyenda(lienzo, "Brillo", texto, "cv2.convertScaleAbs(img, alpha=1, beta=brillo)", op)
        return lienzo

    def contraste(t: float) -> Image.Image:
        fase: float = suave((t - 1) / 5) if t < 8 else 1 - suave((t - 9) / 4)
        alfa: float = 1 + 1.6 * fase
        ajustada = ajustar(retina, ojo, alfa, 0, centro)
        lienzo = lienzo_vacio()
        pegar(lienzo, ajustada, izquierda)
        dibujar_histograma(lienzo, derecha, histograma(ajustada, ojo), tope_retina, titulo="Histograma del ojo")
        insignia(lienzo, f"contraste ×{alfa:.1f}", 60, 50)
        texto, op = texto_en(
            t,
            [
                (
                    0,
                    "Subir el contraste multiplica la distancia de cada tono al medio: los oscuros se oscurecen y los claros se aclaran.",
                ),
                (
                    5,
                    "El histograma se estira. Si se estira de más, los tonos se amontonan en 0 y 255 y se pierde detalle.",
                ),
            ],
        )
        leyenda(lienzo, "Contraste", texto, "cv2.convertScaleAbs(img, alpha=contraste)", op)
        return lienzo

    def comparar(
        a: Image.Image,
        b: Image.Image,
        rotulo_a: str,
        rotulo_b: str,
        titulo_esc: str,
        tramos: list[tuple[float, str]],
        codigo: str,
    ) -> Callable[[float], Image.Image]:
        def cuadro(t: float) -> Image.Image:
            lienzo = lienzo_vacio()
            mezcla: float = suave((t - 1.2) / 1.2)
            pegar(lienzo, a, Caja(40, 90, 380, 400), rotulo_a)
            pegar(lienzo, Image.blend(a, b, mezcla), Caja(860, 90, 380, 400), rotulo_b)
            hist_a = histograma(a, mascara_ojo(original_eq))
            hist_b = histograma(b, mascara_ojo(original_eq))
            tope: float = max(max(hist_a), max(hist_b)) * 1.1
            dibujar_histograma(lienzo, Caja(440, 84, 400, 222), hist_a, tope, titulo=f"Antes: {rotulo_a}")
            dibujar_histograma(
                lienzo, Caja(440, 318, 400, 222), hist_b, tope, progreso=mezcla, titulo=f"Después: {rotulo_b}"
            )
            texto, op = texto_en(t, tramos)
            leyenda(lienzo, titulo_esc, texto, codigo, op)
            return lienzo

        return cuadro

    ecualizar = comparar(
        original_eq,
        ecualizada,
        "Original",
        "Ecualizada",
        "Ecualización del histograma",
        [
            (0, "Reparte los tonos para que ocupen todo el rango, de 0 a 255: la imagen gana contraste sola."),
            (6, "Los vasos se ven mucho más. Pero el fondo negro se vuelve gris y la zona clara del nervio se quema."),
        ],
        "cv2.equalizeHist(img)",
    )
    adaptativa = comparar(
        global_eq,
        clahe,
        "Ecualización global",
        "CLAHE",
        "CLAHE: ecualizar por zonas",
        [
            (0, "CLAHE divide la imagen en zonas, ecualiza cada una y limita cuánto puede estirar el contraste."),
            (5.5, "El fondo sigue negro y la zona del nervio conserva su detalle."),
        ],
        "cv2.createCLAHE(clipLimit=2.0).apply(img)",
    )

    def umbral_otsu(t: float) -> Image.Image:
        lienzo = lienzo_vacio()
        mover: float = suave((t - 1.5) / 3)
        umbral: float = 20 + (107 - 20) * mover
        actual: Image.Image = binarizar(monedas, umbral)
        if t > 5:
            actual = Image.blend(actual, otsu, suave((t - 5) / 0.8))
        pegar(lienzo, monedas, Caja(30, 84, 340, 300), "Monedas (foto real)")
        pegar(lienzo, actual, Caja(390, 84, 340, 300), "Blanco: más claro que el umbral")
        dibujar_histograma(
            lienzo,
            Caja(760, 84, 490, 436),
            hist_monedas,
            max(hist_monedas) * 1.15,
            umbral=umbral,
            titulo="Histograma de las monedas",
        )
        texto, op = texto_en(
            t,
            [
                (0, "El histograma también sirve para separar los objetos del fondo con un umbral."),
                (
                    5,
                    "Otsu prueba los 256 umbrales y elige el que mejor separa los dos grupos de tonos. Acá eligió 107.",
                ),
            ],
        )
        leyenda(
            lienzo,
            "Umbral automático de Otsu",
            texto,
            "cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)",
            op,
        )
        return lienzo

    def cierre(t: float) -> Image.Image:
        lienzo = lienzo_vacio()
        d = ImageDraw.Draw(lienzo)
        d.text((80, 90), "En resumen", font=fuente("titulo", 52), fill=TINTA)
        filas: list[tuple[str, str]] = [
            ("Brillo", "corre el histograma"),
            ("Contraste", "lo estira"),
            ("Ecualización", "lo reparte en todo el rango"),
            ("CLAHE", "lo reparte por zonas, con límite"),
            ("Otsu", "lo corta en dos, solo"),
        ]
        for i, (tecnica, efecto) in enumerate(filas):
            op: float = suave((t - 0.4 - i * 0.5) / 0.4)
            if op <= 0:
                continue
            y: int = 190 + i * 62
            color = tuple(round(c * op + f * (1 - op)) for c, f in zip(ACENTO, FONDO, strict=True))
            d.text((80, y), tecnica, font=fuente("titulo", 34), fill=color)  # type: ignore[arg-type]
            color = tuple(round(c * op + f * (1 - op)) for c, f in zip(TINTA, FONDO, strict=True))
            d.text((380, y), efecto, font=fuente("texto", 34), fill=color)  # type: ignore[arg-type]
        d.text(
            (80, 540),
            "El código de cada paso está en la lección 2.2 del campus.",
            font=fuente("texto", 28),
            fill=TINTA_SUAVE,
        )
        return lienzo

    return [
        Escena(5, titulo),
        Escena(12, que_es),
        Escena(13, brillo),
        Escena(14, contraste),
        Escena(13, ecualizar),
        Escena(11, adaptativa),
        Escena(13, umbral_otsu),
        Escena(8, cierre),
    ]


def oscurecer(cuadro: Image.Image, t: float, duracion: float) -> Image.Image:
    """Fundido a negro de 0,35 s al entrar y al salir de cada escena."""
    nivel: float = min(1.0, t / 0.35, (duracion - t) / 0.35)
    if nivel >= 1:
        return cuadro
    return Image.blend(Image.new("RGB", cuadro.size, FONDO), cuadro, max(0.0, nivel))


# ---------------------------------------------------------------- música


ACORDES: list[list[float]] = [
    [220.00, 261.63, 329.63],  # La menor
    [174.61, 220.00, 261.63],  # Fa mayor
    [261.63, 329.63, 392.00],  # Do mayor
    [196.00, 246.94, 293.66],  # Sol mayor
]


def musica(segundos: float, muestreo: int = MUESTREO) -> list[float]:
    """Acordes suaves en loop (La m, Fa, Do, Sol), 4 s cada uno, con un arpegio leve."""
    total: int = round(segundos * muestreo)
    dur_acorde: float = 4.0
    muestras: list[float] = [0.0] * total
    for i in range(total):
        t: float = i / muestreo
        n: int = int(t // dur_acorde)
        local: float = t - n * dur_acorde
        acorde: list[float] = ACORDES[n % len(ACORDES)]
        previo: list[float] = ACORDES[(n - 1) % len(ACORDES)]
        entrada: float = min(1.0, local / 1.2)  # ataque lento, se encadena con el acorde anterior
        valor: float = 0.0
        for frecuencia in acorde:
            valor += entrada * (
                math.sin(2 * math.pi * frecuencia * t) + 0.5 * math.sin(2 * math.pi * frecuencia * 1.003 * t)
            )
        if n > 0:
            for frecuencia in previo:
                valor += (1 - entrada) * (
                    math.sin(2 * math.pi * frecuencia * t) + 0.5 * math.sin(2 * math.pi * frecuencia * 1.003 * t)
                )
        valor *= 0.06
        valor += 0.10 * math.sin(2 * math.pi * acorde[0] / 2 * t)  # bajo
        paso: int = int(local // 0.5)  # arpegio: una nota cada medio segundo
        nota: float = acorde[paso % 3] * 2
        desde_nota: float = local - paso * 0.5
        valor += 0.06 * math.exp(-desde_nota * 5) * math.sin(2 * math.pi * nota * t)
        muestras[i] = valor
    fundido: int = 2 * muestreo
    for i in range(min(fundido, total)):
        muestras[i] *= i / fundido
        muestras[total - 1 - i] *= i / fundido
    pico: float = max(abs(m) for m in muestras) or 1.0
    return [0.3 * m / pico for m in muestras]


def guardar_wav(muestras: list[float], ruta: Path, muestreo: int = MUESTREO) -> None:
    with wave.open(str(ruta), "wb") as salida:
        salida.setnchannels(1)
        salida.setsampwidth(2)
        salida.setframerate(muestreo)
        salida.writeframes(b"".join(struct.pack("<h", round(m * 32767)) for m in muestras))


# ---------------------------------------------------------------- armado


def main() -> int:
    ffmpeg: str | None = shutil.which("ffmpeg")
    if ffmpeg is None:
        print("Falta ffmpeg: instalalo (por ejemplo, sudo dnf install ffmpeg) y volvé a correr el script.")
        return 1
    escenas: list[Escena] = construir_escenas()
    duracion: float = sum(e.duracion for e in escenas)

    with tempfile.TemporaryDirectory() as carpeta:
        audio: Path = Path(carpeta) / "musica.wav"
        print(f"Generando {duracion:.0f} s de música...")
        guardar_wav(musica(duracion), audio)

        comando: list[str] = [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ANCHO}x{ALTO}", "-r", str(FPS), "-i", "-",
            "-i", str(audio),
            "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart",
            str(SALIDA_VIDEO),
        ]  # fmt: skip
        print("Dibujando los cuadros y codificando el video...")
        proceso = subprocess.Popen(comando, stdin=subprocess.PIPE)
        assert proceso.stdin is not None
        portada: Image.Image | None = None
        for numero, escena in enumerate(escenas):
            for cuadro_n in range(round(escena.duracion * FPS)):
                t: float = cuadro_n / FPS
                cuadro: Image.Image = oscurecer(escena.cuadro(t), t, escena.duracion)
                if numero == 4 and cuadro_n == round(9 * FPS):  # ecualización ya aplicada: buena portada
                    portada = cuadro
                proceso.stdin.write(cuadro.tobytes())
        proceso.stdin.close()
        if proceso.wait() != 0:
            print("ffmpeg terminó con error.")
            return 1

    if portada is not None:
        portada.save(SALIDA_PORTADA, format="WEBP", quality=80)
    print(f"Listo: {SALIDA_VIDEO.relative_to(RAIZ)} ({SALIDA_VIDEO.stat().st_size // 1024} KB, {duracion:.0f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
