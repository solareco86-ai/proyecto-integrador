"""Tests de integración HTTP de GET/POST /panel/eventos/{id}/eliminar (4C-4), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_evento_repository, get_usuario_repository


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


class InMemoryEventoRepo(EventoRepository):
    def __init__(self, eventos: list[Evento] | None = None) -> None:
        self.data: dict[str, Evento] = {e.id: e for e in (eventos or [])}

    async def save(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def get_by_id(self, evento_id: str) -> Evento | None:
        return self.data.get(evento_id)

    async def get_by_slug(self, slug: str) -> Evento | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Evento]:
        return sorted(self.data.values(), key=lambda e: e.fecha_evento)

    async def update(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def delete(self, evento_id: str) -> None:
        self.data.pop(evento_id, None)


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


def _configurar(usuario: Usuario, repo: InMemoryEventoRepo | None = None) -> InMemoryEventoRepo:
    repo = repo or InMemoryEventoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_evento_repository] = lambda: repo
    return repo


def _evento(titulo: str = "Evento de prueba") -> Evento:
    return Evento.create(titulo=titulo, descripcion="Descripción", fecha_evento="2026-09-15T18:30:00")


# --- GET de confirmación ---


@pytest.mark.asyncio
async def test_get_eliminar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    evento = _evento()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/eventos/{evento.id}/eliminar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_eliminar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    evento = _evento()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_eliminar_con_autoridad_devuelve_200():
    usuario = _usuario()
    evento = _evento()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_eliminar_muestra_titulo_del_evento():
    usuario = _usuario()
    evento = _evento(titulo="Acto de fin de año")
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")

    assert "Acto de fin de año" in response.text
    assert "permanente" in response.text.lower()


@pytest.mark.asyncio
async def test_get_eliminar_contiene_csrf_token():
    usuario = _usuario()
    evento = _evento()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")

    assert 'name="csrf_token"' in response.text


@pytest.mark.asyncio
async def test_get_eliminar_evento_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos/id-inexistente/eliminar")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_eliminar_no_elimina_el_evento():
    usuario = _usuario()
    evento = _evento()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/eventos/{evento.id}/eliminar")

    assert evento.id in repo.data


# --- POST de eliminación ---


@pytest.mark.asyncio
async def test_post_eliminar_valido_redirige_303_a_listado_con_ok_eliminado():
    usuario = _usuario()
    evento = _evento()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/eliminar",
            data={"csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/eventos?ok=eliminado"


@pytest.mark.asyncio
async def test_post_eliminar_elimina_el_evento_seleccionado():
    usuario = _usuario()
    evento = _evento()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/eventos/{evento.id}/eliminar", data={"csrf_token": csrf_token})

    assert evento.id not in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_no_afecta_otros_eventos():
    usuario = _usuario()
    evento_1 = _evento(titulo="Evento 1")
    evento_2 = _evento(titulo="Evento 2")
    evento_3 = _evento(titulo="Evento 3")
    repo = _configurar(usuario, InMemoryEventoRepo([evento_1, evento_2, evento_3]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento_2.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/eventos/{evento_2.id}/eliminar", data={"csrf_token": csrf_token})

    assert evento_1.id in repo.data
    assert evento_2.id not in repo.data
    assert evento_3.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_evento_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # Genera un token CSRF válido en sesión vía el form de "nuevo" (no hay evento para el GET de confirmación).
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/id-inexistente/eliminar", data={"csrf_token": csrf_token}
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_eliminar_csrf_incorrecto_devuelve_403():
    usuario = _usuario()
    evento = _evento()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/eventos/{evento.id}/eliminar")

        response = await ac.post(
            f"/panel/eventos/{evento.id}/eliminar", data={"csrf_token": "token-invalido"}
        )

    assert response.status_code == 403
    assert evento.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_sin_csrf_token_no_elimina():
    usuario = _usuario()
    evento = _evento()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/eventos/{evento.id}/eliminar")

        response = await ac.post(f"/panel/eventos/{evento.id}/eliminar", data={})

    # Mismo comportamiento coherente con Noticias: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert evento.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_sin_autorizacion_no_elimina():
    usuario = _usuario(rol="editor")
    evento = _evento()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.post(f"/panel/eventos/{evento.id}/eliminar", data={"csrf_token": "cualquiera"})

    assert response.status_code == 403
    assert evento.id in repo.data
