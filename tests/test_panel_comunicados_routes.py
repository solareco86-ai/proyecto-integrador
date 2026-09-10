"""Tests de integración HTTP de GET /panel/comunicados (solo listado, 4D-1), sin base de datos real."""

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


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(usuario: Usuario, repo: InMemoryComunicadoRepo | None = None) -> InMemoryComunicadoRepo:
    repo = repo or InMemoryComunicadoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_comunicado_repository] = lambda: repo
    return repo


# --- Acceso ---


@pytest.mark.asyncio
async def test_listado_sin_sesion_redirige_a_login():
    _configurar(_usuario())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/comunicados", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_listado_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_listado_con_usuario_inactivo_es_rechazado():
    usuario = _usuario(is_active=False)
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        # El login ya falla para un usuario inactivo (AuthenticateUsuarioUseCase lo rechaza).
        login_response = await ac.post(
            "/panel/login", data={"email": usuario.email, "password": "clave-segura-123"}
        )
        assert login_response.status_code == 401

        response = await ac.get("/panel/comunicados", follow_redirects=False)

    # Sin sesión válida (el login nunca se estableció), redirige a login.
    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_listado_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert response.status_code == 403


# --- Listado ---


@pytest.mark.asyncio
async def test_listado_vacio_muestra_estado_vacio():
    usuario = _usuario()
    _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert response.status_code == 200
    assert "todavía no hay comunicados cargados" in response.text.lower()


@pytest.mark.asyncio
async def test_listado_con_un_comunicado_muestra_titulo_y_cuerpo():
    usuario = _usuario()
    comunicado = Comunicado.create(titulo="Aviso institucional", cuerpo="Contenido del aviso")
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert "Aviso institucional" in response.text
    assert "Contenido del aviso" in response.text


@pytest.mark.asyncio
async def test_listado_con_varios_comunicados_muestra_todos():
    usuario = _usuario()
    c1 = Comunicado.create(titulo="Comunicado 1", cuerpo="Cuerpo 1")
    c2 = Comunicado.create(titulo="Comunicado 2", cuerpo="Cuerpo 2")
    _configurar(usuario, InMemoryComunicadoRepo([c1, c2]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    body = response.text
    assert "Comunicado 1" in body
    assert "Comunicado 2" in body


# --- Arquitectura / dependency injection ---


@pytest.mark.asyncio
async def test_listado_usa_use_case_y_repository_no_sql_directo():
    """Verifica (mediante spy) que la ruta llama list_all() del repository, no SQL directo."""
    usuario = _usuario()

    class SpyComunicadoRepo(InMemoryComunicadoRepo):
        def __init__(self) -> None:
            super().__init__([Comunicado.create(titulo="X", cuerpo="Y")])
            self.list_all_called = False

        async def list_all(self) -> list[Comunicado]:
            self.list_all_called = True
            return await super().list_all()

    spy_repo = SpyComunicadoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_comunicado_repository] = lambda: spy_repo

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert response.status_code == 200
    assert spy_repo.list_all_called is True


@pytest.mark.asyncio
async def test_listado_seccion_activa_comunicados():
    usuario = _usuario()
    _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados")

    assert 'href="/panel/comunicados" class="panel-sidebar__link panel-sidebar__link--active"' in response.text


# --- Alcance: sin editar/eliminar en esta subetapa ---
# (la creación ya se implementó en 4D-2; ver tests/test_panel_comunicados_crear.py)


@pytest.mark.asyncio
async def test_no_existe_ruta_de_editar_comunicado_todavia():
    usuario = _usuario()
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/algun-id/editar")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_no_existe_ruta_de_eliminar_comunicado_todavia():
    usuario = _usuario()
    _configurar(usuario)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/algun-id/eliminar")

    assert response.status_code == 404
