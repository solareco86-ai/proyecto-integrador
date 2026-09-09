### ¿Qué es una señal analógica?

Una señal **analógica** varía de forma continua. Para que un microcontrolador la procese, el **conversor analógico-digital (ADC)** la transforma en un **número digital** proporcional a su tensión.

### El ADC del ESP32

El ESP32 tiene varios canales ADC. En MicroPython:

```python
from machine import ADC, Pin

adc = ADC(Pin(34))      # GPIO34 soporta ADC
valor = adc.read()      # número digital proporcional a la tensión
```

- El valor típico del ADC es de 0 a **4095** (resolución de 12 bits) para tensiones de 0 a 3.3 V.
- La relación: `tension = valor / 4095 * 3.3`.

```python
tension = valor * 3.3 / 4095
print("Tensión:", tension, "V")
```

### Potenciómetro

Un **potenciómetro** es una resistencia variable con tres terminales. Conectado como divisor de tensión, entrega una tensión variable en su pin central que el ADC convierte en un número.

```
3.3V ----[ potenciómetro ]---- GND
                 |
            GPIO34 (ADC)
```

```python
from machine import ADC, Pin
import time

adc = ADC(Pin(34))

while True:
    valor = adc.read()
    print("ADC:", valor)
    time.sleep_ms(200)
```

### LDR (fotorresistencia)

Una **LDR** cambia su resistencia con la luz: menos luz → más resistencia → menor tensión leída. Se arma con una resistencia fija formando un divisor:

```
3.3V ----[ LDR ]----[ R fija ]---- GND
              |          |
              +-- GPIO34(ADC)
```

```python
from machine import ADC, Pin
import time

adc = ADC(Pin(34))

while True:
    luz = adc.read()
    if luz < 1500:
        print("Está oscuro")
    else:
        print("Hay luz")
    time.sleep_ms(300)
```

### Ajustar la atenuación (ESP32)

En algunos ESP32, la lectura máxima depende de la atenuación configurada. Se puede ajustar la escala:

```python
adc.atten(ADC.ATTN_11DB)     # escala hasta ~3.3 V
adc.width(ADC.WIDTH_12BIT)   # resolución de 12 bits
```

### Micro-desafío práctico

> Armá un "detector de oscuridad": un LED debe encenderse cuando la luz ambiente baja (LDR), usando el ADC y una resistencia fija. Mostrá los valores crudos y la tensión calculada en la consola.

### Resumen

- El ADC convierte una tensión analógica en un número digital.
- El ESP32 lee de 0 a 4095 (12 bits) para 0-3.3 V.
- Un potenciómetro entrega una tensión variable; una LDR, una variable con la luz.
- `adc.read()` obtiene el valor; la tensión se calcula con `valor * 3.3 / 4095`.
