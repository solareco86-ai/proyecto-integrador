### Servicios de dominio del juego

La **IA de los fantasmas** y la **detección de colisiones** son lógica transversal: no pertenecen naturalmente a una sola entidad. Por eso las modelamos como **servicios de dominio**.

### La entidad Fantasma

```python
class Fantasma:
    def __init__(self, x, y, nombre, color):
        self.x = x
        self.y = y
        self.nombre = nombre      # Blinky, Pinky, Inky, Clyde
        self.color = color
        self.direccion = "STOP"
        self.movimiento_restante = 0
        self.paso_demora = 2      # los fantasmas son más lentos
```

### Servicio: IA básica de los fantasmas

En cada intersección el fantasma elige entre las **direcciones válidas** (sin volver sobre sus pasos) y, con cierta probabilidad, prefiere las que **acortan la distancia** hacia Pac-Man:

```python
import random

class IA_Fantasmas:
    def __init__(self):
        self.opuestos = {"UP": "DOWN", "DOWN": "UP",
                         "LEFT": "RIGHT", "RIGHT": "LEFT"}

    def elegir_direccion(self, fantasma, pacman, laberinto):
        validas = []
        for nombre, dir in DIRECCIONES.items():
            if nombre == "STOP":
                continue
            nx = fantasma.x + dir.dx
            ny = fantasma.y + dir.dy
            if laberinto.es_celda_libre(nx, ny):
                if nombre != self.opuestos.get(fantasma.direccion):
                    validas.append(nombre)

        # callejón sin salida: permitir volver
        if not validas and fantasma.direccion != "STOP":
            op = self.opuestos[fantasma.direccion]
            d = DIRECCIONES[op]
            if laberinto.es_celda_libre(fantasma.x + d.dx, fantasma.y + d.dy):
                validas.append(op)

        if not validas:
            return "STOP"

        # 30% de probabilidad de perseguir acortando distancia
        persecucion = []
        for nombre in validas:
            d = DIRECCIONES[nombre]
            nx = fantasma.x + d.dx
            ny = fantasma.y + d.dy
            dist_actual = abs(fantasma.x - pacman.x) + abs(fantasma.y - pacman.y)
            dist_nueva = abs(nx - pacman.x) + abs(ny - pacman.y)
            if dist_nueva < dist_actual:
                persecucion.append(nombre)

        if persecucion and random.random() < 0.3:
            return random.choice(persecucion)
        return random.choice(validas)

    def actualizar(self, fantasma, pacman, laberinto):
        fantasma.movimiento_restante += 1
        if fantasma.movimiento_restante < fantasma.paso_demora:
            return
        fantasma.movimiento_restante = 0
        fantasma.direccion = self.elegir_direccion(fantasma, pacman, laberinto)
        d = DIRECCIONES[fantasma.direccion]
        fantasma.x += d.dx
        fantasma.y += d.dy
```

> La IA usa solo reglas del dominio (distancias, celdas libres) y `random`; no conoce el renderizador ni los pines.

### Servicio: detección de colisiones

```python
class Colisiones:
    @staticmethod
    def pacman_vs_fantasma(pacman, fantasma):
        return pacman.x == fantasma.x and pacman.y == fantasma.y

    @staticmethod
    def alguno(pacman, fantasmas):
        for fantasma in fantasmas:
            if Colisiones.pacman_vs_fantasma(pacman, fantasma):
                return fantasma
        return None
```

### Coordinación desde el dominio

El dominio también sabe cómo **avanzar un paso del juego**:

```python
class Partida:
    def __init__(self, laberinto, pacman, fantasmas):
        self.laberinto = laberinto
        self.pacman = pacman
        self.fantasmas = fantasmas
        self.puntaje = 0
        self.estado = "JUGANDO"    # JUGANDO, GAME_OVER, VICTORIA

    def paso(self, ia, colisiones):
        self.puntaje += self.pacman.actualizar(self.laberinto)
        for fantasma in self.fantasmas:
            ia.actualizar(fantasma, self.pacman, self.laberinto)
        if colisiones.alguno(self.pacman, self.fantasmas):
            self.estado = "GAME_OVER"
        elif not self.laberinto.bolitas and not self.laberinto.poderes:
            self.estado = "VICTORIA"
```

### Micro-desafío práctico

> Proponé una mejora simple a la IA: que los fantasmas se muevan con velocidades distintas (Blinky más rápido) o que huyan si Pac-Man comió un poder. ¿Dónde ubicarías ese cambio según DDD?

### Resumen

- La IA de fantasmas es un servicio de dominio con lógica de decisión.
- La detección de colisiones es otro servicio de dominio.
- `Partida.paso()` coordina dominio sin conocer la infraestructura.
- Los servicios solo dependen del dominio (laberinto, entidades).
- Modificar la IA o la velocidad no toca el renderizado ni el hardware.
