### ¿Qué es el framebuffer?

El controlador SSD1306 dibuja sobre un **buffer en memoria** (un framebuffer de 128x64 píxeles) y recién con `show()` se envía completo a la pantalla. Esto evita parpadeos y permite actualizaciones estables.

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
```

### Operaciones básicas de dibujo

El módulo `ssd1306` ofrece primitivas simples:

```python
# Limpiar y mostrar
oled.fill(0)
oled.show()

# Texto
oled.text("Pac-Man", 0, 0)
oled.text("Score: 100", 0, 12)

# Píxeles
oled.pixel(64, 32, 1)          # un punto encendido en (64, 32)
```

### Dibujar formas (módulo framebuf)

Importando `framebuf` se suman rectángulos, líneas y círculos:

```python
import framebuf

oled.rect(10, 10, 20, 20, 1)          # borde de rectángulo
oled.fill_rect(40, 10, 20, 20, 1)     # rectángulo relleno
oled.line(0, 0, 127, 63, 1)           # línea diagonal
oled.hline(0, 40, 128, 1)             # línea horizontal
oled.vline(60, 0, 64, 1)              # línea vertical
oled.show()
```

> Nota: el círculo no está en framebuf; se dibuja con un bucle de píxeles o una tabla predefinida.

### Dibujar Pac-Man con píxeles

Un Pac-Man simple se dibuja con píxeles sobre el buffer:

```python
def dibujar_pacman(oled, cx, cy, r):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            dx = x - cx
            dy = y - cy
            if dx * dx + dy * dy <= r * r:
                # boca: solo píxeles a la derecha del centro
                if x >= cx:
                    oled.pixel(x, y, 1)
```

```python
oled.fill(0)
dibujar_pacman(oled, 30, 30, 8)
oled.show()
```

### Animación básica (mover el personaje)

Combinando bucles y pausas se logra movimiento:

```python
import time

for x in range(0, 110, 2):
    oled.fill(0)
    dibujar_pacman(oled, x, 30, 8)
    oled.show()
    time.sleep_ms(30)
```

### Micro-desafío práctico

> Dibujá un rectángulo que haga de "laberinto" y un cuadrado de 4x4 que se mueva de izquierda a derecha y vuelva, usando `fill_rect`, `oled.text` para un contador y `time.sleep_ms`.

### Resumen

- El framebuffer se dibuja en memoria y se muestra con `show()`.
- `fill`, `text`, `pixel`, `rect`, `fill_rect`, `line`, `hline` y `vline` son las primitivas.
- Los círculos se dibujan por píxeles con un bucle.
- Animar = redibujar y `show()` en cada fotograma con una pausa.
- Esta técnica es la base del renderizador del Pac-Man.
