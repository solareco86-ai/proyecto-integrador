"""Tests de integración HTTP de GET/POST /panel/noticias/{id}/eliminar (4B-4), sin base de datos real."""

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
    def __init__(self, noticias: list[Noticia] | None = None) -> None:
        self.data: dict[str, Noticia] = {n.id: n for n in (noticias or [])}

    async def save(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        return self.data.get(noticia_id)

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


def _extraer_csrf_token(html: str) -> str:
    marker = 'name="csrf_token" value="'
    start = html.index(marker) + len(marker)
    end = html.index('"', start)
    return html[start:end]


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(usuario: Usuario, repo: InMemoryNoticiaRepo | None = None) -> InMemoryNoticiaRepo:
    repo = repo or InMemoryNoticiaRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: repo
    return repo


# --- GET de confirmación ---


@pytest.mark.asyncio
async def test_get_eliminar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_eliminar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_eliminar_noticia_existente_devuelve_200():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_eliminar_muestra_titulo_de_la_noticia():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Título a eliminar", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

    assert "Título a eliminar" in response.text
    assert "permanente" in response.text.lower()


@pytest.mark.asyncio
async def test_get_eliminar_no_elimina_la_noticia():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

    assert noticia.id in repo.data


@pytest.mark.asyncio
async def test_get_eliminar_noticia_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias/id-inexistente/eliminar")

    assert response.status_code == 404


# --- POST de eliminación ---


@pytest.mark.asyncio
async def test_post_eliminar_sin_csrf_token_no_elimina():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

        response = await ac.post(f"/panel/noticias/{noticia.id}/eliminar", data={})

    assert response.status_code == 422  # campo csrf_token requerido faltante, coherente con 4B-2/4B-3
    assert noticia.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_csrf_incorrecto_devuelve_403_y_no_elimina():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/noticias/{noticia.id}/eliminar")

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/eliminar", data={"csrf_token": "token-invalido"}
        )

    assert response.status_code == 403
    assert noticia.id in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_valido_elimina_la_noticia():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/noticias/{noticia.id}/eliminar", data={"csrf_token": csrf_token})

    assert noticia.id not in repo.data


@pytest.mark.asyncio
async def test_post_eliminar_valido_redirige_303_a_listado_con_ok_eliminada():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/eliminar",
            data={"csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/noticias?ok=eliminada"


@pytest.mark.asyncio
async def test_listado_muestra_mensaje_de_eliminacion_exitosa():
    usuario = _usuario()
    _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias?ok=eliminada")

    assert "eliminada correctamente" in response.text.lower()


@pytest.mark.asyncio
async def test_post_eliminar_noticia_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # Genera un token CSRF válido en sesión vía el form de "nueva" (no hay noticia para el GET de confirmación)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/id-inexistente/eliminar", data={"csrf_token": csrf_token}
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_eliminar_una_noticia_no_elimina_las_demas():
    usuario = _usuario()
    noticia_1 = Noticia.create(titulo="Noticia 1", cuerpo="Cuerpo 1")
    noticia_2 = Noticia.create(titulo="Noticia 2", cuerpo="Cuerpo 2")
    noticia_3 = Noticia.create(titulo="Noticia 3", cuerpo="Cuerpo 3")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia_1, noticia_2, noticia_3]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia_2.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(f"/panel/noticias/{noticia_2.id}/eliminar", data={"csrf_token": csrf_token})

    assert noticia_1.id in repo.data
    assert noticia_2.id not in repo.data
    assert noticia_3.id in repo.data


@pytest.mark.asyncio
async def test_listado_posterior_no_muestra_la_noticia_eliminada():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Noticia a eliminar", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/eliminar")
        csrf_token = _extraer_csrf_token(form_response.text)
        await ac.post(f"/panel/noticias/{noticia.id}/eliminar", data={"csrf_token": csrf_token})

        listado_response = await ac.get("/panel/noticias")

    assert "Noticia a eliminar" not in listado_response.text
    assert "todavía no hay noticias cargadas" in listado_response.text.lower()
