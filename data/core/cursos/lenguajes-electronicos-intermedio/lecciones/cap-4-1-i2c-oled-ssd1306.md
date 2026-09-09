### El bus I2C

**I2C** (Inter-Integrated Circuit) es un bus serie de dos hilos que permite conectar varios dispositivos:

- **SDA**: línea de datos.
- **SCL**: línea de reloj.

Cada dispositivo tiene una **dirección única** (7 bits), lo que permite conectar varios periféricos al mismo par de pines. Es ideal para pantallas, sensores y memorias.

### La pantalla OLED SSD1306

La **SSD1306** es un controlador de pantallas OLED monocromas de 128x64 píxeles, con interfaz I2C. En el curso la usamos para dibujar el Pac-Man.

Se conecta así (pines típicos del ESP32):

| Pantalla | ESP32-WROOM |
| :--- | :--- |
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO22 |
| SDA | GPIO21 |

### El controlador en MicroPython

MicroPython incluye el módulo `machine.I2C` y el controlador oficial `ssd1306`:

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
```

### Verificar la pantalla

Se puede comprobar que la pantalla responda listando los dispositivos I2C:

```python
print(i2c.scan())     # debería mostrar [60] (0x3C) para la SSD1306
```

### Primer dibujo

```python
oled.fill(0)                    # limpiar (todo negro)
oled.text("Hola ESP32", 0, 0)   # texto en (x, y)
oled.show()                     # volcar a la pantalla
```

### Micro-desafío práctico

> Conectá la OLED SSD1306 al ESP32, verificá su dirección con `i2c.scan()` y mostrá tu nombre y la dirección encontrada.

### Resumen

- I2C usa dos hilos (SDA, SCL) y direcciones únicas por dispositivo.
- La SSD1306 es una OLED monocroma de 128x64 por I2C.
- Se conecta VCC, GND, SCL (GPIO22) y SDA (GPIO21).
- `i2c.scan()` lista las direcciones encontradas.
- `oled.fill(0)`, `oled.text()` y `oled.show()` son el punto de partida.
