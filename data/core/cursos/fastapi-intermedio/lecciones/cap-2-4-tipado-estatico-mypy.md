### 2.4 Type Hinting y Chequeo Estático con Mypy (Type Hinting & Mypy)

El **Type Hinting** (PEP 484) permite añadir anotaciones de tipo al código de Python. Aunque el intérprete de Python no fuerza las anotaciones en tiempo de ejecución, herramientas como **`mypy`** las utilizan para detectar inconsistencias de tipos de forma estática antes de desplegar a producción.

---

### 1. Primeros Pasos con Mypy (Getting Started)

`mypy` es el analizador estático de tipos por excelencia en el ecosistema de Python.

#### Instalación y Ejecución
```bash
pip install mypy
```

Para verificar la integridad de tipos de un proyecto:
```bash
mypy src/
```

#### Detección de Errores de Tipos
```python
# script_con_error.py
def calcular_promedio(valores: list[float]) -> float:
    return sum(valores) / len(valores)

# Error: se pasa una cadena en lugar de una lista
resultado = calcular_promedio("10.0")
```

Al auditar con `mypy script_con_error.py`:
```text
error: Argument 1 to "calcular_promedio" has incompatible type "str"; expected "list[float]"  [arg-type]
```

---

### 2. El Módulo `typing`

El módulo estándar `typing` provee los constructores de tipos necesarios para anotar estructuras complejas.

#### A. `Any` (Desactivación de Comprobación Estática)
Indicador para permitir cualquier tipo sin validación de `mypy`. Debe usarse con moderación.

#### B. `Callable` (Tipado de Funciones y Callbacks)
Permite anotar argumentos que aceptan funciones: `Callable[[TiposEntrada], TipoRetorno]`.

```python
from typing import Callable

def procesar_datos(
    datos: list[float],
    filtro: Callable[[float], bool]
) -> list[float]:
    return [x for x in datos if filtro(x)]
```

#### C. `cast` (Forzado Explícito de Tipos)
Informa a `mypy` que trate una variable como si fuera de un tipo específico en tiempo de análisis:

```python
from typing import Any, cast

def leer_configuracion(clave: str) -> Any:
    return {"puerto": 8000}[clave]

# cast forzado para mypy
puerto = cast(int, leer_configuracion("puerto"))
```

#### D. Genéricos y Metadatos (`TypeVar` y `Annotated`)
```python
from typing import TypeVar, Annotated

T = TypeVar("T")

def obtener_primero(items: list[T]) -> T | None:
    return items[0] if items else None

# Annotated para metadatos descriptivos
PresionPsi = Annotated[float, "Presión medida en PSI entre 0 y 500"]
```

---

### Resumen de la Lección
Usar Type Hints junto a `mypy` previene fallos silenciosos de tipo antes de tiempo y facilita el autocompletado inteligente en el IDE.
