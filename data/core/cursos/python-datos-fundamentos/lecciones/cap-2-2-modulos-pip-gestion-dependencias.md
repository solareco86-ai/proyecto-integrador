### Módulos: organizar y reutilizar código

Un **módulo** es un archivo `.py` con código reutilizable. Los módulos permiten separar la lógica en unidades manejables y compartir funciones entre proyectos.

```python
# modulos/matematica.py
def promedio(lista):
    return sum(lista) / len(lista)

def maximo(lista):
    return max(lista)
```

Para usar las funciones en otro archivo:

```python
from modulos.matematica import promedio, maximo

datos = [10, 20, 30]
print(promedio(datos))
```

### Paquetes de terceros y pip

La comunidad publica paquetes en el **PyPI** (Python Package Index). El instalador estándar es **`pip`**:

```bash
# Verificar la versión de pip
pip --version

# Instalar un paquete
pip install pandas

# Instalar una versión específica
pip install numpy==1.26.4

# Ver los paquetes instalados
pip list
```

> Recordá instalar los paquetes **dentro del entorno virtual activado** para no contaminar el sistema.

### El archivo requirements.txt

El archivo `requirements.txt` documenta las dependencias del proyecto y permite reproducirlas en otro equipo:

```text
numpy==1.26.4
pandas==2.2.2
matplotlib==3.9.2
jupyter==1.0.0
```

Para generarlo automáticamente:

```bash
pip freeze > requirements.txt
```

Para instalarlo desde cero:

```bash
pip install -r requirements.txt
```

### Buenas prácticas de dependencias

| Práctica | Razón |
| :--- | :--- |
| Fijar versiones (`==`) | Reproducibilidad entre equipos |
| No incluir el entorno virtual en Git | Evitar archivos enormes e incompatibles |
| Documentar en README | Que cualquiera pueda instalar el proyecto |
| Actualizar con cuidado | Los cambios de versión pueden romper código |

### Micro-desafío práctico

> Creá un módulo `analisis.py` con una función `consumo_total(mediciones)`. Instalá el paquete `pandas` en tu entorno virtual, generá un `requirements.txt` y verificá que el archivo incluya a `pandas`.

### Resumen

- Los módulos organizan el código en archivos reutilizables.
- `pip` instala paquetes desde PyPI.
- `requirements.txt` documenta y reproduce las dependencias.
- Fijar versiones y excluir el `venv` de Git son buenas prácticas esenciales.
