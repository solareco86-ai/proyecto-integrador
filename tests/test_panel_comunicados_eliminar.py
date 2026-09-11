"""Tests de integración HTTP de GET/POST /panel/comunicados/{id}/eliminar (4D-4), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_comunicado_repository, get_usuario_repository


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


class InMemoryComunicadoRepo(ComunicadoRepository):
    def __init__(self, comunicados: list[Comunicado] | None = None) -> None:
        self.data: dict[str, Comunicado] = {c.id: c for c in (comunicados or [])}

    async def save(self, comunicado: Comunicado) -> None:
        self.data[comunicado.id] = comunicado

    async def get_by_id(self, comunicado_id: str) -> Comunicado | None:
        return self.data.get(comunicado_id)

    async def get_by_slug(self, slug: str) -> Comunicado | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Comunicado]:
        return list(self.data.values())

    async def update(self, comunicado: Comunicado) -> None:
        self.data[comunicado.id] = comunicado

    async def delete(self, comunicado_id: str) -> None:
        self.data.pop(comunicado_id, None)


def _usuario(rol: str = "autoridad", is_active: bool = True) -> Usuario:
    from src.infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher

    hasher = BcryptPasswordHasher()
    return Usuario.create(
        email="directora@isft199.edu.ar",
        password_hash=hasher.hash("clave-segura-123"),
        nombre="Directora",
        is_active=is_active,
        rol=rol,
    )


async def _login(ac: AsyncClient, usuario: Usuario) -> None:
    await ac.post("/panel/login", data={"email": usuario.email, "password": "clave-segura-123"})


def _extraer_csrf_token(html: str) -> str:
    marker = 'name="csrf_token" value="'
    start = html.index(marker) + len(marker)
    end = html.index('"', start)
    return html[start:end]


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(usuario: Usuario, repo: InMemoryComunicadoRepo | None = None) -> InMemoryComunicadoRepo:
    repo = repo or InMemoryComunicadoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_comunicado_repository] = lambda: repo
    return repo


def _comunicado(titulo: str = "Comunicado de prueba") -> Comunicado:
    return Comunicado.create(titulo=titulo, cuerpo="Cuerpo del comunicado")


# --- GET de confirmación ---


@pytest.mark.asyncio
async def test_get_eliminar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    comunicado = _comunicado()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_eliminar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    comunicado = _comunicado()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_eliminar_con_autoridad_devuelve_200():
    usuario = _usuario()
    comunicado = _comunicado()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_eliminar_muestra_titulo_del_comunicado():
    usuario = _usuario()
    comunicado = _comunicado(titulo="Aviso institucional")
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

    assert "Aviso institucional" in response.text
    assert "permanente" in response.text.lower()


@pytest.mark.asyncio
async def test_get_eliminar_contiene_csrf_token():
    usuario = _usuario()
    comunicado = _comunicado()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

    assert 'name="csrf_token"' in response.text


@pytest.mark.asyncio
async def test_get_eliminar_comunicado_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/id-inexistente/eliminar")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_eliminar_no_elimina_el_comunicado():
    usuario = _usuario()
    comunicado = _comunicado()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

    assert comunicado.id in repo.data


# --- POST de eliminación ---


@pytest.mark.asyncio
async def test_post_eliminar_valido_redirige_303_a_listado_con_ok_eliminado():
    usuario = _usuario()
    comunicado = _comunicado()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/eliminar",
            data={"csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/comunicados?ok=eliminado"


@pytest.mark.asyncio
async def test_post_eliminar_elimina_el_comunicado_seleccionado():
    usuario = _usuario()
    comunicado = _comunicado()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/comunicados/{comunicado.id}/eliminar", data={"csrf_token": csrf_token})

    assert comunicado.id not in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_no_afecta_otros_comunicados():
    usuario = _usuario()
    c1 = _comunicado(titulo="Comunicado 1")
    c2 = _comunicado(titulo="Comunicado 2")
    c3 = _comunicado(titulo="Comunicado 3")
    repo = _configurar(usuario, InMemoryComunicadoRepo([c1, c2, c3]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{c2.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/comunicados/{c2.id}/eliminar", data={"csrf_token": csrf_token})

    assert c1.id in repo.data
    assert c2.id not in repo.data
    assert c3.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_comunicado_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # Genera un token CSRF válido en sesión vía el form de "nuevo" (no hay comunicado para el GET de confirmación).
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/id-inexistente/eliminar", data={"csrf_token": csrf_token}
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


# --- Seguridad ---


@pytest.mark.asyncio
async def test_post_eliminar_csrf_incorrecto_devuelve_403():
    usuario = _usuario()
    comunicado = _comunicado()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/eliminar", data={"csrf_token": "token-invalido"}
        )

    assert response.status_code == 403
    assert comunicado.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_sin_csrf_token_no_elimina():
    usuario = _usuario()
    comunicado = _comunicado()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/comunicados/{comunicado.id}/eliminar")

        response = await ac.post(f"/panel/comunicados/{comunicado.id}/eliminar", data={})

    # Mismo comportamiento coherente con Noticias/Eventos: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert comunicado.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_sin_autorizacion_no_elimina():
    usuario = _usuario(rol="editor")
    comunicado = _comunicado()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.post(f"/panel/comunicados/{comunicado.id}/eliminar", data={"csrf_token": "cualquiera"})

    assert response.status_code == 403
    assert comunicado.id in repo.data
