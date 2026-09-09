### ¿Por qué repetir?

Muchas tareas requieren repetir una o más sentencias una cantidad determinada de veces, o mientras se cumpla una condición. Las estructuras de repetición (bucles) lo resuelven.

### El bucle `while`

Repite un bloque **mientras** se cumpla una condición. Puede necesitar una condición de inicio y un incremento de una variable.

```python
num = 0
while num <= 5:
    print("Vuelta:", num)
    num = num + 1
```

> ¡Ojo! Si la condición nunca se deja de cumplir, el bucle es infinito. En microcontroladores eso se usa a propósito para el programa principal, pero hay que tener cuidado en otros casos.

### El bucle `for`

Repite un bloque **una cantidad conocida de veces**. Itera sobre un iterable, como `range()`.

```python
for i in range(5):
    print("Repetición:", i)
```

`range(inicio, fin, paso)` permite más control:

```python
# Del 1 al 10 de a 2
for i in range(1, 11, 2):
    print(i)

# En orden inverso
for i in range(10, 0, -1):
    print("Cuenta regresiva:", i)
```

### Recorrer colecciones

El `for` también recorre listas y cadenas:

```python
puntajes = [100, 250, 40]
for p in puntajes:
    print("Puntaje:", p)

for letra in "PAC":
    print(letra)
```

### `break` y `continue`

- `break`: corta el bucle de inmediato.
- `continue`: salta a la siguiente iteración.

```python
for i in range(10):
    if i == 3:
        continue          # salta el 3
    if i == 7:
        break             # corta en el 7
    print(i)
```

### Bucles anidados

Un bucle dentro de otro, útil para tablas o matrices:

```python
for fila in range(3):
    for col in range(4):
        print(f"({fila},{col})", end=" ")
    print()
```

### Micro-desafío práctico

> Escribí un programa que muestre la tabla de multiplicar del 7 usando un `for`, y una versión con `while` que sume los números pares del 1 al 50.

### Resumen

- `while` repite mientras se cumpla una condición.
- `for` repite un número conocido de veces usando `range()`.
- `break` corta el bucle; `continue` salta a la siguiente vuelta.
- Los bucles se pueden anidar.
- En microcontroladores, `while True:` crea el bucle principal infinito.
