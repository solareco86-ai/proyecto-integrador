"""Comportamiento del JSON-LD institucional generado por templates/partials/head.html."""

import json
import re
from typing import Any, cast

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app
from src.infrastructure.settings import config

JSON_LD_PATTERN = re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.DOTALL)
TERMINOS_HEREDADOS: tuple[str, ...] = ("powermeter", "xubio", "enre 544", "modbus")
CLAVES_SIN_RESPALDO: tuple[str, ...] = ("knowsAbout", "areaServed", "founder", "hasOfferCatalog")


async def _organizacion_home() -> tuple[dict[str, Any], str]:
    """Devuelve el nodo Organization de la home y el texto crudo de su bloque JSON-LD."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

    bloques: list[str] = JSON_LD_PATTERN.findall(response.text)
    assert bloques, "La home no publica bloques JSON-LD"
    for bloque in bloques:
        data: Any = json.loads(bloque)  # falla si algún bloque no es JSON válido
        if isinstance(data, dict) and "@graph" in data:
            for nodo in cast(list[dict[str, Any]], data["@graph"]):
                if isinstance(nodo, dict) and nodo.get("@type") == "Organization":
                    return nodo, bloque
    pytest.fail("La home no publica un nodo Organization en JSON-LD")


@pytest.mark.asyncio  # type: ignore
async def test_head_json_ld_declares_educational_organization() -> None:
    """El nodo Organization se declara como EducationalOrganization del ISFT N° 199."""
    brand = DataService(data_dir="data").get_contenido().brand
    org, _ = await _organizacion_home()

    assert org["additionalType"] == "https://schema.org/EducationalOrganization"
    assert brand.brandName in org["name"]


@pytest.mark.asyncio  # type: ignore
async def test_head_json_ld_uses_institutional_data() -> None:
    """Dirección, coordenadas, horario, redes y contacto salen de brand.yaml y config."""
    brand = DataService(data_dir="data").get_contenido().brand
    org, _ = await _organizacion_home()
    telefono: str = f"+{config.WHATSAPP_PHONE}"

    direccion: dict[str, Any] = {k: v for k, v in org["address"].items() if k != "@type"}
    assert org["address"]["@type"] == "PostalAddress"
    assert direccion == brand.address

    assert brand.geo is not None
    assert org["geo"]["latitude"] == brand.geo["lat"]
    assert org["geo"]["longitude"] == brand.geo["lng"]
    assert org["openingHours"] == brand.openingHours
    assert org["sameAs"] == brand.sameAs

    assert org["telephone"] == telefono
    assert org["email"] == brand.contactEmail
    assert org["contactPoint"]["contactType"] == "Secretaría"
    assert org["contactPoint"]["telephone"] == telefono
    assert org["contactPoint"]["email"] == brand.contactEmail


@pytest.mark.asyncio  # type: ignore
async def test_head_json_ld_has_no_inherited_or_hardcoded_content() -> None:
    """Sin contenido heredado de DataMaq ni bloques escritos a mano en la plantilla (AGENTS.md §2b)."""
    org, bloque = await _organizacion_home()

    for clave in CLAVES_SIN_RESPALDO:
        assert clave not in org, f"El JSON-LD conserva '{clave}' escrito en la plantilla"

    texto: str = bloque.lower()
    for termino in TERMINOS_HEREDADOS:
        assert termino not in texto, f"El JSON-LD conserva contenido heredado: {termino!r}"
    assert '"price"' not in texto, "El JSON-LD no debe publicar precios (gratuidad, AGENTS.md §7.1)"
