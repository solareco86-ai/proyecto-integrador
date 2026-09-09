### ¿Qué es la arquitectura limpia?

La **arquitectura limpia** (Clean Architecture, de Robert C. Martin) es un conjunto de principios para organizar el código en **capas concéntricas** donde las dependencias apuntan siempre hacia adentro.

Las capas típicas, de afuera hacia adentro:

1. **Infraestructura** (frameworks, hardware, drivers).
2. **Aplicación** (casos de uso).
3. **Dominio** (reglas de negocio del problema).

> La regla de dependencia: el código fuente de las capas internas **no debe conocer** nada de las capas externas. La infraestructura depende del dominio; el dominio nunca depende de la infraestructura.

### Una arquitectura que "grita"

Una arquitectura buena "grita" su propósito: al leer la estructura del proyecto se entiende que es un **juego**, no que usa pygame. Si el código mezcla la lógica del juego con `pygame.display`, `pygame.draw` o `machine.Pin`, la arquitectura "grita" el framework y no el dominio.

Observá este contraejemplo típico (un programa acoplado a pygame):

```python
import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # ...
    def draw(self):
        for (x, y) in self.walls:
            pygame.draw.rect(self.screen, COLOR_WALL, (x * 32, y * 32, 32, 32))
```

Acá la clase `Game` conoce `pygame`: no se puede correr en otro lugar ni probar sin una ventana. Ese es el punto de partida que vamos a **refactorizar**.

### El dominio no conoce la infraestructura

En la versión limpia, el dominio (el juego) solo conoce sus propias reglas:

```python
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direccion = "STOP"

    def mover(self, direccion, laberinto):
        nx = self.x + DIRECCIONES[direccion][0]
        ny = self.y + DIRECCIONES[direccion][1]
        if laberinto.es_celda_libre(nx, ny):
            self.x = nx
            self.y = ny
            self.direccion = direccion
```

Fijate que `PacMan` **no importa** ni `pygame` ni `machine`: solo usa la lógica del laberinto.

### Capas en nuestro proyecto Pac-Man

| Capa | Contenido |
| :--- | :--- |
| **Dominio** | `PacMan`, `Fantasma`, `Laberinto`, `Puntaje`, direcciones, colisiones, IA. |
| **Aplicación** | El bucle principal: coordina el dominio y los puertos. |
| **Infraestructura** | Renderizador pygame (PC), renderizador `machine`+OLED (ESP32), lectura de teclado/pulsadores. |

### Micro-desafío práctico

> Observá el `run.py` de referencia (Pac-Man pygame). Identificá tres lugares donde el código mezcla lógica del juego con infraestructura (pygame) y proponé a qué capa moverías esa lógica.

### Resumen

- La arquitectura limpia organiza el código en capas con dependencias hacia adentro.
- Una buena arquitectura "grita" el dominio del problema, no el framework.
- El dominio no importa pygame ni machine.
- Nuestro proyecto tiene 3 capas: dominio, aplicación e infraestructura.
- El objetivo es poder correr el mismo juego en PC y en ESP32 cambiando solo la infraestructura.
