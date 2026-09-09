### Tres familias de circuitos

Los circuitos electrónicos industriales se clasifican según el **tipo de señal** que procesan y la **potencia** que manejan. Reconocer la familia de un circuito es el primer paso para entenderlo y diagnosticarlo.

### Circuitos analógicos

Trabajan con señales **continuas**, que pueden tomar cualquier valor dentro de un rango.

- **Característica:** la salida varía de forma proporcional y continua con la entrada.
- **Ejemplos:** amplificadores operacionales, filtros, fuentes reguladas, acondicionadores de señal.
- **Uso industrial:** medir temperatura, presión o nivel y escalar la señal (ej. 0-10 V, 4-20 mA).

**Señal analógica típica:**

```
Tensión (V)
10 ┤          ╱╲
 5 ┤        ╱    ╲
 0 ┼──────╱───────╲────► tiempo
```

### Circuitos digitales

Trabajan con señales **discretas**, que solo toman dos niveles (0 y 1, bajo y alto).

- **Característica:** procesan estados lógicos; son inmunes al ruido dentro de márgenes.
- **Ejemplos:** compuertas lógicas, microcontroladores, PLC (en su núcleo), contadores.
- **Uso industrial:** lógica de decisión, comunicaciones, temporizaciones y conteo.

**Señal digital:**

```
Nivel
1 ┤ ┌──┐   ┌──┐
0 ┼─┘  └───┘  └──► tiempo
```

### Circuitos de potencia

Manejan **corrientes y tensiones elevadas** para alimentar cargas (motores, resistencias, iluminación).

- **Característica:** conmutan o regulan potencia; requieren disipación y protecciones.
- **Ejemplos:** rectificadores, inversores (VFD), relés de estado sólido (SSR), contactores, tiristores, IGBT.
- **Uso industrial:** arranque y variación de velocidad de motores, calefacción, control de cargas.

### Comparación

| Familia | Señal | Nivel de potencia | Función típica |
| :--- | :--- | :--- | :--- |
| Analógica | Continua | Baja | Medir y acondicionar |
| Digital | Discreta (0/1) | Baja | Decidir y comunicar |
| Potencia | Conmutada/continua | Alta | Accionar cargas |

### Cómo conviven en un equipo real

Un variador reúne las tres familias: la **electrónica de potencia** (rectificador + inversor) maneja la energía; la **electrónica digital** (microprocesador) decide; y la **electrónica analógica** (sensores de corriente) mide y acondiciona. Por eso, en la práctica, los tres mundos se integran.

### Micro-desafío práctico

> Clasificá estos elementos en analógico, digital o de potencia: un termopar, un contactor, un microcontrolador, un amplificador de señal 4-20 mA, un relé de estado sólido, una compuerta AND.

### Resumen

- **Analógicos:** señales continuas; miden y acondicionan.
- **Digitales:** señales 0/1; deciden, cuentan y comunican.
- **De potencia:** altas corrientes/tensiones; accionan cargas.
- Un equipo industrial integra las tres familias en bloques que cooperan.
