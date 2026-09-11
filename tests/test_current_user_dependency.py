"""Tests unitarios de get_current_user y require_authority, sin base de datos real."""

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.infrastructure.fastapi.dependencies import get_current_user, require_authority


class InMemoryUsuarioRepo(UsuarioRepository):
    def __init__(self, usuarios: list[Usuario]) -> None:
        self.by_id: dict[str, Usuario] = {u.id: u for u in usuarios}

    async def save(self, usuario: Usuario) -> None:
        self.by_id[usuario.id] = usuario

    async def get_by_id(self, usuario_id: str) -> Usuario | None:
        return self.by_id.get(usuario_id)

    async def get_by_email(self, email: str) -> Usuario | None:
        return next((u for u in self.by_id.values() if u.email == email), None)


def _make_request(session: dict) -> Request:
    """Request mínimo con `session` ya poblada, sin necesidad de SessionMiddleware."""
    scope = {"type": "http", "session": session}
    return Request(scope)  # type: ignore[arg-type]


def _usuario(is_active: bool = True) -> Usuario:
    return Usuario.create(
        email="directora@isft199.edu.ar",
        password_hash="hash-irrelevante",
        nombre="Directora",
        is_active=is_active,
    )


@pytest.mark.asyncio
async def test_get_current_user_sin_sesion_devuelve_none():
    repo = InMemoryUsuarioRepo([])
    request = _make_request(session={})

    assert await get_current_user(request, usuario_repository=repo) is None


@pytest.mark.asyncio
async def test_get_current_user_id_inexistente_devuelve_none():
    repo = InMemoryUsuarioRepo([])
    request = _make_request(session={"user_id": "id-que-no-existe"})

    assert await get_current_user(request, usuario_repository=repo) is None


@pytest.mark.asyncio
async def test_get_current_user_inactivo_devuelve_none():
    usuario = _usuario(is_active=False)
    repo = InMemoryUsuarioRepo([usuario])
    request = _make_request(session={"user_id": usuario.id})

    assert await get_current_user(request, usuario_repository=repo) is None


@pytest.mark.asyncio
async def test_get_current_user_sesion_valida_devuelve_usuario():
    usuario = _usuario()
    repo = InMemoryUsuarioRepo([usuario])
    request = _make_request(session={"user_id": usuario.id})

    assert await get_current_user(request, usuario_repository=repo) == usuario


@pytest.mark.asyncio
async def test_require_authority_sin_usuario_redirige_a_login():
    with pytest.raises(HTTPException) as exc_info:
        await require_authority(usuario=None)

    assert exc_info.value.status_code == 303
    assert exc_info.value.headers is not None
    assert exc_info.value.headers["Location"] == "/panel/login"


@pytest.mark.asyncio
async def test_require_authority_con_usuario_lo_devuelve():
    usuario = _usuario()

    assert await require_authority(usuario=usuario) == usuario
