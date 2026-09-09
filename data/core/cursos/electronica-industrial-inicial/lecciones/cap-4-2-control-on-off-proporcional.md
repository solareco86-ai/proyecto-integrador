### El controlador más simple: todo-nada (on-off)

El control **on-off** (o todo-nada) solo tiene dos estados de salida: **encendido o apagado**. No hay valores intermedios.

**Funcionamiento:**
- Si la PV está por debajo de la consigna, la salida se **enciende**.
- Si la PV supera la consigna, la salida se **apaga**.

**Ejemplo:** un termostato de hogar. Cuando la temperatura baja de 20 °C, enciende la caldera; cuando sube, la apaga.

**Problema:** si conmutara exactamente en la consigna, el sistema oscilaría a alta frecuencia (encendido/apagado constante). Para evitarlo se introduce una **banda de histéresis**: la salida enciende en un umbral y apaga en otro ligeramente distinto.

```
Salida ON  ──┐        ┌────────┐
             │        │        │
Salida OFF   └────────┘        └────►  PV
              ↑        ↑
            enciende  apaga   (banda de histéresis)
```

**Ventajas:** simple, económico, robusto.
**Desventajas:** produce oscilación permanente alrededor de la consigna; no sirve para procesos que exigen precisión.

### Control proporcional (P)

El control **proporcional** genera una salida **proporcional al error**, no solo dos estados:

```
MV = Kp · e
```

donde `Kp` es la **ganancia proporcional** y `e` el error.

- A mayor error, mayor acción correctora.
- A medida que el error disminuye, la salida se reduce suavemente (ya no es todo o nada).

**Ejemplo:** una válvula que se abre en proporción a cuánto falta para alcanzar la consigna.

**Problema clásico: el error en régimen permanente (offset).** El control P tiende a estabilizarse dejando un pequeño error residual, porque necesita algo de error para mantener una salida distinta de cero.

### Banda proporcional

En vez de ganancia, muchos equipos expresan el control P como **banda proporcional** (BP): el rango de la PV en el que la salida pasa de 0% a 100%.

```
BP = 100 / Kp   (en %)
```

- **Ganancia alta (BP chica):** respuesta fuerte, pero riesgo de oscilación.
- **Ganancia baja (BP grande):** respuesta suave, pero lenta y con mayor offset.

### Comparación on-off vs proporcional

| Aspecto | On-off | Proporcional |
| :--- | :--- | :--- |
| Estados de salida | 2 | Continuos |
| Oscilación | Sí (permanente) | Menor, amortiguada |
| Precisión en régimen | Baja | Media (con offset) |
| Complejidad | Mínima | Baja |

### Micro-desafío práctico

> Explicá por qué un control on-off puro no sirve para mantener la velocidad exacta de un motor, y por qué un control P la mantiene mejor pero con un pequeño error residual. ¿Cómo se llama ese error?

### Resumen

- **On-off:** dos estados; introduce **histéresis** para evitar conmutación constante; oscila.
- **Proporcional (P):** `MV = Kp · e`; acción suave proporcional al error.
- El control P deja un **offset** (error en régimen permanente).
- La **banda proporcional** es el rango de PV para salida de 0% a 100% (BP = 100/Kp).
