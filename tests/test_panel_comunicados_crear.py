"""Tests de integración HTTP de GET/POST /panel/comunicados/nuevo (4D-2), sin base de datos real."""

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


# --- GET del formulario ---


@pytest.mark.asyncio
async def test_get_formulario_sin_sesion_redirige_a_login():
    _configurar(_usuario())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/comunicados/nuevo", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_formulario_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/nuevo")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_formulario_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/nuevo")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_formulario_contiene_csrf_token():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/nuevo")

    assert 'name="csrf_token"' in response.text
    assert 'name="titulo"' in response.text
    assert 'name="cuerpo"' in response.text


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_crea_comunicado_y_redirige_al_listado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "Aviso institucional", "cuerpo": "Contenido del aviso", "csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/comunicados?ok=creado"
    assert len(repo.data) == 1
    comunicado_creado = next(iter(repo.data.values()))
    assert comunicado_creado.titulo == "Aviso institucional"
    assert comunicado_creado.cuerpo == "Contenido del aviso"


@pytest.mark.asyncio
async def test_post_usa_autor_id_del_usuario_autenticado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
        )

    comunicado_creado = next(iter(repo.data.values()))
    assert comunicado_creado.autor_id == usuario.id


@pytest.mark.asyncio
async def test_post_autor_id_enviado_por_el_cliente_es_ignorado():
    """Un autor_id falso en el body no debe usarse: la ruta no lo declara como parámetro."""
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/comunicados/nuevo",
            data={
                "titulo": "Título",
                "cuerpo": "Cuerpo",
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    comunicado_creado = next(iter(repo.data.values()))
    assert comunicado_creado.autor_id == usuario.id
    assert comunicado_creado.autor_id != "id-falso-inventado-por-el-cliente"


# --- Validaciones ---


@pytest.mark.asyncio
async def test_post_titulo_vacio_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
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
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "     ", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
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
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "x" * 201, "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "200 caracteres" in response.text
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_cuerpo_vacio_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
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
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "Título válido", "cuerpo": "   ", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_error_de_validacion_conserva_valores_ingresados():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "", "cuerpo": "Cuerpo a conservar", "csrf_token": csrf_token},
        )

    assert "Cuerpo a conservar" in response.text


# --- Seguridad: CSRF ---


@pytest.mark.asyncio
async def test_post_sin_csrf_token_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/comunicados/nuevo")

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "Título", "cuerpo": "Cuerpo"},
        )

    # Mismo comportamiento coherente con Noticias/Eventos: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_csrf_incorrecto_devuelve_403_y_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/comunicados/nuevo")

        response = await ac.post(
            "/panel/comunicados/nuevo",
            data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": "token-invalido"},
        )

    assert response.status_code == 403
    assert len(repo.data) == 0
