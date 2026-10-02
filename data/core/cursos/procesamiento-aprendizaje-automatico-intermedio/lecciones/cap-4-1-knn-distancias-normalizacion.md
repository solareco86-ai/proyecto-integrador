### Algoritmo k-NN: métricas de distancia, estandarización y costo de inferencia

El algoritmo $k$-Nearest Neighbors (k-NN) pertenece a la familia del **aprendizaje basado en instancias** (*lazy learning*). No genera una abstracción paramétrica previa durante el entrenamiento, sino que almacena todas las instancias en memoria.

#### Cálculo de Distancias
Para comparar una nueva muestra $x$ con una instancia almacenada $y$:
- **Distancia Euclídea ($L_2$):**
  $$d(x, y) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$
- **Distancia Manhattan ($L_1$):**
  $$d(x, y) = \sum_{i=1}^{n} |x_i - y_i|$$

#### La Importancia Crítica del Escalado
Si una variable mide temperatura (0 a 100) y otra mide corriente (0 a 2000 mA), la corriente dominará completamente el cálculo de distancia. Toda variable en k-NN debe normalizarse (ej. `StandardScaler` o `MinMaxScaler`) antes de calcular distancias.
