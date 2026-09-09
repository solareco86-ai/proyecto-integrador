### Los niveles de lenguaje

Los **lenguajes de programación** son lenguajes creados por el ser humano para comunicarse con las computadoras: un conjunto de símbolos y palabras que permiten darle instrucciones y órdenes para que las ejecute.

Se clasifican en tres niveles:

| Nivel | Cercanía | Recursos | Comprensión |
| :--- | :--- | :--- | :--- |
| Bajo | Cerca de la máquina | Poco uso de memoria | Difícil para el humano |
| Medio | Entre ambos | Equilibrado | Intermedia |
| Alto | Cerca del humano | Mayor uso de memoria | Fácil para el humano |

> Mientras más bajo es el nivel, más cerca del lenguaje de la computadora y más económico en recursos. Mientras más alto, más cercano al lenguaje humano y más fácil de comprender, pero con mayor uso de recursos.

### Lenguajes de bajo nivel

Un lenguaje de **bajo nivel** ejerce control directo sobre el hardware y está condicionado por la estructura física de la computadora. Se usa para tareas críticas: sistemas operativos, aplicaciones en tiempo real o controladores de dispositivos.

La palabra *bajo* no significa que sea menos potente, sino que tiene **menos abstracción** respecto del hardware.

Su estructura se divide en:

1. **Código binario**: el lenguaje básico, admite todo (1) o nada (0). Todo sistema informático está basado en este código, ya que el 1 indica que se permite el paso de la electricidad y el 0 que no. Así se almacenan y ejecutan los programas.
2. **Lenguaje máquina**: utiliza el alfabeto binario (0 y 1, también llamados bits). Con ellos se forman cadenas binarias con las que se escriben las instrucciones que el microprocesador entiende directamente.
3. **Lenguajes ensambladores** (nemotécnicos o nemónicos): no son ejecutables directamente; necesitan un **ensamblador** que los convierta a lenguaje máquina. Sus instrucciones son abreviaciones de las instrucciones máquina y tienen una correspondencia casi directa con ellas.

### Assembler

El **lenguaje ensamblador** (o assembler) es un lenguaje de bajo nivel que consiste en un conjunto de **mnemónicos** que representan instrucciones básicas para computadores, microprocesadores, microcontroladores y otros circuitos integrados programables.

- Implementa una representación simbólica de los códigos de máquina binarios.
- Es la representación más directa del código máquina legible por un programador.
- Cada arquitectura de procesador tiene su propio ensamblador, definido por el fabricante.
- Es específico de una arquitectura, a diferencia de los lenguajes de alto nivel que son portátiles.

Ejemplo conceptual:

```asm
MOV AL, 05   ; copia el valor 5 al registro AL
ADD AL, 03   ; suma 3 al registro AL
```

### Micro-desafío práctico

> Investigá un código binario sencillo (por ejemplo, la representación del número 5 en 8 bits) y explicá por qué el código máquina es específico de cada procesador.

### Resumen

- Hay tres niveles de lenguaje: bajo, medio y alto.
- El bajo nivel controla directamente el hardware y es más económico en recursos.
- El código binario y el lenguaje máquina son los niveles más bajos.
- El ensamblador usa mnemónicos y es específico de cada arquitectura.
- La palabra "bajo" se refiere a la abstracción, no a la potencia.
