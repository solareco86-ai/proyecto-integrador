"""Puerto de aplicación para el almacenamiento de imágenes opcionales de contenido institucional."""

from abc import ABC, abstractmethod


class ImageValidationError(Exception):
    """Error de validación de una imagen subida (extensión, MIME, tamaño o contenido inválido)."""


class ImageStorageGateway(ABC):
    """Interfaz que deben implementar los almacenes de imágenes de contenido.

    El dominio y los casos de uso dependen únicamente de esta interfaz,
    nunca del mecanismo de almacenamiento concreto (disco local, bucket
    externo, etc.). Solo se persiste en la base de datos la ruta relativa
    devuelta por `save`, nunca los bytes de la imagen.
    """

    @abstractmethod
    async def save(self, category: str, filename: str, content_type: str | None, file_bytes: bytes) -> str:
        """Valida y persiste una imagen, devolviendo su ruta relativa.

        `category` identifica el tipo de contenido (p. ej. "noticias").
        `filename` es el nombre original enviado por el usuario: se usa
        únicamente para inspeccionar su extensión declarada, nunca para
        construir la ruta de destino en disco. Lanza `ImageValidationError`
        si el archivo no cumple las validaciones de seguridad/formato.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, ruta_relativa: str | None) -> None:
        """Elimina una imagen por su ruta relativa.

        Debe ser segura ante `None` (no hace nada) y ante una ruta que ya
        no exista en disco (idempotente, no lanza excepción).
        """
        raise NotImplementedError
