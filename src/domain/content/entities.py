"""Entidades de dominio del subdominio de Contenido y Servicios."""

from dataclasses import dataclass, field

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

