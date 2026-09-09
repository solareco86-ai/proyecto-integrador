### ¿Qué es un algoritmo?

Un **algoritmo** es un conjunto de procedimientos ordenados que permiten resolver un problema. Es la representación de la solución general en lenguaje común, sin depender de ningún lenguaje de programación.

### ¿Qué es el Pseudo Código?

El **Pseudo Código** no es una forma de programación: es una herramienta que los analistas de sistemas utilizan para comunicar a los programadores la estructura del programa que van a realizar. Es una forma de diagramar un algoritmo sin atenerse a la sintaxis de ningún lenguaje en particular.

En vez de escribir el programa directamente en un lenguaje determinado (C, Basic, Python, etc.), se crea un **borrador entendible para todos**, para luego, con la idea clara, pasar a la programación propiamente dicha.

```
Requerimientos  -->  Pseudo Código  -->  Codificación
```

### Pseudo Código vs Diagrama de Flujo

El pseudo código **no debe confundirse** con el diagrama de flujo:

- El **diagrama de flujo** representa el transcurso del programa con símbolos: cuándo se obtienen los datos, cuándo se procesan y cuándo se presentan los resultados.
- El **pseudo código** describe esos mismos pasos con palabras, en lenguaje común.

Son dos herramientas que se utilizan en conjunto, cada una representa una parte distinta del diseño.

### Uso práctico por el analista de sistemas

En el trabajo de un analista, una de las tareas más trabajosas es determinar qué necesitan los usuarios finales del sistema: relevar los datos, los tipos de procesamiento, las salidas, etc.

Imaginemos un sistema para una empresa que usa interfaz gráfica en Visual Basic, aplicaciones específicas en C y páginas PHP para Internet. Crear un diagrama específico para cada lenguaje sería tedioso. Con el pseudo código:

- Se reúne a todos los programadores.
- Se dan las pautas de trabajo.
- Cada programador escribe el código en su lenguaje.

Incluso dos programadores del mismo lenguaje pueden tener metodologías distintas: un problema se puede resolver de muchas maneras, todas válidas. El pseudo código **elimina esas diferencias** y da libertad para que cada uno se ajuste a su metodología.

### Ejemplo de pseudo código

Para el problema "calcular el promedio de tres notas":

```
INICIO
  LEER nota1
  LEER nota2
  LEER nota3
  promedio = (nota1 + nota2 + nota3) / 3
  MOSTRAR promedio
FIN
```

### Micro-desafío práctico

> Escribí el pseudo código para decidir si una persona es mayor de edad (18 años) y mostrar un mensaje según el caso.

### Resumen

- Un algoritmo es un conjunto de pasos para resolver un problema.
- El pseudo código describe el algoritmo en lenguaje común, sin sintaxis de ningún lenguaje.
- No es programación ni diagrama de flujo: es el puente entre los requerimientos y la codificación.
- Facilita el trabajo en equipos donde cada programador usa un lenguaje distinto.
