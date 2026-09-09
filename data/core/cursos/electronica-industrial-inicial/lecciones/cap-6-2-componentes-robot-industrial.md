### Los tres subsistemas del robot

Todo robot industrial se compone de tres subsistemas que cooperan:

1. **Mecánica:** la estructura (eslabones y articulaciones) que da la movilidad.
2. **Actuadores:** los "músculos" que generan el movimiento en cada eje.
3. **Controlador y sensores:** el "cerebro" que ejecuta el programa y el "sistema nervioso" que mide.

### Actuadores

Convierten la orden del controlador en movimiento:

- **Servomotores eléctricos:** los más usados en robótica. Motor + reductor + encoder de realimentación. Precisos, limpios y fáciles de controlar.
- **Motores paso a paso:** posicionamiento por pasos; usados en robots pequeños y ejes de baja carga.
- **Actuadores neumáticos:** cilindros para movimientos simples de dos posiciones (grippers, topes).
- **Actuadores hidráulicos:** alta fuerza para robots de gran carga (prensas, manipulación pesada).

### Sensores

Dan al robot información del mundo:

| Tipo | Sensor | Función |
| :--- | :--- | :--- |
| Interno (propioceptivo) | Encoder, resolver | Posición y velocidad de cada eje |
| Externo (exteroceptivo) | Cámara, láser, fuerza/par | Percibir el entorno y las piezas |
| Seguridad | Sensor de par, radar, cortinas | Detección de personas (cobots) |
| Efector final | Sensor de agarre, de contacto | Verificar la pieza sujeta |

### El controlador

El **controlador** ejecuta el programa de movimiento:

- Interpreta la **trayectoria** (puntos y velocidades objetivo).
- Resuelve la **cinemática** (de posición de los ejes a posición de la herramienta, y viceversa).
- Cierra **lazos PID** por cada eje para seguir la trayectoria.
- Gestiona **E/S** (entradas/salidas) para coordinar con la célula (abrir pinza, esperar señal).

### El efector final (la herramienta)

El extremo del robot lleva un **efector final** según la tarea: pinza (*gripper*), ventosa, soplete de soldadura, pistola de pintura, herramienta de mecanizado. Es lo que convierte al robot de "brazo" en "máquina útil".

### El ciclo de operación

```
Programa (trayectoria) → Controlador → Servomotores (ejes) → Efector final → Pieza
                              ↑
                        Sensores (realimentación de posición y entorno)
```

### Micro-desafío práctico

> Para un robot que paletiza cajas, identificá: el actuador de cada eje, un sensor interno, un sensor externo, el controlador y el efector final. Explicá qué pasa si falla el encoder de un eje.

### Resumen

- Los tres subsistemas: **mecánica, actuadores y controlador+sensores**.
- **Servomotores** (motor + reductor + encoder) dominan la robótica.
- Los sensores pueden ser **internos** (posición) o **externos** (entorno), además de seguridad.
- El **controlador** resuelve cinemática y cierra lazos PID por eje; el **efector final** ejecuta la tarea.
