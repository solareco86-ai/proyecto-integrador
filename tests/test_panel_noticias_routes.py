"""Tests de integración HTTP de GET /panel/noticias (solo listado, 4B-1), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_noticia_repository, get_usuario_repository


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


class InMemoryNoticiaRepo(NoticiaRepository):
    def __init__(self, noticias: list[Noticia]) -> None:
        self.data: dict[str, Noticia] = {n.id: n for n in noticias}

    async def save(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        return self.data.get(noticia_id)

    async def get_by_slug(self, slug: str) -> Noticia | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Noticia]:
        return list(self.data.values())

    async def update(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def delete(self, noticia_id: str) -> None:
        self.data.pop(noticia_id, None)


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


@pytest.mark.asyncio
async def test_listado_sin_sesion_redirige_a_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/noticias", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_listado_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: InMemoryNoticiaRepo([])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_listado_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: InMemoryNoticiaRepo([])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_listado_vacio_muestra_estado_vacio():
    usuario = _usuario()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: InMemoryNoticiaRepo([])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert response.status_code == 200
    assert "todavía no hay noticias cargadas" in response.text.lower()


@pytest.mark.asyncio
async def test_listado_con_noticias_muestra_titulo_y_estados():
    usuario = _usuario()
    publicada = Noticia.create(titulo="Inscripciones abiertas", cuerpo="Cuerpo 1", publicada=True)
    borrador = Noticia.create(titulo="Borrador interno", cuerpo="Cuerpo 2", publicada=False)
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: InMemoryNoticiaRepo([publicada, borrador])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert response.status_code == 200
    body = response.text
    assert "Inscripciones abiertas" in body
    assert "Borrador interno" in body
    assert "Publicada" in body
    assert "Borrador" in body


@pytest.mark.asyncio
async def test_listado_no_expone_autor_id():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Con autor", cuerpo="Cuerpo", autor_id=usuario.id)
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: InMemoryNoticiaRepo([noticia])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert usuario.id not in response.text


@pytest.mark.asyncio
async def test_listado_usa_use_case_y_repository_no_sql_directo():
    """Verifica (mediante spy) que la ruta llama list_all() del repository, no SQL directo."""
    usuario = _usuario()

    class SpyNoticiaRepo(InMemoryNoticiaRepo):
        def __init__(self) -> None:
            super().__init__([Noticia.create(titulo="X", cuerpo="Y")])
            self.list_all_called = False

        async def list_all(self) -> list[Noticia]:
            self.list_all_called = True
            return await super().list_all()

    spy_repo = SpyNoticiaRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: spy_repo

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias")

    assert response.status_code == 200
    assert spy_repo.list_all_called is True
