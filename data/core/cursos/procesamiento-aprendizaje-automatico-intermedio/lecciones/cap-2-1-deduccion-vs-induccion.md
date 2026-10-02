### Razonamiento deductivo del LLM vs. inducción estadística de parámetros

Para dominar el desarrollo asistido por IA, es crucial distinguir entre el razonamiento deductivo/simbólico que exhibe un modelo de lenguaje (como los que potencian a Aider o AGY) y el aprendizaje inductivo tradicional de un clasificador estadístico.

#### Deducción (De la regla al caso particular)
- Parte de premisas, contratos y reglas conocidas para derivar consecuencias lógicas.
- Un LLM analiza el contexto de tu código, comprende las firmas de tipos y deduce la implementación adecuada de una función.
- Si las premisas son verdaderas y el razonamiento es correcto, la conclusión es formalmente válida.

#### Inducción (De los casos particulares a la regla general)
- Parte de un conjunto finito de observaciones empíricas (muestras) para generalizar una función matemática subyacente.
- Los algoritmos de machine learning (Bayes, k-NN, regresión) son inductivos: no comprenden el significado de las variables, sino que optimizan una función de pérdida sobre la distribución observada.
- Siempre existe riesgo de error inductivo ante datos no vistos (generalización defectuosa).
