import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

src_dir = Path("static/img/cap_2_1")
slides_dir = Path("static/img/cap_2_1/slides_video")
slides_dir.mkdir(parents=True, exist_ok=True)
out_video = Path("docs/video_reduccion_ruido_suavizado.mp4")

escenas = [
    ("01_original.png", "1/6 · Imagen original (sin ruido)"),
    ("02_suavizado_box_3x3.png", "2/6 · Suavizado promedio 3x3"),
    ("03_suavizado_box_9x9.png", "3/6 · Suavizado promedio 9x9 (más desenfoque)"),
    ("04_ruido_sal_pimienta.png", "4/6 · Ruido sal y pimienta (5%)"),
    ("05_sal_pimienta_con_promedio.png", "5/6 · Sal y pimienta + Filtro promedio (mancha)"),
    ("06_sal_pimienta_con_mediana.png", "6/6 · Sal y pimienta + Filtro mediana (limpio)"),
]

try:
    font_banner = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
except OSError:
    font_banner = ImageFont.load_default()

slide_paths = []
for idx, (fname, titulo) in enumerate(escenas, start=1):
    img = Image.open(src_dir / fname).convert("RGB").resize((1280, 720))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 656, 1280, 720], fill=(15, 23, 42))
    draw.text((28, 672), titulo, fill=(248, 250, 252), font=font_banner)
    s_path = slides_dir / f"slide_{idx:02d}.png"
    img.save(s_path)
    slide_paths.append(s_path)

ffmpeg_bin = shutil.which("ffmpeg")
if not ffmpeg_bin:
    try:
        import imageio_ffmpeg

        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

if ffmpeg_bin:
    list_file = slides_dir / "inputs.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for p in slide_paths:
            f.write(f"file '{p.resolve()}'\n")
            f.write("duration 6\n")
        # Repetir último frame para evitar corte abrupto en concat demuxer
        f.write(f"file '{slide_paths[-1].resolve()}'\n")

    cmd = [
        ffmpeg_bin,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-fps_mode",
        "vfr",
        "-pix_fmt",
        "yuv420p",
        str(out_video),
    ]
    subprocess.run(cmd, check=True)
    print("Video generado:", out_video.resolve())
else:
    print("ffmpeg no está instalado; se generaron los slides listos en:", slides_dir.resolve())
