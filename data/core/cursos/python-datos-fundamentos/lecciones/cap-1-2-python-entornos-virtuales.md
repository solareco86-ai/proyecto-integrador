### Instalación de Python

Antes de instalar Python, verificá si ya tenés una versión disponible:

```bash
python3 --version
```

Si no la tenés o querés una versión específica, instalala desde el sitio oficial o con el gestor de paquetes de tu sistema operativo (apt, Homebrew, etc.).

> En proyectos profesionales se recomienda gestionar versiones con `pyenv`. En este curso usaremos el intérprete del sistema y entornos virtuales con `venv`, que es lo más simple para comenzar.

### Entornos virtuales con venv

Un **entorno virtual** crea una copia aislada del intérprete de Python donde se instalan las dependencias de un proyecto sin afectar al sistema ni a otros proyectos.

```bash
# Crear el entorno virtual dentro del proyecto
python3 -m venv venv

# Activarlo (Linux/macOS)
source venv/bin/activate

# Verificar que el prompt cambió e indicar la versión
which python
python --version
```

En Windows la activación es:

```bash
venv\Scripts\activate
```

### Desactivar el entorno

```bash
deactivate
```

### Estructura de un proyecto de datos

Una organización clara facilita la colaboración y la reproducción:

```text
proyecto-datos/
├── data/          # datasets crudos y procesados
├── notebooks/     # cuadernos Jupyter
├── src/           # código fuente (funciones, módulos)
├── scripts/       # scripts ejecutables
├── tests/         # pruebas automatizadas
├── requirements.txt
└── README.md
```

### Repositorios y control de versiones

Un proyecto de datos serio se versiona con Git y se sube a un repositorio remoto. Un buen `README.md` explica qué hace el proyecto y cómo ejecutarlo:

```markdown
# Proyecto de Análisis de Consumo

Análisis exploratorio del consumo energético industrial.

## Cómo ejecutar
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python scripts/procesar.py`
```

### Micro-desafío práctico

> Creá un proyecto `proyecto-datos` con la estructura de carpetas sugerida, creá un entorno virtual `venv`, activalo y verificá la versión de Python. Luego desactivalo.

### Resumen

- Verificá y gestioná la instalación de Python en tu sistema.
- `venv` aísla las dependencias de cada proyecto.
- Activá el entorno con `source venv/bin/activate`.
- Una estructura de carpetas clara y Git son la base de un proyecto reproducible.
