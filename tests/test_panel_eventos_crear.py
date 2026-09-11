"""Tests de integración HTTP de GET/POST /panel/eventos/nuevo (4C-2), sin base de datos real."""

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


_FECHA_VALIDA = "2026-12-15T18:30"
_FECHA_PASADA = "2020-01-01T10:00"


# --- GET del formulario ---


@pytest.mark.asyncio
async def test_get_formulario_sin_sesion_redirige_a_login():
    _configurar(_usuario())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/panel/eventos/nuevo", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_formulario_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos/nuevo")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_formulario_con_rol_autoridad_devuelve_200():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos/nuevo")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_formulario_contiene_campos_y_csrf():
    usuario = _usuario()
    _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos/nuevo")

    body = response.text
    assert 'name="titulo"' in body
    assert 'name="descripcion"' in body
    assert 'name="fecha_evento"' in body
    assert 'name="lugar"' in body
    assert 'name="csrf_token"' in body


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_crea_evento_y_redirige_al_listado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Acto de fin de año",
                "descripcion": "Descripción del acto",
                "fecha_evento": _FECHA_VALIDA,
                "lugar": "Auditorio",
                "csrf_token": csrf_token,
            },
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/eventos?ok=creado"
    assert len(repo.data) == 1


@pytest.mark.asyncio
async def test_evento_creado_queda_guardado_en_el_repositorio():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Acto de fin de año",
                "descripcion": "Descripción del acto",
                "fecha_evento": _FECHA_VALIDA,
                "csrf_token": csrf_token,
            },
        )

    evento_creado = next(iter(repo.data.values()))
    assert evento_creado.titulo == "Acto de fin de año"
    assert evento_creado.descripcion == "Descripción del acto"
    assert evento_creado.fecha_evento == _FECHA_VALIDA


@pytest.mark.asyncio
async def test_post_usa_autor_id_del_usuario_autenticado():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Título",
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_VALIDA,
                "csrf_token": csrf_token,
            },
        )

    evento_creado = next(iter(repo.data.values()))
    assert evento_creado.autor_id == usuario.id


@pytest.mark.asyncio
async def test_post_autor_id_enviado_por_el_cliente_es_ignorado():
    """Un autor_id falso en el body no debe usarse: la ruta no lo declara como parámetro."""
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Título",
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_VALIDA,
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    evento_creado = next(iter(repo.data.values()))
    assert evento_creado.autor_id == usuario.id
    assert evento_creado.autor_id != "id-falso-inventado-por-el-cliente"


@pytest.mark.asyncio
async def test_post_fecha_pasada_se_acepta():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Evento histórico",
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_PASADA,
                "csrf_token": csrf_token,
            },
            follow_redirects=False,
        )

    assert response.status_code == 303
    evento_creado = next(iter(repo.data.values()))
    assert evento_creado.fecha_evento == _FECHA_PASADA


@pytest.mark.asyncio
async def test_post_lugar_vacio_se_guarda_como_none():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Título",
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_VALIDA,
                "lugar": "   ",
                "csrf_token": csrf_token,
            },
        )

    evento_creado = next(iter(repo.data.values()))
    assert evento_creado.lugar is None


# --- Validaciones ---


@pytest.mark.asyncio
async def test_post_fecha_invalida_se_rechaza():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Título",
                "descripcion": "Descripción",
                "fecha_evento": "no-es-una-fecha",
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "fecha" in response.text.lower()
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_titulo_vacio_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={"titulo": "", "descripcion": "Descripción", "fecha_evento": _FECHA_VALIDA, "csrf_token": csrf_token},
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
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={"titulo": "    ", "descripcion": "Descripción", "fecha_evento": _FECHA_VALIDA, "csrf_token": csrf_token},
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
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "x" * 201,
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_VALIDA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "200 caracteres" in response.text
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_descripcion_vacia_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={"titulo": "Título", "descripcion": "", "fecha_evento": _FECHA_VALIDA, "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "descripción es obligatoria" in response.text.lower()
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_descripcion_solo_espacios_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={"titulo": "Título", "descripcion": "   ", "fecha_evento": _FECHA_VALIDA, "csrf_token": csrf_token},
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
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "",
                "descripcion": "Descripción a conservar",
                "fecha_evento": _FECHA_VALIDA,
                "lugar": "Lugar a conservar",
                "csrf_token": csrf_token,
            },
        )

    body = response.text
    assert "Descripción a conservar" in body
    assert "Lugar a conservar" in body
    assert _FECHA_VALIDA in body


# --- Seguridad: CSRF ---


@pytest.mark.asyncio
async def test_post_sin_csrf_token_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/eventos/nuevo")

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={"titulo": "Título", "descripcion": "Descripción", "fecha_evento": _FECHA_VALIDA},
        )

    # Mismo comportamiento coherente con Noticias: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert len(repo.data) == 0


@pytest.mark.asyncio
async def test_post_csrf_incorrecto_devuelve_403_y_no_crea():
    usuario = _usuario()
    repo = _configurar(usuario)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get("/panel/eventos/nuevo")

        response = await ac.post(
            "/panel/eventos/nuevo",
            data={
                "titulo": "Título",
                "descripcion": "Descripción",
                "fecha_evento": _FECHA_VALIDA,
                "csrf_token": "token-invalido",
            },
        )

    assert response.status_code == 403
    assert len(repo.data) == 0
