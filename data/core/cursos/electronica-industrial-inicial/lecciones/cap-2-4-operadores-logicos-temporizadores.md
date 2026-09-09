### La lógica de contactos

Toda decisión en un automatismo puede expresarse con tres operaciones lógicas básicas. En el lenguaje **escalera** (*ladder*) del PLC, cada operación se dibuja con contactos:

- **AND (Y):** dos contactos en **serie**. La salida se activa solo si ambos están cerrados.
- **OR (O):** dos contactos en **paralelo**. La salida se activa si al menos uno está cerrado.
- **NOT (NO):** un contacto **normalmente cerrado (NC)**. Se activa cuando la señal física está ausente.

### Tablas de verdad

**AND:**

| A | B | Salida |
| :--- | :--- | :--- |
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**OR:**

| A | B | Salida |
| :--- | :--- | :--- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

### Ejemplo: arranque seguro de un motor

Supongamos que un motor debe arrancar solo si se cumplen **todas** estas condiciones:

- Pulsador de marcha accionado (`Marcha`).
- Puerta de seguridad cerrada (`Puerta`, contacto NC).
- No hay sobrecarga térmica (`Termico`, contacto NC).

En escalera, la bobina `Motor` se alimenta con `Marcha` en serie con `Puerta` (NC) y `Termico` (NC):

```
 Marcha     Puerta(NC)   Termico(NC)        Motor
──┤ ├──────┤/├──────────┤/├───────────( )──
```

La lógica equivalente en expresión booleana:

```
Motor = Marcha AND NOT(Puerta_abierta) AND NOT(Termico_disparado)
```

### Temporizadores

Los temporizadores agregan la dimensión **tiempo** a la lógica. Los dos tipos básicos:

- **TON (temporizador a la conexión / retardo a la conexión):** la salida se activa **después** de un tiempo configurado de mantener la entrada activa.
- **TOF (temporizador a la desconexión / retardo a la desconexión):** la salida se mantiene activa **después** de que la entrada se desactiva, durante un tiempo.

**Uso típico:** en una secuencia de arranque estrella-triángulo de un motor, el temporizador espera unos segundos antes de conmutar de estrella a triángulo.

### Contadores

Los contadores cuentan eventos (flancos de subida de una entrada). Permiten, por ejemplo, detener una línea al completar 100 piezas, o activar una alarma cada N ciclos. Combinados con temporizadores, permiten secuencias completas.

### Micro-desafío práctico

> Escribí en expresión booleana la condición para encender una lámpara `L` que debe activarse cuando se presiona `A` **y** no está bloqueado por `B`, **o** bien cuando se presiona `C` directamente. Luego dibujá el circuito escalera equivalente.

### Resumen

- Las tres operaciones lógicas: **AND** (serie), **OR** (paralelo) y **NOT** (contacto NC).
- Una bobina se activa según la combinación de contactos que la alimentan.
- Los **temporizadores** (TON/TOF) agregan retardo a la conexión o desconexión.
- Los **contadores** cuentan eventos y habilitan secuencias y alarmas.
