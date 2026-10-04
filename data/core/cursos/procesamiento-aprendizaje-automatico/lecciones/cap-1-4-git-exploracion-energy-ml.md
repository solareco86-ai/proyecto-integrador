# Guía de Laboratorio Práctico — Capítulo 1: La Terminal, Git y el Entorno de Trabajo en Python

## Lección 1.4: Anatomía y Exploración del Repositorio `energy-ml` con Git

Una vez clonado el proyecto en la lección anterior, es momento de aprender a navegar e inspeccionar un repositorio profesional de Machine Learning utilizando las herramientas de diagnóstico nativas de Git.

---

## Objetivos de Aprendizaje

1. Comprender la estructura de directorios de un proyecto de Ciencia de Datos bajo arquitectura modular.
2. Identificar el rol del directorio oculto `.git/` como base de datos de control de versiones.
3. Dominar los comandos fundamentales de auditoría: `git status`, `git log`, `git branch` y `git remote`.
4. Interpretar el estado del árbol de trabajo (*working tree clean*) como garantía de integridad antes de iniciar cualquier desarrollo.

---

## 1. Confirmar la Ubicación en el Repositorio

Asegúrate de estar posicionado dentro de la carpeta `energy-ml`:

```bash
pwd
```

La salida debe reflejar que te encuentras en `.../aprendizaje-automatico/energy-ml`. Si te encuentras en el directorio padre, ingresa con:

```bash
cd energy-ml
```

---

## 2. Anatomía del Repositorio `energy-ml`

Ejecuta el listado detallado incluyendo archivos ocultos:

```bash
ls -la
```

Observarás una estructura organizada según las mejores prácticas de la industria:

```text
energy-ml/
├── .git/                 ← Base de datos interna de Git (historial, ramas y objetos)
├── .gitignore            ← Lista de exclusión (archivos que Git nunca debe rastrear)
├── .env.example          ← Plantilla pública de variables de entorno y configuración
├── README.md             ← Documentación arquitectónica del caso de estudio NILM
├── requirements.txt      ← Lista de dependencias de Python (FastAPI, Scikit-Learn, Pytest)
├── data/                 ← Registros y mediciones eléctricas para entrenamiento
├── src/                  ← Código fuente en Arquitectura Hexagonal
│   ├── domain/           ← Entidades puras y lógica matemática de desagregación
│   ├── application/      ← Servicios de aplicación y DTOs de validación
│   └── infrastructure/   ← Servidor web FastAPI y persistencia
└── tests/                ← Batería de pruebas automatizadas con pytest
```

> [!NOTE]
> **El directorio oculto `.git/`:** Es el corazón del repositorio. Contiene toda la historia, hashes SHA-1, ramas y commits del proyecto. **Nunca debes modificar ni eliminar manualmente su contenido**.

---

## 3. Comandos de Diagnóstico e Inspección en Git

### Paso 1: Estado del Árbol de Trabajo (`git status`)

El comando más utilizado en el flujo diario de un desarrollador:

```bash
git status
```

**Salida esperada (solo lectura):**

```output
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

* **`On branch main`:** Indica que estás situado en la rama principal de producción.
* **`working tree clean`:** Confirma que no existen archivos modificados, agregados ni eliminados pendientes de registrar. Tu entorno está en un estado puro y reproducible.

---

### Paso 2: Historial Reciente de Confirmaciones (`git log`)

Para entender qué cambios históricos dieron forma al proyecto:

```bash
git log --oneline -n 5
```

Este comando compacta cada commit en una sola línea (hash abreviado + mensaje descriptivo):

```output
a1b2c3d feat(nilm): implementar algoritmo de clasificacion de potencia reactiva
8e4f2a1 test(domain): incorporar pruebas unitarias de umbrales de energia
7c3d1e0 refactor(api): modularizar dependencias de fastapi
5b2a9e8 docs: documentar endpoints de telemetria en README
3f1e7a2 chore: inicializar estructura de repositorio y dependencias base
```

---

### Paso 3: Identificación de Ramas Locales y Remotas (`git branch`)

Comprueba en qué rama te encuentras y qué ramas remotas están registradas:

```bash
# Listar ramas locales
git branch

# Listar todas las ramas (incluyendo las remotas de GitHub)
git branch -a
```

El asterisco `*` antecede a la rama actualmente activa sobre la cual estás parado.

---

### Paso 4: Comprobación del Origen Remoto (`git remote -v`)

Para verificar con qué servidor central de código sincroniza tu repositorio:

```bash
git remote -v
```

**Salida esperada:**

```output
origin  https://github.com/datamaq-automation/energy-ml (fetch)
origin  https://github.com/datamaq-automation/energy-ml (push)
```

`origin` es el alias convencional que Git asigna al repositorio remoto original desde donde se clonó el proyecto.

---

## Checkpoint de Verificación

Antes de continuar a la lección 1.5 (Aislamiento de dependencias con `venv`):
- [ ] Has verificado con `ls -la` la presencia del directorio `.git/` y los archivos de configuración.
- [ ] El comando `git status` reporta `working tree clean`.
- [ ] Has inspeccionado el historial con `git log --oneline -n 5` y comprendes la estructura de los mensajes de commit.
- [ ] El comando `git remote -v` apunta correctamente a la URL de `datamaq-automation/energy-ml`.
