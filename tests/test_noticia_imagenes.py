"""Tests de integración de imágenes opcionales en el CRUD de Noticias (Etapa 3).

Cubren dos niveles:
- Casos de uso (Create/Update/Delete) con `LocalImageStorageGateway` real
  sobre un directorio temporal de pytest (`tmp_path`) — verifica el ciclo de
  vida real del archivo en disco sin tocar `static/uploads/` del proyecto.
- Rutas HTTP del panel (`/panel/noticias/...`) vía `httpx.AsyncClient`,
  también con el gateway apuntando a un directorio temporal inyectado por
  override de dependencia — nunca `data/leads.db` ni archivos reales.
"""

import io
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from src.application.dtos.content_management_dto import CrearNoticiaInput, EditarNoticiaInput
from src.application.gateways.image_storage_gateway import ImageValidationError
from src.application.use_cases.content.create_noticia import CreateNoticiaUseCase
from src.application.use_cases.content.delete_noticia import DeleteNoticiaUseCase
from src.application.use_cases.content.update_noticia import UpdateNoticiaUseCase
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import (
    get_image_storage_gateway,
    get_noticia_repository,
    get_usuario_repository,
)
from src.infrastructure.gateways.local_image_storage_gateway import LocalImageStorageGateway


def _imagen_valida_bytes(formato: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), color="green").save(buffer, format=formato)
    return buffer.getvalue()


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


# ==============================================================================
# Nivel de casos de uso, con LocalImageStorageGateway real sobre tmp_path
# ==============================================================================


class TestCreacionConImagen:
    @pytest.mark.asyncio
    async def test_crear_sin_imagen_queda_none(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        noticia = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Sin imagen", cuerpo="Cuerpo")
        )

        assert noticia.imagen is None
        assert repo.data[noticia.id].imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_valida_persiste_ruta_relativa(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())

        noticia = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Con imagen", cuerpo="Cuerpo", imagen=ruta)
        )

        assert noticia.imagen == ruta
        assert (tmp_path / "uploads" / ruta).is_file()
        assert repo.data[noticia.id].imagen == ruta

    @pytest.mark.asyncio
    async def test_gateway_rechaza_imagen_invalida_antes_de_crear(self, tmp_path: Path):
        """La validación del gateway sigue aplicándose: una imagen inválida nunca llega a persistirse."""
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        with pytest.raises(ImageValidationError):
            await gateway.save("noticias", "malware.jpg", "image/jpeg", b"no es una imagen real")


class TestEdicionConImagen:
    @pytest.mark.asyncio
    async def test_editar_sin_tocar_imagen_la_mantiene(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        creada = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        actualizada = await UpdateNoticiaUseCase(repository=repo, image_gateway=gateway).execute(
            EditarNoticiaInput(id=creada.id, titulo="Editado", cuerpo="Y")
        )

        assert actualizada.imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_y_borra_la_anterior(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("noticias", "vieja.png", "image/png", _imagen_valida_bytes())
        creada = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        ruta_nueva = await gateway.save("noticias", "nueva.png", "image/png", _imagen_valida_bytes())
        actualizada = await UpdateNoticiaUseCase(repository=repo, image_gateway=gateway).execute(
            EditarNoticiaInput(id=creada.id, titulo="Original", cuerpo="X", imagen=ruta_nueva)
        )

        assert actualizada.imagen == ruta_nueva
        assert (tmp_path / "uploads" / ruta_nueva).is_file()
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_quita_imagen_explicitamente(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        creada = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        actualizada = await UpdateNoticiaUseCase(repository=repo, image_gateway=gateway).execute(
            EditarNoticiaInput(id=creada.id, titulo="Original", cuerpo="X", quitar_imagen=True)
        )

        assert actualizada.imagen is None
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_fallo_de_imagen_nueva_no_afecta_la_imagen_anterior(self, tmp_path: Path):
        """Si la nueva imagen es inválida, el gateway la rechaza antes de guardar nada:
        la imagen anterior nunca se toca porque el use case ni siquiera llega a ejecutarse."""
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        creada = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        with pytest.raises(ImageValidationError):
            await gateway.save("noticias", "invalida.png", "image/png", b"contenido invalido")

        # La entidad y el archivo original siguen intactos: el use case nunca se llamó.
        assert repo.data[creada.id].imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()


class TestEliminacionConImagen:
    @pytest.mark.asyncio
    async def test_eliminar_noticia_con_imagen_borra_el_archivo(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        creada = await CreateNoticiaUseCase(repository=repo).execute(
            CrearNoticiaInput(titulo="A", cuerpo="B", imagen=ruta)
        )

        await DeleteNoticiaUseCase(repository=repo, image_gateway=gateway).execute(creada.id)

        assert creada.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_eliminar_noticia_sin_imagen_es_seguro(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        creada = await CreateNoticiaUseCase(repository=repo).execute(CrearNoticiaInput(titulo="A", cuerpo="B"))

        await DeleteNoticiaUseCase(repository=repo, image_gateway=gateway).execute(creada.id)  # No debe lanzar.

        assert creada.id not in repo.data

    @pytest.mark.asyncio
    async def test_eliminar_noticia_inexistente_es_idempotente(self, tmp_path: Path):
        repo = InMemoryNoticiaRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        await DeleteNoticiaUseCase(repository=repo, image_gateway=gateway).execute("no-existe")  # No debe lanzar.


# ==============================================================================
# Nivel HTTP: rutas del panel, con el gateway apuntando a tmp_path
# ==============================================================================


def _usuario(rol: str = "autoridad") -> Usuario:
    from src.infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher

    hasher = BcryptPasswordHasher()
    return Usuario.create(
        email="directora@isft199.edu.ar",
        password_hash=hasher.hash("clave-segura-123"),
        nombre="Directora",
        is_active=True,
        rol=rol,
    )


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


def _configurar(usuario: Usuario, tmp_path: Path, repo: InMemoryNoticiaRepo | None = None) -> InMemoryNoticiaRepo:
    repo = repo or InMemoryNoticiaRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_noticia_repository] = lambda: repo
    app.dependency_overrides[get_image_storage_gateway] = lambda: LocalImageStorageGateway(
        base_dir=tmp_path / "uploads"
    )
    return repo


class TestRutaCrearConImagen:
    @pytest.mark.asyncio
    async def test_crear_con_imagen_valida_persiste_ruta(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/noticias/nueva")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/noticias/nueva",
                data={"titulo": "Con imagen", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                files={"imagen": ("foto.png", _imagen_valida_bytes(), "image/png")},
                follow_redirects=False,
            )

        assert response.status_code == 303
        noticia_creada = next(iter(repo.data.values()))
        assert noticia_creada.imagen is not None
        assert noticia_creada.imagen.startswith("noticias/")
        assert (tmp_path / "uploads" / noticia_creada.imagen).is_file()

    @pytest.mark.asyncio
    async def test_crear_sin_archivo_seleccionado_queda_sin_imagen(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/noticias/nueva")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/noticias/nueva",
                data={"titulo": "Sin imagen", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        noticia_creada = next(iter(repo.data.values()))
        assert noticia_creada.imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_invalida_muestra_error_y_no_crea(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/noticias/nueva")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/noticias/nueva",
                data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                files={"imagen": ("malware.jpg", b"contenido que no es una imagen", "image/jpeg")},
            )

        assert response.status_code == 422
        assert len(repo.data) == 0


class TestRutaEditarConImagen:
    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_por_http(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("noticias", "vieja.png", "image/png", _imagen_valida_bytes())
        existente = Noticia.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryNoticiaRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/noticias/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)
            assert f"/static/uploads/{ruta_original}" in form_response.text

            response = await ac.post(
                f"/panel/noticias/{existente.id}/editar",
                data={"titulo": "Original", "cuerpo": "X", "csrf_token": csrf_token},
                files={"imagen": ("nueva.png", _imagen_valida_bytes(), "image/png")},
                follow_redirects=False,
            )

        assert response.status_code == 303
        actualizada = repo.data[existente.id]
        assert actualizada.imagen is not None
        assert actualizada.imagen != ruta_original
        assert (tmp_path / "uploads" / actualizada.imagen).is_file()
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_quita_imagen_por_http(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Noticia.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryNoticiaRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/noticias/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/noticias/{existente.id}/editar",
                data={
                    "titulo": "Original",
                    "cuerpo": "X",
                    "quitar_imagen": "on",
                    "csrf_token": csrf_token,
                },
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert repo.data[existente.id].imagen is None
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_sin_cambios_de_imagen_la_conserva(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Noticia.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryNoticiaRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/noticias/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/noticias/{existente.id}/editar",
                data={"titulo": "Editado", "cuerpo": "Y", "csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert repo.data[existente.id].imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()


class TestRutaEliminarConImagen:
    @pytest.mark.asyncio
    async def test_eliminar_por_http_borra_el_archivo(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway_previo.save("noticias", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Noticia.create(titulo="A", cuerpo="B")
        existente.imagen = ruta
        repo = _configurar(usuario, tmp_path, InMemoryNoticiaRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            confirm_response = await ac.get(f"/panel/noticias/{existente.id}/eliminar")
            csrf_token = _extraer_csrf_token(confirm_response.text)

            response = await ac.post(
                f"/panel/noticias/{existente.id}/eliminar",
                data={"csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert existente.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()
