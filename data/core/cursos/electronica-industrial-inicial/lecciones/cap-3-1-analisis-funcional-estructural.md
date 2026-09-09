### El enfoque funcional-estructural

Analizar un circuito electrónico industrial **no significa** memorizar cada componente uno por uno. El método profesional es el **análisis funcional-estructural**: descomponer el equipo en **bloques funcionales**, entender qué hace cada bloque y cómo se conectan entre sí. Es decir, razonar en términos de **función** (qué hace) y **estructura** (cómo está organizado).

### Por qué descomponer en bloques

Un equipo real puede tener cientos de componentes. Imposible analizarlo pieza a pieza. En cambio, si lo agrupamos en bloques funcionales, el circuito se vuelve legible:

| Bloque funcional | Pregunta que responde |
| :--- | :--- |
| Fuente de alimentación | ¿De dónde sale la energía para el circuito? |
| Entrada / acondicionamiento | ¿Cómo se capta y normaliza la señal del proceso? |
| Procesamiento | ¿Dónde se toma la decisión lógica o el cálculo? |
| Salida / potencia | ¿Cómo se acciona el actuador final? |
| Realimentación | ¿Cómo se mide el resultado para corregir? |

### Un ejemplo: variador de velocidad

Un **variador de frecuencia (VFD)** regula la velocidad de un motor de inducción. Desde el enfoque funcional-estructural:

1. **Rectificador (entrada):** convierte la corriente alterna de red en continua.
2. **Bus de continua:** almacena y filtra la energía (condensadores).
3. **Inversor (salida):** convierte la continua en alterna de frecuencia variable.
4. **Control:** microprocesador que decide frecuencia y tensión según consigna.
5. **Medición:** sensores de corriente y tensión que realimentan al control.

No hace falta entender cada transistor del inversor: basta saber que ese bloque "genera CA de frecuencia variable".

### Los procesos productivos como cadenas de bloques

En una planta, el mismo razonamiento se aplica a procesos completos. Una línea de envasado puede verse como:

```
Sensor de presencia → Controlador → Actuador de dosificado → Realimentación de peso
```

Cada bloque es una "caja" con entradas, salidas y una función. Si la línea falla, el técnico **aisla el bloque** defectuoso midiendo entrada y salida de cada uno, en lugar de revisar todo el circuito.

### Cómo leer un equipo con este método

1. Identificá la **alimentación** (¿qué lo energiza?).
2. Localizá las **entradas** (¿qué variables capta?).
3. Encontrá el **procesamiento** (¿quién decide?).
4. Seguí la **salida** (¿qué acciona?).
5. Buscá la **realimentación** (¿cómo se corrige?).

### Micro-desafío práctico

> Tomá un horno eléctrico con control de temperatura. Descomponelo en bloques funcionales: entrada, procesamiento, salida y realimentación. Indicá qué componente real cumple cada función.

### Resumen

- El **análisis funcional-estructural** descompone el equipo en bloques por función.
- Los bloques típicos: alimentación, entrada, procesamiento, salida y realimentación.
- Permite leer equipos complejos (VFD, PLC) sin memorizar cada componente.
- Ante una falla, se aísla el bloque midiendo entrada y salida de cada uno.
