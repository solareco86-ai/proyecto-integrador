### Entradas digitales con MicroPython

Un pin configurado como **entrada** lee el nivel lógico presente en él: `1` (alto) o `0` (bajo). La forma típica de generar una entrada es con un **pulsador** que conecta o desconecta el pin.

### Configurar una entrada

```python
from machine import Pin

boton = Pin(0, Pin.IN)
```

### Leer el valor

```python
if boton.value() == 1:
    print("Pulsador presionado")
```

### El problema del estado flotante

Si un pin de entrada queda desconectado (sin tensión definida), su valor es **indeterminado** (flotante): cambia con el ruido. Para fijar el estado en reposo se usan **resistencias pull-up o pull-down**:

- **Pull-up**: resistencia hacia la alimentación → reposo en `1`; el pulsador lleva el pin a masa (`0`) al presionar.
- **Pull-down**: resistencia hacia masa → reposo en `0`; el pulsador lleva el pin a la alimentación (`1`) al presionar.

### Resistencias internas del ESP32

El ESP32 tiene **resistencias pull-up/pull-down internas** configurables por programa, evitando el hardware externo:

```python
from machine import Pin

boton = Pin(0, Pin.IN, Pin.PULL_UP)   # reposo en 1, presionado en 0
```

> Con `PULL_UP`, el valor en reposo es `1` y al presionar baja a `0`. El esquema:

```
3.3V ---[ R interna ]--- GPIO0 ---[ pulsador ]--- GND
```

### El rebote (debounce)

Al presionar un pulsador, el contacto **rebota** unos milisegundos generando lecturas múltiples. Una solución simple es esperar un pequeño tiempo y releer:

```python
from machine import Pin
import time

boton = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    if boton.value() == 0:          # presionado (lógica pull-up)
        time.sleep_ms(20)           # esperar el rebote
        if boton.value() == 0:      # confirmar
            print("Pulsador confirmado")
```

### LED controlado por pulsador

Combinando lo aprendido:

```python
from machine import Pin

boton = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

while True:
    if boton.value() == 0:
        led.value(1)
    else:
        led.value(0)
```

### Micro-desafío práctico

> Conectá un pulsador a un GPIO libre (ej. GPIO4) con pull-up interno y hacé que cada presión **alterne** el estado de un LED (encendido/apagado), con un debounce simple.

### Resumen

- `Pin(n, Pin.IN)` configura una entrada; `value()` la lee.
- Sin resistencia, un pin flota y da lecturas erráticas.
- El ESP32 tiene resistencias internas: `Pin.PULL_UP` y `Pin.PULL_DOWN`.
- Con pull-up, presionar lleva el pin a `0`.
- El debounce evita lecturas múltiples por rebote del contacto.
