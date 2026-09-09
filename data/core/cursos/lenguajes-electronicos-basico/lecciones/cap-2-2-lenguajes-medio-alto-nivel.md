### Lenguajes de medio nivel

Un lenguaje de **medio nivel** se encuentra entre los de alto y bajo nivel. Suele clasificarse como de alto nivel, pero permite ciertos manejos de bajo nivel.

Es preciso para aplicaciones como los sistemas operativos: permite un manejo abstracto (independiente de la máquina) sin perder el poder y la eficiencia de los de bajo nivel.

Una característica distintiva del lenguaje **C** (considerado de medio nivel) es que permite **manejar las letras como si fueran números**, mientras que los de alto nivel concatenan cadenas con el operador suma. Otra característica peculiar de C es el uso de **apuntadores**, muy útiles en listas ligadas, tablas hash y algoritmos de búsqueda y ordenamiento.

### Lenguajes de alto nivel

Un lenguaje de **alto nivel** expresa el algoritmo de una manera adecuada a la capacidad cognitiva humana, en lugar de la capacidad ejecutora de las máquinas.

- Se refieren a **variables, matrices, objetos, aritmética compleja, expresiones booleanas, subrutinas, funciones, bucles**, etc.
- Enfocan la facilidad de uso por sobre la eficiencia óptima.
- Se crearon para que el usuario común pudiese solucionar problemas de procesamiento de datos de manera más fácil y rápida.

Principales lenguajes de alto nivel: VB.NET, Ada, ALGOL, BASIC, C Sharp, FORTRAN, Java, Lisp, Modula-2, **Pascal**, Perl, PHP, PL/1, PL/SQL, **Python**, Ruby, MATLAB.

### Lenguajes aplicados en electrónica

En electrónica se usaron y se usan distintos lenguajes:

| Lenguaje | Uso típico en electrónica |
| :--- | :--- |
| C / C++ | Microcontroladores, sistemas embebidos, firmware. |
| Pascal / Delphi | Herramientas de simulación y desarrollo de PC. |
| Visual Basic | Interfaces de control y adquisición de datos en PC. |
| Python / MicroPython | Prototipado, IoT, microcontroladores modernos (ESP32, RP2040). |

### Entornos de programación, compiladores e intérpretes

- **Entorno de programación**: conjunto de herramientas para escribir, probar y depurar código (editor, depurador, etc.).
- **Compilador**: traduce el programa completo de un lenguaje a otro (generalmente a lenguaje máquina) en una sola pasada. Si hay errores, no se genera el ejecutable.
- **Intérprete**: ejecuta el programa instrucción por instrucción, sin generar un archivo ejecutable. Python y MicroPython son lenguajes interpretados.
- **Linkeador**: une los distintos módulos compilados y las bibliotecas en un único programa ejecutable.

En este curso trabajaremos con **MicroPython**, un lenguaje interpretado que no necesita compilar ni linkear: escribimos el programa y lo ejecutamos directamente.

```python
# Esto se interpreta y ejecuta al instante
print("Hola desde un lenguaje interpretado")
```

### Micro-desafío práctico

> Explicá con tus palabras la diferencia entre compilar y ejecutar un programa con un intérprete, y mencioná un ejemplo de lenguaje para cada caso.

### Resumen

- Los lenguajes de medio nivel (como C) mezclan abstracción con control de bajo nivel.
- Los de alto nivel priorizan la facilidad de uso y el poder expresivo.
- En electrónica conviven C/C++, Pascal/Delphi, Visual Basic y Python/MicroPython.
- Un compilador traduce todo el programa; un intérprete lo ejecuta paso a paso.
- MicroPython es interpretado: no requiere compilar ni linkear.
