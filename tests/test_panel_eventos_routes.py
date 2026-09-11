"""Tests de integración HTTP de GET /panel/eventos (solo listado, 4C-1), sin base de datos real."""

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
        # Mismo criterio que EventoRepositorySQL: ordenado por fecha_evento ASC.
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


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(usuario: Usuario, repo: InMemoryEventoRepo | None = None) -> InMemoryEventoRepo:
    repo = repo or InMemoryEventoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_evento_repository] = lambda: repo
    return repo


# --- Acceso ---


@pytest.mark.asyncio
async def test_listado_sin_sesion_redirige_a_login():
    _configurar(_usuario())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/eventos", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_listado_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_listado_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert response.status_code == 200


# --- Listado ---


@pytest.mark.asyncio
async def test_listado_vacio_muestra_estado_vacio():
    usuario = _usuario()
    _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert response.status_code == 200
    assert "todavía no hay eventos cargados" in response.text.lower()


@pytest.mark.asyncio
async def test_listado_con_eventos_muestra_titulo():
    usuario = _usuario()
    evento = Evento.create(
        titulo="Acto de fin de año", descripcion="Descripción", fecha_evento="2026-12-15T18:30:00"
    )
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert "Acto de fin de año" in response.text


@pytest.mark.asyncio
async def test_listado_muestra_fecha_en_formato_dd_mm_aaaa_hh_mm():
    usuario = _usuario()
    evento = Evento.create(
        titulo="Evento con fecha", descripcion="Descripción", fecha_evento="2026-09-15T18:30:00"
    )
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert "15/09/2026 18:30" in response.text


@pytest.mark.asyncio
async def test_listado_muestra_lugar():
    usuario = _usuario()
    evento = Evento.create(
        titulo="Evento con lugar",
        descripcion="Descripción",
        fecha_evento="2026-09-15T18:30:00",
        lugar="Auditorio principal",
    )
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert "Auditorio principal" in response.text


@pytest.mark.asyncio
async def test_listado_lugar_none_muestra_guion():
    usuario = _usuario()
    evento = Evento.create(
        titulo="Evento sin lugar", descripcion="Descripción", fecha_evento="2026-09-15T18:30:00", lugar=None
    )
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    assert "—" in response.text


@pytest.mark.asyncio
async def test_listado_seccion_activa_eventos():
    usuario = _usuario()
    _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    body = response.text
    assert "Eventos" in body
    # El link "Eventos" del sidebar debe llevar la clase de sección activa.
    assert 'href="/panel/eventos" class="panel-sidebar__link panel-sidebar__link--active"' in body


@pytest.mark.asyncio
async def test_listado_respeta_orden_por_fecha_evento_ascendente():
    usuario = _usuario()
    evento_tardio = Evento.create(titulo="Evento tardío", descripcion="D", fecha_evento="2026-12-01T10:00:00")
    evento_temprano = Evento.create(titulo="Evento temprano", descripcion="D", fecha_evento="2026-01-01T10:00:00")
    # Se insertan en orden inverso a propósito: el repo debe devolverlos ordenados por fecha.
    repo = _configurar(usuario, InMemoryEventoRepo([evento_tardio, evento_temprano]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos")

    body = response.text
    assert body.index("Evento temprano") < body.index("Evento tardío")
    assert len(repo.data) == 2
