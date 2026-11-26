"""Ejecuta con `node --test` las pruebas de los módulos JS del widget (tests/js/*.test.mjs)."""

import shutil
import subprocess
from pathlib import Path

import pytest

PRUEBAS_JS = sorted((Path(__file__).resolve().parent / "js").glob("*.test.mjs"))


@pytest.mark.parametrize("archivo", PRUEBAS_JS, ids=[p.name for p in PRUEBAS_JS])
def test_modulo_js_en_node(archivo: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js no está instalado (el pipeline del pre-push ya lo requiere para Tailwind y tsc).")
    resultado = subprocess.run([node, "--test", str(archivo)], capture_output=True, text=True, timeout=120)
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
