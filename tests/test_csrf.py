"""Tests unitarios del helper de CSRF manual del panel, sin base de datos real."""

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf


def _make_request(session: dict) -> Request:
    scope = {"type": "http", "session": session}
    return Request(scope)  # type: ignore[arg-type]


def test_get_or_create_csrf_token_genera_uno_nuevo_si_no_existe():
    session: dict = {}
    request = _make_request(session)

    token = get_or_create_csrf_token(request)

    assert token
    assert session["csrf_token"] == token


def test_get_or_create_csrf_token_reutiliza_el_existente():
    session = {"csrf_token": "token-ya-existente"}
    request = _make_request(session)

    token = get_or_create_csrf_token(request)

    assert token == "token-ya-existente"


@pytest.mark.asyncio
async def test_verify_csrf_token_correcto_no_lanza_excepcion():
    session = {"csrf_token": "token-valido"}
    request = _make_request(session)

    await verify_csrf(request, csrf_token="token-valido")


@pytest.mark.asyncio
async def test_verify_csrf_token_incorrecto_lanza_403():
    session = {"csrf_token": "token-valido"}
    request = _make_request(session)

    with pytest.raises(HTTPException) as exc_info:
        await verify_csrf(request, csrf_token="token-falso")

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_verify_csrf_sin_token_en_sesion_lanza_403():
    session: dict = {}
    request = _make_request(session)

    with pytest.raises(HTTPException) as exc_info:
        await verify_csrf(request, csrf_token="cualquiera")

    assert exc_info.value.status_code == 403
