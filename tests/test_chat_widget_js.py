"""Auditoría estática del comportamiento del widget conversacional (FE 4.2, issue #146)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAT_WIDGET_JS = (ROOT / "static/js/modules/ChatWidget.js").read_text(encoding="utf-8")
APP_JS = (ROOT / "static/js/app.js").read_text(encoding="utf-8")

# APIs que interpretan texto como HTML o código: con ellas, una respuesta del servidor podría ejecutar scripts.
APIS_PELIGROSAS = ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function")


def _codigo_sin_comentarios(fuente: str) -> str:
    sin_bloques = re.sub(r"/\*.*?\*/", "", fuente, flags=re.S)
    return re.sub(r"^\s*//.*$", "", sin_bloques, flags=re.M)


def test_el_widget_no_interpreta_respuestas_como_html() -> None:
    codigo = _codigo_sin_comentarios(CHAT_WIDGET_JS)
    usadas = [api for api in APIS_PELIGROSAS if api in codigo]
    assert not usadas, f"ChatWidget.js no debe usar {usadas}: insertar texto con textContent"
    assert "textContent" in codigo


def test_los_enlaces_de_fuentes_pasan_por_la_validacion() -> None:
    codigo = _codigo_sin_comentarios(CHAT_WIDGET_JS)
    assert "urlDeFuenteSegura(" in codigo
    assert codigo.count("enlace.href =") == 1


def test_app_inicializa_el_widget() -> None:
    assert "import { initChatWidgets } from './modules/ChatWidget.js';" in APP_JS
    assert "initChatWidgets();" in APP_JS
