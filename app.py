#!/usr/bin/env python3
"""app.py — Punto de entrada para iniciar el servidor web del ISFT N° 199."""
import os
import sys

# Asegurar que el entorno virtual esté en el path si se ejecuta con python del sistema
venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "python")
if sys.executable != venv_python and os.path.exists(venv_python):
    os.execv(venv_python, [venv_python] + sys.argv)

import run

if __name__ == "__main__":
    run.main()
