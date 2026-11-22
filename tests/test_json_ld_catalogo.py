"""JSON-LD del catálogo de carreras (`hasOfferCatalog` del head) generado desde carreras.yaml."""

from typing import Any

from src.adapters.presenters.content_presenter import present_catalogo_carreras_json_ld
from src.application.dtos import CarreraModel


def _carrera(slug: str, title: str, description_short: str) -> CarreraModel:
    return CarreraModel(
        id=slug,
        slug=slug,
        title=title,
        titulo_otorgado=f"Técnico/a en {slug}",
        duracion="3 años",
        modalidad="Presencial",
        turno="Vespertino",
        description_short=description_short,
    )


def test_presenter_arma_un_offer_con_su_course_por_carrera_en_orden() -> None:
    carreras: list[CarreraModel] = [
        _carrera("prueba-a", "Tecnicatura de Prueba A", "Descripción A."),
        _carrera("prueba-b", "Tecnicatura de Prueba B", "Descripción B."),
    ]

    elementos: list[dict[str, Any]] = present_catalogo_carreras_json_ld(carreras)

    assert elementos == [
        {
            "@type": "Offer",
            "itemOffered": {"@type": "Course", "name": "Tecnicatura de Prueba A", "description": "Descripción A."},
        },
        {
            "@type": "Offer",
            "itemOffered": {"@type": "Course", "name": "Tecnicatura de Prueba B", "description": "Descripción B."},
        },
    ]


def test_presenter_con_catalogo_vacio_no_inventa_carreras() -> None:
    assert present_catalogo_carreras_json_ld([]) == []
