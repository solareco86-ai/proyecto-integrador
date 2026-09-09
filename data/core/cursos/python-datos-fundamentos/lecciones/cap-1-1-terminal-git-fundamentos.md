### La terminal y su importancia en Ciencia de Datos

La **terminal** (o línea de comandos) es la puerta de entrada a las herramientas profesionales de datos: ejecutar scripts, gestionar entornos virtuales, usar Git y conectarse a servidores. Aunque existen interfaces gráficas, la terminal es rápida, reproducible y es donde se ejecutan la mayoría de las herramientas de datos.

### Comandos básicos de navegación y archivos

| Comando | Acción |
| :--- | :--- |
| `pwd` | Muestra el directorio actual |
| `ls` | Lista los archivos y carpetas |
| `cd <carpeta>` | Cambia de directorio |
| `mkdir <nombre>` | Crea una carpeta |
| `touch <archivo>` | Crea un archivo vacío |
| `rm <archivo>` | Elimina un archivo |

Ejemplo de sesión:

```bash
mkdir proyecto-datos
cd proyecto-datos
touch datos.csv
ls
```

### ¿Qué es Git y por qué usarlo?

**Git** es un sistema de control de versiones distribuido: registra un historial de todos los cambios de tu proyecto. En ciencia de datos es indispensable para reproducir experimentos, colaborar y deshacer errores.

### Flujo básico de Git

```bash
# Configuración inicial (una sola vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Inicializar un repositorio
git init

# Ver el estado de los cambios
git status

# Preparar archivos para el commit
git add datos.csv

# Guardar el cambio en el historial local
git commit -m "Agrego dataset de consumo energético"

# Ver el historial
git log --oneline
```

### Ramas (branches)

Las ramas permiten trabajar en paralelo sin romper la versión estable:

```bash
# Crear y moverse a una rama nueva
git branch feature/limpieza
git checkout feature/limpieza

# Volver a la rama principal
git checkout main

# Fusionar la rama de trabajo
git merge feature/limpieza
```

### Repositorio remoto (GitHub)

Para compartir el proyecto:

```bash
git remote add origin https://github.com/tu-usuario/proyecto-datos.git
git push -u origin main
```

### Micro-desafío práctico

> Creá una carpeta `mi-primer-repo`, inicializá Git, agregá un archivo `README.md` con una línea de texto y realizá tu primer commit.

### Resumen

- La terminal es la base del flujo de trabajo en datos.
- Git registra el historial de cambios y habilita la colaboración.
- El flujo básico es: `add` → `commit` → `push`.
- Las ramas permiten trabajar en paralelo de forma segura.
