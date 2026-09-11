"""Tests de integración HTTP de GET/POST /panel/eventos/{id}/editar (4C-3), sin base de datos real."""

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


_FECHA_ORIGINAL = "2026-06-01T10:00:00"
_FECHA_NUEVA = "2026-12-15T18:30"
_FECHA_PASADA = "2020-01-01T10:00"


def _evento_original(autor_id: str = "autor-real-123") -> Evento:
    return Evento.create(
        titulo="Título original",
        descripcion="Descripción original",
        fecha_evento=_FECHA_ORIGINAL,
        lugar="Lugar original",
        autor_id=autor_id,
    )


# --- GET del formulario de edición ---


@pytest.mark.asyncio
async def test_get_editar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/eventos/{evento.id}/editar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_editar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/editar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_editar_con_autoridad_devuelve_200():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/editar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_editar_carga_datos_actuales():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/editar")

    body = response.text
    assert "Título original" in body
    assert "Descripción original" in body
    assert "Lugar original" in body
    assert "Editar evento" in body
    assert "Guardar cambios" in body


@pytest.mark.asyncio
async def test_get_editar_carga_fecha_sin_segundos():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/eventos/{evento.id}/editar")

    assert 'value="2026-06-01T10:00"' in response.text
    assert "2026-06-01T10:00:00" not in response.text


@pytest.mark.asyncio
async def test_get_editar_evento_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/eventos/id-inexistente/editar")

    assert response.status_code == 404


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_editar_redirige_303_a_listado_con_ok_editado():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "lugar": "Lugar editado",
                "csrf_token": csrf_token,
            },
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/eventos?ok=editado"


@pytest.mark.asyncio
async def test_post_editar_actualiza_titulo_descripcion_fecha_y_lugar():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "lugar": "Lugar editado",
                "csrf_token": csrf_token,
            },
        )

    actualizado = repo.data[evento.id]
    assert actualizado.titulo == "Título editado"
    assert actualizado.descripcion == "Descripción editada"
    assert actualizado.fecha_evento == _FECHA_NUEVA
    assert actualizado.lugar == "Lugar editado"


@pytest.mark.asyncio
async def test_post_editar_lugar_vacio_se_guarda_como_none():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "lugar": "   ",
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[evento.id].lugar is None


@pytest.mark.asyncio
async def test_post_editar_autor_id_permanece_intacto():
    usuario = _usuario()
    evento = _evento_original(autor_id="autor-real-123")
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[evento.id].autor_id == "autor-real-123"


@pytest.mark.asyncio
async def test_post_editar_created_at_permanece_intacto():
    usuario = _usuario()
    evento = _evento_original()
    created_at_original = evento.created_at
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[evento.id].created_at == created_at_original


@pytest.mark.asyncio
async def test_post_editar_updated_at_cambia():
    usuario = _usuario()
    evento = _evento_original()
    assert evento.updated_at is None
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[evento.id].updated_at is not None


@pytest.mark.asyncio
async def test_post_editar_autor_id_malicioso_no_altera_el_autor():
    usuario = _usuario()
    evento = _evento_original(autor_id="autor-real-123")
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[evento.id].autor_id == "autor-real-123"


@pytest.mark.asyncio
async def test_post_editar_fecha_pasada_es_valida():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título editado",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_PASADA,
                "csrf_token": csrf_token,
            },
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert repo.data[evento.id].fecha_evento == _FECHA_PASADA


# --- Validaciones (mismas reglas que crear) ---


@pytest.mark.asyncio
async def test_post_editar_titulo_vacio_devuelve_422_y_no_modifica():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "título es obligatorio" in response.text.lower()
    assert repo.data[evento.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_titulo_solo_espacios_devuelve_422():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "    ",
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert repo.data[evento.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_titulo_mayor_a_200_devuelve_422():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "x" * 201,
                "descripcion": "Descripción editada",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "200 caracteres" in response.text
    assert repo.data[evento.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_descripcion_vacia_devuelve_422():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título válido",
                "descripcion": "",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "descripción es obligatoria" in response.text.lower()
    assert repo.data[evento.id].descripcion == "Descripción original"


@pytest.mark.asyncio
async def test_post_editar_descripcion_solo_espacios_devuelve_422():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título válido",
                "descripcion": "   ",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert repo.data[evento.id].descripcion == "Descripción original"


@pytest.mark.asyncio
async def test_post_editar_fecha_invalida_devuelve_422():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Título válido",
                "descripcion": "Descripción válida",
                "fecha_evento": "no-es-una-fecha",
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 422
    assert "fecha" in response.text.lower()
    assert repo.data[evento.id].fecha_evento == _FECHA_ORIGINAL


@pytest.mark.asyncio
async def test_post_editar_error_conserva_valores_enviados():
    usuario = _usuario()
    evento = _evento_original()
    _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/eventos/{evento.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "",
                "descripcion": "Descripción a conservar",
                "fecha_evento": _FECHA_NUEVA,
                "lugar": "Lugar a conservar",
                "csrf_token": csrf_token,
            },
        )

    body = response.text
    assert "Descripción a conservar" in body
    assert "Lugar a conservar" in body
    assert _FECHA_NUEVA in body


# --- Evento inexistente en POST ---


@pytest.mark.asyncio
async def test_post_editar_evento_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # No hay GET previo posible (el evento no existe); generamos CSRF vía el form de "nuevo".
        form_response = await ac.get("/panel/eventos/nuevo")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/eventos/id-inexistente/editar",
            data={
                "titulo": "X",
                "descripcion": "Y",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": csrf_token,
            },
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


# --- Seguridad ---


@pytest.mark.asyncio
async def test_post_editar_csrf_incorrecto_devuelve_403_y_no_modifica():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/eventos/{evento.id}/editar")

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={
                "titulo": "Hackeado",
                "descripcion": "Hackeado",
                "fecha_evento": _FECHA_NUEVA,
                "csrf_token": "token-invalido",
            },
        )

    assert response.status_code == 403
    assert repo.data[evento.id].titulo == "Título original"


@pytest.mark.asyncio
async def test_post_editar_sin_csrf_token_no_modifica():
    usuario = _usuario()
    evento = _evento_original()
    repo = _configurar(usuario, InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/eventos/{evento.id}/editar")

        response = await ac.post(
            f"/panel/eventos/{evento.id}/editar",
            data={"titulo": "Hackeado", "descripcion": "Hackeado", "fecha_evento": _FECHA_NUEVA},
        )

    # Mismo comportamiento coherente con Noticias/Eventos: campo requerido faltante -> 422 de FastAPI.
    assert response.status_code == 422
    assert repo.data[evento.id].titulo == "Título original"
