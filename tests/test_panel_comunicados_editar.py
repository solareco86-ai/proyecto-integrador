"""Tests de integración HTTP de GET/POST /panel/comunicados/{id}/editar (4D-3), sin base de datos real."""

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


def _comunicado_original(autor_id: str = "autor-real-123") -> Comunicado:
    return Comunicado.create(titulo="Título original", cuerpo="Cuerpo original", autor_id=autor_id)


# --- GET del formulario de edición ---


@pytest.mark.asyncio
async def test_get_editar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    comunicado = _comunicado_original()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_editar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    comunicado = _comunicado_original()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_editar_con_autoridad_devuelve_200():
    usuario = _usuario()
    comunicado = _comunicado_original()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_editar_carga_datos_actuales():
    usuario = _usuario()
    comunicado = _comunicado_original()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")

    body = response.text
    assert "Título original" in body
    assert "Cuerpo original" in body
    assert "Editar comunicado" in body
    assert "Guardar cambios" in body


@pytest.mark.asyncio
async def test_get_editar_comunicado_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/comunicados/id-inexistente/editar")

    assert response.status_code == 404


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_editar_redirige_303_a_listado_con_ok_editado():
    usuario = _usuario()
    comunicado = _comunicado_original()
    _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Título editado", "cuerpo": "Cuerpo editado", "csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/comunicados?ok=editado"


@pytest.mark.asyncio
async def test_post_editar_actualiza_titulo_y_cuerpo():
    usuario = _usuario()
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Título editado", "cuerpo": "Cuerpo editado", "csrf_token": csrf_token},
        )

    actualizado = repo.data[comunicado.id]
    assert actualizado.titulo == "Título editado"
    assert actualizado.cuerpo == "Cuerpo editado"


@pytest.mark.asyncio
async def test_post_editar_autor_id_permanece_intacto():
    usuario = _usuario()
    comunicado = _comunicado_original(autor_id="autor-real-123")
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={
                "titulo": "Título editado",
                "cuerpo": "Cuerpo editado",
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[comunicado.id].autor_id == "autor-real-123"


@pytest.mark.asyncio
async def test_post_editar_created_at_permanece_intacto():
    usuario = _usuario()
    comunicado = _comunicado_original()
    created_at_original = comunicado.created_at
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Título editado", "cuerpo": "Cuerpo editado", "csrf_token": csrf_token},
        )

    assert repo.data[comunicado.id].created_at == created_at_original


@pytest.mark.asyncio
async def test_post_editar_updated_at_se_actualiza():
    usuario = _usuario()
    comunicado = _comunicado_original()
    assert comunicado.updated_at is None
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Título editado", "cuerpo": "Cuerpo editado", "csrf_token": csrf_token},
        )

    assert repo.data[comunicado.id].updated_at is not None


# --- Validaciones (mismas reglas que crear) ---


@pytest.mark.asyncio
async def test_post_editar_titulo_vacio_no_actualiza():
    usuario = _usuario()
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "título es obligatorio" in response.text.lower()
    assert repo.data[comunicado.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_cuerpo_vacio_no_actualiza():
    usuario = _usuario()
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/comunicados/{comunicado.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Título válido", "cuerpo": "", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "cuerpo es obligatorio" in response.text.lower()
    assert repo.data[comunicado.id].cuerpo == "Cuerpo original"


# --- Comunicado inexistente en POST ---


@pytest.mark.asyncio
async def test_post_editar_comunicado_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # No hay GET previo posible (el comunicado no existe); generamos CSRF vía el form de "nuevo".
        form_response = await ac.get("/panel/comunicados/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/comunicados/id-inexistente/editar",
            data={"titulo": "X", "cuerpo": "Y", "csrf_token": csrf_token},
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


# --- Seguridad ---


@pytest.mark.asyncio
async def test_post_editar_csrf_incorrecto_devuelve_403_y_no_modifica():
    usuario = _usuario()
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/comunicados/{comunicado.id}/editar")

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Hackeado", "cuerpo": "Hackeado", "csrf_token": "token-invalido"},
        )

    assert response.status_code == 403
    assert repo.data[comunicado.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_sin_csrf_token_no_modifica():
    usuario = _usuario()
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/comunicados/{comunicado.id}/editar")

        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Hackeado", "cuerpo": "Hackeado"},
        )

    # Mismo comportamiento coherente con Noticias/Eventos: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert repo.data[comunicado.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_sin_autorizacion_no_modifica():
    usuario = _usuario(rol="editor")
    comunicado = _comunicado_original()
    repo = _configurar(usuario, InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.post(
            f"/panel/comunicados/{comunicado.id}/editar",
            data={"titulo": "Hackeado", "cuerpo": "Hackeado", "csrf_token": "cualquiera"},
        )

    assert response.status_code == 403
    assert repo.data[comunicado.id].titulo == "Título original"
