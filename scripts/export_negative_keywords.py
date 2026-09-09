#!/usr/bin/env python3
"""
Extractor y formateador de la Super-Lista Maestra de Palabras Clave Negativas (DataMaq).
Genera archivos de importación limpios para:
1. Google Ads Web Console (texto plano / copy-paste).
2. Google Ads Editor (formato CSV con columnas List Name / Criterion Type / Keyword Text / Match Type).
"""

import re
from pathlib import Path

DOC_PATH = Path("/home/agustin/proyectos_software/www-datamaq/docs/google_ads_campaigns_setup.md")
OUTPUT_DIR = Path("/home/agustin/proyectos_software/www-datamaq/data/ads")


def extract_negative_keywords() -> list[str]:
    content = DOC_PATH.read_text(encoding="utf-8")

    # Extraer la sección de la Super-Lista Maestra
    match = re.search(
        r"## 🚫 SUPER-LISTA MAESTRA DE PALABRAS CLAVE NEGATIVAS.*?\`\`\`text\n(.*?)\`\`\`", content, re.DOTALL
    )
    if not match:
        raise ValueError("No se encontró el bloque de negativas en la ficha técnica.")

    raw_block = match.group(1)
    keywords: list[str] = []

    for line in raw_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        keywords.append(line)

    return keywords


def generate_export_files() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    keywords = extract_negative_keywords()

    # 1. Archivo de texto plano (para copiar y pegar en la consola web)
    plain_text_file = OUTPUT_DIR / "negative_keywords_clean.txt"
    plain_text_file.write_text("\n".join(keywords) + "\n", encoding="utf-8")

    # 2. Archivo CSV para Google Ads Editor (Shared List)
    csv_editor_file = OUTPUT_DIR / "negative_keywords_editor.csv"
    lines = ["List Name,Criterion Type,Keyword Text,Match Type"]
    list_name = "DataMaq — Super-Lista Maestra Negativas B2B"
    for kw in keywords:
        lines.append(f'"{list_name}",Negative Keyword,"{kw}",Broad')
    csv_editor_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"✔ Total de palabras clave negativas procesadas: {len(keywords)}")
    print(f"✔ Archivo texto plano: {plain_text_file}")
    print(f"✔ Archivo CSV Editor: {csv_editor_file}")


if __name__ == "__main__":
    generate_export_files()
