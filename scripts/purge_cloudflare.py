#!/usr/bin/env python3
"""Purga la caché de Cloudflare tras un despliegue exitoso.

Semántica de salida (no bloqueante para el deploy local):
- Sin CF_API_TOKEN o CF_ZONE_ID: advertencia y exit 0 (se omite la purga).
- La API responde success=true: exit 0.
- La API responde con error (HTTP/red) o success=false: exit 1 (señala purga
  manual pendiente; el código ya está desplegado).
"""

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

_PURGE_URL = "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"


def _load_env_file(path: str = ".env") -> None:
    """Carga variables CLAVE=valor de un archivo .env sin pisar el entorno real.

    Usa solo la librería estándar para que el script corra en el runner de CI
    (que no tiene python-dotenv instalado). La ausencia del archivo no es error.
    """
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, _, value = stripped.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)
    except OSError:
        pass


_load_env_file()


def purge_cache(zone_id: str, token: str) -> bool:
    """Envía la purga total de caché de la zona y reporta el resultado."""
    payload = b'{"purge_everything": true}'
    request = urllib.request.Request(
        _PURGE_URL.format(zone_id=zone_id),
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        print(
            f"[purge_cloudflare] Error de red al contactar la API: {exc.reason}",
            file=sys.stderr,
        )
        return False

    try:
        data: dict[str, Any] = json.loads(raw_body)
        success = bool(data.get("success"))
    except (json.JSONDecodeError, AttributeError):
        success = False

    if success:
        print("[purge_cloudflare] Caché de Cloudflare purgada correctamente.")
    else:
        print(
            f"[purge_cloudflare] La API respondió sin éxito: {raw_body}",
            file=sys.stderr,
        )
    return success


def main() -> int:
    """Punto de entrada: lee credenciales del entorno y ejecuta la purga."""
    token = os.getenv("CF_API_TOKEN", "")
    zone_id = os.getenv("CF_ZONE_ID", "")
    if not token or not zone_id:
        print(
            "[purge_cloudflare] CF_API_TOKEN o CF_ZONE_ID no definidos; se omite la purga.",
            file=sys.stderr,
        )
        return 0
    return 0 if purge_cache(zone_id, token) else 1


if __name__ == "__main__":
    sys.exit(main())
