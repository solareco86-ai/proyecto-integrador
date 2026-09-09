### ¿Por qué planificar antes de codificar?

El **Modo Plan** invierte la tendencia natural de escribir código de inmediato. En lugar de eso, el agente primero razona sobre el problema, explora el contexto del repositorio y te presenta una **estrategia de implementación** antes de tocar una sola línea.

### Objetivos del Modo Plan

| Objetivo | Descripción |
| :--- | :--- |
| Comprender | Leer los archivos y entender cómo encaja el cambio propuesto |
| Diseñar | Definir qué se va a modificar, crear o eliminar |
| Anticipar riesgos | Detectar conflictos, dependencias y efectos colaterales |
| Acordar | Confirmar el enfoque con el usuario antes de implementar |

### Cuándo usar el Modo Plan

- Cuando la tarea es **ambigua** o tiene múltiples soluciones posibles.
- Cuando el cambio **afecta a varios módulos** del proyecto.
- Cuando querés **educar** al equipo: el plan se convierte en documentación viva.
- Cuando el costo de equivocarse es **alto** (producción, datos sensibles).

### Ejemplo en un proyecto de datos

Imaginá que querés agregar una función que calcule métricas de consumo energético:

```text
Consigna (Modo Plan):
"Quiero agregar una función que calcule el consumo promedio por
instalación a partir del dataset de telemetría. Analizá el esquema
actual y proponé dónde debería vivir esta función, qué validaciones
necesita y cómo testearla."
```

El agente debería responder con un plan que mencione los archivos involucrados, el diseño de la función y los pasos de verificación, **sin modificar código todavía**.

### Verificación del plan

Un buen plan debe poder responderse afirmativamente:

1. ¿Identifica los archivos y funciones que se verán afectados?
2. ¿Propone un enfoque concreto y justificado?
3. ¿Anticipa riesgos (rendimiento, datos faltantes, compatibilidad)?
4. ¿Define cómo se va a verificar el resultado?

### Resumen

- El Modo Plan separa el diseño de la implementación.
- Es ideal para tareas ambiguas, de alto impacto o multi-módulo.
- Un buen plan nombra archivos, justifica el enfoque y define la verificación.
- Aprobá el plan antes de pasar al Modo Build.
