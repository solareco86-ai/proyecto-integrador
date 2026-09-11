"""DTOs internos para los casos de uso de gestión de contenido institucional.

A diferencia de los DTOs Pydantic de `content_dto.py` (usados para validar
payloads HTTP), estos son dataclasses simples desacopladas de la capa web,
igual que `SubmitLeadInput` en `use_cases/submit_lead.py`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CrearNoticiaInput:
    """Datos de entrada para crear una noticia."""

    titulo: str
    cuerpo: str
    autor_id: str | None = None
    publicada: bool = True


@dataclass(frozen=True)
class EditarNoticiaInput:
    """Datos de entrada para editar una noticia existente."""

    id: str
    titulo: str
    cuerpo: str
    publicada: bool = True


@dataclass(frozen=True)
class CrearEventoInput:
    """Datos de entrada para crear un evento."""

    titulo: str
    descripcion: str
    fecha_evento: str
    lugar: str | None = None
    autor_id: str | None = None


@dataclass(frozen=True)
class EditarEventoInput:
    """Datos de entrada para editar un evento existente."""

    id: str
    titulo: str
    descripcion: str
    fecha_evento: str
    lugar: str | None = None


@dataclass(frozen=True)
class CrearComunicadoInput:
    """Datos de entrada para crear un comunicado."""

    titulo: str
    cuerpo: str
    autor_id: str | None = None


@dataclass(frozen=True)
class EditarComunicadoInput:
    """Datos de entrada para editar un comunicado existente."""

    id: str
    titulo: str
    cuerpo: str
