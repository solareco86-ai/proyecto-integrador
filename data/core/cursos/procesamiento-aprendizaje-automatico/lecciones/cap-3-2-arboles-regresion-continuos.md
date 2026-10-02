### Árboles de regresión y poda para prevención de overfitting

Cuando la variable objetivo es continua en lugar de categórica, se emplean **árboles de regresión**. En cada hoja, la predicción es el promedio de los valores de entrenamiento que cayeron en ese nodo, y el criterio de partición minimiza el Error Cuadrático Medio (MSE).

#### El Peligro del Crecimiento Ilimitado
Un árbol sin restricciones crecerá hasta aislar cada muestra individual en una hoja (`overfitting` puro), memorizando el ruido con un error de entrenamiento nulo pero fallando estrepitosamente en producción.

#### Estrategias de Poda (*Pruning*)
- **Pre-poda (Early Stopping):** Limitar la profundidad máxima (`max_depth`), exigir un número mínimo de muestras para particionar (`min_samples_split`) o para formar una hoja (`min_samples_leaf`).
- **Post-poda (Cost-Complexity Pruning):** Permitir que el árbol crezca completamente y luego podar recursivamente las ramas que aporten menor reducción del error ponderado por la complejidad del árbol.
