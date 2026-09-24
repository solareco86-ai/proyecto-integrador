### Preparación del Entorno: Entorno Virtual y `requirements.txt`

Antes de escribir la primera línea de código de procesamiento de imágenes, es fundamental aislar las dependencias del proyecto del resto del sistema. Para esto se utiliza un **entorno virtual** (`venv`), que crea una instalación de Python independiente con sus propias librerías.

### Crear el Entorno Virtual (`python -m venv .venv`)

El módulo `venv` viene incluido en la instalación estándar de Python. Para crear un entorno virtual llamado `.venv` en la carpeta del proyecto:

```bash
python -m venv .venv
```

Esto genera una carpeta `.venv/` con una copia del intérprete de Python y un gestor de paquetes (`pip`) propio, sin interferir con otros proyectos ni con el Python global del sistema.

### Activar el Entorno Virtual

Una vez creado, el entorno debe activarse en cada sesión de trabajo antes de instalar o ejecutar código:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Con el entorno activado, la terminal muestra el prefijo `(.venv)` y cualquier paquete instalado con `pip install` queda aislado dentro de esa carpeta.

### Gestión de Dependencias con `requirements.txt`

El archivo `requirements.txt` lista las librerías necesarias para el proyecto, junto con sus versiones, de modo que cualquier persona (o servidor) pueda reproducir el mismo entorno:

```text
opencv-python>=4.10.0
numpy>=1.26.0
matplotlib>=3.9.0
```

Para instalar todas las dependencias listadas de una sola vez:

```bash
pip install -r requirements.txt
```

Y para dejar registradas las versiones exactas de lo instalado (útil al agregar una librería nueva):

```bash
pip freeze > requirements.txt
```

> **Buena práctica:** El directorio `.venv/` nunca se sube al control de versiones (se agrega a `.gitignore`); solo `requirements.txt` viaja con el proyecto, ya que permite recrear el entorno completo con dos comandos.
