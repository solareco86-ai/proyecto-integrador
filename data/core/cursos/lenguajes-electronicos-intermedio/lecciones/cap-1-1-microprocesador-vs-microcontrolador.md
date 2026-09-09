### ¿Qué es un microcontrolador?

Un **microcontrolador** es un circuito integrado programable que contiene todos los componentes de un computador. Se emplea para controlar el funcionamiento de una tarea determinada y, debido a su reducido tamaño, suele ir incorporado en el propio dispositivo al que gobierna: por eso se lo llama **controlador incrustado**.

> Un microcontrolador es un computador completo, aunque de limitadas prestaciones, que está contenido en el chip de un circuito integrado y se destina a gobernar una sola tarea.

### Microprocesador vs microcontrolador

La diferencia clave es el nivel de integración:

| | Microprocesador | Microcontrolador |
| :--- | :--- | :--- |
| Sistema | **Abierto** | **Cerrado** |
| Construcción | Se arma acoplándole módulos externos (memoria, periféricos) | Todo está dentro del chip |
| Prestaciones | Altas, configurables | Limitadas y fijas |
| Uso típico | Computadoras de propósito general | Control de una tarea específica |

- Un **microprocesador** es un sistema abierto con el que puede construirse una computadora con las características que se desee, acoplándole los módulos necesarios.
- Un **microcontrolador** es un sistema cerrado que contiene una computadora completa y de prestaciones limitadas que **no se pueden modificar**.

### El caso del ESP32-WROOM

El **ESP32-WROOM** es un módulo basado en el microcontrolador ESP32 de Espressif. Es un microcontrolador moderno con:

- Procesador de doble núcleo.
- Wi-Fi y Bluetooth integrados.
- Memorias FLASH y RAM internas.
- Muchos pines de entrada/salida (GPIO).
- Convertidor analógico-digital (ADC), PWM, I2C, SPI, UART y más.

Es la placa que usaremos durante el curso: un microcontrolador real con el que corremos programas en MicroPython.

### Micro-desafío práctico

> Explicá con tus palabras por qué un lavarropas o una heladera moderna utilizan un microcontrolador y no un microprocesador con PC. ¿Qué significa "sistema cerrado"?

### Resumen

- El microcontrolador integra en un chip computador, memoria y periféricos.
- Es un sistema cerrado, dedicado a una sola tarea.
- El microprocesador es un sistema abierto que se construye con módulos externos.
- El ESP32-WROOM es un microcontrolador con Wi-Fi/BT muy popular en IoT.
