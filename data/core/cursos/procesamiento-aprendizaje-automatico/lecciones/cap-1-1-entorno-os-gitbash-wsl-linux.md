# Guía de Laboratorio Práctico — Capítulo 1: La Terminal, Git y el Entorno de Trabajo en Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## Objetivos de Aprendizaje

Al finalizar esta lección, el estudiante será capaz de:
1. Comprender por qué **GNU/Linux** es el estándar de facto y el sistema operativo objetivo en Ciencia de Datos, Machine Learning y despliegue de modelos.
2. Evaluar las alternativas de entorno en estaciones de trabajo Windows: la vía rápida con **Git Bash** (instalación fácil) y la vía de alta fidelidad con **WSL 2** (instalación intermedia con kernel real).
3. Instalar, configurar y verificar una terminal Bash funcional en su equipo personal de desarrollo.
4. Ejecutar comandos de diagnóstico del sistema para comprobar la arquitectura, el kernel y la disponibilidad de herramientas esenciales (`git`, `python3`, `bash`).

---

## 1. El Sistema Objetivo: ¿Por qué buscamos un entorno GNU/Linux?

En el ámbito profesional del Machine Learning, la ingeniería de datos y la automatización con agentes inteligentes:
* **Estándar en Servidores y Nube:** La totalidad de los servidores de cómputo en la nube, clusters de GPUs (NVIDIA CUDA) y contenedores (Docker/Kubernetes) corren sobre distribuciones GNU/Linux (como Ubuntu Server o Debian).
* **Semántica POSIX:** Las herramientas de desarrollo en Python, los servidores ASGI (como FastAPI y Uvicorn) y los asistentes de código por consola (Aider, OpenCode, AGY CLI) asumen un comportamiento POSIX nativo: rutas con barras diagonales directas (`/`), gestión granular de permisos (`chmod`), señales de procesos (`SIGINT`, `SIGTERM`) y tuberías de datos (*pipes* `|`).
* **La distinción entre Linux y GNU:** Linux es el **kernel** (el núcleo del sistema que administra el procesador, la memoria RAM y el hardware), mientras que el proyecto **GNU** aporta las herramientas de usuario esenciales: el compilador GCC, la biblioteca estándar de C y el intérprete de comandos **Bash** (*Bourne Again SHell*). Ambos conforman el sistema operativo completo **GNU/Linux**.

---

## 2. Opciones de Entorno en Estaciones de Trabajo Windows

Cuando los estudiantes inician su formación técnica en computadoras con Microsoft Windows, no es obligatorio reemplazar de inmediato su sistema operativo. Se definen tres alternativas según el nivel de complejidad y compatibilidad:

| Criterio | Git Bash (Fácil) | WSL 2 (Intermedio) | GNU/Linux Nativo (Objetivo Ideal) |
| :--- | :--- | :--- | :--- |
| **Dificultad de Instalación** | **Baja** (instalador `.exe` estándar en 5 minutos). | **Media** (un comando en PowerShell y reinicio). | **Alta** (instalación en disco físico o dual-boot). |
| **Núcleo / Kernel** | No tiene kernel Linux (emulación Win32/MSYS2). | **Kernel Linux real** ejecutado en hipervisor liviano. | **Kernel Linux nativo** directo sobre el hardware. |
| **Gestor de Paquetes** | No dispone de `apt` ni paquetes `.deb`. | Dispone de `apt` (acceso a todo el catálogo de Ubuntu/Debian). | Dispone de `apt`, `pacman` o `dnf` según la distribución. |
| **Compatibilidad con Agentes y ML** | Buena para Git y scripts básicos de Python. | **Excelente** (soporta Docker, CUDA y binarios Linux). | **Nativa y total** (máximo rendimiento sin capas intermedias). |
| **Aceleración GPU (CUDA / DirectML)** | Limitada a binarios Windows. | Soporta NVIDIA CUDA nativo sobre WSL. | Soporta NVIDIA CUDA y drivers ROCm nativos. |
| **Requisitos Previos** | Ninguno (corre sobre cualquier Windows 10/11). | Requiere virtualización en BIOS/UEFI activada. | Requiere particionar disco o una máquina dedicada. |

---

## 3. Opción 1: Git Bash (Instalación Rápida y Fácil)

**Git Bash** es la solución más rápida para estudiantes que necesitan comenzar a trabajar de inmediato sin modificar la configuración del sistema.

### Características Principales
* Viene incluido dentro del paquete oficial **Git for Windows**.
* Provee una ventana de emulación de terminal (MinTTY) que ejecuta Bash y utilidades GNU básicas (`ls`, `cat`, `grep`, `mkdir`, `cp`, `mv`, `rm`, `ssh`).
* Utiliza el ejecutable de Python de Windows (`python.exe`), mapeando rutas de disco como `/c/Users/usuario/`.

### Paso a Paso de Instalación
1. Descarga el instalador oficial desde el sitio web: [git-scm.com](https://git-scm.com).
2. Ejecuta el archivo instalador `.exe`.
3. En la pantalla **"Choosing the default editor used by Git"**, selecciona *Visual Studio Code* (o *Nano* si prefieres la consola).
4. En **"Adjusting your PATH environment"**, elige la opción recomendada: *Git from the command line and also from 3rd-party software*.
5. En **"Configuring the line ending conversions"**, selecciona: *Checkout Windows-style, commit Unix-style line endings* (`core.autocrlf = true`).
6. En **"Choosing the terminal emulator"**, elige *Use MinTTY (the default terminal of MSYS2)*.
7. Finaliza la instalación.

### Verificación en Git Bash
Abre el acceso directo **Git Bash** desde el Menú Inicio y ejecuta:

```bash
# Comprobar la versión del shell Bash
bash --version

# Comprobar la versión del cliente Git
git --version
```

---

## 4. Opción 2: WSL 2 (Instalación Intermedia — Solución Recomendada)

**WSL 2** (*Windows Subsystem for Linux*) es la opción profesional recomendada para estudiantes que utilizan Windows, ya que proporciona un sistema operativo GNU/Linux completo dentro de Windows con integración transparente.

### Ventajas para Ciencia de Datos y Machine Learning
* Permite instalar dependencias complejas de C++ y Python mediante `sudo apt install`.
* Ejecuta exactamente el mismo entorno que se usará en servidores de producción y plataformas en la nube.
* Se integra directamente con Visual Studio Code a través de la extensión oficial **WSL**.

### Paso a Paso de Instalación

#### Paso 1: Verificar Virtualización en BIOS/UEFI
Abre el *Administrador de Tareas* de Windows (Ctrl + Shift + Esc), ve a la pestaña *Rendimiento > CPU* y confirma que figure **"Virtualización: Habilitada"**. Si está deshabilitada, actívala en el setup de la BIOS de tu placa madre (Intel VT-x o AMD-V / SVM).

#### Paso 2: Instalación de WSL
Abre **PowerShell** como Administrador (clic derecho > *Ejecutar como administrador*) y escribe:

```powershell
wsl --install
```

Este comando habilita las características necesarias de Windows, descarga el kernel Linux actualizado e instala la distribución **Ubuntu LTS** por defecto.

#### Paso 3: Reinicio del Sistema
Reinicia el equipo cuando el sistema lo solicite.

#### Paso 4: Configuración Inicial de Ubuntu
Al reiniciar, se abrirá automáticamente una ventana de terminal de Ubuntu. Espera la inicialización e introduce:
* **Nombre de usuario UNIX** (en minúsculas, por ejemplo: `alumno`).
* **Contraseña** (no se mostrarán caracteres mientras escribes; confirma la clave presionando Enter).

#### Paso 5: Actualización del Sistema y Paquetes de Desarrollo
Dentro de la terminal de Ubuntu recién configurada, actualiza los paquetes base e instala las herramientas esenciales de desarrollo:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl build-essential
```

#### Paso 6: Integración con Visual Studio Code
1. Abre VS Code en Windows e instala la extensión **"WSL"** (de Microsoft).
2. Desde la terminal de Ubuntu en WSL, navega a tu carpeta de trabajo y escribe:
   ```bash
   code .
   ```
   VS Code se abrirá en Windows, pero ejecutando el servidor de desarrollo, las extensiones y el intérprete de Python dentro del entorno Linux.

### Verificación en WSL
Ejecuta los siguientes comandos dentro de la consola de WSL:

```bash
# Verificar información del kernel Linux real
uname -a

# Verificar la distribución instalada
cat /etc/os-release
```

---

## 5. Opción 3: GNU/Linux Nativo (Objetivo Ideal)

Para equipos dedicados al desarrollo, laboratorios del instituto o estaciones de entrenamiento con GPUs dedicadas:
* **Distribuciones Recomendadas:** **Ubuntu Desktop** (22.04 LTS o 24.04 LTS), **Debian GNU/Linux** o **Linux Mint**.
* **Ventajas Inmediatas:** Cero latencia en el sistema de archivos, sin consumo adicional de memoria por máquinas virtuales y compatibilidad directa con todas las librerías científicas (`numpy`, `scipy`, `torch`, `scikit-learn`).

---

## 6. Ejercicio Práctico: Diagnóstico Automatizado del Entorno

Abre tu consola (ya sea **Git Bash**, **WSL** o **GNU/Linux nativo**) y copia la siguiente secuencia de comandos para auditar el entorno en el que estás operando:

```bash
# 1. Comprobar intérprete y arquitectura
echo "=== AUDITORÍA DEL ENTORNO DE DESARROLLO ==="
echo "Usuario actual: $(whoami)"
echo "Shell en ejecución: $SHELL"
echo "Nombre del sistema: $(uname -s)"
echo "Arquitectura de CPU: $(uname -m)"
echo "Kernel del sistema: $(uname -r)"

# 2. Comprobar herramientas fundamentales instaladas
echo "--- Verificación de Herramientas ---"
git --version || echo "⚠️ Git no encontrado"
python3 --version 2>/dev/null || python --version 2>/dev/null || echo "⚠️ Python no encontrado"

# 3. Comprobar si el entorno es GNU/Linux real, WSL o emulación
if [ -f /etc/os-release ]; then
    echo "--- Sistema GNU/Linux Detectado ---"
    grep -E "^(PRETTY_NAME|NAME|VERSION)=" /etc/os-release
elif uname -o 2>/dev/null | grep -qi "msys"; then
    echo "--- Entorno Git Bash (MSYS2 / Win32) Detectado ---"
fi
```

---

## Checkpoint de Verificación

Antes de avanzar a la siguiente lección, confirma:
- [ ] Tienes al menos un entorno de consola Bash operativo en tu computadora (**Git Bash** o **WSL 2**).
- [ ] El comando `git --version` responde correctamente con la versión instalada.
- [ ] Comprendes la diferencia técnica entre un emulador de comandos sobre Windows y un kernel Linux real.
- [ ] Puedes abrir tu terminal y ejecutar el comando `pwd` para visualizar tu directorio de trabajo actual.
