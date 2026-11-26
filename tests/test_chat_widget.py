"""Pruebas de la plantilla del widget conversacional flotante (FE 4.1, issue #145)."""

from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from src.application.data_service import DataService
from src.application.dtos import ChatWidgetModel
from src.infrastructure.fastapi.dependencies import templates

ROOT = Path(__file__).resolve().parent.parent


class _Elementos(HTMLParser):
    """Junta los atributos de cada elemento del HTML, indexados por id y por atributo data-chat-*."""

    def __init__(self) -> None:
        super().__init__()
        self.por_clave: dict[str, dict[str, str | None]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        atributos: dict[str, str | None] = dict(attrs)
        claves: list[str] = [
            nombre for nombre, _ in attrs if nombre.startswith("data-chat-") or nombre == "data-component"
        ]
        if atributos.get("id"):
            claves.append(f"#{atributos['id']}")
        for clave in claves:
            self.por_clave[clave] = {"tag": tag, **atributos}


@pytest.fixture(scope="module")
def textos() -> ChatWidgetModel:
    return DataService(data_dir=str(ROOT / "data")).get_chat_widget()


def _renderizar(textos: ChatWidgetModel, abierto: bool = False) -> str:
    modulo: Any = templates.env.get_template("partials/components/chat_widget.html").module
    return str(modulo.chat_widget(textos, abierto=abierto))


def _elementos(html: str) -> dict[str, dict[str, str | None]]:
    parser = _Elementos()
    parser.feed(html)
    return parser.por_clave


def test_widget_cerrado_por_defecto(textos: ChatWidgetModel) -> None:
    elementos = _elementos(_renderizar(textos))

    boton = elementos["data-chat-toggle"]
    assert boton["aria-expanded"] == "false"
    assert boton["aria-controls"] == "chat-widget-panel"
    assert boton["aria-label"] == textos.etiquetas.abrir

    panel = elementos["#chat-widget-panel"]
    assert "hidden" in panel
    assert panel["role"] == "dialog"
    assert panel["aria-labelledby"] == "chat-widget-titulo"
    assert "is-open" not in (elementos["data-component"]["class"] or "")


def test_widget_abierto_muestra_la_ventana(textos: ChatWidgetModel) -> None:
    elementos = _elementos(_renderizar(textos, abierto=True))

    assert elementos["data-chat-toggle"]["aria-expanded"] == "true"
    assert "hidden" not in elementos["#chat-widget-panel"]
    assert "is-open" in (elementos["data-component"]["class"] or "")


def test_textos_y_controles_salen_de_los_datos(textos: ChatWidgetModel) -> None:
    html = _renderizar(textos)
    elementos = _elementos(html)

    for texto in (textos.titulo, textos.subtitulo, textos.saludo, textos.aviso, textos.etiquetas.campo):
        assert texto in html

    campo = elementos["data-chat-input"]
    assert campo["maxlength"] == str(textos.longitudMaxima)
    assert campo["placeholder"] == textos.placeholder
    assert elementos["#chat-widget-input"] == campo

    assert elementos["data-chat-send"]["aria-label"] == textos.etiquetas.enviar
    assert elementos["data-chat-close"]["aria-label"] == textos.etiquetas.cerrar
    # El micrófono queda oculto hasta que FE 4.3 confirme que el navegador puede grabar.
    assert "hidden" in elementos["data-chat-mic"]
    assert elementos["data-chat-messages"]["aria-live"] == "polite"


def test_estilos_del_widget_se_incluyen_en_el_bundle() -> None:
    entrada = (ROOT / "static/css/src/input.css").read_text(encoding="utf-8")
    assert '@import "../ChatWidget.css";' in entrada
    assert ".c-chat-widget__panel" in (ROOT / "static/css/index.css").read_text(encoding="utf-8")
