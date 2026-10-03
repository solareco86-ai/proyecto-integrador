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
4. Entender la diferencia entre ejecutar un script como subproceso (`bash script.sh`) o en la sesión actual (`source script.sh`).
5. Crear y organizar la estructura de directorios de trabajo para proyectos de Ciencia de Datos y Machine Learning.

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

Para evitar errores manuales de tipeo y garantizar que todos comiencen desde el mismo lugar, utilizaremos un script en Bash que:
1. Detecta automáticamente la plataforma en ejecución (**Git Bash**, **WSL** o **GNU/Linux Nativo**).
2. Identifica el nombre de usuario activo.
3. Localiza el **Escritorio** (*Desktop* o *Escritorio*).
4. Crea la carpeta de trabajo del curso: `aprendizaje-automatico`.
5. Estructura los subdirectorios esenciales de un proyecto de Machine Learning (`src`, `data`, `notebooks`, `config`).

---

### 2.4. Script Bash: `preparar_entorno.sh`

Crea o guarda el siguiente archivo con el nombre `preparar_entorno.sh`:

```bash
#!/usr/bin/env bash
# ==============================================================================
# preparar_entorno.sh
# Detección de plataforma, usuario y creación del espacio de trabajo
# ISFT N° 199 — Tecnicatura Superior en Ciencia de Datos e IA
# ==============================================================================

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
    
    if command -v xdg-user-dir >/dev/null 2>&1; then
        RUTA_ESCRITORIO=$(xdg-user-dir DESKTOP)
    elif [ -d "$HOME/Escritorio" ]; then
        RUTA_ESCRITORIO="$HOME/Escritorio"
    elif [ -d "$HOME/Desktop" ]; then
        RUTA_ESCRITORIO="$HOME/Desktop"
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

# 5. Reporte y verificación
echo ""
echo "=========================================================="
echo "✅ ¡Espacio de trabajo creado con éxito!"
echo "=========================================================="
echo "📍 Directorio del proyecto:"
echo "   $CARPETA_PROYECTO"
echo ""
echo "📋 Contenido del directorio:"
ls -la "$CARPETA_PROYECTO"
echo ""

# Si se ejecutó con 'source', navegamos automáticamente
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    cd "$CARPETA_PROYECTO"
    echo "📍 Te encuentras en: $(pwd)"
else
    echo "👉 Para posicionarte dentro del proyecto en tu terminal, ejecuta:"
    echo "   cd \"$CARPETA_PROYECTO\""
fi
```

---

### 2.5. ¿Cómo ejecutar el script y por qué puede cerrarse la terminal?

Existen tres formas de interactuar con scripts en la consola y es fundamental entender la diferencia:

#### Opción A: Ejecución como subproceso (`bash preparar_entorno.sh`)
```bash
bash preparar_entorno.sh
```
* **Qué hace:** Abre un subproceso hijo de Bash, ejecuta todas las instrucciones y cuando finaliza, regresa el control a tu terminal principal.
* Luego de ejecutarlo, te mueves al directorio con el comando sugerido en pantalla:
  ```bash
  cd ~/Desktop/aprendizaje-automatico
  ```

#### Opción B: Ejecución en la sesión actual (`source preparar_entorno.sh`)
```bash
source preparar_entorno.sh
```
* **Qué hace:** Ejecuta las líneas directamente **dentro de tu terminal actual**. Al finalizar, el comando `cd` te dejará parado directamente dentro de `aprendizaje-automatico/`.

#### ⚠️ ¿Por qué se cierra la terminal si haces doble clic desde el explorador?
Si haces doble clic sobre el archivo `.sh` desde el explorador de Windows o Linux:
1. El sistema operativo abre una ventana de terminal temporal exclusivamente para correr el script.
2. El script corre en milisegundos y finaliza su tarea con éxito.
3. Como el comando terminó, **el sistema cierra automáticamente la ventana**.
4. **Regla de oro:** En desarrollo profesional, nunca se hace doble clic a los scripts. **Siempre se abre primero la terminal** (Git Bash, WSL o consola de Linux) y se ejecuta el script desde allí con comandos.

#### ⚠️ La trampa de `set -e` en sesiones interactivas
En versiones anteriores de scripts se solía incluir `set -e` (*exit on error*). Si ejecutas un script con `set -e` usando `source`, esa bandera queda grabada en tu terminal activa: **cualquier comando posterior que arroje un código distinto de cero (incluso presionar Tab o un `grep` sin resultados) cerrará inmediatamente toda tu sesión de terminal**. Por ello, el script actual omite `set -e` garantizando estabilidad.

---

### 2.6. Explicación Detallada de los Comandos Utilizados

1. **`#!/usr/bin/env bash` (*Shebang*):** Selecciona el intérprete Bash del entorno sin importar su ruta absoluta.
2. **`whoami` y `$USER` / `$USERNAME`:** Obtiene el usuario activo del sistema operativo.
3. **`grep -qi "microsoft" /proc/version`:** Inspecciona el archivo virtual del kernel `/proc/version`, que en WSL delata el kernel de Microsoft.
4. **`cmd.exe /c "echo %USERNAME%"` y `tr -d '\r'`:** Permite a WSL consultar al Windows anfitrión para ubicar su Escritorio real, eliminando los retornos de carro `\r`.
5. **`uname -o`:** Permite identificar a Git Bash gracias al identificador `Msys`.
6. **`xdg-user-dir DESKTOP`:** En Linux lee la configuración del estándar FreeDesktop (`~/.config/user-dirs.dirs`), resolviendo diferencias entre idiomas (`Desktop` vs. `Escritorio`).
7. **`mkdir -p "$CARPETA_PROYECTO/..."`:** Crea directorios recursivamente y de forma idempotente (no falla si ya existen).
8. **`cat << 'EOF' > ...` (*Here-Document*):** Redirección multilínea para escribir archivos sin encadenar comandos `echo`.
9. **`[[ "${BASH_SOURCE[0]}" != "${0}" ]]`:** Técnica avanzada que detecta si el script fue llamado mediante `source` (en cuyo caso ejecuta el `cd` en la terminal actual) o como comando externo (en cuyo caso imprime la instrucción `cd`).

---

## 3. Checkpoint de Verificación

Antes de avanzar a la clonación del repositorio de Git:
- [ ] Tu terminal permanece abierta después de ejecutar `bash preparar_entorno.sh` o `source preparar_entorno.sh`.
- [ ] Has verificado con `pwd` que estás dentro de `aprendizaje-automatico`.
- [ ] El comando `ls -la` lista las carpetas `src`, `data`, `notebooks`, `config` y los archivos iniciales.
- [ ] La carpeta es visible en tu Escritorio físico.
