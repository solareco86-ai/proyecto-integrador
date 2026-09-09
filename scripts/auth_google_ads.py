#!/usr/bin/env python3
"""
Script Asistente para Autenticación OAuth2 de Google Ads y Generación de Refresh Token.
Lee GOOGLE_ADS_CLIENT_ID y GOOGLE_ADS_CLIENT_SECRET desde el archivo .env.
Soporta múltiples URIs de redirección (127.0.0.1, localhost, OAuth Playground o manual).
"""

import http.server
import json
import os
import socketserver
import sys
import urllib.parse
import urllib.request
from typing import Any
from urllib.error import HTTPError

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_ADS_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "").strip()

SCOPES = [
    "https://www.googleapis.com/auth/adwords",
]

auth_code_holder: dict[str, str] = {}


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)

        if "code" in params:
            auth_code_holder["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html_response = (
                "<html><body style='font-family:sans-serif;text-align:center;padding:50px;background:#0f172a;color:#f8fafc;'>"
                "<h1 style='color:#22c55e;'>¡Autenticación Exitosa!</h1>"
                "<p>El código de autorización fue recibido correctamente. Podés cerrar esta pestaña y volver a la terminal.</p>"
                "</body></html>"
            )
            self.wfile.write(html_response.encode("utf-8"))
        elif "error" in params:
            auth_code_holder["error"] = params["error"][0]
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Error de autorización: {params['error'][0]}".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        pass


def exchange_code_for_tokens(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict[str, Any]:
    token_url = "https://oauth2.googleapis.com/token"
    payload = urllib.parse.urlencode(
        {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        token_url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return data
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"\n❌ Error al canjear código por tokens: {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    print("\n" + "=" * 70)
    print(" 🚀 ASISTENTE DE AUTENTICACIÓN OAUTH2 — GOOGLE ADS (DataMaq)")
    print("=" * 70 + "\n")

    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: GOOGLE_ADS_CLIENT_ID o GOOGLE_ADS_CLIENT_SECRET no están definidos en el archivo .env")
        sys.exit(1)

    print(f"✔ Client ID: {CLIENT_ID[:15]}...{CLIENT_ID[-15:]}")

    # Selección de Redirect URI
    print("\nSeleccioná la URI de redireccionamiento configurada en tu Google Cloud Console:")
    print("  [1] http://127.0.0.1:8080  (Recomendada para servidor local)")
    print("  [2] http://localhost:8080")
    print("  [3] http://localhost")
    print("  [4] https://developers.google.com/oauthplayground")
    print("  [5] Ingresar URI personalizada manualmente")

    choice = input("\nOpción (default: 1): ").strip()

    port = 8080
    use_local_server = True

    if choice == "2":
        redirect_uri = "http://localhost:8080"
        port = 8080
    elif choice == "3":
        redirect_uri = "http://localhost"
        port = 80
        use_local_server = False
    elif choice == "4":
        redirect_uri = "https://developers.google.com/oauthplayground"
        use_local_server = False
    elif choice == "5":
        redirect_uri = input("Ingresá la Redirect URI exacta: ").strip()
        use_local_server = "8080" in redirect_uri
    else:
        redirect_uri = "http://127.0.0.1:8080"
        port = 8080

    print(f"\n✔ Usando Redirect URI: {redirect_uri}\n")

    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(auth_params)}"

    print("👉 PASO 1: Abrí el siguiente enlace en tu navegador:\n")
    print(f"   {auth_url}\n")

    if use_local_server:
        print(f"👉 PASO 2: Esperando autorización automática en {redirect_uri}...")
        print("   (Presioná Ctrl+C para cancelar o ingresar el código a mano)\n")
        try:
            with socketserver.TCPServer(("127.0.0.1", port), OAuthCallbackHandler) as httpd:
                while "code" not in auth_code_holder and "error" not in auth_code_holder:
                    httpd.handle_request()
        except (KeyboardInterrupt, OSError):
            print("\n⚠ Servidor local detenido o cancelado.")
            raw_input = input("Pegá aquí el código o la URL completa tras autorizar: ").strip()
            if "code=" in raw_input:
                parsed = urllib.parse.urlparse(raw_input)
                qs = urllib.parse.parse_qs(parsed.query)
                auth_code_holder["code"] = qs.get("code", [""])[0]
            else:
                auth_code_holder["code"] = raw_input
    else:
        print("👉 PASO 2: Tras autorizar en el navegador, Google te redirigirá a una URL.")
        raw_input = input(
            "Copiá y pegá aquí la URL completa a la que fuiste redirigido (o el parámetro ?code=...): "
        ).strip()
        if "code=" in raw_input:
            parsed = urllib.parse.urlparse(raw_input)
            qs = urllib.parse.parse_qs(parsed.query)
            auth_code_holder["code"] = qs.get("code", [""])[0]
        else:
            auth_code_holder["code"] = raw_input

    if "error" in auth_code_holder:
        print(f"❌ Error en la autorización: {auth_code_holder['error']}")
        sys.exit(1)

    code = auth_code_holder.get("code")
    if not code:
        print("❌ No se recibió un código válido.")
        sys.exit(1)

    print("\n⏳ Canjeando código de autorización por Refresh Token...")
    tokens = exchange_code_for_tokens(code, CLIENT_ID, CLIENT_SECRET, redirect_uri)

    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")

    if not refresh_token:
        print(
            "\n⚠ Google no devolvió un refresh_token nuevo. Esto ocurre si la aplicación ya fue autorizada previamente sin el parámetro prompt=consent."
        )
        if access_token:
            print(f"Access Token temporal: {str(access_token)[:20]}...")
    else:
        print("\n" + "=" * 70)
        print(" 🎉 ¡REFRESH TOKEN OBTENIDO CON ÉXITO!")
        print("=" * 70)
        print(f"\nGOOGLE_ADS_REFRESH_TOKEN={refresh_token}\n")
        print("👉 Agregá esta línea a tu archivo .env local:")
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}\n")


if __name__ == "__main__":
    main()
