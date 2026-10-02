### Entropía, ganancia de información (ID3/C4.5) e impureza de Gini (CART)

Los árboles de decisión particionan recursivamente el espacio de características buscando maximizar la homogeneidad de los subconjuntos resultantes.

#### Entropía de Shannon
Mide el desorden o incertidumbre de una distribución de clases:
$$H(S) = - \sum_{i=1}^{c} p_i \log_2(p_i)$$
- Si todas las muestras pertenecen a la misma clase: $H(S) = 0$ (pureza máxima).
- Si las clases están distribuidas equitativamente: la entropía alcanza su valor máximo.

#### Ganancia de Información (Information Gain)
Es la reducción esperada en entropía al particionar por el atributo $A$:
$$IG(S, A) = H(S) - \sum_{v \in Valores(A)} \frac{|S_v|}{|S|} H(S_v)$$

#### Impureza de Gini (Algoritmo CART)
Mide la probabilidad de que un elemento aleatorio sea clasificado incorrectamente:
$$Gini(S) = 1 - \sum_{i=1}^{c} p_i^2$$
CART utiliza Gini debido a su menor costo computacional (evita el cómputo de logaritmos).
