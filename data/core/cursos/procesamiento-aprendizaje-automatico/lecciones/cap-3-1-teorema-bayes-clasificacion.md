### Teorema de Bayes: probabilidades a priori, verosimilitud y a posteriori

El Teorema de Bayes es la piedra angular del aprendizaje probabilístico. Permite actualizar la creencia sobre una hipótesis $H$ a la luz de una nueva evidencia observada $E$.

#### Formulación Matemática
$$P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)}$$

- **$P(H)$ (Probabilidad a priori):** La probabilidad basal de la hipótesis antes de conocer los datos.
- **$P(E|H)$ (Verosimilitud / Likelihood):** La probabilidad de observar la evidencia dado que la hipótesis es cierta.
- **$P(E)$ (Evidencia marginal):** La probabilidad total de observar la evidencia bajo cualquier hipótesis.
- **$P(H|E)$ (Probabilidad a posteriori):** La probabilidad refinada de la hipótesis tras observar la evidencia.

#### La Asunción "Naive" (Ingenua)
Asume que todas las características observadas son condicionalmente independientes entre sí dada la clase. Aunque en la práctica las variables suelen tener correlaciones, esta simplificación matemática otorga una velocidad de cálculo excepcional y un rendimiento sorprendentemente competitivo en clasificación de textos y eventos.
