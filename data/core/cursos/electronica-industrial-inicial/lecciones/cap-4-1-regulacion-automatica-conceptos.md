### El vocabulario de la regulación automática

La **regulación automática** es la técnica que mantiene una variable de proceso en un valor deseado **sin intervención humana**. Para hablar con precisión, definimos sus términos:

| Término | Símbolo | Definición |
| :--- | :--- | :--- |
| Variable de proceso | **PV** (*Process Variable*) | La magnitud que se controla (temperatura, presión, nivel, velocidad). |
| Consigna / Setpoint | **SP** (*Set Point*) | El valor deseado de la variable. |
| Error / Desviación | **e** | Diferencia entre consigna y medición: `e = SP − PV`. |
| Variable manipulada | **MV** | La salida del controlador que actúa sobre el proceso (ej. apertura de válvula, potencia). |
| Perturbación | — | Influencia externa que desvía la variable de su consigna. |

### El bucle de regulación

Todo sistema de regulación forma un **lazo cerrado**:

```
        SP ──→ (+)── error ──→ [Controlador] ──MV──→ [Actuador] ──→ [Proceso] ──PV──┐
                ↑                                                                    │
                └──────────────────── [Sensor / Medición] ◄───────────────────────────┘
```

1. El **sensor** mide la PV real.
2. Se compara con la **SP** para obtener el **error**.
3. El **controlador** calcula la **MV** según el error y su algoritmo.
4. El **actuador** aplica la MV al **proceso**.
5. El proceso cambia la PV y el ciclo se repite.

### Consigna fija vs variable

- **Regulación de consigna fija:** el SP es constante (ej. mantener un tanque a 60 °C).
- **Regulación de seguimiento:** el SP cambia en el tiempo y el sistema debe seguirlo (ej. un horno con rampa de temperatura).
- **Control en cascada:** la salida de un controlador es la consigna de otro (ej. temperatura → caudal).

### Perturbaciones: el enemigo a vencer

Una perturbación es cualquier cambio externo que tiende a sacar la variable de su consigna: variación de carga, cambios de temperatura ambiente, fluctuaciones de red. El lazo de regulación existe para **rechazar** esas perturbaciones: las detecta vía el error y reacciona.

### Régimen transitorio y permanente

Cuando ocurre una perturbación o un cambio de consigna, la respuesta tiene dos fases:

- **Transitorio:** la variable se mueve hacia el nuevo equilibrio; puede oscilar.
- **Permanente (estacionario):** la variable se estabiliza cerca de la consigna.

La **calidad** de la regulación se juzga por: rapidez de respuesta, sobrepico máximo y error en régimen permanente.

### Micro-desafío práctico

> En un sistema de calefacción de un tanque, identificá PV, SP, MV, sensor, actuador y una posible perturbación. Dibujá el bucle con estos elementos.

### Resumen

- **PV:** variable controlada; **SP:** valor deseado; **error** = SP − PV.
- La **MV** es la salida del controlador hacia el actuador.
- La **perturbación** es la influencia externa que desvía la variable.
- La respuesta tiene fase **transitoria** y **permanente**; se evalúa rapidez, sobrepico y error residual.
