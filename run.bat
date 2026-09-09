@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Configuración del puerto (por defecto 8001 para convivir con datamaq-telemetry en 8000)
:: Uso: run.bat [--debug] [PUERTO]
if "%PORT%"=="" (
    set "PORT=8001"
)
set "DEBUG_MODE=0"

:parse_args
if "%~1"=="" goto args_done
if /i "%~1"=="--debug" (
    set "DEBUG_MODE=1"
    shift
    goto parse_args
)
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="/?" goto show_help

:: Verificar si el argumento es numérico (puerto)
set "ARG_VAL=%~1"
echo !ARG_VAL!| findstr /r "^[0-9][0-9]*$" >nul
if not errorlevel 1 (
    set "PORT=!ARG_VAL!"
    shift
    goto parse_args
)

echo [ERROR] Argumento no reconocido: %~1
goto show_help

:show_help
echo Uso: run.bat [--debug] [PUERTO]
echo   --debug   Fuerza DEBUG=true (telemetría local :8000, sin caché estática)
echo   PUERTO    Puerto del servidor (default: 8001 o variable %%PORT%%)
exit /b 1

:args_done
if "!DEBUG_MODE!"=="1" (
    set "DEBUG=true"
    echo [INFO] Modo DEBUG activado (DEBUG=true)
)

:: Detener proceso previo en caso de que esté ocupando el puerto configurado
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":!PORT! " 2^>nul ^| findstr LISTENING 2^>nul') do (
    echo [INFO] Deteniendo proceso previo en puerto !PORT! (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

:: Detección y activación del entorno virtual (.venv o venv)
set "VENV_DIR="
if exist ".venv\Scripts\activate.bat" (
    set "VENV_DIR=.venv"
) else if exist "venv\Scripts\activate.bat" (
    set "VENV_DIR=venv"
) else (
    set "VENV_DIR=.venv"
    echo [INFO] Entorno virtual no encontrado. Creando !VENV_DIR!...
    python -m venv .venv
)

if exist "!VENV_DIR!\Scripts\activate.bat" (
    call "!VENV_DIR!\Scripts\activate.bat"
)

:: Verificar dependencias mínimas requeridas para el arranque
python -c "import uvicorn, fastapi, email_validator" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Dependencias faltantes o incompletas en el entorno virtual.
    echo [INFO] Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
)

:: Configurar PYTHONPATH apuntando a la raíz del proyecto
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo [INFO] Iniciando servidor ISFT N° 199 en http://127.0.0.1:!PORT!
echo [INFO] Recarga automática activada en carpetas src/ y data/
echo [INFO] Presione Ctrl+C para detener el servidor.

python -m uvicorn src.infrastructure.fastapi.app:app --reload --reload-dir src --reload-dir data --port !PORT!
