"""Pruebas de los textos del widget conversacional (data/config/chat_widget.yaml, issue #145)."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import pytest
from pydantic import ValidationError

from src.application.data_service import DataService
from src.application.dtos import ChatWidgetModel
from src.infrastructure.fastapi.dependencies import templates

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def textos() -> ChatWidgetModel:
    return DataService(data_dir=str(ROOT / "data")).get_chat_widget()


def test_textos_se_cargan_desde_data(textos: ChatWidgetModel) -> None:
    assert textos.titulo
    assert textos.saludo
    assert textos.longitudMaxima > 0
    assert (ROOT / textos.avatar.src.lstrip("/")).is_file()


def test_modelo_rechaza_longitud_maxima_invalida(textos: ChatWidgetModel) -> None:
    datos: dict[str, Any] = textos.model_dump()
    datos["longitudMaxima"] = 0
    with pytest.raises(ValidationError):
        ChatWidgetModel.model_validate(datos)


def test_configuracion_del_cliente_sale_de_los_datos(textos: ChatWidgetModel) -> None:
    config = textos.configuracion_cliente()

    assert config["longitudMaxima"] == textos.longitudMaxima
    assert config["api"]["baseUrl"] == "/api/v1/chat"
    assert set(config["errores"]) == {"timeout", "red", "servidor", "validacion", "audioVacio", "respuestaInvalida"}
    assert all(config["errores"].values())
    assert "{mensaje}" in config["mock"]["respuesta"]


def test_modelo_rechaza_confianza_mock_fuera_de_rango(textos: ChatWidgetModel) -> None:
    datos: dict[str, Any] = textos.model_dump()
    datos["mock"]["confianza"] = 1.5
    with pytest.raises(ValidationError):
        ChatWidgetModel.model_validate(datos)


def test_funcion_global_de_jinja_devuelve_los_textos() -> None:
    funcion = cast(Callable[[], object], templates.env.globals["chat_widget_textos"])
    assert isinstance(funcion(), ChatWidgetModel)
