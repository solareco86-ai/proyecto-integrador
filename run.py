#!/usr/bin/env python3
"""run.py — Script de arranque multiplataforma para desarrollo local del ISFT N° 199.

Uso:
    python run.py [--debug] [PUERTO]
"""

import os
import sys
from typing import NoReturn


def show_help() -> NoReturn:
    print("Uso: python run.py [--debug] [PUERTO]")
    print("  --debug   Fuerza DEBUG=true (telemetría local :8000, sin caché estática)")
    print("  PUERTO    Puerto del servidor (default: 8001 o variable PORT)")
    sys.exit(0)


def main() -> None:
    # Asegurar que el directorio raíz esté en sys.path
    root_dir: str = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    # Configuración de puerto y modo debug
    raw_port: str = os.environ.get("PORT", "8001")
    port: int = int(raw_port) if raw_port.isdigit() else 8001
    debug_mode: bool = os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")

    for arg in sys.argv[1:]:
        if arg.lower() == "--debug":
            debug_mode = True
            os.environ["DEBUG"] = "true"
        elif arg.isdigit():
            port = int(arg)
        elif arg.lower() in ("-h", "--help", "/?"):
            show_help()
        else:
            print(f"[ERROR] Argumento no reconocido: {arg}")
            show_help()

    if debug_mode:
        os.environ["DEBUG"] = "true"
        print("[INFO] Modo DEBUG activado (DEBUG=true)")

    try:
        import uvicorn
    except ImportError:
        print("[ERROR] uvicorn no está instalado en el entorno actual.")
        print("[INFO] Ejecutá: pip install -r requirements.txt")
        sys.exit(1)

    print(f"[INFO] Iniciando servidor ISFT N° 199 en http://127.0.0.1:{port}")
    print("[INFO] Recarga automática activada en carpetas src/ y data/")
    print("[INFO] Presione Ctrl+C para detener el servidor.")

    uvicorn.run(
        "src.infrastructure.fastapi.app:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        reload_dirs=["src", "data"],
    )


if __name__ == "__main__":
    main()
