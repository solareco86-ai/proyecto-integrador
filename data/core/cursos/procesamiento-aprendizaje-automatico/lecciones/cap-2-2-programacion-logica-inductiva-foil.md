### Programación Lógica Inductiva (FOIL): aprendizaje de relaciones de primer orden

La Programación Lógica Inductiva (ILP) expande el aprendizaje inductivo desde representaciones atributivas planas (tablas) hacia **lógica de predicados de primer orden**. El algoritmo **FOIL** (*First-Order Inductive Learner*) induce reglas relacionales capaces de razonar sobre grafos, estructuras y relaciones entre múltiples entidades.

#### ¿Por qué es fundamental para entender agentes?
Los agentes de software (como AGY u OpenCode) razonan sobre relaciones de primer orden en tu código:
- `importa(ArchivoA, ModuloB)`
- `depende_de(ClaseC, InterfazD)`
- `llama_a(FuncionX, EndpointY)`

FOIL aprende cláusulas de Horn inductivamente utilizando ganancia de información basada en la cantidad de tuplas positivas que satisface el nuevo predicado. Comprender este fundamento permite entender cómo los sistemas simbólicos y neuro-simbólicos extraen patrones estructurales complejos.
