### Sensor vs transductor

Aunque se usan como sinónimos, conviene distinguir:

- **Transductor:** dispositivo que convierte una forma de energía en otra (ej. mecánica → eléctrica).
- **Sensor:** transductor que convierte una **magnitud física del proceso** en una **señal eléctrica** medible.

Todo sensor es un transductor, pero no todo transductor es un sensor de proceso.

### Magnitudes que se miden en planta

| Magnitud | Sensor típico | Señal de salida habitual |
| :--- | :--- | :--- |
| Temperatura | Termopar, RTD (Pt100), termistor | mV, Ω, 4-20 mA |
| Presión | Transductor piezoeléctrico, strain gauge | 0-10 V, 4-20 mA |
| Nivel | Flotante, capacitivo, ultrasónico | Digital o analógica |
| Caudal | Turbina, electromagnético | Pulsos o 4-20 mA |
| Posición | Encoder, potenciómetro, final de carrera | Digital o analógica |
| Proximidad | Inductivo, capacitivo, fotoeléctrico | Digital (ON/OFF) |

### Señales de salida: 4-20 mA y 0-10 V

En lazo de corriente **4-20 mA** es el estándar industrial por excelencia:

- El **4 mA** representa el valor mínimo (no 0 mA): si la corriente es 0, significa **cable cortado**, lo que permite detectar fallas de lazo.
- Es inmune al ruido eléctrico en distancias largas.
- El **0-10 V** es común para distancias cortas dentro de un tablero.

### Acondicionamiento de señal

La señal cruda de un sensor rara vez sirve directamente. El **acondicionamiento** la normaliza:

1. **Amplificación:** elevar una señal débil (ej. milivoltios de un termopar) a un nivel útil.
2. **Filtrado:** eliminar ruido y frecuencias no deseadas.
3. **Linealización:** corregir la respuesta no lineal del sensor (ej. termopar).
4. **Aislamiento galvánico:** separar eléctricamente el campo del control para seguridad.
5. **Conversión:** adaptar al estándar del controlador (4-20 mA, 0-10 V, o digital).

### La cadena de medición completa

```
Magnitud física → Sensor → Acondicionamiento → Señal normalizada → Entrada del PLC/control
```

Cada eslabón puede introducir error. La calidad de la medición depende del eslabón más débil, no del mejor.

### Micro-desafío práctico

> Un termopar entrega unos pocos milivoltios y su respuesta no es lineal. Describí qué etapas de acondicionamiento necesitarías para llevar esa señal a una entrada analógica de 4-20 mA de un PLC.

### Resumen

- **Transductor** convierte energías; **sensor** convierte una magnitud física en señal eléctrica.
- Señales estándar: **4-20 mA** (robusto, detecta cable cortado) y **0-10 V** (cortas distancias).
- El **acondicionamiento** amplifica, filtra, linealiza, aísla y convierte la señal.
- La cadena completa: magnitud → sensor → acondicionamiento → señal → PLC.
