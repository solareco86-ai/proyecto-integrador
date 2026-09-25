"""DTOs internos para los casos de uso de gestión de contenido institucional.

A diferencia de los DTOs Pydantic de `content_dto.py` (usados para validar
payloads HTTP), estos son dataclasses simples desacopladas de la capa web,
igual que `SubmitLeadInput` en `use_cases/submit_lead.py`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CrearNoticiaInput:
    """Datos de entrada para crear una noticia.

    `imagen` es la ruta relativa ya validada y guardada por
    `ImageStorageGateway` (nunca bytes ni el nombre original del archivo).
    """

    titulo: str
    cuerpo: str
    autor_id: str | None = None
    publicada: bool = True
    imagen: str | None = None


@dataclass(frozen=True)
class EditarNoticiaInput:
    """Datos de entrada para editar una noticia existente.

    `imagen`: ruta relativa de una imagen nueva ya guardada por
    `ImageStorageGateway` (None si no se subió ninguna). `quitar_imagen`
    indica que la imagen actual debe quitarse explícitamente. Si ninguna de
    las dos aplica, la imagen existente se conserva sin cambios.
    """

    id: str
    titulo: str
    cuerpo: str
    publicada: bool = True
    imagen: str | None = None
    quitar_imagen: bool = False


@dataclass(frozen=True)
class CrearEventoInput:
    """Datos de entrada para crear un evento.

    `imagen` es la ruta relativa ya validada y guardada por
    `ImageStorageGateway` (nunca bytes ni el nombre original del archivo).
    """

    titulo: str
    descripcion: str
    fecha_evento: str
    lugar: str | None = None
    autor_id: str | None = None
    publicada: bool = False
    imagen: str | None = None


@dataclass(frozen=True)
class EditarEventoInput:
    """Datos de entrada para editar un evento existente.

    `imagen`: ruta relativa de una imagen nueva ya guardada por
    `ImageStorageGateway` (None si no se subió ninguna). `quitar_imagen`
    indica que la imagen actual debe quitarse explícitamente. Si ninguna de
    las dos aplica, la imagen existente se conserva sin cambios.
    """

    id: str
    titulo: str
    descripcion: str
    fecha_evento: str
    lugar: str | None = None
    publicada: bool = False
    imagen: str | None = None
    quitar_imagen: bool = False


@dataclass(frozen=True)
class CrearComunicadoInput:
    """Datos de entrada para crear un comunicado.

    `imagen` es la ruta relativa ya validada y guardada por
    `ImageStorageGateway` (nunca bytes ni el nombre original del archivo).
    """

    titulo: str
    cuerpo: str
    autor_id: str | None = None
    publicada: bool = False
    imagen: str | None = None


@dataclass(frozen=True)
class EditarComunicadoInput:
    """Datos de entrada para editar un comunicado existente.

    `imagen`: ruta relativa de una imagen nueva ya guardada por
    `ImageStorageGateway` (None si no se subió ninguna). `quitar_imagen`
    indica que la imagen actual debe quitarse explícitamente. Si ninguna de
    las dos aplica, la imagen existente se conserva sin cambios.
    """

    id: str
    titulo: str
    cuerpo: str
    publicada: bool = False
    imagen: str | None = None
    quitar_imagen: bool = False
