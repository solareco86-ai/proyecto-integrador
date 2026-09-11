"""Tests de integración HTTP de GET/POST /panel/noticias/{id}/editar (4B-3), sin base de datos real."""

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


# --- GET del formulario de edición ---


@pytest.mark.asyncio
async def test_get_editar_sin_sesion_redirige_a_login():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo", autor_id=usuario.id)
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/panel/noticias/{noticia.id}/editar", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/login"


@pytest.mark.asyncio
async def test_get_editar_con_rol_no_autorizado_devuelve_403():
    usuario = _usuario(rol="editor")
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/editar")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_editar_noticia_existente_devuelve_200():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/editar")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_editar_carga_valores_actuales():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Título original", cuerpo="Cuerpo original", publicada=False)
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get(f"/panel/noticias/{noticia.id}/editar")

    body = response.text
    assert "Título original" in body
    assert "Cuerpo original" in body
    assert "Editar noticia" in body
    assert "Guardar cambios" in body
    # publicada=False -> el checkbox no debe aparecer marcado
    assert "checked" not in body.split('name="publicada"')[1].split(">")[0]


@pytest.mark.asyncio
async def test_get_editar_noticia_inexistente_devuelve_404():
    usuario = _usuario()
    _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias/id-inexistente/editar")

    assert response.status_code == 404


# --- POST válido ---


@pytest.mark.asyncio
async def test_post_editar_actualiza_titulo_y_cuerpo():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Título editado", "cuerpo": "Cuerpo editado", "csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    actualizada = repo.data[noticia.id]
    assert actualizada.titulo == "Título editado"
    assert actualizada.cuerpo == "Cuerpo editado"


@pytest.mark.asyncio
async def test_post_editar_permite_publicada_true_a_false():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo", publicada=True)
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Original", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
        )

    assert repo.data[noticia.id].publicada is False


@pytest.mark.asyncio
async def test_post_editar_permite_publicada_false_a_true():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo", publicada=False)
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Original", "cuerpo": "Cuerpo", "publicada": "on", "csrf_token": csrf_token},
        )

    assert repo.data[noticia.id].publicada is True


@pytest.mark.asyncio
async def test_post_editar_redirige_303_a_listado_con_ok_editada():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Editado", "cuerpo": "Editado", "csrf_token": csrf_token},
            follow_redirects=False,
        )

    assert response.status_code == 303
    assert response.headers["location"] == "/panel/noticias?ok=editada"


@pytest.mark.asyncio
async def test_listado_muestra_mensaje_de_edicion_exitosa():
    usuario = _usuario()
    _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        response = await ac.get("/panel/noticias?ok=editada")

    assert "editada correctamente" in response.text.lower()


# --- Validaciones (mismas reglas que crear) ---


@pytest.mark.asyncio
async def test_post_editar_titulo_vacio_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "título es obligatorio" in response.text.lower()
    assert repo.data[noticia.id].titulo == "Original"


@pytest.mark.asyncio
async def test_post_editar_titulo_solo_espacios_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "    ", "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert repo.data[noticia.id].titulo == "Original"


@pytest.mark.asyncio
async def test_post_editar_titulo_mayor_a_200_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "x" * 201, "cuerpo": "Cuerpo válido", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "200 caracteres" in response.text
    assert repo.data[noticia.id].titulo == "Original"


@pytest.mark.asyncio
async def test_post_editar_cuerpo_vacio_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Título válido", "cuerpo": "", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert "cuerpo es obligatorio" in response.text.lower()
    assert repo.data[noticia.id].cuerpo == "Cuerpo original"


@pytest.mark.asyncio
async def test_post_editar_cuerpo_solo_espacios_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Título válido", "cuerpo": "   ", "csrf_token": csrf_token},
        )

    assert response.status_code == 422
    assert repo.data[noticia.id].cuerpo == "Cuerpo original"


# --- Noticia inexistente en POST ---


@pytest.mark.asyncio
async def test_post_editar_noticia_inexistente_devuelve_404():
    usuario = _usuario()
    repo = _configurar(usuario, InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        # No hay GET previo (la noticia no existe), pero necesitamos un token CSRF válido en sesión:
        await ac.get("/panel/noticias")  # no genera csrf; usamos el de un GET de nueva
        form_response = await ac.get("/panel/noticias/nueva")
        csrf_token = _extraer_csrf_token(form_response.text)

        response = await ac.post(
            "/panel/noticias/id-inexistente/editar",
            data={"titulo": "X", "cuerpo": "Y", "csrf_token": csrf_token},
        )

    assert response.status_code == 404
    assert len(repo.data) == 0


# --- Seguridad ---


@pytest.mark.asyncio
async def test_post_editar_csrf_incorrecto_devuelve_403():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/noticias/{noticia.id}/editar")

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Hackeado", "cuerpo": "Hackeado", "csrf_token": "token-invalido"},
        )

    assert response.status_code == 403
    assert repo.data[noticia.id].titulo == "Original"


@pytest.mark.asyncio
async def test_post_editar_sin_csrf_token_no_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo original")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        await ac.get(f"/panel/noticias/{noticia.id}/editar")

        response = await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Hackeado", "cuerpo": "Hackeado"},
        )

    assert response.status_code == 422  # mismo comportamiento coherente con 4B-2: campo requerido faltante
    assert repo.data[noticia.id].titulo == "Original"


@pytest.mark.asyncio
async def test_post_editar_autor_id_malicioso_no_modifica_autor_real():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo", autor_id="autor-real-123")
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={
                "titulo": "Editado",
                "cuerpo": "Editado",
                "autor_id": "id-falso-inventado-por-el-cliente",
                "csrf_token": csrf_token,
            },
        )

    assert repo.data[noticia.id].autor_id == "autor-real-123"


@pytest.mark.asyncio
async def test_post_editar_created_at_no_cambia():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    created_at_original = noticia.created_at
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Editado", "cuerpo": "Editado", "csrf_token": csrf_token},
        )

    assert repo.data[noticia.id].created_at == created_at_original


@pytest.mark.asyncio
async def test_post_editar_updated_at_se_actualiza():
    usuario = _usuario()
    noticia = Noticia.create(titulo="Original", cuerpo="Cuerpo")
    assert noticia.updated_at is None
    repo = _configurar(usuario, InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        await _login(ac, usuario)
        form_response = await ac.get(f"/panel/noticias/{noticia.id}/editar")
        csrf_token = _extraer_csrf_token(form_response.text)

        await ac.post(
            f"/panel/noticias/{noticia.id}/editar",
            data={"titulo": "Editado", "cuerpo": "Editado", "csrf_token": csrf_token},
        )

    assert repo.data[noticia.id].updated_at is not None
