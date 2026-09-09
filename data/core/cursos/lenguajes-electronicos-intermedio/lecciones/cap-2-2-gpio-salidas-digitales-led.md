### GPIO como salidas digitales

Un **GPIO** (General Purpose Input/Output) es un pin de propósito general que el programa puede configurar como entrada o salida. En MicroPython se maneja con la clase `Pin` del módulo `machine`.

### Configurar una salida

```python
from machine import Pin

led = Pin(2, Pin.OUT)     # GPIO2 configurado como salida
```

### Encender, apagar y alternar

```python
led.value(1)              # nivel alto: LED encendido
led.value(0)              # nivel bajo: LED apagado
led.toggle()              # invierte el estado
```

### Proteger el pin: la resistencia

Cada pin de una salida **no debe superar la corriente máxima** (en muchos microcontroladores ~20-40 mA). Para conectar un LED se usa siempre una **resistencia limitadora** en serie:

- Alimentación 3.3 V, LED rojo (~2 V, ~10 mA) → R ≈ (3.3 − 2) / 0.01 ≈ 130 Ω. Un valor estándar de **220 Ω** es una buena elección.

```
ESP32 (GPIO2) ----[ R 220Ω ]----[ LED ]---- GND
```

### Parpadeo con temporización

El módulo `time` permite esperar entre cambios:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```

> El bucle `while True:` crea el **bucle principal infinito** típico de los microcontroladores.

### Buena práctica: constantes para pines

Definir los pines como constantes hace el programa claro y fácil de adaptar:

```python
from machine import Pin
import time

PIN_LED = 2
led = Pin(PIN_LED, Pin.OUT)

for _ in range(10):
    led.toggle()
    time.sleep_ms(200)
```

`time.sleep_ms()` permite esperas en milisegundos, más precisas en electrónica.

### Micro-desafío práctico

> Conectá un LED con su resistencia a otro GPIO libre (por ejemplo GPIO23) y hacé que parpadee con el patrón: 1 segundo encendido, 2 apagados, repitiendo 5 veces, usando `time.sleep_ms`.

### Resumen

- `Pin(n, Pin.OUT)` configura un GPIO como salida.
- `value(1/0)` y `toggle()` controlan el estado.
- Siempre usar una resistencia en serie con el LED.
- `time.sleep()` y `time.sleep_ms()` dan pausas temporales.
- `while True:` es el bucle principal típico de un microcontrolador.
