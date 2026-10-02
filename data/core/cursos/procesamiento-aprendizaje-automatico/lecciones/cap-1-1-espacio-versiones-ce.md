### Generalización y especialización: algoritmo Candidate-Elimination

El aprendizaje de conceptos puede formularse formalmente como una tarea de búsqueda a través de un espacio predefinido de hipótesis potenciales. El algoritmo **Candidate-Elimination** computa la descripción exacta del conjunto de todas las hipótesis consistentes con los datos observados.

#### Estructura del Espacio de Versiones
El espacio de versiones se delimita mediante dos fronteras complementarias:
- **Frontera General ($G$):** El conjunto de las hipótesis más generales que son consistentes con los ejemplos positivos y no cubren ningún ejemplo negativo.
- **Frontera Específica ($S$):** El conjunto de las hipótesis más específicas que cubren todos los ejemplos positivos y ningún ejemplo negativo.

#### Dinámica de Actualización
- Ante un **ejemplo positivo**: La frontera $S$ se generaliza mínimamente para incluir el ejemplo, y se eliminan de $G$ las hipótesis que no lo cubran.
- Ante un **ejemplo negativo**: La frontera $G$ se especializa mínimamente para excluir el ejemplo, y se eliminan de $S$ las hipótesis que lo cubran.

Cuando $S$ y $G$ convergen en una única hipótesis idéntica, el concepto ha sido unívocamente aprendido.
