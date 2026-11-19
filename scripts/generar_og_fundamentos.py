from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Dimensiones estándar Open Graph
WIDTH, HEIGHT = 1200, 630

# Ajustá esta ruta a la que indique el curso / PR #83
output_path = Path("static/img/og-fundamentos-programacion.webp")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Lienzo con gradiente horizontal limpio
img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
draw = ImageDraw.Draw(img)

for x in range(WIDTH):
    r = int(15 + (30 - 15) * (x / WIDTH))
    g = int(23 + (58 - 23) * (x / WIDTH))
    b = int(42 + (138 - 42) * (x / WIDTH))
    draw.line([(x, 0), (x, HEIGHT)], fill=(r, g, b))

# Marco y detalles geométricos sutiles
draw.rounded_rectangle(
    [48, 48, WIDTH - 48, HEIGHT - 48],
    radius=24,
    outline=(56, 189, 248),
    width=3,
)
draw.rectangle([96, 120, 290, 156], fill=(56, 189, 248))

# Tipografía (fallback seguro si no está DejaVuSans)
try:
    font_tag = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except OSError:
    font_tag = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

draw.text((112, 126), "CURSO · CAMPUS", fill=(15, 23, 42), font=font_tag)
draw.text((96, 205), "Fundamentos de la\nProgramación", fill=(248, 250, 252), font=font_title)
draw.text(
    (96, 365),
    "Lógica algorítmica, diseño estructurado\ny buenas prácticas de desarrollo",
    fill=(186, 230, 253),
    font=font_sub,
)
draw.text(
    (96, 505),
    "Tecnicatura Superior en Ciencia de Datos e IA",
    fill=(148, 163, 184),
    font=font_sub,
)

# Guardar en formato WebP con calidad alta
img.save(output_path, format="WEBP", quality=90, method=6)
print("Generada:", output_path.resolve())
