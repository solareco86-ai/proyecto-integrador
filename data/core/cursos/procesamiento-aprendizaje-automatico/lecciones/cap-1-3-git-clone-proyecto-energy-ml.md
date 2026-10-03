# Guía de Laboratorio Práctico — Capítulo 1: La Terminal, Git y el Entorno de Trabajo en Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 1. Objetivos de Aprendizaje y Competencias

Al finalizar este laboratorio, el estudiante será capaz de:
1. Comprender los fundamentos de los sistemas de control de versiones distribuidos (Git) y la plataforma GitHub.
2. Configurar la identidad global de autor en Git (`user.name` y `user.email`).
3. Descargar el caso de estudio oficial del curso mediante el comando `git clone https://github.com/datamaq-automation/energy-ml`.
4. Inspeccionar la anatomía de un repositorio profesional de Machine Learning con arquitectura limpia y verificar su estado con `git status` y `git log`.

---

## 2. Sección 1.3: Control de Versiones con Git y Descarga del Proyecto Base (`energy-ml`)

### 2.1. Conceptos Fundamentales: ¿Por qué clonamos en lugar de descargar un ZIP?

En ingeniería de software y desarrollo de Machine Learning profesional:
* **Repositorio de Git:** Es una base de datos que registra la evolución histórica completa de un proyecto (quién modificó qué línea, en qué fecha y por qué motivo).
* **`git clone` vs. Descargar ZIP:** Descargar un archivo comprimido sólo copia una foto estática del código, perdiendo todo el árbol de commits, ramas y la capacidad de sincronización. Al ejecutar `git clone`, se descarga el proyecto completo junto con su historial `.git/`, permitiendo recibir actualizaciones (`git pull`) y trabajar con asistentes de código y agentes autónomos.
* **El Proyecto `energy-ml`:** Es el repositorio de código abierto y caso de estudio oficial del curso (desarrollado bajo los lineamientos académicos del ISFT N° 199). Implementa monitoreo no intrusivo de cargas eléctricas (NILM) mediante modelos de clustering (DBSCAN), evaluación con matriz de confusión y exposición de APIs REST con FastAPI.

---

### 2.2. Configuración Inicial de Identidad en Git

Antes de interactuar con repositorios, Git necesita saber quién eres para firmar tus futuros commits y auditorías. Ejecuta en tu terminal:

```bash
# 1. Configurar tu nombre completo (o alias profesional)
git config --global user.name "Tu Nombre"

# 2. Configurar tu correo electrónico institucional o personal
git config --global user.email "tu.email@ejemplo.com"

# 3. Comprobar que la configuración quedó registrada correctamente
git config --list --show-origin | grep -E "user\.(name|email)"
```

---

### 2.3. Paso a Paso: Navegación y Clonado en el Espacio de Trabajo

#### Paso 1: Posicionarse en la carpeta del curso
Abre tu consola (**Git Bash**, **WSL** o **GNU/Linux Nativo**) y navega a la carpeta `aprendizaje-automatico` que creamos en la lección 1.2:

```bash
# Navegar hacia el directorio de trabajo (adaptado a tu plataforma)
if [ -d "$HOME/Desktop/aprendizaje-automatico" ]; then
    cd "$HOME/Desktop/aprendizaje-automatico"
elif [ -d "$HOME/Escritorio/aprendizaje-automatico" ]; then
    cd "$HOME/Escritorio/aprendizaje-automatico"
elif [ -d "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico" ]; then
    cd "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico"
elif [ -d "/c/Users/$USERNAME/Desktop/aprendizaje-automatico" ]; then
    cd "/c/Users/$USERNAME/Desktop/aprendizaje-automatico"
else
    # Si estás en cualquier otra ubicación, verifica con pwd
    pwd
fi

# Confirmar la ruta actual
pwd
```

#### Paso 2: Clonar el Repositorio Oficial
Ejecuta el comando `git clone` apuntando a la URL pública del repositorio del curso:

```bash
git clone https://github.com/datamaq-automation/energy-ml
```

Verás una salida similar a:
```text
Cloning into 'energy-ml'...
remote: Enumerating objects: 124, done.
remote: Counting objects: 100% (124/124), done.
remote: Compressing objects: 100% (78/78), done.
Receiving objects: 100% (124/124), 85.20 KiB | 2.10 MiB/s, done.
Resolving deltas: 100% (42/42), done.
```

#### Paso 3: Ingresar al Proyecto Clonado
Navega dentro de la carpeta descargada:

```bash
cd energy-ml
pwd
```

---

### 2.4. Anatomía del Repositorio `energy-ml`

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

### 2.5. Primeros Comandos de Verificación en Git

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

## 3. Checkpoint de Verificación

Antes de avanzar a la creación del entorno virtual (`venv`):
- [ ] Has configurado `user.name` y `user.email` en tu configuración global de Git.
- [ ] El comando `git clone` se completó exitosamente sin errores de red.
- [ ] La carpeta `energy-ml/` existe dentro de tu directorio de trabajo `aprendizaje-automatico`.
- [ ] Al ejecutar `git status` dentro de `energy-ml`, la terminal responde `On branch main` (o `master`) y `working tree clean`.
- [ ] Puedes visualizar el archivo `requirements.txt` ejecutando `cat requirements.txt`.
