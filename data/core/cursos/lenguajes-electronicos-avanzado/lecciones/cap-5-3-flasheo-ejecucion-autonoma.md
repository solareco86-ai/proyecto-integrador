### Llevar el juego al ESP32

Con el dominio, la aplicación y los adaptadores listos, el último paso es **grabar los archivos en la placa** y lograr la **ejecución autónoma**: el Pac-Man arranca solo al encender el ESP32, sin la computadora conectada.

### Estructura de archivos en la placa

MicroPython ejecuta automáticamente `main.py` al encender. La estructura típica del proyecto:

```
/ (raíz del sistema de archivos del ESP32)
├── boot.py          # configuración inicial (opcional)
├── main.py          # se ejecuta al encender: compone y arranca el juego
├── dominio.py       # PacMan, Fantasma, Laberinto, Direccion, Colisiones, IA
└── infraestructura.py  # RenderizadorOled, ControladorPulsadores
```

> Es conveniente separar archivos igual que en PC, respetando las capas de la arquitectura limpia.

### El `main.py` (composición en infraestructura)

```python
from dominio import Laberinto, PacMan, Fantasma, Partida, IA_Fantasmas, Colisiones
from infraestructura import RenderizadorOled, ControladorPulsadores
from aplicacion import MotorDeJuego

MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "############################",
]

laberinto = Laberinto(MAP)
pacman = PacMan(15, 20)
fantasmas = [
    Fantasma(11, 3, "Blinky", 0),
    Fantasma(14, 3, "Pinky", 0),
    Fantasma(17, 3, "Inky", 0),
    Fantasma(14, 13, "Clyde", 0),
]

partida = Partida(laberinto, pacman, fantasmas)
juego = MotorDeJuego(
    partida=partida,
    renderizador=RenderizadorOled(),
    controlador=ControladorPulsadores(),
    ia=IA_Fantasmas(),
    colisiones=Colisiones(),
    fps=8,
)
juego.ejecutar()
```

### Controlador de pulsadores

En el ESP32, 4 pulsadores (con pull-up interno) reemplazan las flechas del teclado:

```python
from machine import Pin

class ControladorPulsadores:
    def __init__(self):
        self.arriba = Pin(25, Pin.IN, Pin.PULL_UP)
        self.abajo = Pin(26, Pin.IN, Pin.PULL_UP)
        self.izq = Pin(27, Pin.IN, Pin.PULL_UP)
        self.der = Pin(32, Pin.IN, Pin.PULL_UP)
        self.ultima = "STOP"

    def leer_direccion(self):
        if self.arriba.value() == 0:
            self.ultima = "UP"
        elif self.abajo.value() == 0:
            self.ultima = "DOWN"
        elif self.izq.value() == 0:
            self.ultima = "LEFT"
        elif self.der.value() == 0:
            self.ultima = "RIGHT"
        return self.ultima
```

> Guardar la última dirección permite que Pac-Man siga moviéndose cuando se suelta el pulsador.

### Subir los archivos

Se pueden subir con `mpremote` (herramienta oficial) o con Thonny (interfaz gráfica):

```bash
pip install mpremote
mpremote connect /dev/ttyUSB0 cp main.py :
mpremote connect /dev/ttyUSB0 cp dominio.py :
mpremote connect /dev/ttyUSB0 cp infraestructura.py :
mpremote connect /dev/ttyUSB0 reset
```

### Ejecución autónoma

Al resetear o encender la placa:

1. `boot.py` corre la configuración básica.
2. `main.py` compone el juego y llama `ejecutar()`.
3. La partida queda corriendo de forma autónoma, con la OLED como pantalla y los pulsadores como control.

### Depuración

Si algo falla, los errores aparecen por el puerto serie. Un patrón útil es capturar y mostrar el error en la OLED:

```python
import sys

try:
    from main_juego import main
    main()
except Exception as e:
    sys.print_exception(e)      # mostrar en consola serie
```

### Micro-desafío práctico

> Subí tu versión del Pac-Man al ESP32 y probá la ejecución autónoma: desconectá la placa de la PC, alimentala por USB (power bank o adaptador) y verificá que el juego arranque solo.

### Resumen

- `main.py` se ejecuta automáticamente al encender el ESP32.
- La composición (qué adaptadores usar) vive en `main.py`, en la infraestructura.
- Los pulsadores con pull-up interno son el controlador del ESP32.
- `mpremote cp` sube los archivos a la placa.
- La ejecución autónoma funciona sin la PC: el juego arranca solo.
