"""Tests del script de purga de caché de Cloudflare (spec cache-busting-frontend F3)."""

import urllib.error
import urllib.request
from email.message import Message

import pytest

import scripts.purge_cloudflare as pc


class _FakeResponse:
    """Simula la respuesta de urllib.urlopen compatible con context manager."""

    def __init__(self, body: str) -> None:
        self._body = body

    def read(self) -> bytes:
        return self._body.encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_purge_sin_vars_omite_y_sale_cero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CF_API_TOKEN", raising=False)
    monkeypatch.delenv("CF_ZONE_ID", raising=False)

    def boom(*args: object, **kwargs: object) -> None:
        raise AssertionError("urlopen no debe llamarse sin credenciales")

    monkeypatch.setattr(pc.urllib.request, "urlopen", boom)
    assert pc.main() == 0


def test_purge_exitosa_sale_cero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CF_API_TOKEN", "token-secreto")
    monkeypatch.setenv("CF_ZONE_ID", "zona-123")
    llamadas: list[urllib.request.Request] = []

    def fake_urlopen(request: urllib.request.Request, timeout: int = 0) -> _FakeResponse:
        llamadas.append(request)
        return _FakeResponse('{"success": true}')

    monkeypatch.setattr(pc.urllib.request, "urlopen", fake_urlopen)
    assert pc.main() == 0
    assert len(llamadas) == 1
    request = llamadas[0]
    assert request.data == b'{"purge_everything": true}'
    assert request.get_header("Authorization") == "Bearer token-secreto"
    assert "zones/zona-123/purge_cache" in request.full_url


def test_purge_http_error_sale_uno(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CF_API_TOKEN", "token")
    monkeypatch.setenv("CF_ZONE_ID", "zona")

    def fake_urlopen(request: urllib.request.Request, timeout: int = 0) -> None:
        raise urllib.error.HTTPError("url", 401, "Unauthorized", Message(), None)

    monkeypatch.setattr(pc.urllib.request, "urlopen", fake_urlopen)
    assert pc.main() == 1


def test_purge_api_success_false_sale_uno(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CF_API_TOKEN", "token")
    monkeypatch.setenv("CF_ZONE_ID", "zona")

    def fake_urlopen(request: urllib.request.Request, timeout: int = 0) -> _FakeResponse:
        return _FakeResponse('{"success": false, "errors": [{"message": "x"}]}')

    monkeypatch.setattr(pc.urllib.request, "urlopen", fake_urlopen)
    assert pc.main() == 1
