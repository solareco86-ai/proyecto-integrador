### ¿Qué es un sistema de control?

Un **sistema de control** es un conjunto de elementos que, actuando de forma coordinada, logran que una variable de un proceso se comporte de la manera deseada. Esa variable se llama **variable controlada** (por ejemplo, la temperatura de un horno) y el valor que queremos alcanzar es la **consigna** o *setpoint*.

### Lazo abierto

En un sistema de **lazo abierto**, la salida se calcula a partir de la entrada, pero **no se mide el resultado** para corregir la acción. La decisión se toma "a ciegas".

```
Entrada → [Controlador] → [Actuador] → Proceso → Salida
```

**Ejemplo:** un lavarropas con temporizador fijo. El usuario programa 30 minutos de lavado y la máquina los ejecuta sin medir si la ropa quedó limpia.

**Características del lazo abierto:**
- Simple y económico.
- No corrige perturbaciones (cambios de carga, desgaste, variaciones).
- Requiere un modelo muy preciso del proceso para ser exacto.

### Lazo cerrado

En un sistema de **lazo cerrado** (o con **realimentación**), se mide la salida real del proceso, se la compara con la consigna y se corrige la acción en consecuencia.

```
Consigna → [Comparador] → [Controlador] → [Actuador] → Proceso → Salida
                  ↑                                                  │
                  └────────────────── Sensor (realimentación) ◄──────┘
```

**Ejemplo:** un horno con termostato. El sensor mide la temperatura real; si es menor que la consigna, el controlador enciende la resistencia; si la supera, la apaga.

**Características del lazo cerrado:**
- Corrige perturbaciones automáticamente.
- Es más robusto y preciso.
- Puede volverse inestable si no se diseña bien (oscilaciones).

### El error: la clave de la realimentación

En lazo cerrado, la diferencia entre consigna y valor medido se llama **error**:

```
error = consigna − valor medido
```

El controlador actúa sobre ese error: cuanto mayor es, más intensa es la corrección. Si el error es cero, el sistema está en equilibrio y no hay acción correctiva.

### Perturbaciones

Una **perturbación** es cualquier influencia externa que tiende a desviar la variable del valor deseado: un cambio en la carga de un motor, una ráfaga de frío en un horno, una variación de presión en una tubería. El lazo cerrado existe, precisamente, para combatir las perturbaciones.

### Micro-desafío práctico

> Para cada caso, indicá si es lazo abierto o cerrado: (a) un tostador con perilla de tiempo; (b) un aire acondicionado con sensor de ambiente; (c) un semáforo con tiempos fijos; (d) un crucero (velocidad constante) de un auto. Justificá cada respuesta.

### Resumen

- El sistema de control gobierna una **variable controlada** hacia una **consigna**.
- **Lazo abierto:** no mide el resultado; simple pero sensible a perturbaciones.
- **Lazo cerrado:** realimenta la medición, compara y corrige; robusto y preciso.
- El **error** (consigna − medición) es la señal que guía la corrección.
