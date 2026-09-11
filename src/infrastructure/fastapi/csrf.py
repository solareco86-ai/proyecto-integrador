"""Protección CSRF manual para los formularios POST del panel de autoridades.

No es un middleware global: se aplica únicamente vía dependency en los
endpoints POST del panel, para no afectar rutas públicas (contacto,
tracking de eventos, etc.) que no la necesitan. Reutiliza la sesión que ya
provee SessionMiddleware, sin agregar cookies ni dependencias nuevas.
"""

import secrets

from fastapi import Form, HTTPException, Request

_SESSION_KEY = "csrf_token"


def get_or_create_csrf_token(request: Request) -> str:
    """Devuelve el token CSRF de la sesión actual, generándolo si no existe."""
    token = request.session.get(_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        request.session[_SESSION_KEY] = token
    return token


async def verify_csrf(request: Request, csrf_token: str = Form(...)) -> None:
    """Valida el token CSRF recibido en un formulario POST contra el de la sesión.

    Lanza 403 si no coincide o si la sesión no tiene un token generado
    (p. ej. el formulario se abrió sin pasar antes por el GET que lo genera).
    """
    token_en_sesion = request.session.get(_SESSION_KEY)
    if not token_en_sesion or not secrets.compare_digest(csrf_token, token_en_sesion):
        raise HTTPException(status_code=403, detail="Token CSRF inválido o ausente")
