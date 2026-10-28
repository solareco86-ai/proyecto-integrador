"""Clasificación de reportes de violación CSP recibidos en `POST /csp-report`.

Decide si un reporte corresponde a ruido conocido (beacon de Cloudflare Web
Analytics, extensiones del navegador del visitante, `wasm-eval`) o a una
violación que debe alertar. La decisión compara host y esquema exactos de los
campos estructurados del reporte; nunca busca substrings en el body crudo,
porque el endpoint es público y el body lo controla cualquiera.
"""

import json
from typing import Final, cast
from urllib.parse import urlsplit

_ESQUEMAS_EXTENSION: Final[frozenset[str]] = frozenset({"chrome-extension", "moz-extension", "safari-extension"})
_HOSTS_CLOUDFLARE_INSIGHTS: Final[frozenset[str]] = frozenset({"cloudflareinsights.com"})
_VALORES_RUIDO: Final[frozenset[str]] = frozenset({"wasm-eval"})

# Campos del formato CSP Level 3 (`report-uri`) y del formato Reporting API.
_CAMPOS_BLOQUEADO: Final[tuple[str, ...]] = ("blocked-uri", "blockedURL")
_CAMPOS_ORIGEN: Final[tuple[str, ...]] = ("source-file", "sourceFile")


def _es_ruido_valor(valor: str) -> bool:
    """Indica si una URI o palabra clave de CSP pertenece a una fuente de ruido conocida."""
    if valor in _VALORES_RUIDO:
        return True
    try:
        partes = urlsplit(valor)
    except ValueError:
        return False
    if partes.scheme.lower() in _ESQUEMAS_EXTENSION:
        return True
    host = (partes.hostname or "").lower()
    return host in _HOSTS_CLOUDFLARE_INSIGHTS or host.endswith(".cloudflareinsights.com")


def _valores_campos(cuerpo: dict[str, object], campos: tuple[str, ...]) -> list[str]:
    return [valor for campo in campos if isinstance(valor := cuerpo.get(campo), str) and valor]


def _es_ruido_cuerpo(cuerpo: dict[str, object]) -> bool:
    """Un reporte es ruido si lo bloqueado o su origen pertenece a una fuente conocida."""
    bloqueados = _valores_campos(cuerpo, _CAMPOS_BLOQUEADO)
    origenes = _valores_campos(cuerpo, _CAMPOS_ORIGEN)
    return any(_es_ruido_valor(valor) for valor in bloqueados + origenes)


def _cuerpos_reportados(payload: object) -> list[dict[str, object] | None]:
    """Extrae el cuerpo de cada reporte, admitiendo el formato `report-uri` y Reporting API."""
    if isinstance(payload, dict):
        objeto = cast(dict[str, object], payload)
        cuerpo_csp = objeto.get("csp-report")
        return [cast(dict[str, object], cuerpo_csp)] if isinstance(cuerpo_csp, dict) else [None]
    if isinstance(payload, list):
        elementos = cast(list[object], payload)
        cuerpos: list[dict[str, object] | None] = []
        for elemento in elementos:
            if isinstance(elemento, dict):
                entrada = cast(dict[str, object], elemento)
                cuerpo_reporting = entrada.get("body")
                cuerpos.append(
                    cast(dict[str, object], cuerpo_reporting) if isinstance(cuerpo_reporting, dict) else None
                )
            else:
                cuerpos.append(None)
        return cuerpos
    return [None]


def es_ruido_csp(cuerpo_crudo: str) -> bool:
    """Devuelve True solo si el reporte completo es ruido conocido.

    Un body que no es JSON válido, un reporte sin cuerpo reconocible o un lote
    con al menos un reporte no clasificable se trata como violación real.
    """
    try:
        payload: object = json.loads(cuerpo_crudo)
    except (ValueError, RecursionError):
        return False
    cuerpos = _cuerpos_reportados(payload)
    return all(cuerpo is not None and _es_ruido_cuerpo(cuerpo) for cuerpo in cuerpos)
