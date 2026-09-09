#!/bin/bash

# Configuración del puerto (por defecto 8001 para convivir con datamaq-telemetry en 8000)
# Uso: ./run.sh [--debug] [PUERTO]
PORT="${PORT:-8001}"
DEBUG_MODE=0

for arg in "$@"; do
  case "$arg" in
    --debug)
      DEBUG_MODE=1
      ;;
    *)
      if [[ "$arg" =~ ^[0-9]+$ ]]; then
        PORT="$arg"
      else
        echo "Uso: ./run.sh [--debug] [PUERTO]" >&2
        echo "  --debug   Fuerza DEBUG=true (telemetría local :8000, sin caché estática)" >&2
        echo "  PUERTO    Puerto del servidor (default: 8001 o \$PORT)" >&2
        exit 1
      fi
      ;;
  esac
done

if [ "$DEBUG_MODE" -eq 1 ]; then
  export DEBUG=true
  echo "Modo DEBUG activado (DEBUG=true)"
fi

# Detener proceso ocupando el puerto configurado
PIDS=$(lsof -t -i:$PORT)
if [ ! -z "$PIDS" ]; then
  echo "Deteniendo procesos en puerto $PORT"
  kill -9 $PIDS 2>/dev/null
fi

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "Entorno virtual no encontrado. Creando $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
  echo "Instalando dependencias desde requirements.txt..."
  "$VENV_DIR/bin/pip" install -r requirements.txt
fi

source "$VENV_DIR/bin/activate"

if ! python3 -c "import uvicorn" 2>/dev/null; then
  echo "Dependencias no encontradas. Instalando desde requirements.txt..."
  pip install -r requirements.txt
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m uvicorn src.infrastructure.fastapi.app:app --reload --reload-dir src --reload-dir data --port "$PORT"
