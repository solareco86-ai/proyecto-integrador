### ¿Qué es PWM?

**PWM** (Pulse Width Modulation, modulación por ancho de pulso) genera una señal digital que alterna entre nivel alto y bajo a una frecuencia fija, variando el **tiempo en alto** (ciclo de trabajo o *duty cycle*).

- **Duty 0%**: la señal nunca está en alto → salida apagada.
- **Duty 100%**: siempre en alto → salida máxima.
- **Duty 50%**: mitad del tiempo en alto.

El valor promedio de la señal varía con el duty, lo que permite, por ejemplo, **regular el brillo de un LED**.

### PWM en MicroPython

```python
from machine import Pin, PWM

led = PWM(Pin(2), freq=1000)    # frecuencia 1 kHz
led.duty(512)                   # duty ~50% (escala 0-1023)
```

> En muchas versiones de MicroPython la escala de `duty()` va de **0 a 1023** (10 bits). En las versiones más nuevas se usa `duty_u16()` (0-65535) o `duty_ns()`.

### Variación de brillo en un bucle

```python
from machine import Pin, PWM
import time

led = PWM(Pin(2), freq=1000)

while True:
    # Aumentar brillo
    for d in range(0, 1024, 16):
        led.duty(d)
        time.sleep_ms(10)
    # Disminuir brillo
    for d in range(1023, -1, -16):
        led.duty(d)
        time.sleep_ms(10)
```

### PWM y lógica del juego

La técnica PWM sirve también para **salidas analógicas falsas**: atenuar un LED de "vida", hacer un fade al inicio de una partida o generar un efecto de "game over". En el proyecto Pac-Man se puede usar un LED que late.

```python
from machine import Pin, PWM
import time

led = PWM(Pin(2), freq=1000)

for _ in range(3):          # latido: 3 veces
    for d in range(0, 1024, 32):
        led.duty(d)
        time.sleep_ms(5)
    for d in range(1023, -1, -32):
        led.duty(d)
        time.sleep_ms(5)
```

### Detener el PWM

Para liberar el pin como salida digital común:

```python
led.deinit()
```

### Micro-desafío práctico

> Hacé que un LED realice un "fade in" de 2 segundos (de apagado a brillo máximo), una pausa de 1 segundo y un "fade out" de 2 segundos, repitiendo el ciclo 3 veces.

### Resumen

- PWM modula el tiempo en alto (duty cycle) a una frecuencia fija.
- El promedio de la señal regula el brillo de un LED.
- `PWM(Pin(n), freq=...)` crea la señal; `duty()` la ajusta.
- El duty va de 0 a 1023 en muchas versiones.
- `deinit()` apaga el PWM y libera el pin.
