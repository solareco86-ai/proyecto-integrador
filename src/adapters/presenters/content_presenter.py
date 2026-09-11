from dataclasses import asdict
from typing import Any

from src.application.dtos import CasoModel, ContenidoModel, CourseModel, GuiaModel
from src.domain.content.entities import Noticia


def present_contenido(contenido: ContenidoModel) -> dict[str, Any]:
    """Prepara el modelo de contenido general para su presentación, inyectando CTAs dinámicos."""
    data = contenido.model_dump()
    if "content" in data and "services" in data["content"] and "cards" in data["content"]["services"]:
        for card in data["content"]["services"]["cards"]:
            if not card.get("cta") and card.get("title"):
                # Usar la primera palabra del título como fallback (mejor que nada),
                # pero lo correcto es definir cta explícito en home_sections.yaml
                first_word = card["title"].split(" ")[0].rstrip(",")
                card["cta"] = f"Consultá por {first_word}"
    return data


def present_course(course: CourseModel) -> dict[str, Any]:
    """Prepara un curso para su presentación, inyectando og_image y dimensiones por defecto si faltan."""
    data = course.model_dump()
    if not data.get("og_image") and data.get("slug"):
        data["og_image"] = f"/static/media/cursos/og-{data['slug']}.webp"
    # Definir dimensiones OG estándar si no están presentes
    if not data.get("og_image_width"):
        data["og_image_width"] = 1200
    if not data.get("og_image_height"):
        data["og_image_height"] = 630
    return data


def present_caso(caso: CasoModel) -> dict[str, Any]:
    """Prepara un caso para su presentación, inyectando og_image por defecto si falta."""
    data = caso.model_dump()
    if not data.get("og_image"):
        data["og_image"] = "/static/og-default.webp"
    return data


def present_guia(guia: GuiaModel) -> dict[str, Any]:
    """Prepara una guía técnica para su presentación, inyectando og_image por defecto si falta."""
    data = guia.model_dump()
    if not data.get("og_image"):
        data["og_image"] = "/static/og-default.webp"
    return data


def present_noticia(noticia: Noticia) -> dict[str, Any]:
    """Prepara una noticia para su presentación pública, sin exponer autor_id."""
    data = asdict(noticia)
    data.pop("autor_id", None)
    return data
