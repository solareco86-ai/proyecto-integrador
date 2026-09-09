### El movimiento como regla del dominio

El movimiento de Pac-Man es lógica pura del dominio: decidir a qué celda moverse, validar contra el laberinto y actualizar la posición. **No involucra hardware ni renderizado.**

### Value Objects de dirección

Reutilizamos los value objects definidos en DDD:

```python
class Direccion:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

ARRIBA = Direccion(0, -1)
ABAJO = Direccion(0, 1)
IZQUIERDA = Direccion(-1, 0)
DERECHA = Direccion(1, 0)
```

### La entidad PacMan

```python
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direccion_actual = "STOP"
        self.direccion_solicitada = "STOP"
        self.animacion = 0

    def solicitar_direccion(self, direccion):
        self.direccion_solicitada = direccion

    def actualizar(self, laberinto):
        # Intentar girar hacia la dirección solicitada si es posible
        if self.direccion_solicitada != "STOP":
            dir = DIRECCIONES[self.direccion_solicitada]
            if laberinto.es_celda_libre(self.x + dir.dx, self.y + dir.dy):
                self.direccion_actual = self.direccion_solicitada
                self.direccion_solicitada = "STOP"

        # Avanzar en la dirección actual
        if self.direccion_actual != "STOP":
            dir = DIRECCIONES[self.direccion_actual]
            if laberinto.es_celda_libre(self.x + dir.dx, self.y + dir.dy):
                self.x += dir.dx
                self.y += dir.dy
            else:
                self.direccion_actual = "STOP"   # chocó contra una pared

        # Comer bolitas
        if laberinto.comer_bolita(self.x, self.y):
            return 10    # puntos ganados
        return 0
```

Con el diccionario:

```python
DIRECCIONES = {
    "UP": ARRIBA,
    "DOWN": ABAJO,
    "LEFT": IZQUIERDA,
    "RIGHT": DERECHA,
    "STOP": Direccion(0, 0),
}
```

> Nota la separación: `solicitar_direccion` (intención del jugador) y `actualizar` (regla del dominio). El dominio decide si el giro es válido.

### Probarlo sin pantalla (ventaja del dominio puro)

Como el dominio no depende de pygame ni de machine, se puede **probar en la PC** con un test simple:

```python
def test_pacman_choca_con_pared():
    laberinto = Laberinto(LEVEL_MAP)
    pacman = PacMan(15, 15)
    pacman.solicitar_direccion("LEFT")
    x0, y0 = pacman.x, pacman.y
    pacman.actualizar(laberinto)
    assert (pacman.x, pacman.y) == (x0, y0)  # no se movió
```

### Micro-desafío práctico

> Escribí el laberinto de prueba más simple posible (5x5 con una pared central) y verificá manualmente tres casos: movimiento libre, giro válido y choque contra pared.

### Resumen

- El movimiento es una regla del dominio, independiente del hardware.
- `solicitar_direccion` guarda la intención; `actualizar` aplica las reglas.
- El laberinto valida cada celda antes de moverse.
- Al chocar contra una pared, Pac-Man se detiene.
- El dominio puro se puede probar sin pantalla ni placa.
