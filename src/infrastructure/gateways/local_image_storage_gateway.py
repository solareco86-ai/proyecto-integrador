"""Implementación de ImageStorageGateway sobre el sistema de archivos local."""

import io
import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from src.application.gateways.image_storage_gateway import ImageStorageGateway, ImageValidationError

# Categorías de contenido institucional habilitadas para carga de imágenes.
# Actúa como allowlist: cualquier otro valor es rechazado antes de tocar el
# sistema de archivos (evita que un valor no previsto se use para construir
# una ruta de destino fuera de static/uploads).
_ALLOWED_CATEGORIES = frozenset({"noticias", "eventos", "comunicados"})

_ALLOWED_EXTENSIONS = frozenset({"jpg", "jpeg", "png", "webp"})

# MIME declarado por el cliente -> formatos Pillow reales que debe coincidir.
# El MIME/extensión declarados solo se usan para rechazar rápido; el formato
# real siempre se re-verifica contra el contenido efectivo del archivo.
_ALLOWED_MIME_TO_PIL_FORMATS: dict[str, frozenset[str]] = {
    "image/jpeg": frozenset({"JPEG"}),
    "image/png": frozenset({"PNG"}),
    "image/webp": frozenset({"WEBP"}),
}

_PIL_FORMAT_TO_EXTENSION: dict[str, str] = {
    "JPEG": "jpg",
    "PNG": "png",
    "WEBP": "webp",
}

_DEFAULT_MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class LocalImageStorageGateway(ImageStorageGateway):
    """Guarda imágenes en `static/uploads/<category>/<uuid>.<ext>` del disco local.

    El nombre de archivo en disco nunca proviene del nombre original enviado
    por el usuario: siempre se genera con `uuid4()` a partir del formato real
    detectado por Pillow, lo que elimina de raíz el riesgo de path traversal
    y de colisión de nombres.
    """

    def __init__(
        self,
        base_dir: str | Path = "static/uploads",
        max_file_size_bytes: int = _DEFAULT_MAX_FILE_SIZE_BYTES,
    ) -> None:
        self._base_dir = Path(base_dir).resolve()
        self._max_file_size_bytes = max_file_size_bytes

    async def save(self, category: str, filename: str, content_type: str | None, file_bytes: bytes) -> str:
        """Valida y persiste una imagen en `static/uploads/<category>/`."""
        if category not in _ALLOWED_CATEGORIES:
            raise ImageValidationError(f"Categoría de imagen no permitida: {category!r}")

        if not file_bytes:
            raise ImageValidationError("El archivo está vacío.")

        if len(file_bytes) > self._max_file_size_bytes:
            max_mb = self._max_file_size_bytes // (1024 * 1024)
            raise ImageValidationError(f"El archivo supera el tamaño máximo permitido ({max_mb} MB).")

        extension_declarada = Path(filename).suffix.lstrip(".").lower()
        if extension_declarada not in _ALLOWED_EXTENSIONS:
            raise ImageValidationError(f"Extensión de archivo no permitida: '.{extension_declarada}'")

        formatos_esperados = _ALLOWED_MIME_TO_PIL_FORMATS.get(content_type or "")
        if formatos_esperados is None:
            raise ImageValidationError(f"Tipo de contenido no permitido: {content_type!r}")

        formato_real = self._detectar_formato_real(file_bytes)

        if formato_real not in formatos_esperados:
            raise ImageValidationError(
                f"El contenido real del archivo ({formato_real}) no coincide con el tipo declarado ({content_type})."
            )

        extension_final = _PIL_FORMAT_TO_EXTENSION[formato_real]
        nombre_generado = f"{uuid.uuid4().hex}.{extension_final}"

        destino_dir = self._base_dir / category
        destino_dir.mkdir(parents=True, exist_ok=True)
        destino_path = destino_dir / nombre_generado

        # Cinturón de seguridad extra: el archivo final debe quedar
        # estrictamente dentro de destino_dir. `nombre_generado` es siempre
        # nuestro (uuid), nunca el nombre enviado por el usuario, por lo que
        # esta condición es estructuralmente cierta; se mantiene como
        # verificación defensiva explícita contra path traversal.
        if destino_dir.resolve() not in destino_path.resolve().parents:
            raise ImageValidationError("Ruta de destino inválida.")

        destino_path.write_bytes(file_bytes)

        return f"{category}/{nombre_generado}"

    async def delete(self, ruta_relativa: str | None) -> None:
        """Elimina una imagen por su ruta relativa; segura ante None o archivo inexistente."""
        if not ruta_relativa:
            return

        candidate = (self._base_dir / ruta_relativa).resolve()

        # Si la ruta relativa fue manipulada para escapar de static/uploads
        # (p. ej. "../../etc/passwd"), no se borra nada fuera del árbol
        # permitido.
        if self._base_dir.resolve() not in candidate.parents:
            return

        candidate.unlink(missing_ok=True)

    @staticmethod
    def _detectar_formato_real(file_bytes: bytes) -> str:
        """Verifica que los bytes sean una imagen real y devuelve su formato Pillow.

        Lanza `ImageValidationError` si el archivo está corrupto o no es una
        imagen soportada por Pillow.
        """
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.verify()
            # Pillow exige reabrir el buffer tras verify(): el objeto queda
            # inutilizable para lecturas posteriores una vez verificado.
            with Image.open(io.BytesIO(file_bytes)) as img:
                formato = img.format
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ImageValidationError("El archivo no es una imagen válida o está corrupto.") from exc

        if formato is None:
            raise ImageValidationError("No se pudo determinar el formato real de la imagen.")
        return formato
