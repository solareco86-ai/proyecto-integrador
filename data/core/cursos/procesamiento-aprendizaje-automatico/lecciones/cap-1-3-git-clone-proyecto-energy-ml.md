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

Para evitar configurar accidentalmente valores genéricos o incompletos, copia y pega el siguiente script interactivo en tu terminal:

```bash
# ==========================================================
# Configuración Interactiva de Identidad en Git
# ==========================================================
echo "=========================================================="
echo "👤 Configuración de Identidad en Git"
echo "=========================================================="

GIT_NAME=""
while [ -z "$GIT_NAME" ]; do
    read -p "Ingresa tu nombre y apellido (ej. Juan Pérez): " GIT_NAME
    if [ -z "$GIT_NAME" ]; then
        echo "⚠️  El nombre no puede estar vacío. Inténtalo de nuevo."
    fi
done

GIT_EMAIL=""
while [ -z "$GIT_EMAIL" ]; do
    read -p "Ingresa tu correo electrónico (ej. juan@ejemplo.com): " GIT_EMAIL
    if [ -z "$GIT_EMAIL" ]; then
        echo "⚠️  El correo no puede estar vacío. Inténtalo de nuevo."
    fi
done

# Aplicar la configuración global en Git
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo ""
echo "✅ ¡Identidad configurada con éxito en Git!"
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

---

## 4. Anatomía del Repositorio `energy-ml`

Explora los archivos que componen el proyecto ejecutando `ls -la`:

```bash
ls -la
```

Observarás una estructura organizada según los estándares de la industria:

```text
energy-ml/
├── .git/                 ← Base de datos interna de Git (historial y ramas)
├── .gitignore            ← Lista de exclusión (archivos que Git nunca sube)
├── .env.example          ← Plantilla pública de variables de entorno
├── README.md             ← Documentación general del caso de estudio
├── requirements.txt      ← Lista de dependencias de Python (FastAPI, Scikit-Learn)
├── data/                 ← Datos CSV de mediciones eléctricas para clustering
├── src/                  ← Código fuente en Arquitectura Hexagonal
│   ├── domain/           ← Entidades puras y lógica matemática
│   ├── application/      ← Casos de uso y DTOs de validación
│   └── infrastructure/   ← Servidor FastAPI y algoritmos de Machine Learning
└── tests/                ← Batería de pruebas automatizadas con pytest
```

---

## 5. Primeros Comandos de Verificación en Git

Estando dentro de la carpeta `energy-ml`, ejecuta los comandos indispensables de auditoría:

```bash
# 1. Comprobar la rama activa y el estado del árbol de trabajo
git status

# 2. Explorar los commits recientes del historial del proyecto
git log --oneline -n 5

# 3. Comprobar el origen remoto conectado
git remote -v
```

---

## Checkpoint de Verificación

Antes de avanzar a la creación del entorno virtual (`venv`):
- [ ] Has configurado tu identidad en Git usando el script interactivo y verificado que no contiene valores por defecto.
- [ ] El comando `git clone` se completó exitosamente sin errores de red.
- [ ] La carpeta `energy-ml/` existe dentro de tu directorio de trabajo `aprendizaje-automatico`.
- [ ] Al ejecutar `git status` dentro de `energy-ml`, la terminal responde `On branch main` (o `master`) y `working tree clean`.
- [ ] Puedes visualizar el archivo `requirements.txt` ejecutando `cat requirements.txt`.
