"""Tests de integración de imágenes opcionales en el CRUD de Comunicados (Etapa 5).

Mismo patrón que tests/test_noticia_imagenes.py (Etapa 3) y
tests/test_evento_imagenes.py (Etapa 4): casos de uso con
`LocalImageStorageGateway` real sobre `tmp_path`, y rutas HTTP del panel con
el gateway inyectado apuntando también a un directorio temporal. Nunca toca
`data/leads.db` ni `static/uploads/` real del proyecto.
"""

import io
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from src.application.dtos.content_management_dto import CrearComunicadoInput, EditarComunicadoInput
from src.application.gateways.image_storage_gateway import ImageValidationError
from src.application.use_cases.content.create_comunicado import CreateComunicadoUseCase
from src.application.use_cases.content.delete_comunicado import DeleteComunicadoUseCase
from src.application.use_cases.content.update_comunicado import UpdateComunicadoUseCase
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import (
    get_comunicado_repository,
    get_image_storage_gateway,
    get_usuario_repository,
)
from src.infrastructure.gateways.local_image_storage_gateway import LocalImageStorageGateway


def _imagen_valida_bytes(formato: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), color="purple").save(buffer, format=formato)
    return buffer.getvalue()


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


# ==============================================================================
# Nivel de casos de uso, con LocalImageStorageGateway real sobre tmp_path
# ==============================================================================


class TestCreacionConImagen:
    @pytest.mark.asyncio
    async def test_crear_sin_imagen_queda_none(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        comunicado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Sin imagen", cuerpo="Cuerpo")
        )

        assert comunicado.imagen is None
        assert repo.data[comunicado.id].imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_valida_persiste_ruta_relativa_en_categoria_comunicados(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())

        comunicado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Con imagen", cuerpo="Cuerpo", imagen=ruta)
        )

        assert comunicado.imagen == ruta
        assert ruta.startswith("comunicados/")
        assert (tmp_path / "uploads" / ruta).is_file()
        assert repo.data[comunicado.id].imagen == ruta

    @pytest.mark.asyncio
    async def test_gateway_rechaza_imagen_invalida_antes_de_crear(self, tmp_path: Path):
        """La validación del gateway sigue aplicándose: una imagen inválida nunca llega a persistirse."""
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        with pytest.raises(ImageValidationError):
            await gateway.save("comunicados", "malware.jpg", "image/jpeg", b"no es una imagen real")


class TestEdicionConImagen:
    @pytest.mark.asyncio
    async def test_editar_sin_tocar_imagen_la_mantiene(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        actualizado = await UpdateComunicadoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarComunicadoInput(id=creado.id, titulo="Editado", cuerpo="Y")
        )

        assert actualizado.imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_y_borra_la_anterior(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("comunicados", "vieja.png", "image/png", _imagen_valida_bytes())
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        ruta_nueva = await gateway.save("comunicados", "nueva.png", "image/png", _imagen_valida_bytes())
        actualizado = await UpdateComunicadoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarComunicadoInput(id=creado.id, titulo="Original", cuerpo="X", imagen=ruta_nueva)
        )

        assert actualizado.imagen == ruta_nueva
        assert (tmp_path / "uploads" / ruta_nueva).is_file()
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_quita_imagen_explicitamente(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        actualizado = await UpdateComunicadoUseCase(repository=repo, image_gateway=gateway).execute(
            EditarComunicadoInput(id=creado.id, titulo="Original", cuerpo="X", quitar_imagen=True)
        )

        assert actualizado.imagen is None
        assert not (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_fallo_de_imagen_nueva_no_afecta_la_imagen_anterior(self, tmp_path: Path):
        """Si la nueva imagen es inválida, el gateway la rechaza antes de guardar nada:
        la imagen anterior nunca se toca porque el use case ni siquiera llega a ejecutarse."""
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="Original", cuerpo="X", imagen=ruta_original)
        )

        with pytest.raises(ImageValidationError):
            await gateway.save("comunicados", "invalida.png", "image/png", b"contenido invalido")

        # La entidad y el archivo original siguen intactos: el use case nunca se llamó.
        assert repo.data[creado.id].imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()


class TestEliminacionConImagen:
    @pytest.mark.asyncio
    async def test_eliminar_comunicado_con_imagen_borra_el_archivo(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="A", cuerpo="B", imagen=ruta)
        )

        await DeleteComunicadoUseCase(repository=repo, image_gateway=gateway).execute(creado.id)

        assert creado.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_eliminar_comunicado_sin_imagen_es_seguro(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        creado = await CreateComunicadoUseCase(repository=repo).execute(
            CrearComunicadoInput(titulo="A", cuerpo="B")
        )

        await DeleteComunicadoUseCase(repository=repo, image_gateway=gateway).execute(creado.id)  # No debe lanzar.

        assert creado.id not in repo.data

    @pytest.mark.asyncio
    async def test_eliminar_comunicado_inexistente_es_idempotente(self, tmp_path: Path):
        repo = InMemoryComunicadoRepo()
        gateway = LocalImageStorageGateway(base_dir=tmp_path / "uploads")

        await DeleteComunicadoUseCase(repository=repo, image_gateway=gateway).execute("no-existe")  # No debe lanzar.


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


def _configurar(
    usuario: Usuario, tmp_path: Path, repo: InMemoryComunicadoRepo | None = None
) -> InMemoryComunicadoRepo:
    repo = repo or InMemoryComunicadoRepo()
    app.dependency_overrides[get_usuario_repository] = lambda: InMemoryUsuarioRepo([usuario])
    app.dependency_overrides[get_comunicado_repository] = lambda: repo
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
            form_response = await ac.get("/panel/comunicados/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/comunicados/nuevo",
                data={"titulo": "Con imagen", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                files={"imagen": ("foto.png", _imagen_valida_bytes(), "image/png")},
                follow_redirects=False,
            )

        assert response.status_code == 303
        comunicado_creado = next(iter(repo.data.values()))
        assert comunicado_creado.imagen is not None
        assert comunicado_creado.imagen.startswith("comunicados/")
        assert (tmp_path / "uploads" / comunicado_creado.imagen).is_file()

    @pytest.mark.asyncio
    async def test_crear_sin_archivo_seleccionado_queda_sin_imagen(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/comunicados/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/comunicados/nuevo",
                data={"titulo": "Sin imagen", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        comunicado_creado = next(iter(repo.data.values()))
        assert comunicado_creado.imagen is None

    @pytest.mark.asyncio
    async def test_crear_con_imagen_invalida_muestra_error_y_no_crea(self, tmp_path: Path):
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get("/panel/comunicados/nuevo")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                "/panel/comunicados/nuevo",
                data={"titulo": "Título", "cuerpo": "Cuerpo", "csrf_token": csrf_token},
                files={"imagen": ("malware.jpg", b"contenido que no es una imagen", "image/jpeg")},
            )

        assert response.status_code == 422
        assert len(repo.data) == 0

    @pytest.mark.asyncio
    async def test_crear_sin_sesion_redirige_a_login(self, tmp_path: Path):
        """Acceso no autorizado: sin sesión, la ruta protegida redirige al login (no crea nada)."""
        usuario = _usuario()
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            response = await ac.get("/panel/comunicados/nuevo", follow_redirects=False)

        assert response.status_code == 303
        assert response.headers["location"] == "/panel/login"
        assert len(repo.data) == 0

    @pytest.mark.asyncio
    async def test_crear_con_rol_no_autorizado_devuelve_403(self, tmp_path: Path):
        """Acceso no autorizado: un usuario sin rol autoridad no puede crear comunicados con imagen."""
        usuario = _usuario(rol="editor")
        repo = _configurar(usuario, tmp_path)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            response = await ac.post(
                "/panel/comunicados/nuevo",
                data={"titulo": "Título", "cuerpo": "Cuerpo"},
                files={"imagen": ("foto.png", _imagen_valida_bytes(), "image/png")},
            )

        assert response.status_code == 403
        assert len(repo.data) == 0


class TestRutaEditarConImagen:
    @pytest.mark.asyncio
    async def test_editar_reemplaza_imagen_por_http(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("comunicados", "vieja.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/comunicados/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)
            assert f"/static/uploads/{ruta_original}" in form_response.text

            response = await ac.post(
                f"/panel/comunicados/{existente.id}/editar",
                data={"titulo": "Original", "cuerpo": "X", "csrf_token": csrf_token},
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
        ruta_original = await gateway_previo.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/comunicados/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/comunicados/{existente.id}/editar",
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
        ruta_original = await gateway_previo.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            form_response = await ac.get(f"/panel/comunicados/{existente.id}/editar")
            csrf_token = _extraer_csrf_token(form_response.text)

            response = await ac.post(
                f"/panel/comunicados/{existente.id}/editar",
                data={"titulo": "Editado", "cuerpo": "Y", "csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert repo.data[existente.id].imagen == ruta_original
        assert (tmp_path / "uploads" / ruta_original).is_file()

    @pytest.mark.asyncio
    async def test_editar_sin_sesion_redirige_a_login(self, tmp_path: Path):
        """Acceso no autorizado: sin sesión, editar redirige a login sin tocar la imagen existente."""
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta_original = await gateway_previo.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="Original", cuerpo="X")
        existente.imagen = ruta_original
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            response = await ac.get(f"/panel/comunicados/{existente.id}/editar", follow_redirects=False)

        assert response.status_code == 303
        assert response.headers["location"] == "/panel/login"
        assert repo.data[existente.id].imagen == ruta_original


class TestRutaEliminarConImagen:
    @pytest.mark.asyncio
    async def test_eliminar_por_http_borra_el_archivo(self, tmp_path: Path):
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway_previo.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="A", cuerpo="B")
        existente.imagen = ruta
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            await _login(ac, usuario)
            confirm_response = await ac.get(f"/panel/comunicados/{existente.id}/eliminar")
            csrf_token = _extraer_csrf_token(confirm_response.text)

            response = await ac.post(
                f"/panel/comunicados/{existente.id}/eliminar",
                data={"csrf_token": csrf_token},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert existente.id not in repo.data
        assert not (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_eliminar_sin_sesion_redirige_a_login_y_no_borra_nada(self, tmp_path: Path):
        """Acceso no autorizado: sin sesión, no se elimina el comunicado ni su imagen."""
        usuario = _usuario()
        gateway_previo = LocalImageStorageGateway(base_dir=tmp_path / "uploads")
        ruta = await gateway_previo.save("comunicados", "foto.png", "image/png", _imagen_valida_bytes())
        existente = Comunicado.create(titulo="A", cuerpo="B")
        existente.imagen = ruta
        repo = _configurar(usuario, tmp_path, InMemoryComunicadoRepo([existente]))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://test") as ac:
            response = await ac.post(
                f"/panel/comunicados/{existente.id}/eliminar",
                data={"csrf_token": "no-importa-sin-sesion"},
                follow_redirects=False,
            )

        assert response.status_code == 303
        assert response.headers["location"] == "/panel/login"
        assert existente.id in repo.data
        assert (tmp_path / "uploads" / ruta).is_file()
