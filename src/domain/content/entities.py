"""Entidades de dominio del subdominio de Contenido y Servicios."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from src.domain.common.slugify import slugify
from src.domain.common.value_objects import Slug


@dataclass
class ServiceCard:
    id: str
    title: str
    description: str
    problem: str
    key_points: list[str]
    cta: str | None = None
    proof: str | None = None
    caso_slug: str | None = None
    modality: str | None = "both"


@dataclass
class TelemetryPlan:
    id: str
    name: str
    price: str
    tagline: str
    features: list[str] = field(default_factory=lambda: list[str]())
    badge: str | None = None
    featured: bool = False
    cta_label: str = "Consultar"
    cta_whatsapp_text: str = ""


@dataclass
class Caso:
    slug: Slug
    title: str
    industry: str
    location: str
    summary: str
    problem: str
    solution: str
    results: list[str] = field(default_factory=lambda: list[str]())
    published_at: str = ""
    client: str | None = None
    og_image: str | None = None
    content: str | None = None


@dataclass
class Carrera:
    id: str
    slug: Slug
    title: str
    titulo_otorgado: str
    duracion: str
    modalidad: str
    turno: str
    resolucion: str | None = None
    badge: str | None = None
    icon: str | None = None
    description_short: str = ""
    description_long: str = ""
    perfil_egresado: str = ""
    materias_destacadas: list[str] = field(default_factory=lambda: list[str]())
    salida_laboral: list[str] = field(default_factory=lambda: list[str]())


@dataclass
class Noticia:
    id: str
    titulo: str
    cuerpo: str
    autor_id: str | None = None
    publicada: bool = True
    slug: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def create(
        cls,
        titulo: str,
        cuerpo: str,
        autor_id: str | None = None,
        publicada: bool = True,
    ) -> "Noticia":
        """Crea una instancia de Noticia con un id, slug base y created_at nuevos.

        El slug generado acá es determinístico (a partir del título); la
        resolución de colisiones contra otros registros existentes es
        responsabilidad del caso de uso de creación/edición, que sí tiene
        acceso al repositorio.
        """
        return cls(
            id=str(uuid4()),
            titulo=titulo,
            cuerpo=cuerpo,
            autor_id=autor_id,
            publicada=publicada,
            slug=slugify(titulo),
            created_at=datetime.now(UTC).isoformat(),
        )


@dataclass
class Evento:
    id: str
    titulo: str
    descripcion: str
    fecha_evento: str
    lugar: str | None = None
    autor_id: str | None = None
    slug: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def create(
        cls,
        titulo: str,
        descripcion: str,
        fecha_evento: str,
        lugar: str | None = None,
        autor_id: str | None = None,
    ) -> "Evento":
        """Crea una instancia de Evento con un id, slug base y created_at nuevos."""
        return cls(
            id=str(uuid4()),
            titulo=titulo,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            lugar=lugar,
            autor_id=autor_id,
            slug=slugify(titulo),
            created_at=datetime.now(UTC).isoformat(),
        )


@dataclass
class Comunicado:
    id: str
    titulo: str
    cuerpo: str
    autor_id: str | None = None
    slug: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def create(
        cls,
        titulo: str,
        cuerpo: str,
        autor_id: str | None = None,
    ) -> "Comunicado":
        """Crea una instancia de Comunicado con un id, slug base y created_at nuevos."""
        return cls(
            id=str(uuid4()),
            titulo=titulo,
            cuerpo=cuerpo,
            autor_id=autor_id,
            slug=slugify(titulo),
            created_at=datetime.now(UTC).isoformat(),
        )

