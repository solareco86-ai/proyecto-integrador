### Dos formas de implementar la lógica de control

La lógica de un automatismo (encender un motor si se cierran dos contactos, por ejemplo) puede implementarse de dos maneras radicalmente distintas:

- **Lógica cableada:** la "decisión" está físicamente en el cableado de componentes electromecánicos (relés, contactores, temporizadores).
- **Lógica programada:** la decisión está escrita como un programa que ejecuta un controlador (PLC).

### Lógica cableada

En la lógica cableada, cada función lógica se logra **uniendo contactos con cables**. Un contacto en serie es un AND, dos contactos en paralelo son un OR, un contacto normalmente cerrado es un NOT.

**Ventajas:**
- No requiere programación ni software.
- Respuesta prácticamente instantánea y robusta ante cortes.

**Desventajas:**
- Cualquier cambio de lógica implica **recablear** físicamente el tablero.
- Ocupa mucho espacio y es difícil de diagnosticar.
- Difícil de documentar y de escalar.

### Lógica programada (PLC)

En la lógica programada, los contactos y bobinas se **representan simbólicamente** en un programa (típicamente en **lenguaje escalera** o *ladder*). El PLC ejecuta el programa de forma cíclica y activa sus salidas físicas.

**Ventajas:**
- Cambiar la lógica es **editar un programa**, no recablear.
- Permite temporizadores, contadores y lógica compleja con poco hardware.
- Fácil de documentar, versionar y diagnosticar.

**Desventajas:**
- Requiere un controlador y conocimientos de programación.
- Tiene un pequeño retardo por el **ciclo de scan** (se estudia en la próxima lección).

### Relés, contactores y PLC: ¿quién hace qué?

| Elemento | Función | Naturaleza |
| :--- | :--- | :--- |
| Relé | Conmutar señales de baja potencia | Electromecánico |
| Contactor | Conmutar potencia (motores, resistencias) | Electromecánico |
| PLC | Ejecutar la lógica de decisión | Electrónico programable |

El patrón típico: el **PLC** decide (baja potencia), y un **contactor** ejecuta la conexión del motor (alta potencia). El PLC no maneja directamente la corriente del motor.

### Un mismo automatismo, dos soluciones

*Arranque de un motor con pulsador de marcha y parada:*
- **Cableado:** pulsador de marcha en paralelo con un contacto auxiliar de enclavamiento (realimentación), en serie con el pulsador de parada (NC) y la bobina del contactor.
- **Programado:** en ladder, una bobina `M` se activa con el contacto `Marcha` OR el propio `M` (enclavamiento), todo en serie con el contacto `Parada` (NC).

### Micro-desafío práctico

> Describí las ventajas de migrar un tablero de lógica cableada con 20 relés a un PLC. ¿Qué pasaría si mañana el cliente pide cambiar una secuencia? Compará el esfuerzo en cada caso.

### Resumen

- **Lógica cableada:** la función lógica está en los cables y contactos; robusta pero rígida.
- **Lógica programada:** la función lógica es un programa en un PLC; flexible y escalable.
- El **relé** conmuta señales, el **contactor** conmuta potencia y el **PLC** decide.
- La migración cableado → programado reduce espacio, cableado y tiempo de cambios.
