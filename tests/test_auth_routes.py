"""Tests de integración HTTP de /panel/login y /panel/logout (Form + redirect)."""

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


def _usuario_con_password(password: str, is_active: bool = True, rol: str = "autoridad") -> Usuario:
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
async def test_get_login_sin_sesion_muestra_formulario():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/login")

    assert response.status_code == 200
    assert "form" in response.text.lower()


@pytest.mark.asyncio
async def test_get_login_con_sesion_valida_redirige_al_panel():
    usuario = _usuario_con_password("clave-segura-123")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test", follow_redirects=True) as ac:
        login_response = await ac.post(
            "/panel/login", data={"email": usuario.email, "password": "clave-segura-123"}
        )
        assert login_response.status_code == 200  # tras seguir el redirect 303, cae en /panel

        get_response = await ac.get("/panel/login")

    assert get_response.status_code == 200
    assert get_response.url.path == "/panel"


@pytest.mark.asyncio
async def test_post_login_correcto_redirige_al_panel():
    usuario = _usuario_con_password("clave-segura-123")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.post(
            "/panel/login",
            data={"email": usuario.email, "password": "clave-segura-123"},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel"
    assert "isft199_session" in response.cookies


@pytest.mark.asyncio
async def test_post_login_incorrecto_reintenta_formulario():
    usuario = _usuario_con_password("clave-segura-123")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.post("/panel/login", data={"email": usuario.email, "password": "incorrecta"})

    assert response.status_code == 401
    assert "incorrectos" in response.text.lower()


@pytest.mark.asyncio
async def test_post_login_usuario_inactivo_falla_igual_que_credenciales_invalidas():
    usuario = _usuario_con_password("clave-segura-123", is_active=False)
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.post(
            "/panel/login", data={"email": usuario.email, "password": "clave-segura-123"}
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_y_logout_flujo_completo():
    usuario = _usuario_con_password("clave-segura-123")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        login_response = await ac.post(
            "/panel/login",
            data={"email": usuario.email, "password": "clave-segura-123"},
            follow_redirects=False,
        )
        assert login_response.status_code == 303
        assert "isft199_session" in login_response.cookies

        logout_response = await ac.post("/panel/logout", follow_redirects=False)
        assert logout_response.status_code == 303
        assert logout_response.headers["location"] == "/panel/login"

        panel_after_logout = await ac.get("/panel", follow_redirects=False)
        assert panel_after_logout.status_code == 303
        assert panel_after_logout.headers["location"] == "/panel/login"
