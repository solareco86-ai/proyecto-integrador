# Guía de Laboratorio Práctico — Capítulo 1: La Terminal, Git y el Entorno de Trabajo en Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## Objetivos de Aprendizaje

Al finalizar esta lección, el estudiante será capaz de:
1. Comprender los fundamentos de los sistemas de control de versiones distribuidos (Git) y la plataforma GitHub.
2. Configurar la identidad global de autor en Git mediante un script interactivo con validación de entradas.
3. Descargar el caso de estudio oficial del curso mediante el comando `git clone https://github.com/datamaq-automation/energy-ml`.
4. Inspeccionar la anatomía de un repositorio profesional de Machine Learning con arquitectura limpia y verificar su estado con `git status` y `git log`.

---

## 1. Conceptos Fundamentales: ¿Por qué clonamos en lugar de descargar un ZIP?

En ingeniería de software y desarrollo de Machine Learning profesional:
* **Repositorio de Git:** Es una base de datos que registra la evolución histórica completa de un proyecto (quién modificó qué línea, en qué fecha y por qué motivo).
* **`git clone` vs. Descargar ZIP:** Descargar un archivo comprimido sólo copia una foto estática del código, perdiendo todo el árbol de commits, ramas y la capacidad de sincronización. Al ejecutar `git clone`, se descarga el proyecto completo junto con su historial `.git/`, permitiendo recibir actualizaciones (`git pull`) y trabajar con asistentes de código y agentes autónomos.
* **El Proyecto `energy-ml`:** Es el repositorio de código abierto y caso de estudio oficial del curso (desarrollado bajo los lineamientos académicos del ISFT N° 199). Implementa monitoreo no intrusivo de cargas eléctricas (NILM) mediante modelos de clustering (DBSCAN), evaluación con matriz de confusión y exposición de APIs REST con FastAPI.

---

## 2. Configuración Interactiva de Identidad en Git

Antes de interactuar con repositorios, Git necesita asociar cada commit a tu nombre y correo electrónico.

Para evitar configurar accidentalmente valores genéricos o incompletos, copia y pega el siguiente script interactivo en tu terminal. Si ya tienes nombre o correo configurados en Git, el script no te los vuelve a pedir: solo consulta el dato que falte.

```bash
# ==========================================================
# Configuración Interactiva de Identidad en Git
# ==========================================================
echo "=========================================================="
echo "👤 Configuración de Identidad en Git"
echo "=========================================================="

GIT_NAME="$(git config --global user.name)"
GIT_EMAIL="$(git config --global user.email)"

if [ -z "$GIT_NAME" ]; then
    while [ -z "$GIT_NAME" ]; do
        read -p "Ingresa tu nombre y apellido (ej. Juan Pérez): " GIT_NAME
        if [ -z "$GIT_NAME" ]; then
            echo "⚠️  El nombre no puede estar vacío. Inténtalo de nuevo."
        fi
    done
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$GIT_EMAIL" ]; then
    while [ -z "$GIT_EMAIL" ]; do
        read -p "Ingresa tu correo electrónico (ej. juan@ejemplo.com): " GIT_EMAIL
        if [ -z "$GIT_EMAIL" ]; then
            echo "⚠️  El correo no puede estar vacío. Inténtalo de nuevo."
        fi
    done
    git config --global user.email "$GIT_EMAIL"
fi

echo ""
echo "✅ ¡Identidad de Git lista!"
echo "   Nombre registrado: $(git config --global user.name)"
echo "   Email registrado:  $(git config --global user.email)"
echo "=========================================================="
```
> [!NOTE]
> Este script utiliza el comando `read -p` de Bash (el equivalente a `input()` en Python) para solicitar los datos por teclado, asegurando que no se guarden campos vacíos.

---

## 3. Navegación y Clonado en el Espacio de Trabajo

### Paso 1: Posicionarse en la carpeta del curso
Abre tu consola (**Git Bash**, **WSL** o **GNU/Linux Nativo**) y navega a la carpeta `aprendizaje-automatico` creada en la lección 1.2:

```bash
# Navegar hacia el directorio de trabajo
if [ -d "$HOME/Desktop/aprendizaje-automatico" ]; then
    cd "$HOME/Desktop/aprendizaje-automatico"
elif [ -d "$HOME/Escritorio/aprendizaje-automatico" ]; then
    cd "$HOME/Escritorio/aprendizaje-automatico"
elif [ -d "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico" ]; then
    cd "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico"
elif [ -d "/c/Users/$USERNAME/Desktop/aprendizaje-automatico" ]; then
    cd "/c/Users/$USERNAME/Desktop/aprendizaje-automatico"
fi

# Confirmar la ruta actual
pwd
```

### Paso 2: Clonar el Repositorio Oficial
Ejecuta el comando `git clone` apuntando a la URL pública del repositorio del curso:

```bash
git clone https://github.com/datamaq-automation/energy-ml
```

> [!NOTE]
> **Salida esperada en terminal:** La siguiente información es el reporte automático que genera Git tras la descarga. Es de **solo lectura** (no debes ejecutarla ni copiarla):

```output
Cloning into 'energy-ml'...
remote: Enumerating objects: 124, done.
remote: Counting objects: 100% (124/124), done.
remote: Compressing objects: 100% (78/78), done.
Receiving objects: 100% (124/124), 85.20 KiB | 2.10 MiB/s, done.
Resolving deltas: 100% (42/42), done.
```

### Paso 3: Ingresar al Proyecto Clonado
Navega dentro de la carpeta descargada:

```bash
cd energy-ml
pwd
```

Al ingresar a la carpeta, tu terminal reflejará que te encuentras dentro del proyecto clonado y listo para inspeccionar su estructura interna.

---

## 4. Retomar el Trabajo: Actualizar tu Copia con `git pull`

Tu clon es una copia del repositorio tal como estaba en el momento de clonarlo. Si pasan días o semanas antes de que lo retomes, el repositorio original puede tener cambios nuevos (correcciones de la cátedra, lecciones o código actualizado). Antes de seguir trabajando, actualiza tu copia.

### Paso 1: Revisar el estado de tu copia

Ubícate dentro de `energy-ml` y comprueba si tienes cambios propios sin guardar:

```bash
cd energy-ml
git status
```

Si estás en una rama de ejercicio (por ejemplo `ejercicio/diff-energia`, de la lección 2.2), vuelve a `main` antes de actualizar:

```bash
git checkout main
```

### Paso 2: Traer y aplicar las actualizaciones

```bash
git pull --ff-only
```

La opción `--ff-only` hace que Git solo avance si puede hacerlo sin mezclar historias. Si no puede, falla y no modifica nada. Así evitas combinaciones automáticas que no entiendes.

### Si Git no te deja actualizar

**Caso 1: `Your local changes ... would be overwritten by merge`** (tienes cambios sin guardar en archivos que llegan con la actualización). Guarda tus cambios temporalmente, actualiza y recupéralos:

```bash
git stash
git pull --ff-only
git stash pop
```

**Caso 2: `fatal: Not possible to fast-forward, aborting`** (tu historia local y la remota divergieron): no fuerces la actualización ni uses `git reset --hard`. Consulta con el docente antes de seguir.

> [!WARNING]
> Nunca uses `git pull --force` ni `git reset --hard` para "arreglar" una actualización: borran cambios sin posibilidad de recuperarlos.

---

## Checkpoint de Verificación

Antes de avanzar a la exploración del repositorio en la lección 1.4:
- [ ] Has configurado tu identidad en Git usando el script interactivo y verificado que tus credenciales son correctas con `git config --list`.
- [ ] El comando `git clone` se completó exitosamente sin errores de red.
- [ ] Has ingresado a la carpeta `energy-ml/` y el comando `pwd` confirma que estás dentro del proyecto.
- [ ] Tu terminal ya detecta el contexto de Git (indicando la rama activa en el prompt o permitiendo ejecutar comandos de Git).
- [ ] Sabes actualizar tu copia con `git status` y `git pull --ff-only` antes de retomar el trabajo después de un tiempo.
