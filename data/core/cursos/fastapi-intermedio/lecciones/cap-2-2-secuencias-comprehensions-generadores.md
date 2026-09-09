### 2.2 Operaciones sobre Secuencias: List Comprehensions y Generadores (Operating Over Sequences)

Python proporciona estructuras de datos integradas de alto rendimiento (`list`, `tuple`, `dict`, `set`) e sintaxis expresiva para transformar secuencias mediante **List Comprehensions** y **Generadores** de memoria eficiente.

---

### 1. Estructuras de Datos Nativas (Data Structures)

| Estructura | Sintaxis | Mutabilidad | Ordenada | Complejidad Búsqueda |
| :--- | :--- | :--- | :--- | :--- |
| **Lista (`list`)** | `[1, 2, 3]` | Mutable | Sí | $O(n)$ |
| **Tupla (`tuple`)** | `(1, 2, 3)` | Inmutable | Sí | $O(n)$ |
| **Diccionario (`dict`)** | `{"k": "v"}` | Mutable | Sí (Python 3.7+) | $O(1)$ promedio |
| **Conjunto (`set`)** | `{1, 2, 3}` | Mutable | No | $O(1)$ promedio |

---

### 2. Comprensión de Listas (List Comprehensions)

Las **List Comprehensions** ofrecen una sintaxis concisa y optimizada a nivel de C para filtrar y transformar secuencias en una sola línea.

#### Sintaxis Básica:
`[expresion for elemento in iterable if condicion]`

```python
lecturas_raw = [12.4, -999.0, 45.1, 0.0, -999.0, 88.3]

# Filtrar lecturas anómalas (-999.0) y convertir a Fahrenheit
lecturas_f = [round((c * 9/5) + 32, 2) for c in lecturas_raw if c != -999.0]
# Resultado: [54.32, 113.18, 32.0, 190.94]
```

#### Dictionary y Set Comprehensions:
```python
# Dict Comprehension
sensores = ["s1", "s2", "s3"]
umbrales = {s: 100.0 for s in sensores}  # {'s1': 100.0, 's2': 100.0, 's3': 100.0}

# Set Comprehension (elimina duplicados automáticamente)
plantas_raw = ["Avellaneda", "Pilar", "Avellaneda", "Rosario"]
plantas_unicas = {p.upper() for p in plantas_raw}  # {'AVELLANEDA', 'PILAR', 'ROSARIO'}
```

---

### 3. Generadores y la Palabra Clave `yield` (Generators)

Cuando trabajamos con grandes volúmenes de datos (ej. millones de registros de sensores o archivos de datasets gigantes), cargar toda la lista en memoria RAM es ineficiente.

Un **Generador** evalúa los elementos de manera perezosa (*lazy evaluation*), calculando y retornando un valor a la vez únicamente cuando es solicitado.

#### A. Funciones Generadoras con `yield`
```python
def leer_stream_sensores(total_registros: int):
    """
    Produce registros uno a uno sin saturar la memoria RAM.
    """
    for i in range(1, total_registros + 1):
        # yield suspende la función y retorna el valor actual
        yield {"id": f"sensor_{i}", "valor": i * 1.5}

# El generador no ocupa memoria por los 1,000,000 de elementos
stream = leer_stream_sensores(1000000)
primer_elemento = next(stream)  # {"id": "sensor_1", "valor": 1.5}
```

#### B. Expresiones Generadoras (Generator Expressions)
Tienen una sintaxis idéntica a las *list comprehensions*, pero utilizan paréntesis `()` en lugar de corchetes `[]`:

```python
import sys

# List comprehension (almacena todo en RAM)
lista_cuadrados = [x ** 2 for x in range(100000)]
# Expresión generadora (calcula bajo demanda)
gen_cuadrados = (x ** 2 for x in range(100000))

print(sys.getsizeof(lista_cuadrados))  # ~800,000 bytes
print(sys.getsizeof(gen_cuadrados))     # ~200 bytes (constante)
```

---

### Resumen de la Lección
Las *list comprehensions* mejoran la legibilidad y velocidad al transformar secuencias, mientras que los *generadores* con `yield` o sintaxis `()` permiten procesar flujos masivos de datos con consumo de memoria cercano a cero.
