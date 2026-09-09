### ¿Qué es DDD?

El **Domain-Driven Design** (DDD, de Eric Evans) es un enfoque para modelar software complejo poniendo el foco en el **dominio** (el problema que resolvemos) y en su **lenguaje ubicuo**.

> El **lenguaje ubicuo** es un vocabulario común y sin ambigüedades que comparten todos: en nuestro caso "bolita", "pared", "fantasma", "poder", "laberinto". El código, el diseño y las conversaciones usan los mismos términos.

### Entidades

Una **Entidad** es un objeto con **identidad propia** que se mantiene a lo largo del tiempo, aunque sus atributos cambien.

```python
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direccion = "STOP"
        self.animacion = 0
```

Pac-Man tiene identidad: sigue siendo Pac-Man aunque se mueva y cambie de dirección.

```python
class Fantasma:
    def __init__(self, x, y, color, nombre):
        self.x = x
        self.y = y
        self.color = color
        self.nombre = nombre      # Blinky, Pinky, Inky, Clyde
        self.direccion = "STOP"
```

### Value Objects

Un **Value Object** es un objeto **inmutable** que se define por sus atributos y no tiene identidad propia: dos iguales son intercambiables.

```python
class Posicion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otra):
        return self.x == otra.x and self.y == otra.y
```

```python
class Direccion:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

ARRIBA = Direccion(0, -1)
ABAJO  = Direccion(0, 1)
IZQ    = Direccion(-1, 0)
DER    = Direccion(1, 0)
```

### El Agregado Laberinto

Un **Agregado** agrupa entidades y value objects con una raíz que garantiza su consistencia. El **Laberinto** es la raíz: contiene las paredes y las bolitas, y valida movimientos.

```python
class Laberinto:
    def __init__(self, mapa):
        self.paredes = set()
        self.bolitas = set()
        self.poderes = set()
        self._cargar(mapa)

    def _cargar(self, mapa):
        for y, fila in enumerate(mapa):
            for x, celda in enumerate(fila):
                if celda == "#":
                    self.paredes.add((x, y))
                elif celda == ".":
                    self.bolitas.add((x, y))
                elif celda == "o":
                    self.poderes.add((x, y))

    def es_celda_libre(self, x, y):
        return (x, y) not in self.paredes

    def comer_bolita(self, x, y):
        if (x, y) in self.bolitas:
            self.bolitas.remove((x, y))
            return True
        return False
```

### Servicios de dominio

Los **Servicios de dominio** contienen lógica que no pertenece naturalmente a una entidad. La detección de colisiones es un ejemplo clásico.

```python
class Colisiones:
    @staticmethod
    def pacman_vs_fantasma(pacman, fantasma):
        return pacman.x == fantasma.x and pacman.y == fantasma.y
```

### Trazado del modelo

| Concepto DDD | Elemento del juego |
| :--- | :--- |
| Lenguaje ubicuo | bolita, pared, fantasma, laberinto, poder |
| Entidad | PacMan, Fantasma |
| Value Object | Posicion, Direccion, Puntaje |
| Agregado | Laberinto |
| Servicio de dominio | Colisiones, IA de fantasmas |

### Micro-desafío práctico

> Elegí un objeto del juego y clasificá en Entidad o Value Object. ¿El Puntaje es una Entidad o un Value Object? ¿Por qué? Justificá con las reglas de DDD.

### Resumen

- DDD pone el foco en el dominio y su lenguaje ubicuo.
- Las Entidades tienen identidad propia y ciclo de vida.
- Los Value Objects son inmutables y se comparan por valor.
- El Agregado Laberinto garantiza la consistencia del tablero.
- Los Servicios de dominio contienen lógica transversal (colisiones, IA).
- Todo este modelado vive en el dominio, sin infraestructura.
