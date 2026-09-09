### Tipos de datos básicos

Python ofrece tipos fundamentales que usaremos a lo largo del curso:

| Tipo | Ejemplo | Uso típico |
| :--- | :--- | :--- |
| `int` | `42` | Contadores, índices |
| `float` | `3.14` | Mediciones, métricas |
| `str` | `"energía"` | Etiquetas, texto |
| `bool` | `True` | Condiciones |

### Estructuras de datos

**Listas** (`list`): colecciones ordenadas y modificables.

```python
mediciones = [45.2, 47.1, 46.8, 45.9]
mediciones.append(48.0)
promedio = sum(mediciones) / len(mediciones)
print(f"Promedio: {promedio:.2f} kW")
```

**Diccionarios** (`dict`): pares clave-valor, ideales para datos con nombre.

```python
sensor = {
    "id": "vfd-01",
    "potencia_kw": 45.2,
    "activo": True,
}
print(sensor["potencia_kw"])
```

**Tuplas** (`tuple`): inmutables, útiles para valores que no cambian.

```python
coordenadas = (-34.6, -58.4)
```

### Control de flujo

**Condicionales:**

```python
if potencia_kw > 40:
    print("Consumo alto")
elif potencia_kw > 20:
    print("Consumo medio")
else:
    print("Consumo bajo")
```

**Bucles:**

```python
# for sobre una lista
for valor in mediciones:
    print(valor)

# while con condición
contador = 0
while contador < 3:
    print(contador)
    contador += 1
```

### Funciones

Las funciones organizan el código en bloques reutilizables:

```python
def calcular_consumo(potencia_kw, horas):
    """Calcula la energía consumida en kWh."""
    return potencia_kw * horas

consumo = calcular_consumo(45.2, 24)
print(f"Energía diaria: {consumo} kWh")
```

### Comprensiones de listas

Una forma concisa de construir listas:

```python
valores = [1, 2, 3, 4, 5]
pares = [v for v in valores if v % 2 == 0]
print(pares)  # [2, 4]
```

### Micro-desafío práctico

> Escribí una función `estadisticas(lista)` que reciba una lista de números y devuelva un diccionario con el `promedio`, el `maximo` y el `minimo`. Probala con `mediciones`.

### Resumen

- Python ofrece listas, diccionarios y tuplas para organizar datos.
- `if`/`elif`/`else` y los bucles controlan el flujo del programa.
- Las funciones encapsulan lógica reutilizable con `def`.
- Las comprensiones de listas hacen el código más conciso.
