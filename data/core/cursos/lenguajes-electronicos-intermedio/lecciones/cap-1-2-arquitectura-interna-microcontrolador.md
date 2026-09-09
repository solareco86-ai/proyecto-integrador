### Arquitectura interna del microcontrolador

Un microcontrolador posee todos los componentes de un computador, con características fijas que no pueden alterarse. Sus partes principales:

1. **Procesador** (CPU).
2. **Memoria no volátil** para contener el programa.
3. **Memoria de lectura y escritura** (RAM) para guardar los datos.
4. **Memoria de datos no volátil**.
5. **Líneas de E/S** para los controladores de periféricos (paralelo, serie, I2C, USB...).
6. **Recursos auxiliares**: circuito de reloj, temporizadores, watchdog, conversores AD y DA, comparadores, protección ante fallos de alimentación y estados de bajo consumo.

### Memoria de programa

El microcontrolador está diseñado para que en su **memoria de programa** se almacenen todas las instrucciones del programa de control. Como el programa a ejecutar siempre es el mismo, debe estar grabado de forma permanente.

Tipos de memoria de programa:

| Tipo | Característica |
| :--- | :--- |
| ROM con máscara | Grabada en fabricación; solo para series muy grandes. |
| EPROM | Borrable con rayos ultravioleta mediante un grabador. |
| OTP | Programable una sola vez; para prototipos y series cortas. |
| EEPROM | Se graba y borra eléctricamente muchas veces. |
| FLASH | No volátil, se escribe y borra en circuito; ~1.000 ciclos. **Es la usada por el ESP32.** |

### Memoria de datos

Los datos que manejan los programas varían continuamente, por lo que se guardan en **RAM estática (SRAM)**, que es volátil: se pierde al cortarse la alimentación. Algunos microcontroladores añaden memoria no volátil (EEPROM) para conservar datos ante cortes de energía.

### El oscilador

El oscilador genera la **señal de reloj** que sincroniza todo el circuito. Los PIC clásicos ofrecían varias configuraciones (LP, XT, HS, RC, interno, externo...). El ESP32, en cambio, trae un oscilador interno de alta precisión integrado, sin necesidad de configurarlo por programa ni agregar cristales externos.

### El ESP32 en detalle

| Recurso | Valor típico |
| :--- | :--- |
| CPU | Doble núcleo Xtensa LX6 |
| FLASH | 4 MB (varía por módulo) |
| SRAM | ~520 KB |
| Reloj | Interno, configurable |
| Periféricos | ADC, DAC, PWM, I2C, SPI, UART, Wi-Fi, Bluetooth |

### Micro-desafío práctico

> Investigá la diferencia entre memoria volátil y no volátil, y explicá por qué el programa debe vivir en FLASH mientras que los datos variables se guardan en SRAM.

### Resumen

- El microcontrolador integra CPU, memorias y periféricos.
- La memoria de programa (FLASH) guarda el código; la de datos (SRAM) los valores que cambian.
- Hay 5 familias de memoria de programa; FLASH es la moderna.
- El oscilador genera la señal de reloj.
- El ESP32 tiene oscilador interno y periféricos ricos integrados.
