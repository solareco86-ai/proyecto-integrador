### Estructura de un programa en MicroPython

MicroPython es la versión de Python pensada para microcontroladores. Su sintaxis es **interpretada** (no se compila) y se delimita por **indentación**, no por llaves.

Las reglas esenciales:

- Cada línea es una instrucción.
- Los **bloques** se delimitan por dos puntos (`:`) y sangría (espacios o tabulaciones consistentes).
- No se usan punto y coma obligatorios ni llaves.

```python
# Programa más simple
print("Hola, Lenguajes Electrónicos")
```

### Tipos de datos básicos

MicroPython no declara el tipo: se asigna un valor y el tipo se **infiere** automáticamente.

| Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `int` | Números enteros | `edad = 18` |
| `float` | Números decimales | `tension = 3.3` |
| `str` | Cadenas de caracteres | `nombre = "Pac-Man"` |
| `bool` | Verdadero o falso | `encendido = True` |
| `list` | Colección ordenada | `posiciones = [1, 2, 3]` |

```python
edad = 18                 # int
tension = 3.3             # float
nombre = "Pac-Man"        # str
encendido = True          # bool
puntajes = [100, 250, 40] # list
```

### Variables locales y globales

Las variables tienen validez solo en el ambiente en que se declaran.

- **Global**: definida fuera de todas las funciones. Todas las funciones pueden leerla o modificarla.
- **Local**: definida dentro de una función. Solo esa función la reconoce.

```python
puntos = 0                      # variable global

def comer_bolita():
    puntos_parciales = 10       # variable local
    global puntos
    puntos = puntos + puntos_parciales
```

### Constantes

Python no tiene constantes en el lenguaje, pero por convención se escriben en MAYÚSCULAS y no se modifican:

```python
ANCHO_PANTALLA = 128
ALTO_PANTALLA = 64
FPS = 60
```

### Entrada y salida de datos

- `print(...)`: muestra datos en la consola.
- `input(...)`: lee texto ingresado por el usuario.

```python
nombre = input("¿Cómo te llamás? ")
print("Hola,", nombre)
```

### Micro-desafío práctico

> Escribí un programa que pida el ancho y el alto de una habitación, calcule el área y la muestre. Usá variables globales para los datos fijos y locales para los cálculos.

### Resumen

- MicroPython es interpretado y usa indentación para delimitar bloques.
- Los tipos principales son int, float, str, bool y list.
- El tipo se infiere al asignar un valor.
- Las variables globales se declaran fuera de las funciones; las locales, dentro.
- Las constantes se escriben en MAYÚSCULAS por convención.
- `print()` y `input()` permiten la entrada y salida básica.
