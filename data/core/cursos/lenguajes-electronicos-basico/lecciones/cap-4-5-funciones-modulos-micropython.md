### ¿Qué es una función?

Una **función** es un bloque de código con nombre que se puede llamar varias veces. Permite organizar el programa, reutilizar lógica y darle claridad.

```python
def saludar():
    print("Hola, Lenguajes Electrónicos")

saludar()
saludar()
```

### Funciones con argumentos y retorno

Las funciones reciben **argumentos** y pueden devolver un valor con `return`:

```python
def area_rectangulo(base, altura):
    return base * altura

a = area_rectangulo(4, 3)
print("Área:", a)
```

En MicroPython las variables dentro de la función son locales; para modificar una global se usa `global`:

```python
puntaje = 0

def sumar_puntos(cantidad):
    global puntaje
    puntaje = puntaje + cantidad

sumar_puntos(100)
print("Puntaje:", puntaje)
```

### Funciones matemáticas básicas

El módulo `math` (o `umath` en MicroPython) aporta funciones matemáticas:

```python
import math

print(math.sqrt(16))      # 4.0
print(math.pow(2, 10))    # 1024.0
print(math.pi)            # 3.141592...
print(math.floor(3.7))    # 3
print(math.ceil(3.2))     # 4
```

### Funciones sobre caracteres y cadenas

A diferencia de C (donde existen `ctype.h` y `string.h`), en MicroPython las cadenas tienen métodos propios:

```python
texto = "Pac-Man"

print(texto.upper())      # PAC-MAN
print(texto.lower())      # pac-man
print(len(texto))         # 7
print(texto.startswith("Pac"))   # True
print(texto.split("-"))   # ['Pac', 'Man']
```

### Módulos

Un **módulo** es un archivo (o librería) con funciones reutilizables. Se importa con `import`:

```python
import random

print(random.randint(1, 6))     # un número al azar entre 1 y 6
```

También se puede crear un módulo propio. Guardamos en un archivo `utilidades.py`:

```python
# utilidades.py
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b
```

Y lo usamos desde otro archivo:

```python
import utilidades

print(utilidades.suma(10, 5))
```

### Micro-desafío práctico

> Creá un módulo `geometria.py` con funciones para el área del círculo y del triángulo (usando `math`), e importalo desde un programa principal que pida los datos y muestre los resultados.

### Resumen

- Las funciones organizan y reutilizan código.
- Reciben argumentos y devuelven valores con `return`.
- `import math` aporta funciones matemáticas.
- Las cadenas tienen métodos integrados (upper, split, len...).
- Los módulos agrupan funciones y se importan con `import`.
- Las variables locales viven dentro de la función; `global` expone las globales.
