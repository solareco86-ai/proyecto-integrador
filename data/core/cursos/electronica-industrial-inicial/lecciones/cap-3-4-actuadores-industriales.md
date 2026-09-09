### ¿Qué es un actuador?

El **actuador** es el elemento final de la cadena de control: recibe la orden del controlador y produce una **acción física** sobre el proceso (movimiento, calor, caudal). Es el "músculo" del sistema, mientras el PLC es el "cerebro".

### Motores eléctricos

Convierten energía eléctrica en movimiento rotativo. Según el tipo:

- **Motor de inducción (asincrónico):** el caballo de batalla industrial; robusto, económico, velocidad casi fija según la frecuencia de red.
- **Motor de corriente continua (CC):** control de velocidad sencillo; usado en aplicaciones de precisión.
- **Servomotor:** motor con realimentación de posición (encoder) para control preciso de ángulo y velocidad; base de la robótica.
- **Motor paso a paso:** avanza en pasos discretos; ideal para posicionamiento sin realimentación.

### Válvulas y cilindros

En procesos con fluidos o movimiento lineal:

- **Válvula solenoide:** conmuta el paso de un fluido (aire, agua, aceite) con una bobina eléctrica. ON/OFF.
- **Válvula proporcional:** regula el caudal de forma continua, no solo abierto/cerrado.
- **Cilindro neumático/hidráulico:** produce movimiento lineal a partir de aire o aceite a presión, comandado por electroválvulas.

### Variadores de frecuencia (VFD)

El **variador de frecuencia** es el actuador por excelencia para motores de inducción:

- Convierte la frecuencia de red (50 Hz) en una **frecuencia variable**, variando así la velocidad del motor.
- Permite **arranque suave** (sin picos de corriente) y **ahorro energético**.
- Recibe consigna del PLC (por señales analógicas o comunicación Modbus/Profibus) y devuelve datos de estado (corriente, velocidad, alarmas).

**Relación fundamental:** la velocidad de un motor de inducción es proporcional a la frecuencia de alimentación:

```
velocidad ∝ frecuencia / número de polos
```

### Relés y contactores

- **Relé:** conmuta señales de baja potencia (salidas de PLC → circuitos de mando).
- **Contactor:** conmuta potencia (alimenta motores, resistencias, bancos de capacitores). Se acciona con una bobina de baja tensión.

### La cadena de actuación completa

```
PLC (decisión) → Salida digital/analógica → Relé/contactor/VFD → Motor/válvula/resistencia
```

### Micro-desafío práctico

> Para arrancar y regular la velocidad de una cinta transportadora con un PLC, ¿qué actuadores usarías y cómo los conectarías? Distinguí el elemento de mando (baja potencia) del elemento de fuerza (alta potencia).

### Resumen

- El **actuador** convierte la orden del control en acción física.
- **Motores:** inducción, CC, servomotores y paso a paso.
- **Válvulas:** solenoides (ON/OFF) y proporcionales (continuas).
- El **VFD** varía velocidad y ahorra energía; el **relé** conmuta mando y el **contactor** conmuta potencia.
