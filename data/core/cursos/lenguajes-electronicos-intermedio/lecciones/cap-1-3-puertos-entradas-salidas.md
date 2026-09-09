### Los puertos de E/S

Los microcontroladores cuentan con uno, dos o más puertos (PORTA, PORTB, etc.) de hasta 8 pines. Cada pin puede configurarse como **entrada** o como **salida** por programa.

En los PIC clásicos, la configuración se hacía con los registros **TRISx** (TRISA, TRISB...): un `0` configuraba el pin como salida y un `1` como entrada. En el ESP32 con MicroPython esto se hace con la clase `Pin`:

```python
from machine import Pin

led = Pin(2, Pin.OUT)      # pin 2 como salida
boton = Pin(0, Pin.IN)     # pin 0 como entrada
```

### Entradas digitales

Un pin configurado como entrada digital lee **niveles lógicos**: tensión alta (1) o baja (0).

- **Lógica positiva**: el 1 se obtiene conectando el pin a la alimentación (5 V o 3.3 V) y el 0 a masa.
- **Lógica negativa**: invertida respecto de la anterior.

En el ESP32 se lee con:

```python
valor = boton.value()   # devuelve 0 o 1
```

### Entradas analógicas

Si el microcontrolador tiene **conversor analógico-digital (A/D)**, algunos pines configurados como entradas analógicas pueden leer señales continuas (tensión variable). Ejemplos: un potenciómetro o una LDR (fotorresistencia).

En MicroPython:

```python
from machine import ADC, Pin

adc = ADC(Pin(34))      # pin con capacidad ADC
valor = adc.read()      # valor digital proporcional a la tensión
```

> Este tema se desarrolla a fondo en la lección de ADC de este curso.

### Salidas

Cuando un pin se configura como **salida**, entrega corriente para gobernar un periférico. Dos reglas críticas:

- **Limitar la corriente** (en PICs hasta ~20 mA): siempre usar una resistencia en serie.
- **No sobrecargar el pin** si se gobierna un actuador de potencia (relay, motor, triac): usar etapas de transistor u optoacoplador.

Salidas típicas:

| Salida | Uso |
| :--- | :--- |
| LED con resistencia | Indicación directa. |
| Transistor | Amplificación de corriente. |
| Relay (con diodo y transistor) | Conmutar cargas de 12/24 V. |
| Relay optoacoplado | Aislamiento eléctrico. |
| TRIAC | Controlar cargas de 220 VCA (con precaución). |

En MicroPython, encender y apagar una salida:

```python
led.value(1)     # encender
led.value(0)     # apagar
led.toggle()     # invertir estado
```

### Micro-desafío práctico

> Identificá los pines de tu placa ESP32-WROOM (los números GPIO suelen estar impresos) y proponé a qué pin conectarías un LED y a cuál un pulsador. ¿Qué resistencia usarías en el LED?

### Resumen

- Los puertos agrupan pines configurables como entrada o salida.
- Las entradas digitales leen 0 o 1; las analógicas, valores proporcionales a la tensión.
- Las salidas deben limitar corriente y usar etapas de potencia para cargas grandes.
- En MicroPython: `Pin(2, Pin.OUT)`, `pin.value()`, `pin.toggle()`.
