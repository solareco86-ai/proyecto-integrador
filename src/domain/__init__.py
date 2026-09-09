"""Capa de Dominio Pura (Clean Architecture & DDD).

Organizada por Bounded Contexts:
- common: Value objects y excepciones compartidas (Price, Slug, DomainError).
- leads: Subdominio de captación, prospectos y formularios de contacto.
- lms: Subdominio educativo de cursos, lecciones, instructores y cuestionarios.
- content: Subdominio de propuesta de valor, servicios, planes de telemetría y marca.
- seo: Subdominio de SEO técnico, esquemas estructurados y landings locales.
"""

from src.domain.common.exceptions import DomainError, EntityNotFoundError, ValidationError
from src.domain.common.value_objects import Price, Slug
from src.domain.leads.entities import Lead
from src.domain.leads.repositories import LeadRepository
from src.domain.leads.value_objects import ContactInfo, LeadSubmissionResult

__all__ = [
    "DomainError",
    "EntityNotFoundError",
    "ValidationError",
    "Price",
    "Slug",
    "Lead",
    "LeadRepository",
    "ContactInfo",
    "LeadSubmissionResult",
]
