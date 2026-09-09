### El renderizador OLED como adaptador

El **RenderizadorOled** implementa el puerto `Renderizador` usando la pantalla SSD1306 de 128x64. Vive en la **infraestructura**: conoce el hardware, pero el dominio no lo conoce a él.

### Escala y conversión de coordenadas

El laberinto del juego es de 26 columnas x 28 filas, y la OLED es de 128x64. Hay que **escalar** las celdas a píxeles:

- Un factor de escala de 4 píxeles por celda da 104x112: demasiado alto.
- Una solución práctica es usar una **vista recortada** o un laberinto reducido. Con escala de 4 y `cortando` las últimas filas, se muestra el área de juego principal.

```python
class RenderizadorOled(Renderizador):
    def __init__(self, ancho=128, alto=64, escala=4):
        from machine import Pin, I2C
        from ssd1306 import SSD1306_I2C

        i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
        self.oled = SSD1306_I2C(ancho, alto, i2c)
        self.escala = escala
```

### Los colores de las entidades

La OLED es **monocroma** (blanco/amarillo sobre negro), así que cada entidad se dibuja con un patrón de píxeles distinto en vez de colores:

```python
    def dibujar_pacman(self, x, y):
        e = self.escala
        # Pac-Man: bloque con "boca" (esquina vacía)
        for dy in range(e):
            for dx in range(e):
                if dx + dy < e // 2:     # deja la boca vacía
                    continue
                self.oled.pixel(x * e + dx, y * e + dy, 1)

    def dibujar_fantasma(self, x, y, patron):
        e = self.escala
        for dy in range(e):
            for dx in range(e):
                self.oled.pixel(x * e + dx, y * e + dy, 1)
```

### Las bolitas y las paredes

```python
    def dibujar_bolita(self, x, y):
        self.oled.pixel(x * self.escala + self.escala // 2,
                        y * self.escala + self.escala // 2, 1)

    def dibujar_celda(self, x, y, color):
        e = self.escala
        self.oled.fill_rect(x * e, y * e, e, e, color)
```

### El laberinto completo

La aplicación dibuja el laberinto recorriendo las celdas del dominio:

```python
    def dibujar_laberinto(self, laberinto):
        self.limpiar()
        for (x, y) in laberinto.paredes:
            self.dibujar_celda(x, y, 1)
        for (x, y) in laberinto.bolitas:
            self.dibujar_bolita(x, y)
```

### Mostrar el framebuffer

Recordá la técnica del framebuffer: se dibuja todo en memoria y se vuelca con una sola llamada:

```python
    def mostrar(self):
        self.oled.show()
```

### Micro-desafío práctico

> Adaptá `dibujar_pacman` para que la "boca" apunte según la dirección actual (pista: pasá la dirección como argumento y elegí qué esquina dejar vacía).

### Resumen

- El renderizador OLED es un adaptador de la infraestructura.
- La OLED es monocroma: las entidades se distinguen por patrones, no colores.
- El laberinto de 26x28 se adapta a 128x64 con una escala y vista recortada.
- Todo se dibuja en el framebuffer y se muestra con `show()`.
- El dominio no conoce estas decisiones: solo llama al puerto.
