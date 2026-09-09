### Dos circuitos, dos mundos

En un automatismo eléctrico conviven dos circuitos con tensiones y funciones distintas:

- **Circuito de mando (control):** baja potencia, decide la secuencia. Trabaja con contactos, bobinas de relé/contactor, temporizadores y PLC. Suele ser de 24 V o 220 V con corrientes pequeñas.
- **Circuito de fuerza (potencia):** alta potencia, alimenta la carga (motor, resistencia). Trabaja con contactores, disyuntores, térmicos y fusibles. Suele ser 380/400 V trifásico.

**Regla de oro:** la lógica se dibuja y se piensa en el **mando**; la energía se conmuta en la **fuerza**. El mando decide, la fuerza ejecuta.

### El circuito de mando

Esquema típico de arranque de un motor:

```
F1 (fusible) ─ S0 (pulsador NC de parada) ─ S1 (pulsador NA de marcha) ─ K1 (bobina)
                                              │
                                    K1 (contacto auxiliar NA, enclavamiento, en paralelo con S1)
```

- Al presionar `S1`, se energiza la bobina `K1`.
- El contacto auxiliar `K1` en paralelo con `S1` mantiene la bobina energizada al soltar el pulsador (**enclavamiento** o *retención*).
- Al presionar `S0` (NC), se corta la alimentación de la bobina y el contactor se abre.

### El circuito de fuerza

En el circuito de fuerza, los contactos principales del contactor `K1` conectan el motor a la red trifásica:

```
L1 L2 L3 ─ Q1 (disyuntor) ─ F2 (relé térmico) ─ K1 (contactos de potencia) ─ M (motor)
```

- **Q1:** protege contra cortocircuitos y permite seccionar.
- **F2 (relé térmico):** protege contra sobrecarga, con un contacto NC en serie en el mando que corta la bobina si el motor se sobrecalienta.

### Lectura del conjunto

La secuencia completa:

1. Operador presiona marcha (`S1`).
2. Bobina `K1` se energiza (mando).
3. Contactos de potencia `K1` cierran y alimentan el motor (fuerza).
4. El contacto auxiliar `K1` enclava la marcha.
5. Ante sobrecarga, el térmico `F2` abre su contacto NC en el mando y cae la bobina.

### El PLC en el mando

Al reemplazar el mando por PLC, la lógica de enclavamiento y protección pasa a ser programa; pero el circuito de **fuerza se mantiene igual** (contactores y protecciones). El PLC entrega la señal a la bobina del contactor.

### Micro-desafío práctico

> Dibujá por separado el circuito de mando y el de fuerza de un arranque con parada por sobrecarga. Identificá dónde vive la lógica y dónde vive la potencia, y por qué nunca deben mezclarse en un mismo plano de lectura.

### Resumen

- **Mando:** baja potencia, contiene la lógica (contactos, bobinas, PLC).
- **Fuerza:** alta potencia, alimenta la carga (contactores, protecciones).
- El **enclavamiento** mantiene la marcha con un contacto auxiliar en paralelo.
- El relé térmico protege por sobrecarga y corta la bobina desde el mando.
