"""Verifica que no queden referencias a términos prohibidos tras el pivote de
posicionamiento (Vaca Muerta, Oil & Gas, Neuquén)."""

import re
from pathlib import Path

import pytest

PROHIBITED_TERMS = [
    "vaca muerta",
    "oil & gas",
    "yacimiento",
    "cuenca neuquina",
    "neuquén capital",
    "siderca",
    "tenaris",
    "techint",
]

# Archivos que no son contenido público (redirects técnicos, etc.)
EXCLUDED_FILES = {"data/config/redirects.yaml"}

DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")


def _yaml_and_html_files(root: Path):
    """Generador de archivos YAML y HTML bajo un directorio."""
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in (".yaml", ".yml", ".html", ".md"):
            yield path


@pytest.mark.parametrize("file_path", list(_yaml_and_html_files(DATA_DIR)))
def test_data_files_no_prohibited_terms(file_path: Path):
    """Barre data/ en busca de términos prohibidos."""
    # Saltar archivos excluidos (ej. redirects.yaml contiene paths técnicos)
    rel_path = str(file_path).replace("\\", "/")
    if any(excluded in rel_path for excluded in EXCLUDED_FILES):
        return
    content = file_path.read_text(errors="ignore").lower()
    for term in PROHIBITED_TERMS:
        pattern = re.escape(term).replace(r"\ ", r"\s+")
        if re.search(pattern, content):
            pytest.fail(f"Término prohibido '{term}' encontrado en {file_path}")


@pytest.mark.parametrize("file_path", list(_yaml_and_html_files(TEMPLATES_DIR)))
def test_template_files_no_prohibited_terms(file_path: Path):
    """Barre templates/ en busca de términos prohibidos."""
    content = file_path.read_text(errors="ignore").lower()
    for term in PROHIBITED_TERMS:
        pattern = re.escape(term).replace(r"\ ", r"\s+")
        if re.search(pattern, content):
            pytest.fail(f"Término prohibido '{term}' encontrado en {file_path}")
