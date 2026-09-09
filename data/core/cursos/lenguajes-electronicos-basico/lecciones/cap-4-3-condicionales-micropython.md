### ¿Por qué decidir?

En un programa no siempre se ejecutan las mismas sentencias. A veces, según el valor de variables o señales externas, hay que cambiar la secuencia de ejecución. Las estructuras condicionales permiten tomar caminos distintos.

### La sentencia `if`

Ejecuta un bloque solo si la condición es verdadera (camino del SI). Si es falsa, no hace nada.

```python
temperatura = 28

if temperatura > 25:
    print("Hace calor, encender el ventilador")
```

### La sentencia `if / else`

Ejecuta un bloque si la condición es verdadera y **otro** si es falsa (camino del NO).

```python
tiene_bolitas = True

if tiene_bolitas:
    print("Seguir comiendo")
else:
    print("Nivel completado")
```

### La sentencia `if / elif / else`

Permite evaluar varias condiciones en cadena. `elif` es la abreviatura de "else if".

```python
puntaje = 250

if puntaje >= 1000:
    nivel = "experto"
elif puntaje >= 500:
    nivel = "avanzado"
elif puntaje >= 100:
    nivel = "intermedio"
else:
    nivel = "principiante"

print("Nivel:", nivel)
```

> Las condiciones se evalúan en orden: al cumplirse una, se ejecuta su bloque y se salta el resto.

### El operador ternario

MicroPython también permite una condicional compacta en una línea:

```python
estado = "ganó" if puntaje == 0 else "continúa"
```

Es equivalente a:

```python
if puntaje == 0:
    estado = "ganó"
else:
    estado = "continúa"
```

### Anidar condicionales

Se pueden poner condicionales dentro de condicionales:

```python
comiendo = True
con_poder = False

if comiendo:
    if con_poder:
        print("Pac-Man puede comer fantasmas")
    else:
        print("Evitar los fantasmas")
```

### Micro-desafío práctico

> Escribí un programa que lea una nota del 0 al 10 y muestre: Aprobado (>= 6), Desaprobado (< 4) o Recupera (4 a 5.99), usando if/elif/else.

### Resumen

- `if` ejecuta un bloque cuando la condición es verdadera.
- `else` cubre el caso contrario.
- `elif` encadena varias condiciones.
- El operador ternario condensa un if/else en una línea.
- Las condicionales se pueden anidar.
