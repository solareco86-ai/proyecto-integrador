### ¿Por qué no alcanza con el control P?

El control proporcional deja un **error en régimen permanente (offset)** y puede ser lento. Para eliminarlo y mejorar la respuesta, se suman dos acciones más: la **integral (I)** y la **derivativa (D)**. Juntas forman el control **PID**, el algoritmo de control más usado en la industria.

### Acción integral (I)

La acción integral actúa sobre la **acumulación del error en el tiempo**:

```
MV_I = Ki · ∫ e dt
```

- Si el error persiste en el tiempo, la acción integral **crece** hasta eliminarlo.
- **Efecto principal:** elimina el offset (error en régimen permanente).
- **Riesgo:** puede volver el sistema más lento y propenso a oscilar si es muy agresiva.

**Intuición:** el término I "recuerda" el pasado; si el sistema lleva mucho tiempo por debajo de la consigna, empuja cada vez más.

### Acción derivativa (D)

La acción derivativa actúa sobre la **velocidad de cambio** del error:

```
MV_D = Kd · de/dt
```

- Reacciona a la **tendencia**, anticipando el futuro antes de que el error crezca.
- **Efecto principal:** amortigua oscilaciones y mejora la estabilidad.
- **Riesgo:** amplifica el ruido de medición; por eso a veces se filtra.

**Intuición:** el término D "predice"; si el error crece rápido, frena la corrección antes de pasarse de largo.

### El controlador PID completo

La salida del PID es la suma de las tres acciones:

```
MV = Kp·e  +  Ki·∫ e dt  +  Kd·de/dt
```

| Término | Actúa sobre | Efecto | Problema típico |
| :--- | :--- | :--- | :--- |
| P (proporcional) | Error presente | Respuesta rápida | Deja offset |
| I (integral) | Error acumulado | Elimina offset | Puede oscilar |
| D (derivativa) | Velocidad del error | Amortigua | Amplifica ruido |

### Formas de un PID

- **P:** solo proporcional (procesos simples, con offset tolerable).
- **PI:** elimina offset; el más usado en industria (temperatura, nivel, presión).
- **PID:** añade anticipación para procesos con inercia (posición, velocidad, robótica).

### Sintonía (tuning)

**Sintonizar** es elegir los valores de Kp, Ki y Kd para que el lazo responda rápido, con poco sobrepico y sin oscilar. Métodos clásicos: **Ziegler-Nichols**, prueba y error, o auto-tune del propio equipo. Una sintonía agresiva (ganancias altas) es rápida pero inestable; una conservadora es estable pero lenta.

### Micro-desafío práctico

> Un horno con control P queda 3 °C por debajo de la consigna. ¿Qué acción agregarías para eliminar esa diferencia? ¿Y si además el horno oscila al corregir, qué acción ayudaría a amortiguarlo?

### Resumen

- **P** responde al error presente; rápido pero con offset.
- **I** acumula el error y **elimina el offset**; puede oscilar.
- **D** responde a la tendencia y **amortigua**; amplifica ruido.
- **PID = Kp·e + Ki·∫e dt + Kd·de/dt**; la sintonía equilibra rapidez y estabilidad.
