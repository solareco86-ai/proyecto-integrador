### Tipos de planos según su propósito

No hay un único "plano" de un equipo: hay **varios documentos** que responden a preguntas distintas:

| Documento | Pregunta que responde | Nivel de detalle |
| :--- | :--- | :--- |
| Diagrama de bloques | ¿Qué hace el sistema y cómo se conectan sus partes? | Muy general |
| Esquemático (circuito) | ¿Cómo se conectan los componentes entre sí? | Componente a componente |
| Layout de tablero | ¿Dónde se ubica cada componente físicamente? | Distribución espacial |
| Lista de materiales (BOM) | ¿Qué componentes lleva y cuántos? | Inventario |
| Diagrama de cableado | ¿Qué cables van de un punto a otro? | Conexiones físicas |

### Diagrama de bloques

Es el punto de partida. Representa cada función como un **bloque** conectado por flechas que indican flujo de señal o energía.

```
Red CA → [Rectificador] → [Bus CC] → [Inversor] → Motor
                              ↑
                          [Control]
```

No muestra componentes individuales, solo funciones. Es ideal para entender el equipo **antes** de entrar al detalle.

### Esquemático (circuito)

Muestra **cada componente** con su símbolo y cómo se conectan. Es el documento técnico central para diagnóstico y reparación.

- Los componentes se identifican con designación (K1, Q2, F3...).
- Se lee por "carriles" de alimentación: la corriente entra por arriba, sale por abajo.
- Cada conexión entre símbolos representa un conductor real.

### Layout de tablero

Indica la **ubicación física** de componentes dentro del gabinete: rieles DIN, canaletas, borneras, contactores, PLC, fuente.

- Sirve para **montar** y para **ubicar** un componente durante el mantenimiento.
- Suele acompañarse de una vista frontal con referencias (fila/columna).

### Cómo leer un plano en orden

1. Empezá por el **diagrama de bloques** para entender la función.
2. Identificá la **alimentación** en el esquemático.
3. Seguí el **mando** (lógica) antes que la fuerza.
4. Relacioná bobinas y contactos por sus **designaciones y referencias cruzadas**.
5. Recurrí al **layout** solo cuando necesites ubicar físicamente algo.

### Micro-desafío práctico

> Dado un variador de frecuencia, indicá qué documento consultarías para: (a) entender qué hace, (b) reparar una etapa dañada, (c) ubicar el componente en el gabinete, (d) comprar un repuesto.

### Resumen

- Distintos planos responden a distintas preguntas: bloques, esquemático, layout, BOM, cableado.
- El **diagrama de bloques** explica la función; el **esquemático** el detalle de conexión; el **layout** la ubicación física.
- La lectura ordenada: bloques → alimentación → mando → fuerza → layout.
- Las **designaciones y referencias cruzadas** son la brújula dentro del esquemático.
