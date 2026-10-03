# Guía de Laboratorio Práctico — Capítulo 1: La Terminal y el Entorno de Desarrollo Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 1. Objetivos de Aprendizaje y Competencias

Al finalizar este laboratorio, el estudiante será capaz de:
1. Operar con soltura en la interfaz de línea de comandos (Bash), gestionando rutas absolutas y relativas sin depender de exploradores gráficos.
2. Comprender cómo se mapean los sistemas de archivos entre diferentes plataformas (GNU/Linux nativo, WSL y Git Bash).
3. Construir y ejecutar scripts en Bash con detección dinámica de entorno, usuario y rutas del sistema.
4. Crear y organizar la estructura de directorios de trabajo para proyectos de Ciencia de Datos y Machine Learning.

---

## 2. Sección 1.2: Navegación y Manipulación en Terminal (Bash)

### 2.1. Conceptos Clave: Rutas y Sistema de Archivos
* **Ruta Absoluta:** Especifica la ubicación completa de un archivo o directorio desde la raíz del sistema de archivos (`/`). Ejemplo: `/home/agustin/Desktop` o `/c/Users/alumno/Desktop`.
* **Ruta Relativa:** Toma como referencia el directorio de trabajo actual (`.`). El directorio padre se referencia con `..`.
* **El Directorio Home (`~`):** Representa la carpeta personal del usuario actual (ej. `/home/usuario` en Linux o `/c/Users/usuario` en Git Bash).
* **Navegación sin GUI:** La terminal es el entorno primario para ejecutar scripts, levantar servidores FastAPI y coordinar asistentes de código por consola (Aider, OpenCode, AGY CLI).

---

### 2.2. Comandos Indispensables de Navegación y Archivos

| Comando | Parámetros Comunes | Descripción |
| :--- | :--- | :--- |
| `pwd` | *(sin argumentos)* | Muestra la ruta absoluta del directorio actual (*Print Working Directory*). |
| `ls` | `-la`, `-lh` | Lista archivos y carpetas, incluyendo ocultos (`.env`, `.git`), con permisos, tamaños y fechas. |
| `cd` | `<ruta>`, `..`, `~` | Cambia el directorio de trabajo. `cd ~` regresa al home; `cd ..` asciende un nivel. |
| `mkdir` | `-p` | Crea directorios. La bandera `-p` (*parents*) crea la jerarquía completa si no existe. |
| `touch` | `<archivo>` | Crea un archivo vacío o actualiza su marca temporal. |
| `cp` | `-r`, `-v` | Copia archivos o directorios recursivamente (`-r`). |
| `mv` | `<origen> <destino>` | Mueve o renombra archivos y carpetas. |
| `rm` | `-r`, `-rf` | Elimina archivos o directorios de forma recursiva y forzada (utilizar con máxima precaución). |
| `cat` | `<archivo>` | Imprime en pantalla el contenido textual completo de un archivo. |
| `whoami` | *(sin argumentos)* | Imprime el nombre del usuario activo en la sesión del shell. |

---

### 2.3. Detección de Entorno y Creación del Espacio de Trabajo

En un grupo de estudio o equipo de desarrollo, cada integrante puede estar utilizando un sistema operativo diferente:
1. **GNU/Linux Nativo:** Las carpetas del usuario residen directamente en `/home/<usuario>/Desktop` o `/home/<usuario>/Escritorio`.
2. **Git Bash (Windows):** Las unidades de disco de Windows se montan como `/c/Users/<usuario>/Desktop` o `/c/Users/<usuario>/Escritorio`.
3. **WSL 2 (Windows Subsystem for Linux):** El sistema de archivos de Windows es accesible a través del punto de montaje `/mnt/c/Users/<usuario_windows>/Desktop`.

Para evitar errores manuales de tipeo y garantizar que todos comiencen desde el mismo lugar, crearemos un script en Bash que:
1. Detecta automáticamente la plataforma en ejecución (**Git Bash**, **WSL** o **GNU/Linux Nativo**).
2. Identifica el nombre de usuario activo.
3. Localiza el **Escritorio** (*Desktop* o *Escritorio*).
4. Crea la carpeta de trabajo del curso: `aprendizaje-automatico`.
5. Estructura los subdirectorios esenciales de un proyecto de Machine Learning (`src`, `data`, `notebooks`).

---

### 2.4. Script Bash: `preparar_entorno.sh`

Copia el siguiente script en tu terminal o guárdalo en un archivo llamado `preparar_entorno.sh`:

```bash
#!/usr/bin/env bash
# ==============================================================================
# preparar_entorno.sh
# Detección de plataforma, usuario y creación del espacio de trabajo
# ISFT N° 199 — Tecnicatura Superior en Ciencia de Datos e IA
# ==============================================================================

set -e  # Detener ejecución ante cualquier error inesperado

echo "=========================================================="
echo "🔍 Iniciando diagnóstico de entorno y espacio de trabajo..."
echo "=========================================================="

# 1. Identificación del usuario activo
USUARIO_ACTUAL=$(whoami)
echo "👤 Usuario detectado en el shell: $USUARIO_ACTUAL"

# 2. Detección de la plataforma y resolución de la ruta del Escritorio
if grep -qi "microsoft" /proc/version 2>/dev/null; then
    PLATAFORMA="WSL 2 (Windows Subsystem for Linux)"
    
    # En WSL, consultamos el usuario de Windows para ubicar su Escritorio real
    WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
    if [ -n "$WIN_USER" ] && [ -d "/mnt/c/Users/$WIN_USER" ]; then
        if [ -d "/mnt/c/Users/$WIN_USER/Escritorio" ]; then
            RUTA_ESCRITORIO="/mnt/c/Users/$WIN_USER/Escritorio"
        else
            RUTA_ESCRITORIO="/mnt/c/Users/$WIN_USER/Desktop"
        fi
    else
        # Fallback al home de Linux en WSL
        RUTA_ESCRITORIO="$HOME/Desktop"
    fi

elif uname -o 2>/dev/null | grep -qi "msys"; then
    PLATAFORMA="Git Bash (MSYS2 / Windows)"
    WIN_USER="${USERNAME:-$USER}"
    
    if [ -d "/c/Users/$WIN_USER/Escritorio" ]; then
        RUTA_ESCRITORIO="/c/Users/$WIN_USER/Escritorio"
    else
        RUTA_ESCRITORIO="/c/Users/$WIN_USER/Desktop"
    fi

else
    PLATAFORMA="GNU/Linux Nativo"
    
    # En Linux consultamos la configuración XDG o los directorios habituales
    if command -v xdg-user-dir >/dev/null 2>&1; then
        RUTA_ESCRITORIO=$(xdg-user-dir DESKTOP)
    elif [ -d "$HOME/Escritorio" ]; then
        RUTA_ESCRITORIO="$HOME/Escritorio"
    else
        RUTA_ESCRITORIO="$HOME/Desktop"
    fi
fi

echo "💻 Plataforma: $PLATAFORMA"
echo "📂 Ruta del Escritorio resuelta: $RUTA_ESCRITORIO"

# 3. Definición y creación de la carpeta de trabajo
CARPETA_PROYECTO="$RUTA_ESCRITORIO/aprendizaje-automatico"

echo "⚙️  Creando estructura en: $CARPETA_PROYECTO"
mkdir -p "$CARPETA_PROYECTO/src"
mkdir -p "$CARPETA_PROYECTO/data"
mkdir -p "$CARPETA_PROYECTO/notebooks"
mkdir -p "$CARPETA_PROYECTO/config"

# 4. Crear archivos base de trabajo
touch "$CARPETA_PROYECTO/README.md"
touch "$CARPETA_PROYECTO/.gitignore"
touch "$CARPETA_PROYECTO/src/main.py"

# Escribir encabezado en README.md
cat << 'EOF' > "$CARPETA_PROYECTO/README.md"
# Proyecto: Aprendizaje Automático
Curso: Procesamiento de Aprendizaje Automático — ISFT N° 199
Entorno inicializado correctamente desde la consola Bash.
EOF

# 5. Verificación de la estructura creada
echo ""
echo "=========================================================="
echo "✅ ¡Espacio de trabajo creado con éxito!"
echo "=========================================================="
cd "$CARPETA_PROYECTO"
echo "📍 Directorio actual de trabajo:"
pwd
echo ""
echo "📋 Contenido del directorio:"
ls -la
```

---

### 2.5. Explicación Detallada de los Comandos Utilizados

Comprender qué hace cada línea del script es indispensable para dominar la consola:

1. **`#!/usr/bin/env bash` (*Shebang*):**
   - Le indica al cargador de programas del sistema operativo que debe ejecutar este script utilizando el intérprete `bash` que se encuentre en el `$PATH` del entorno.
2. **`set -e`:**
   - Modo de ejecución segura: si cualquier comando falla arrojando un código de salida distinto de cero, el script se detiene de inmediato evitando estados inconsistentes.
3. **`whoami` y `$USER` / `$USERNAME`:**
   - `whoami` consulta la tabla de contraseñas del sistema (`/etc/passwd` o la API de Windows) e imprime el nombre del usuario de la sesión actual.
   - En Linux nativo y WSL, `$USER` contiene el nombre de usuario UNIX.
   - En Windows (y en Git Bash), `$USERNAME` contiene el usuario de la cuenta de Windows.
4. **`grep -qi "microsoft" /proc/version`:**
   - `/proc/version` es un archivo virtual provisto por el kernel de Linux. En WSL 2, contiene la firma del kernel personalizado de Microsoft (ej. `Linux version 5.15.153.1-microsoft-standard-WSL2`).
   - La bandera `-q` activa el modo silencioso (*quiet*, sin imprimir texto) y `-i` ignora mayúsculas/minúsculas.
5. **`cmd.exe /c "echo %USERNAME%"` y `tr -d '\r'` (Interoperabilidad WSL):**
   - Una de las grandes ventajas de WSL es que permite invocar binarios de Windows desde la consola Linux. Con `cmd.exe` consultamos el nombre del usuario anfitrión de Windows.
   - Dado que los comandos de Windows finalizan sus líneas con retorno de carro (`\r\n`), `tr -d '\r'` limpia ese carácter invisible para evitar rutas corruptas en Linux.
6. **`uname -o`:**
   - El comando `uname` (*Unix Name*) muestra datos del sistema. Con la opción `-o` (*operating system*), en Git Bash devuelve `Msys`, lo que nos permite diferenciarlo de un Linux estándar.
7. **`xdg-user-dir DESKTOP`:**
   - En entornos de escritorio GNU/Linux (GNOME, KDE, XFCE), esta utilidad lee la configuración del estándar FreeDesktop (`~/.config/user-dirs.dirs`) para saber exactamente cómo se llama la carpeta del escritorio, resolviendo diferencias entre idiomas (`Desktop` vs. `Escritorio`).
8. **`mkdir -p "$CARPETA_PROYECTO/..."`:**
   - La opción `-p` (*parents*) garantiza dos cosas:
     - Si los directorios superiores no existen, los crea en cadena.
     - Si el directorio ya existe, **no arroja error**, permitiendo que el script sea *idempotente* (se puede ejecutar múltiples veces sin romper nada).
   - Siempre se entrecomilla la variable (`"$CARPETA_PROYECTO"`) para soportar rutas con espacios (ej. `/mnt/c/Users/Juan Perez/Desktop`).
9. **`cat << 'EOF' > ...` (*Here-Document*):**
   - Permite redirigir un bloque multilínea de texto directamente a un archivo sin necesidad de concatenar múltiples comandos `echo`.

---

### 2.6. Nota sobre WSL 2 y Rendimiento de Disco

En WSL 2, puedes guardar proyectos en el Escritorio de Windows (`/mnt/c/...`) para verlos en el Explorador de Windows. Sin embargo, para proyectos de Machine Learning con miles de archivos pequeños (como librerías dentro del `venv/` o grandes volúmenes de datos), el sistema de archivos nativo de Linux (`/home/<usuario>/`) es entre 5 y 10 veces más rápido que acceder al disco NTFS de Windows a través del puente de red 9P.  
En etapas posteriores, aprenderás a trabajar directamente dentro de `~/` en WSL y abrir VS Code con `code .`.

---

## 3. Checkpoint de Verificación

Antes de avanzar a la configuración de entornos virtuales, comprueba en tu consola:
- [ ] Has ejecutado el script o los comandos manuales para crear la carpeta `aprendizaje-automatico`.
- [ ] Al ejecutar `pwd`, la terminal confirma que estás dentro del directorio `aprendizaje-automatico`.
- [ ] El comando `ls -la` lista las carpetas `src`, `data`, `notebooks`, `config` y los archivos iniciales.
- [ ] Tu carpeta es visible en tu Escritorio (o en tu explorador de archivos).
