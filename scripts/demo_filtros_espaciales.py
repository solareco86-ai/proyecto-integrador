from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

out_dir = Path("static/img/cap_2_1")
out_dir.mkdir(parents=True, exist_ok=True)

# 1. Crear una imagen sintética limpia con formas geométricas, gradientes y texto/bordes
h, w = 360, 640
x = np.linspace(0, 1, w, dtype=np.float32)
y = np.linspace(0, 1, h, dtype=np.float32)
xx, yy = np.meshgrid(x, y)

base = np.zeros((h, w, 3), dtype=np.uint8)
base[..., 0] = np.clip(40 + 140 * xx, 0, 255).astype(np.uint8)
base[..., 1] = np.clip(60 + 130 * yy, 0, 255).astype(np.uint8)
base[..., 2] = np.clip(180 - 90 * xx, 0, 255).astype(np.uint8)

img_clean = Image.fromarray(base, mode="RGB")
draw = ImageDraw.Draw(img_clean)
draw.rectangle([50, 60, 230, 240], fill=(245, 158, 11), outline=(15, 23, 42), width=4)
draw.ellipse([290, 75, 560, 285], fill=(16, 185, 129), outline=(15, 23, 42), width=4)
draw.line([(40, 310), (600, 310)], fill=(248, 250, 252), width=6)

img_clean.save(out_dir / "01_original.png")

# 2. Suavizado con filtro promedio (BoxBlur 3x3 y 9x9)
blur_3 = img_clean.filter(ImageFilter.BoxBlur(1))
blur_9 = img_clean.filter(ImageFilter.BoxBlur(4))
blur_3.save(out_dir / "02_suavizado_box_3x3.png")
blur_9.save(out_dir / "03_suavizado_box_9x9.png")

# 3. Ruido sal y pimienta (5% de píxeles alterados a 255 o 0)
rng = np.random.default_rng(42)
arr_sp = np.array(img_clean).copy()
mask = rng.random((h, w))
arr_sp[mask < 0.025] = [255, 255, 255]  # sal
arr_sp[(mask >= 0.025) & (mask < 0.05)] = [0, 0, 0]  # pimienta

img_sp = Image.fromarray(arr_sp, mode="RGB")
img_sp.save(out_dir / "04_ruido_sal_pimienta.png")

# 4. Comparación: Promedio (BoxBlur) vs Mediana (MedianFilter 3x3) sobre sal y pimienta
sp_box = img_sp.filter(ImageFilter.BoxBlur(1))
sp_median = img_sp.filter(ImageFilter.MedianFilter(size=3))

sp_box.save(out_dir / "05_sal_pimienta_con_promedio.png")
sp_median.save(out_dir / "06_sal_pimienta_con_mediana.png")

print("Imágenes generadas en:", out_dir.resolve())
