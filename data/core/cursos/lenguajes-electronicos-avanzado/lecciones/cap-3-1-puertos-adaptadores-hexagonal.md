### Puertos y adaptadores (arquitectura hexagonal)

El patrón **puertos y adaptadores** (arquitectura hexagonal) define contratos llamados **puertos** en el dominio, y **adaptadores** que los implementan en la infraestructura.

- **Puerto**: una interfaz (contrato) que el dominio declara.
- **Adaptador**: una implementación concreta (pygame, OLED, teclado, pulsadores) que se **inyecta** desde afuera.

El dominio no conoce qué adaptador se usa: solo conoce el contrato.

### Puerto de renderizado

El juego necesita dibujarse. El dominio declara el contrato:

```python
class Renderizador:
    """Puerto: qué puede hacer un renderizador del juego."""

    def limpiar(self):
        raise NotImplementedError

    def dibujar_celda(self, x, y, color):
        raise NotImplementedError

    def dibujar_texto(self, texto, x, y):
        raise NotImplementedError

    def mostrar(self):
        raise NotImplementedError
```

> En Python los puertos suelen ser clases base o interfaces sin implementación real: solo definen el contrato.

### Adaptador pygame (PC)

En la PC, el adaptador implementa el contrato con pygame:

```python
import pygame

class RenderizadorPygame(Renderizador):
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))

    def limpiar(self):
        self.screen.fill((0, 0, 0))

    def dibujar_celda(self, x, y, color):
        pygame.draw.rect(self.screen, color,
                         (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA))

    def dibujar_texto(self, texto, x, y):
        # renderizar con pygame.font y dibujar
        pass

    def mostrar(self):
        pygame.display.flip()
```

### Adaptador machine + OLED (ESP32)

En el ESP32, el mismo contrato se implementa con el módulo `machine` y la OLED:

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class RenderizadorOled(Renderizador):
    def __init__(self, ancho=128, alto=64):
        i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
        self.oled = SSD1306_I2C(ancho, alto, i2c)

    def limpiar(self):
        self.oled.fill(0)

    def dibujar_celda(self, x, y, color):
        # dibujar un bloque de píxeles en (x, y)
        self.oled.fill_rect(x * ESCALA, y * ESCALA, ESCALA, ESCALA, color)

    def dibujar_texto(self, texto, x, y):
        self.oled.text(texto, x, y)

    def mostrar(self):
        self.oled.show()
```

### Puerto de control (entrada del jugador)

De la misma forma, el dominio define cómo recibe la dirección:

```python
class Controlador:
    """Puerto: qué fuente de entrada conoce el juego."""

    def leer_direccion(self):
        raise NotImplementedError
```

Con dos adaptadores: el **teclado** en PC y los **pulsadores** en el ESP32.

### Composición con inyección de dependencias

El bucle de aplicación recibe los puertos por constructor (inyección): no importa nada de pygame ni de machine.

```python
class Juego:
    def __init__(self, renderizador, controlador, laberinto, pacman, fantasmas):
        self.renderizador = renderizador   # puerto
        self.controlador = controlador     # puerto
        self.laberinto = laberinto
        self.pacman = pacman
        self.fantasmas = fantasmas
```

Luego, desde la infraestructura, se arma la composición:

```python
# En la PC
juego = Juego(RenderizadorPygame(800, 600), ControladorTeclado(), laberinto, pacman, fantasmas)

# En el ESP32
juego = Juego(RenderizadorOled(), ControladorPulsadores(), laberinto, pacman, fantasmas)
```

El dominio **no cambia**: solo cambia el adaptador inyectado.

### Micro-desafío práctico

> Escribí la interfaz `Controlador` con dos adaptadores: uno de teclado (pygame) y otro de pulsadores (machine). ¿Qué devuelve `leer_direccion()` en cada caso? ¿El dominio cambia entre uno y otro?

### Resumen

- El puerto es un contrato definido en el dominio.
- El adaptador es una implementación concreta en la infraestructura.
- Renderizador (salida) y Controlador (entrada) son nuestros dos puertos.
- Se inyectan por constructor: el dominio no conoce pygame ni machine.
- Cambiar de PC a ESP32 solo implica cambiar el adaptador.
