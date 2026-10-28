"""Tests unitarios del clasificador de reportes CSP con ruido conocido."""

import json

import pytest

from src.application.csp_report import es_ruido_csp


def _reporte(**campos: str) -> str:
    return json.dumps(
        {"csp-report": {"document-uri": "https://isftn199.com.ar/", "violated-directive": "script-src", **campos}}
    )


@pytest.mark.parametrize(
    "blocked_uri",
    [
        "https://static.cloudflareinsights.com/beacon.min.js/vce701823e78c4301a35b7e07294d87301792088814092",
        "https://cloudflareinsights.com/beacon.min.js",
        "chrome-extension://abcdef/content.js",
        "moz-extension://1234/inject.js",
        "safari-extension://com.example/script.js",
        "wasm-eval",
    ],
)
def test_ruido_conocido_en_blocked_uri(blocked_uri: str) -> None:
    assert es_ruido_csp(_reporte(**{"blocked-uri": blocked_uri})) is True


def test_extension_en_source_file_es_ruido() -> None:
    assert es_ruido_csp(_reporte(**{"blocked-uri": "data", "source-file": "chrome-extension://abc/x.js"})) is True


def test_beacon_con_source_file_del_sitio_sigue_siendo_ruido() -> None:
    reporte = _reporte(
        **{
            "blocked-uri": "https://static.cloudflareinsights.com/beacon.min.js/v1",
            "source-file": "https://isftn199.com.ar/carreras",
        }
    )
    assert es_ruido_csp(reporte) is True


def test_host_parecido_no_es_cloudflare() -> None:
    assert es_ruido_csp(_reporte(**{"blocked-uri": "https://cloudflareinsights.com.evil.example/x.js"})) is False
    assert es_ruido_csp(_reporte(**{"blocked-uri": "https://evil.example/cloudflareinsights.com/x.js"})) is False


def test_facebook_pixel_queda_como_violacion() -> None:
    assert es_ruido_csp(_reporte(**{"blocked-uri": "https://connect.facebook.net/en_US/pcm.js"})) is False


def test_texto_cloudflare_en_campo_no_estructurado_no_es_ruido() -> None:
    reporte = _reporte(**{"blocked-uri": "https://evil.example/x.js", "script-sample": "cloudflareinsights.com"})
    assert es_ruido_csp(reporte) is False


def test_texto_en_document_uri_no_silencia_violacion() -> None:
    reporte = _reporte(**{"blocked-uri": "https://evil.example/x.js"}).replace(
        "https://isftn199.com.ar/", "https://cloudflareinsights.com/"
    )
    assert es_ruido_csp(reporte) is False


def test_body_no_json_es_violacion() -> None:
    assert es_ruido_csp("cloudflareinsights.com wasm-eval") is False


def test_csp_report_sin_objeto_es_violacion() -> None:
    assert es_ruido_csp(json.dumps({"otra-cosa": {}})) is False
    assert es_ruido_csp(json.dumps(["texto"])) is False


def test_lote_reporting_api_solo_es_ruido_si_todos_lo_son() -> None:
    ruido: dict[str, object] = {"type": "csp-violation", "body": {"blockedURL": "wasm-eval"}}
    real: dict[str, object] = {"type": "csp-violation", "body": {"blockedURL": "https://evil.example/x.js"}}
    assert es_ruido_csp(json.dumps([ruido])) is True
    assert es_ruido_csp(json.dumps([ruido, real])) is False
    assert es_ruido_csp(json.dumps([ruido, "no-es-objeto"])) is False


def test_profundidad_excesiva_es_violacion() -> None:
    anidado = "[" * 100000 + "]" * 100000
    assert es_ruido_csp(anidado) is False
