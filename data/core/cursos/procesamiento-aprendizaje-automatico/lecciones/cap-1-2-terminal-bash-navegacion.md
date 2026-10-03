# Guía de Laboratorio Práctico — Capítulo 1: La Terminal y el Entorno de Desarrollo Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 1. Objetivos de Aprendizaje y Competencias

Al finalizar este laboratorio, el estudiante será capaz de:
1. Operar con soltura en la interfaz de línea de comandos (Bash), gestionando rutas y archivos sin interfaz gráfica.
2. Aislar entornos de trabajo en Python 3 utilizando `venv` y administrar paquetes de forma ordenada con `pip`.
3. Implementar el resguardo seguro de credenciales (API Keys) mediante variables de entorno (`.env`), previniendo su exposición inadvertida en repositorios de código.

---

## 2. Sección 1.2: Navegación y Manipulación en Terminal (Bash)

### 2.1. Conceptos Clave
* **Ruta Absoluta vs. Relativa:** Una ruta absoluta parte desde el directorio raíz (`/`), mientras que una relativa toma como referencia el directorio de trabajo actual (`.`).
* **Navegación sin GUI:** La terminal es el entorno primario para ejecutar scripts, levantar servidores y controlar el flujo de trabajo con asistentes de código.

### 2.2. Comandos Indispensables
| Comando | Descripción |
| :--- | :--- |
| `pwd` | Muestra la ruta absoluta del directorio actual (*Print Working Directory*). |
| `ls -la` | Lista todos los archivos y carpetas, incluyendo ocultos (`.env`, `.git`), con permisos y tamaños. |
| `cd <directorio>` | Cambia el directorio de trabajo. `cd ..` asciende un nivel. |
| `mkdir -p <ruta>` | Crea directorios (y carpetas padre si no existen). |
| `touch <archivo>` | Crea un archivo vacío o actualiza su marca de tiempo. |
| `cp -r <origen> <destino>` | Copia archivos o carpetas recursivamente. |
| `mv <origen> <destino>` | Mueve o renombra archivos y directorios. |
| `rm -rf <directorio>` | Elimina archivos o directorios de forma recursiva y forzada (usar con precaución). |

### 2.3. Ejercicio Práctico 1.2: Creación de la Estructura del Proyecto
Ejecuta la siguiente secuencia de comandos en tu terminal Bash para estructurar el proyecto base:

```bash
# 1. Crear la carpeta raíz del laboratorio y navegar a ella
mkdir -p laboratorio_cap1/src laboratorio_cap1/config
cd laboratorio_cap1

# 2. Crear los archivos base de trabajo
touch README.md src/main.py .env.example .gitignore

# 3. Verificar la estructura creada
ls -la
ls -la src/
```
