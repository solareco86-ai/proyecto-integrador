### ¿Qué es MicroPython?

**MicroPython** es una implementación del lenguaje Python optimizada para microcontroladores y sistemas embebidos. Ejecuta un intérprete en el propio chip, lo que permite escribir programas en un lenguaje moderno sin necesidad de compilar.

### El firmware

Para usar MicroPython en el ESP32-WROOM hay que **grabar el firmware** en la memoria FLASH de la placa. Este firmware incluye el intérprete y el módulo `machine`, que da acceso al hardware.

Pasos generales:

1. Descargar el firmware `.bin` de MicroPython para ESP32 desde el sitio oficial.
2. Conectar la placa por USB e identificar el puerto serie (ej. `/dev/ttyUSB0` en Linux).
3. Grabar el firmware con `esptool.py`:

```bash
pip install esptool
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin
```

> En Windows el puerto suele ser `COM3` o similar, y se puede usar la herramienta gráfica **esptool** o **Thonny**, que flashea automáticamente.

### La consola REPL

Tras el flasheo, la placa queda con MicroPython activo. Al conectar por USB e abrir un terminal serie (o Thonny), aparece el **REPL**:

- **R**ead (lee tu sentencia)
- **E**val (la evalúa)
- **P**rint (muestra el resultado)
- **L**oop (vuelve a esperar)

```python
>>> print("Hola desde el ESP32")
Hola desde el ESP32
>>> 2 + 3
5
```

### Probar el hardware al instante

Con el REPL se puede encender el LED azul de la placa (GPIO2) de inmediato:

```python
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.value(1)
```

### Programas y archivos en la placa

MicroPython crea en la placa un pequeño sistema de archivos. En el REPL se gestionan con comandos como:

```python
>>> import os
>>> os.listdir()
```

Los archivos se suben con herramientas como Thonny o `mpremote`. Un programa guardado como `main.py` se ejecuta automáticamente al encender la placa.

### Micro-desafío práctico

> Flasheá tu placa ESP32-WROOM con MicroPython (o prepará Thonny para conectarte), abrí el REPL y mostrá por consola: tu nombre, el resultado de `5 * 7` y el encendido del LED azul.

### Resumen

- MicroPython es Python para microcontroladores, sin compilar.
- Se graba un firmware en la FLASH con esptool.
- El REPL permite ejecutar sentencias en tiempo real.
- El módulo `machine` da acceso al hardware.
- Un archivo `main.py` se ejecuta al encender la placa.
