### Algoritmo AQ y cobertura secuencial: extracción de reglas interpretables

A diferencia de los modelos de caja negra (redes neuronales profundas), los algoritmos de recubrimiento secuencial como **AQ** inducen conjuntos de reglas lógicas de la forma `SI [condición] ENTONCES [clase]`, garantizando total explicabilidad y auditoría humana.

#### Estrategia de Recubrimiento Secuencial (*Separate and Conquer*)
1. Seleccionar un ejemplo positivo semilla que aún no esté cubierto por ninguna regla.
2. Encontrar una regla general (denominada *estrella* en AQ) que cubra la semilla y la mayor cantidad de positivos posible, sin cubrir ejemplos negativos.
3. Agregar la regla encontrada a la base de conocimiento (`Rule Set`).
4. Remover del dataset todos los ejemplos positivos cubiertos por esta nueva regla.
5. Repetir el proceso hasta que todos los positivos estén cubiertos.

Las reglas resultantes son disyunciones de conjunciones lógicas que pueden traducirse directamente a sentencias de código o políticas operativas de planta.
