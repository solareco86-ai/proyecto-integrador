"""JSON-LD del catálogo de carreras (`hasOfferCatalog` del head) generado desde carreras.yaml."""

import json
import re
from typing import Any, cast

import pytest
from httpx import ASGITransport, AsyncClient

from src.adapters.presenters.content_presenter import present_catalogo_carreras_json_ld
from src.application.data_service import DataService
from src.application.dtos import CarreraModel
from src.infrastructure.fastapi import dependencies
from src.infrastructure.fastapi.app import app


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


async def _catalogo_del_home() -> dict[str, Any]:
    """Devuelve el `hasOfferCatalog` del nodo Organization publicado en el JSON-LD del home."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        respuesta = await cliente.get("/")
    assert respuesta.status_code == 200
    bloques: list[str] = re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", respuesta.text, re.DOTALL)
    for bloque in bloques:
        datos: dict[str, Any] = json.loads(bloque)
        for nodo in cast(list[dict[str, Any]], datos.get("@graph", [])):
            if nodo.get("@type") == "Organization" and "hasOfferCatalog" in nodo:
                return cast(dict[str, Any], nodo["hasOfferCatalog"])
    raise AssertionError("el home no publica hasOfferCatalog en el nodo Organization")


def _cursos(catalogo: dict[str, Any]) -> list[dict[str, Any]]:
    elementos = cast(list[dict[str, Any]], catalogo["itemListElement"])
    return [cast(dict[str, Any], elemento["itemOffered"]) for elemento in elementos]


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_del_home_refleja_el_catalogo_inyectado(monkeypatch: pytest.MonkeyPatch) -> None:
    """Si cambia el catálogo de datos, cambia el JSON-LD: no hay una copia escrita en la plantilla."""
    inyectadas: list[CarreraModel] = [
        _carrera("prueba-a", "Tecnicatura de Prueba A", "Descripción de prueba A."),
        _carrera("prueba-b", "Tecnicatura de Prueba B", "Descripción de prueba B."),
    ]
    monkeypatch.setattr(dependencies.data_service, "get_carreras", lambda: inyectadas)

    catalogo = await _catalogo_del_home()

    assert catalogo["@type"] == "OfferCatalog"
    assert [(curso["name"], curso["description"]) for curso in _cursos(catalogo)] == [
        ("Tecnicatura de Prueba A", "Descripción de prueba A."),
        ("Tecnicatura de Prueba B", "Descripción de prueba B."),
    ]


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_del_home_publica_las_descripciones_de_carreras_yaml() -> None:
    oficiales: list[CarreraModel] = DataService(data_dir="data").get_carreras()
    assert oficiales, "carreras.yaml no tiene carreras"

    catalogo = await _catalogo_del_home()

    assert [(curso["name"], curso["description"]) for curso in _cursos(catalogo)] == [
        (carrera.title, carrera.description_short) for carrera in oficiales
    ]


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_del_catalogo_escapa_comillas_ampersand_y_etiquetas(monkeypatch: pytest.MonkeyPatch) -> None:
    """Textos con caracteres especiales producen JSON válido dentro de <script> y conservan su valor."""
    texto = 'Datos "reales" & <b>prácticas</b> </script> \\ fin'
    inyectadas: list[CarreraModel] = [_carrera("especial", 'Tecnicatura "Especial" & Cía', texto)]
    monkeypatch.setattr(dependencies.data_service, "get_carreras", lambda: inyectadas)

    catalogo = await _catalogo_del_home()

    assert _cursos(catalogo) == [
        {"@type": "Course", "name": 'Tecnicatura "Especial" & Cía', "description": texto},
    ]
