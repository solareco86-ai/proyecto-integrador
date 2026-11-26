"""Ejecuta las pruebas JS del cliente de la API del widget (FE 4.4, issue #148) con `node --test`."""

import shutil
import subprocess
from pathlib import Path

import pytest

PRUEBAS_JS = Path(__file__).resolve().parent / "js" / "chat_api_client.test.mjs"


def test_cliente_api_del_widget_en_node() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js no está instalado (el pipeline del pre-push ya lo requiere para Tailwind y tsc).")
    resultado = subprocess.run([node, "--test", str(PRUEBAS_JS)], capture_output=True, text=True, timeout=120)
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
