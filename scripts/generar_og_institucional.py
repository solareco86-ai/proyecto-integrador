from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Dimensiones estándar Open Graph (1.91:1)
WIDTH = 1200
HEIGHT = 630

output_path = Path("static/og-default.webp")
output_path.parent.mkdir(parents=True, exist_ok=True)

# 1. Crear lienzo con gradiente institucional (#0a192f -> #0f2744)
img = Image.new("RGB", (WIDTH, HEIGHT), (10, 25, 47))
draw = ImageDraw.Draw(img)

for x in range(WIDTH):
    factor = x / WIDTH
    r = int(10 + (17 - 10) * factor)
    g = int(25 + (44 - 25) * factor)
    b = int(47 + (80 - 47) * factor)
    draw.line([(x, 0), (x, HEIGHT)], fill=(r, g, b))

# 2. Marco decorativo institucional
draw.rounded_rectangle(
    [32, 32, WIDTH - 32, HEIGHT - 32],
    radius=24,
    outline=(30, 58, 99),
    width=2,
)

# Acento cian superior
draw.line([(56, 32), (360, 32)], fill=(56, 189, 248), width=4)

# 3. Cargar fuentes TrueType
font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_path_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

try:
    font_badge = ImageFont.truetype(font_path_bold, 18)
    font_brand = ImageFont.truetype(font_path_bold, 58)
    font_subbrand = ImageFont.truetype(font_path_bold, 28)
    font_tagline = ImageFont.truetype(font_path_bold, 22)
    font_careers = ImageFont.truetype(font_path_reg, 20)
    font_footer = ImageFont.truetype(font_path_bold, 19)
except OSError:
    font_badge = font_brand = font_subbrand = font_tagline = font_careers = font_footer = ImageFont.load_default()

# 4. Colocar el Logo del ISFT N° 199 en tarjeta contenedor con contraste óptimo
logo_src = Path("static/media/logo-isft199.webp")
if logo_src.exists():
    logo_orig = Image.open(logo_src).convert("RGBA")
    # Tarjeta blanca para el logo (fondo original del escudo)
    card_x0, card_y0, card_x1, card_y1 = 70, 110, 370, 470
    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=20,
        fill=(255, 255, 255),
        outline=(56, 189, 248),
        width=3,
    )

    # Redimensionar logo manteniendo proporción
    target_w = 230
    target_h = int(logo_orig.height * (target_w / logo_orig.width))
    logo_resized = logo_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Centrar logo dentro de la tarjeta
    logo_pos_x = card_x0 + (card_x1 - card_x0 - target_w) // 2
    logo_pos_y = card_y0 + (card_y1 - card_y0 - target_h) // 2
    img.paste(logo_resized, (logo_pos_x, logo_pos_y), mask=logo_resized)

# 5. Textos informativos e institucionales
text_x = 420

# Badge superior (DGCyE / Buenos Aires)
draw.rounded_rectangle([text_x, 80, text_x + 430, 114], radius=8, fill=(17, 34, 64))
draw.text(
    (text_x + 16, 88),
    "DGCyE · PROVINCIA DE BUENOS AIRES · REGIÓN 6",
    fill=(56, 189, 248),
    font=font_badge,
)

# Título y Nombre institucional
draw.text((text_x, 140), "ISFT N° 199", fill=(248, 250, 252), font=font_brand)
draw.text(
    (text_x, 215),
    "Instituto Superior de Formación Técnica",
    fill=(148, 163, 184),
    font=font_subbrand,
)

# Separador
draw.line([(text_x, 260), (text_x + 680, 260)], fill=(30, 58, 99), width=2)

# Propuesta de valor: 100% Pública y Gratuita
draw.rounded_rectangle([text_x, 280, text_x + 480, 320], radius=8, fill=(16, 185, 129))
draw.text(
    (text_x + 16, 289),
    "EDUCACIÓN SUPERIOR PÚBLICA Y GRATUITA",
    fill=(10, 25, 47),
    font=font_tagline,
)

# Carreras / Tecnicaturas
draw.text(
    (text_x, 345),
    "Tecnicaturas Superiores Oficiales de 3 Años (Validez Nacional):",
    fill=(226, 232, 240),
    font=font_tagline,
)
draw.text(
    (text_x, 385),
    "• Ciencia de Datos e IA   • Logística   • Higiene y Seguridad\n• Administración de Recursos Humanos   • Turismo   • Hotelería",
    fill=(148, 163, 184),
    font=font_careers,
)

# Footer bar dentro del gráfico
draw.line([(text_x, 480), (text_x + 680, 480)], fill=(30, 58, 99), width=1)
draw.text(
    (text_x, 505),
    "Sede: Maestra Celina Voena 1750, El Talar (Tigre)   |   Turno vespertino",
    fill=(148, 163, 184),
    font=font_footer,
)
draw.text(
    (text_x, 545),
    "Sitio Oficial: isftn199.com.ar",
    fill=(56, 189, 248),
    font=font_footer,
)

# 6. Guardar en formato WebP de alta fidelidad
img.save(output_path, format="WEBP", quality=80, method=6)
print(f"✅ Imagen Open Graph institucional generada con éxito en {output_path.resolve()}")
