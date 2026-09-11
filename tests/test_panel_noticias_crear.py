"""Tests de integración HTTP de GET/POST /panel/noticias/nueva (4B-2), sin base de datos real."""

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


# --- GET del formulario ---


@pytest.mark.asyncio
async def test_get_formulario_sin_sesion_redirige_a_login():
    _configurar(_usuario())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/noticias/nueva", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_formulario_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias/nueva")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_formulario_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias/nueva")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_formulario_contiene_campos_y_csrf():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias/nueva")

    body = response.text
    assert 'name="titulo"' in body
    assert 'name="cuerpo"' in body
    assert 'name="publicada"' in body
    assert 'name="csrf_token"' in body


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_crea_noticia_y_redirige_al_listado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Inscripciones abiertas", "cuerpo": "Cuerpo de la noticia", "publicada": "on", "csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/noticias?ok=creada"
    assert len(repo.data) == 1
    noticia_creada = next(iter(repo.data.values()))
    assert noticia_creada.titulo == "Inscripciones abiertas"
    assert noticia_creada.publicada is True


@pytest.mark.asyncio
async def test_post_usa_autor_id_del_usuario_autenticado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
        )

    noticia_creada = next(iter(repo.data.values()))
    assert noticia_creada.autor_id == usuario.id


@pytest.mark.asyncio
async def test_post_autor_id_enviado_por_el_cliente_es_ignorado():
    """Un autor_id falso en el body no debe usarse: el DTO/ruta no lo aceptan."""
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/noticias/nueva",
            data={
                "titulo": "Título",
                "cuerpo": "Cuerpo",
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    noticia_creada = next(iter(repo.data.values()))
    assert noticia_creada.autor_id == usuario.id
    assert noticia_creada.autor_id != "id-falso-inventado-por-el-cliente"


@pytest.mark.asyncio
async def test_post_publicada_no_marcada_queda_como_borrador():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
        )

    noticia_creada = next(iter(repo.data.values()))
    assert noticia_creada.publicada is False


# --- Validaciones ---


@pytest.mark.asyncio
async def test_post_titulo_vacio_no_crea_y_muestra_error():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "título es obligatorio" in response.text.lower()
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_titulo_solo_espacios_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "     ", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_cuerpo_vacio_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título válido", "cuerpo": "", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "cuerpo es obligatorio" in response.text.lower()
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_cuerpo_solo_espacios_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título válido", "cuerpo": "   ", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_titulo_mayor_a_200_caracteres_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "x" * 201, "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "200 caracteres" in response.text
    assert len(repo.data) == 0


# --- Seguridad: CSRF ---


@pytest.mark.asyncio
async def test_post_sin_csrf_token_devuelve_403_y_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/noticias/nueva")  # genera el token en sesión, pero no lo enviamos

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título", "cuerpo": "Cuerpo"},
        )

    assert response.status_code == 422  # falta el campo requerido csrf_token -> FastAPI 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_csrf_incorrecto_devuelve_403_y_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/noticias/nueva")

        response = await ac.post(
            "/panel/noticias/nueva",
            data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": "token-invalido"},
        )

    assert response.status_code == 403
    assert len(repo.data) == 0
