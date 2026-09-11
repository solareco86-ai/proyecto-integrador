"""Tests de integración HTTP de GET /panel (router privado), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_usuario_repository


class InMemoryUsuarioRepo(UsuarioRepository):
    def __init__(self, usuarios: list[Usuario]) -> None:
        self.by_id: dict[str, Usuario] = {u.id: u for u in usuarios}
        self.by_email: dict[str, Usuario] = {u.email: u for u in usuarios}

    async def save(self, usuario: Usuario) -> None:
        self.by_id[usuario.id] = usuario
        self.by_email[usuario.email] = usuario

    async def get_by_id(self, usuario_id: str) -> Usuario | None:
        return self.by_id.get(usuario_id)

    async def get_by_email(self, email: str) -> Usuario | None:
        return self.by_email.get(email)


def _usuario(password: str = "clave-segura-123", rol: str = "autoridad", is_active: bool = True) -> Usuario:
    from src.infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher

    hasher = BcryptPasswordHasher()
    return Usuario.create(
        email="directora@isft199.edu.ar",
        password_hash=hasher.hash(password),
        nombre="Directora",
        is_active=is_active,
        rol=rol,
    )


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_panel_sin_sesion_redirige_a_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_panel_con_sesion_valida_muestra_dashboard():
    usuario = _usuario()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await ac.post("/panel/login", data={"email": usuario.email, "password": "clave-segura-123"})
        response = await ac.get("/panel")

    assert response.status_code == 200
    assert usuario.nombre in response.text


@pytest.mark.asyncio
async def test_panel_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await ac.post("/panel/login", data={"email": usuario.email, "password": "clave-segura-123"})
        response = await ac.get("/panel")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_panel_usuario_desactivado_despues_del_login_pierde_acceso():
    """La sesión sigue viva pero get_current_user descarta usuarios inactivos en cada request."""
    usuario = _usuario()
    repo = InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_usuario_repository] = lambda: repo

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await ac.post("/panel/login", data={"email": usuario.email, "password": "clave-segura-123"})

        # Se desactiva el usuario "en caliente", simulando una baja mientras la sesión sigue viva.
        usuario.is_active = False

        response = await ac.get("/panel", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"
