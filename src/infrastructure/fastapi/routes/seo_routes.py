from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, LandingContentModel
from src.infrastructure.fastapi.dependencies import (
    get_contenido,
    get_cursos_service,
    get_geografia,
    get_landing_content,
    templates,
)
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter()


@router.get("/{provincia}")
async def pagina_provincia(
    request: Request,
    provincia: str,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: dict[str, Any] = Depends(get_geografia),
    cursos_service: DataService = Depends(get_cursos_service),
):
    """Página hub de provincia: lista los municipios y sus localidades."""
    locs: dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia)

    if not prov:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    provincia_nombre = provincia.replace("-", " ").title()

    # Armar lista de municipios con sus localidades
    municipios_list: list[dict[str, Any]] = []
    all_localidades: list[dict[str, str]] = []
    for muni_key, localidades in prov.items():
        muni_nombre = muni_key.replace("-", " ").title()
        loc_list: list[dict[str, str]] = []
        for loc_key, loc_nombre in localidades.items():
            loc_url = f"/{provincia}/{muni_key}/{loc_key}.html"
            loc_list.append({"nombre": loc_nombre, "url": loc_url})
            all_localidades.append({"nombre": loc_nombre, "url": loc_url, "municipio": muni_nombre})
        municipios_list.append({"nombre": muni_nombre, "slug": muni_key, "localidades": loc_list})

    seo: dict[str, Any] = {
        "title": f"Telemetría y calidad de energía en {provincia_nombre} | {brand_data['brandName']}",
        "description": f"Monitoreo IoT en tiempo real, corrección de factor de potencia (ENRE 544/2024) y optimización de potencia contratada T2/T3 en {provincia_nombre}. Visitas técnicas en campo.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "hub_type": "provincia",
        "hub_title": f"Telemetría y calidad de energía en {provincia_nombre}",
        "hub_subtitle": f"Seleccioná tu municipio para ver la cobertura en {provincia_nombre}.",
        "municipios": municipios_list,
        "provincia": provincia_nombre,
        "provincia_slug": provincia,
        "casos": cursos_service.get_casos(),
        "guias": cursos_service.get_guias(),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@router.get("/{provincia}/{municipio}")
async def pagina_municipio(
    request: Request,
    provincia: str,
    municipio: str,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: dict[str, Any] = Depends(get_geografia),
    cursos_service: DataService = Depends(get_cursos_service),
):
    """Página hub de municipio: lista las localidades."""
    locs: dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia)

    if not prov:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")

    mun = prov.get(municipio)
    if not mun:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    provincia_nombre = provincia.replace("-", " ").title()
    municipio_nombre = municipio.replace("-", " ").title()

    localidades_list: list[dict[str, str]] = []
    for loc_key, loc_nombre in mun.items():
        localidades_list.append(
            {
                "nombre": loc_nombre,
                "url": f"/{provincia}/{municipio}/{loc_key}.html",
            }
        )

    seo: dict[str, Any] = {
        "title": f"Telemetría y calidad de energía en {municipio_nombre}, {provincia_nombre} | {brand_data['brandName']}",
        "description": f"Monitoreo IoT en tiempo real, corrección de factor de potencia (ENRE 544/2024) y optimización de potencia contratada T2/T3 en {municipio_nombre}, {provincia_nombre}. Visitas técnicas en campo.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "hub_type": "municipio",
        "hub_title": f"Telemetría y calidad de energía en {municipio_nombre}",
        "hub_subtitle": f"Seleccioná tu localidad en {municipio_nombre}, {provincia_nombre} para ver la cobertura.",
        "localidades": localidades_list,
        "municipio": municipio_nombre,
        "municipio_slug": municipio,
        "provincia": provincia_nombre,
        "provincia_slug": provincia,
        "casos": cursos_service.get_casos(),
        "guias": cursos_service.get_guias(),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@router.get("/{provincia}/{municipio}/{localidad}.html")
async def pagina_localidad(
    request: Request,
    provincia: str,
    municipio: str,
    localidad: str,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: dict[str, Any] = Depends(get_geografia),
    landing_content: LandingContentModel = Depends(get_landing_content),
    cursos_service: DataService = Depends(get_cursos_service),
):
    # Validar existencia
    locs: dict[str, Any] = geografia.get("localidades", {})
    prov = locs.get(provincia, {})
    mun = prov.get(municipio, {})
    nombre_localidad = mun.get(localidad)

    if not nombre_localidad:
        raise HTTPException(status_code=404, detail="Localidad no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    servicios_data = content_data["services"]["cards"]

    municipio_formateado = municipio.replace("-", " ").title()

    localidad_content = landing_content.localidades.get(provincia, {}).get(municipio, {}).get(localidad)

    seo: dict[str, Any] = {
        "title": f"Telemetría y calidad de energía en {nombre_localidad}, {municipio_formateado} | {brand_data['brandName']}",
        "description": f"Monitoreo IoT en tiempo real, corrección de factor de potencia (ENRE 544/2024) y optimización de potencia contratada T2/T3 en {nombre_localidad}. Visitas técnicas en campo.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Telemetría y calidad de energía en {nombre_localidad}"
    hero_subtitle = f"Monitoreo IoT en tiempo real, corrección de factor de potencia bajo la Res. ENRE 544/2024 y optimización de potencia contratada T2/T3 en {nombre_localidad}, {municipio_formateado}."

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "servicios": servicios_data,
        "faq": content_data["faq"]["questions"],
        "localidad_nombre": nombre_localidad,
        "municipio": municipio_formateado,
        "municipio_slug": municipio,
        "provincia": provincia.replace("-", " ").title(),
        "provincia_slug": provincia,
        "seo": seo,
        "footer": presented.get("footer"),
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "landing_localidad": localidad_content.model_dump() if localidad_content else None,
        "casos": cursos_service.get_casos(),
        "guias": cursos_service.get_guias(),
    }
    return templates.TemplateResponse(request=request, name="seo/localidad.html", context=context)
