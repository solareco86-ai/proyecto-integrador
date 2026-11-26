"""Datos de contacto humano que ofrece el widget conversacional (FE 4.5, issue #149)."""

from typing import TypedDict
from urllib.parse import quote


class ChatWidgetContacto(TypedDict):
    """Alternativa al asistente: WhatsApp si está habilitado; si no, el correo de Secretaría."""

    whatsappUrl: str | None
    correoUsuario: str | None
    correoDominio: str | None


def present_chat_widget_contacto(
    correo: str, whatsapp_habilitado: bool, telefono: str, mensaje: str
) -> ChatWidgetContacto:
    """Arma el enlace de WhatsApp y separa el correo en usuario y dominio.

    El correo se entrega en dos partes para que EmailProtector.js lo reconstruya en el
    navegador y no quede en texto plano para los bots (mismo criterio que el pie de página).
    Mientras el número institucional siga en trámite, WHATSAPP_ENABLED queda en False y el
    widget ofrece el correo.
    """
    digitos = "".join(caracter for caracter in telefono if caracter.isdigit())
    whatsapp_url = f"https://wa.me/{digitos}?text={quote(mensaje)}" if whatsapp_habilitado and digitos else None
    usuario, separador, dominio = correo.partition("@")
    tiene_correo = bool(separador and usuario and dominio)
    return {
        "whatsappUrl": whatsapp_url,
        "correoUsuario": usuario if tiene_correo else None,
        "correoDominio": dominio if tiene_correo else None,
    }
