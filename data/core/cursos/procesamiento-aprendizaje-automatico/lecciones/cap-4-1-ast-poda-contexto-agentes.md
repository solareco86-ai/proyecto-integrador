### Cómo leen código los agentes: Árboles de Sintaxis Abstracta (AST) y poda de contexto

Los asistentes de desarrollo avanzados como **AGY CLI** no envían archivos enteros de miles de líneas a los modelos de lenguaje; eso saturaría el contexto y dispararía costos. En su lugar, analizan el **Árbol de Sintaxis Abstracta (AST)** localmente en CPU para podar el código de forma determinística ($0 tokens).

#### ¿Qué es un AST?
Es una representación en árbol de la estructura sintáctica del código fuente. Cada nodo del árbol denota un constructo del lenguaje (clases, funciones, asignaciones, decoradores).

#### Poda Determinística de Contexto
- El analizador de AST preserva firmas de funciones, contratos de tipos y docstrings, reemplazando los cuerpos internos con `...`.
- El agente recibe un esqueleto ultrapreciso de <500 tokens que describe fielmente la interfaz del sistema sin sobrecargar la ventana de atención.
- El estudiante experimenta en la terminal ejecutando herramientas de poda sobre su propia base de código de FastAPI.
