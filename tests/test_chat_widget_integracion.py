"""Integración del widget conversacional en el sitio (FE 4.5, issue #149)."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.adapters.presenters.chat_widget_presenter import present_chat_widget_contacto
from src.infrastructure.fastapi.app import app

# Páginas públicas principales: todas heredan el widget de base.html.
PAGINAS = ["/", "/carreras", "/contact", "/cursos", "/ruta-que-no-existe"]


@pytest.mark.asyncio  # type: ignore
@pytest.mark.parametrize("ruta", PAGINAS)
async def test_el_widget_aparece_en_las_paginas_del_sitio(ruta: str) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as cliente:
        respuesta = await cliente.get(ruta)

    assert respuesta.text.count('data-component="chat-widget"') == 1
    assert "c-whatsapp-fab" not in respuesta.text


def test_contacto_ofrece_whatsapp_solo_si_esta_habilitado() -> None:
    habilitado = present_chat_widget_contacto(
        "isft199@abc.gob.ar", True, "+54 9 11 1234-5678", "Hola, ¿cómo me inscribo?"
    )
    deshabilitado = present_chat_widget_contacto("isft199@abc.gob.ar", False, "5491112345678", "Hola")

    assert habilitado["whatsappUrl"] == "https://wa.me/5491112345678?text=Hola%2C%20%C2%BFc%C3%B3mo%20me%20inscribo%3F"
    assert deshabilitado["whatsappUrl"] is None
    assert (deshabilitado["correoUsuario"], deshabilitado["correoDominio"]) == ("isft199", "abc.gob.ar")


def test_contacto_sin_telefono_ni_correo_validos() -> None:
    contacto = present_chat_widget_contacto("sin-arroba", True, "sin números", "Hola")

    assert contacto == {"whatsappUrl": None, "correoUsuario": None, "correoDominio": None}
