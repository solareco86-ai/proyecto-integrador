"""Tests aislados de LocalImageStorageGateway: validaciones, seguridad y almacenamiento.

Usan exclusivamente directorios temporales de pytest (`tmp_path`) — nunca
tocan `data/leads.db` ni `static/uploads/` real del proyecto.
"""

import io
from pathlib import Path

import pytest
from PIL import Image

from src.application.gateways.image_storage_gateway import ImageStorageGateway, ImageValidationError
from src.infrastructure.gateways.local_image_storage_gateway import LocalImageStorageGateway


def _imagen_valida_bytes(formato: str) -> bytes:
    """Genera bytes de una imagen real y válida en el formato Pillow indicado."""
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), color="blue").save(buffer, format=formato)
    return buffer.getvalue()


class FakeImageStorageGateway(ImageStorageGateway):
    """Almacén en memoria, sin tocar disco, para tests de casos de uso que dependan del gateway."""

    def __init__(self) -> None:
        self.guardadas: dict[str, bytes] = {}

    async def save(self, category: str, filename: str, content_type: str | None, file_bytes: bytes) -> str:
        ruta = f"{category}/fake-{len(self.guardadas)}.jpg"
        self.guardadas[ruta] = file_bytes
        return ruta

    async def delete(self, ruta_relativa: str | None) -> None:
        if ruta_relativa is not None:
            self.guardadas.pop(ruta_relativa, None)


@pytest.fixture
def gateway(tmp_path: Path) -> LocalImageStorageGateway:
    return LocalImageStorageGateway(base_dir=tmp_path / "uploads")


class TestGuardarImagenValida:
    @pytest.mark.asyncio
    async def test_guarda_jpeg_y_devuelve_ruta_relativa(self, gateway: LocalImageStorageGateway, tmp_path: Path):
        contenido = _imagen_valida_bytes("JPEG")

        ruta = await gateway.save("noticias", "foto.jpg", "image/jpeg", contenido)

        assert ruta.startswith("noticias/")
        assert ruta.endswith(".jpg")
        assert (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_guarda_png(self, gateway: LocalImageStorageGateway, tmp_path: Path):
        contenido = _imagen_valida_bytes("PNG")

        ruta = await gateway.save("eventos", "afiche.png", "image/png", contenido)

        assert ruta.startswith("eventos/")
        assert ruta.endswith(".png")
        assert (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_guarda_webp(self, gateway: LocalImageStorageGateway, tmp_path: Path):
        contenido = _imagen_valida_bytes("WEBP")

        ruta = await gateway.save("comunicados", "banner.webp", "image/webp", contenido)

        assert ruta.startswith("comunicados/")
        assert ruta.endswith(".webp")
        assert (tmp_path / "uploads" / ruta).is_file()

    @pytest.mark.asyncio
    async def test_archivo_creado_dentro_del_directorio_de_categoria(
        self, gateway: LocalImageStorageGateway, tmp_path: Path
    ):
        contenido = _imagen_valida_bytes("PNG")

        ruta = await gateway.save("noticias", "foto.png", "image/png", contenido)
        archivo = tmp_path / "uploads" / ruta

        assert archivo.parent == tmp_path / "uploads" / "noticias"
        assert archivo.read_bytes() == contenido

    @pytest.mark.asyncio
    async def test_nombre_generado_no_usa_el_nombre_original(self, gateway: LocalImageStorageGateway):
        contenido = _imagen_valida_bytes("JPEG")

        ruta = await gateway.save("noticias", "nombre-original-del-usuario.jpg", "image/jpeg", contenido)

        assert "nombre-original-del-usuario" not in ruta


class TestValidaciones:
    @pytest.mark.asyncio
    async def test_rechaza_extension_no_permitida(self, gateway: LocalImageStorageGateway):
        contenido = _imagen_valida_bytes("PNG")

        with pytest.raises(ImageValidationError, match="[Ee]xtensión"):
            await gateway.save("noticias", "imagen.gif", "image/png", contenido)

    @pytest.mark.asyncio
    async def test_rechaza_content_type_no_permitido(self, gateway: LocalImageStorageGateway):
        contenido = _imagen_valida_bytes("PNG")

        with pytest.raises(ImageValidationError, match="contenido"):
            await gateway.save("noticias", "imagen.png", "application/octet-stream", contenido)

    @pytest.mark.asyncio
    async def test_rechaza_archivo_que_no_es_imagen_real(self, gateway: LocalImageStorageGateway):
        contenido_falso = b"esto no es una imagen, son bytes cualquiera" * 10

        with pytest.raises(ImageValidationError, match="v[aá]lida|corrupto"):
            await gateway.save("noticias", "imagen.jpg", "image/jpeg", contenido_falso)

    @pytest.mark.asyncio
    async def test_rechaza_mismatch_entre_content_type_y_contenido_real(self, gateway: LocalImageStorageGateway):
        """Un PNG real declarado como image/jpeg debe rechazarse (no confiar solo en el header)."""
        contenido_png_real = _imagen_valida_bytes("PNG")

        with pytest.raises(ImageValidationError):
            await gateway.save("noticias", "imagen.jpg", "image/jpeg", contenido_png_real)

    @pytest.mark.asyncio
    async def test_rechaza_archivo_que_supera_tamano_maximo(self, tmp_path: Path):
        contenido = _imagen_valida_bytes("PNG")
        gateway_limitado = LocalImageStorageGateway(
            base_dir=tmp_path / "uploads", max_file_size_bytes=len(contenido) - 1
        )

        with pytest.raises(ImageValidationError, match="tamaño"):
            await gateway_limitado.save("noticias", "imagen.png", "image/png", contenido)

    @pytest.mark.asyncio
    async def test_rechaza_archivo_vacio(self, gateway: LocalImageStorageGateway):
        with pytest.raises(ImageValidationError):
            await gateway.save("noticias", "imagen.png", "image/png", b"")

    @pytest.mark.asyncio
    async def test_rechaza_categoria_no_permitida(self, gateway: LocalImageStorageGateway):
        contenido = _imagen_valida_bytes("PNG")

        with pytest.raises(ImageValidationError, match="[Cc]ategor[ií]a"):
            await gateway.save("comercial", "imagen.png", "image/png", contenido)


class TestPathTraversal:
    @pytest.mark.asyncio
    async def test_nombre_original_con_path_traversal_no_escapa_del_directorio(
        self, gateway: LocalImageStorageGateway, tmp_path: Path
    ):
        contenido = _imagen_valida_bytes("PNG")

        ruta = await gateway.save("noticias", "../../../etc/passwd.png", "image/png", contenido)

        archivo = (tmp_path / "uploads" / ruta).resolve()
        base_permitida = (tmp_path / "uploads" / "noticias").resolve()
        assert base_permitida in archivo.parents or archivo.parent == base_permitida
        assert ".." not in ruta

    @pytest.mark.asyncio
    async def test_categoria_con_path_traversal_es_rechazada(self, gateway: LocalImageStorageGateway):
        contenido = _imagen_valida_bytes("PNG")

        with pytest.raises(ImageValidationError):
            await gateway.save("../../etc", "imagen.png", "image/png", contenido)

    @pytest.mark.asyncio
    async def test_extension_doble_disfrazada_se_valida_por_contenido_real(self, gateway: LocalImageStorageGateway):
        """Un archivo 'disfrazado.exe.jpg' con contenido no-imagen debe rechazarse igual."""
        contenido_no_imagen = b"contenido binario arbitrario que no es una imagen valida" * 5

        with pytest.raises(ImageValidationError):
            await gateway.save("noticias", "disfrazado.exe.jpg", "image/jpeg", contenido_no_imagen)


class TestFakeImageStorageGateway:
    """Verifica que la interfaz ImageStorageGateway es sustituible por un doble de test en memoria."""

    @pytest.mark.asyncio
    async def test_fake_guarda_y_elimina_sin_tocar_disco(self):
        fake = FakeImageStorageGateway()

        ruta = await fake.save("noticias", "foto.jpg", "image/jpeg", b"contenido-de-prueba")

        assert ruta in fake.guardadas
        assert fake.guardadas[ruta] == b"contenido-de-prueba"

        await fake.delete(ruta)

        assert ruta not in fake.guardadas

    @pytest.mark.asyncio
    async def test_fake_eliminar_none_no_hace_nada(self):
        fake = FakeImageStorageGateway()
        await fake.delete(None)  # No debe lanzar excepción.


class TestEliminar:
    @pytest.mark.asyncio
    async def test_elimina_una_imagen_existente(self, gateway: LocalImageStorageGateway, tmp_path: Path):
        contenido = _imagen_valida_bytes("PNG")
        ruta = await gateway.save("noticias", "foto.png", "image/png", contenido)
        archivo = tmp_path / "uploads" / ruta
        assert archivo.is_file()

        await gateway.delete(ruta)

        assert not archivo.is_file()

    @pytest.mark.asyncio
    async def test_eliminar_none_no_hace_nada(self, gateway: LocalImageStorageGateway):
        await gateway.delete(None)  # No debe lanzar excepción.

    @pytest.mark.asyncio
    async def test_eliminar_ruta_inexistente_no_lanza_excepcion(self, gateway: LocalImageStorageGateway):
        await gateway.delete("noticias/no-existe-nunca.jpg")  # Idempotente, sin excepción.

    @pytest.mark.asyncio
    async def test_eliminar_con_path_traversal_no_borra_fuera_del_directorio(
        self, gateway: LocalImageStorageGateway, tmp_path: Path
    ):
        archivo_externo = tmp_path / "archivo_sensible.txt"
        archivo_externo.write_text("no debe borrarse")

        await gateway.delete("../archivo_sensible.txt")

        assert archivo_externo.is_file()
