"""Tests de integración de imágenes opcionales en el CRUD de Eventos (Etapa 4).

Mismo patrón que tests/test_noticia_imagenes.py (Etapa 3): casos de uso con
`LocalImageStorageGateway` real sobre `tmp_path`, y rutas HTTP del panel con
el gateway inyectado apuntando también a un directorio temporal. Nunca toca
`data/leads.db` ni `static/uploads/` real del proyecto.
"""

import io
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from src.application.dtos.content_management_dto import CrearEventoInput, EditarEventoInput
from src.application.gateways.image_storage_gateway import ImageValidationError
from src.application.use_cases.content.create_evento import CreateEventoUseCase
from src.application.use_cases.content.delete_evento import DeleteEventoUseCase
from src.application.use_cases.content.update_evento import UpdateEventoUseCase
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import (
    get_evento_repository,
    get_image_storage_gateway,
    get_usuario_repository,
)
from src.infrastructure.gateways.local_image_storage_gateway import LocalImageStorageGateway

_FECHA_EVENTO = "2027-05-20T18:00:00"


def _imagen_valida_bytes(formato: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), color="orange").save(buffer, format=formato)
    return buffer.getvalue()


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
        return list(self.data.values())

    async def update(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def delete(self, evento_id: str) -> None:
        self.data.pop(evento_id, None)


# ==============================================================================
# Nivel de casos de uso, con LocalImageStorageGateway real sobre tmp_path
# ==============================================================================


class TestCreacionConImagen:
    @pytest.mark.asyncio
    async def test_crear_sin_imagen_queda_none(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        evento = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Sin imagen", descripcion="Cuerpo", fecha_evento=_FECHA_EVENTO)
        )

        assert evento.imagen is None
        assert repo.data[evento.id].imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_valida_persiste_ruta_relativa_en_categoria_eventos(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())

        evento = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Con imagen", descripcion="Cuerpo", fecha_evento=_FECHA_EVENTO, imagen=ruta)
        )

        assert evento.imagen == ruta
        assert ruta.startswith("eventos/")
        assert (tmp_path / "uploads" / ruta).is_file()
        assert repo.data[evento.id].imagen == ruta

    @pytest.mark.asyncio
    async def test_gateway_rechaza_imagen_invalida_antes_de_crear(self, tmp_path: Path):
        """La validación del gateway sigue aplicándose: una imagen inválida nunca llega a persistirse."""
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        with pytest.raises(ImageValidationError):
            await gateway.save("eventos", "malware.jpg", "image/jpeg", b"no es una imagen real")


class TestEdicionConImagen:
    @pytest.mark.asyncio
    async def test_editar_sin_tocar_imagen_la_mantiene(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, imagen=ruta_original)
        )

        actualizado = await UpdateEventoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarEventoInput(id=creado.id, titulo="Editado", descripcion="Y", fecha_evento=_FECHA_EVENTO)
        )

        assert actualizado.imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_y_borra_la_anterior(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("eventos", "vieja.png", "image/png", _imagen_valida_bytes())
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, imagen=ruta_original)
        )

        ruta_nueva = await gateway.save("eventos", "nueva.png", "image/png", _imagen_valida_bytes())
        actualizado = await UpdateEventoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarEventoInput(
                id=creado.id, titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, imagen=ruta_nueva
            )
        )

        assert actualizado.imagen == ruta_nueva
        assert (tmp_path / "uploads" / ruta_nueva).is_file()
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_quita_imagen_explicitamente(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, imagen=ruta_original)
        )

        actualizado = await UpdateEventoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarEventoInput(
                id=creado.id, titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, quitar_imagen=True
            )
        )

        assert actualizado.imagen is None
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_fallo_de_imagen_nueva_no_afecta_la_imagen_anterior(self, tmp_path: Path):
        """Si la nueva imagen es inválida, el gateway la rechaza antes de guardar nada:
        la imagen anterior nunca se toca porque el use case ni siquiera llega a ejecutarse."""
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO, imagen=ruta_original)
        )

        with pytest.raises(ImageValidationError):
            await gateway.save("eventos", "invalida.png", "image/png", b"contenido invalido")

        # La entidad y el archivo original siguen intactos: el use case nunca se llamó.
        assert repo.data[creado.id].imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()


class TestEliminacionConImagen:
    @pytest.mark.asyncio
    async def test_eliminar_evento_con_imagen_borra_el_archivo(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="A", descripcion="B", fecha_evento=_FECHA_EVENTO, imagen=ruta)
        )

        await DeleteEventoUseCase(repository=repo, image_gateway=gateway).execute(creado.id)

        assert creado.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_eliminar_evento_sin_imagen_es_seguro(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        creado = await CreateEventoUseCase(repository=repo).execute(
            CrearEventoInput(titulo="A", descripcion="B", fecha_evento=_FECHA_EVENTO)
        )

        await DeleteEventoUseCase(repository=repo, image_gateway=gateway).execute(creado.id)  # No debe lanzar.

        assert creado.id not in repo.data

    @pytest.mark.asyncio
    async def test_eliminar_evento_inexistente_mantiene_comportamiento_idempotente(self, tmp_path: Path):
        repo = InMemoryEventoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        await DeleteEventoUseCase(repository=repo, image_gateway=gateway).execute("no-existe")  # No debe lanzar.


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


def _configurar(usuario: Usuario, tmp_path: Path, repo: InMemoryEventoRepo | None = None) -> InMemoryEventoRepo:
    repo = repo or InMemoryEventoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_evento_repository] = lambda: repo
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
            form_response = await ac.get("/panel/eventos/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/eventos/nuevo",
                data={
                    "titulo": "Con imagen",
                    "descripcion": "Cuerpo",
                    "fecha_evento": _FECHA_EVENTO,
                    "csrf_token": csrf_token,
                },
                files={"imagen": ("foto.png", _imagen_valida_bytes(), "image/png")},
                follow_redirects=False,
            )

        assert response.status_code == 303
        evento_creado = next(iter(repo.data.values()))
        assert evento_creado.imagen is not None
        assert evento_creado.imagen.startswith("eventos/")
        assert (tmp_path / "uploads" / evento_creado.imagen).is_file()

    @pytest.mark.asyncio
    async def test_crear_sin_archivo_seleccionado_queda_sin_imagen(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/eventos/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/eventos/nuevo",
                data={
                    "titulo": "Sin imagen",
                    "descripcion": "Cuerpo",
                    "fecha_evento": _FECHA_EVENTO,
                    "csrf_token": csrf_token,
                },
                follow_redirects=False,
            )

        assert response.status_code == 303
        evento_creado = next(iter(repo.data.values()))
        assert evento_creado.imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_invalida_muestra_error_y_no_crea(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/eventos/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/eventos/nuevo",
                data={
                    "titulo": "Título",
                    "descripcion": "Cuerpo",
                    "fecha_evento": _FECHA_EVENTO,
                    "csrf_token": csrf_token,
                },
                files={"imagen": ("malware.jpg", b"contenido que no es una imagen", "image/jpeg")},
            )

        assert response.status_code == 422
        assert len(repo.data) == 0


class TestRutaEditarConImagen:
    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_por_http(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("eventos", "vieja.png", "image/png", _imagen_valida_bytes())
        existente = Evento.create(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO)
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryEventoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/eventos/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)
            assert f"/static/uploads/{ruta_original}" in form_response.text

            response = await ac.post(
                f"/panel/eventos/{existente.id}/editar",
                data={
                    "titulo": "Original",
                    "descripcion": "X",
                    "fecha_evento": _FECHA_EVENTO,
                    "csrf_token": csrf_token,
                },
                files={"imagen": ("nueva.png", _imagen_valida_bytes(), "image/png")},
                follow_redirects=False,
            )

        assert response.status_code == 303
        actualizado = repo.data[existente.id]
        assert actualizado.imagen is not None
        assert actualizado.imagen != ruta_original
        assert (tmp_path / "uploads" / actualizado.imagen).is_file()
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_quita_imagen_por_http(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Evento.create(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO)
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryEventoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/eventos/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/eventos/{existente.id}/editar",
                data={
                    "titulo": "Original",
                    "descripcion": "X",
                    "fecha_evento": _FECHA_EVENTO,
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
        ruta_original = await gateway_previo.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Evento.create(titulo="Original", descripcion="X", fecha_evento=_FECHA_EVENTO)
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryEventoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/eventos/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/eventos/{existente.id}/editar",
                data={
                    "titulo": "Editado",
                    "descripcion": "Y",
                    "fecha_evento": _FECHA_EVENTO,
                    "csrf_token": csrf_token,
                },
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
        ruta = await gateway_previo.save("eventos", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Evento.create(titulo="A", descripcion="B", fecha_evento=_FECHA_EVENTO)
        existente.imagen = ruta
        repo = _configurar(usuario, tmp_path, InMemoryEventoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            confirm_response = await ac.get(f"/panel/eventos/{existente.id}/eliminar")
            csrf_token = _extraer_csrf_token(confirm_response.text)

            response = await ac.post(
                f"/panel/eventos/{existente.id}/eliminar",
                data={"csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert existente.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()
