### El archivo que orienta al agente

Un archivo **AGENTS.md** es un documento de contexto que vive en la raíz del repositorio y le informa al agente de IA cómo trabajar en ese proyecto específico. Funciona como una *memoria de proyecto*: describe la arquitectura, las convenciones y los comandos que el agente debe respetar.

### ¿Por qué es necesario?

Sin contexto, el agente adivina. Con un buen AGENTS.md, el agente sabe:

1. **Qué arquitectura seguir** (por ejemplo, capas, patrones, carpetas).
2. **Qué convenciones respetar** (nombres, estilo, idioma de los comentarios).
3. **Qué comandos validar** (tests, lints, build) antes de dar por terminada una tarea.
4. **Qué reglas están prohibidas** (desplegar sin autorización, hardcodear datos, etc.).

### Estructura recomendada

```markdown
# Instrucciones para Agentes de IA

## Arquitectura
- [descripción de capas o módulos]

## Convenciones
- [estilo, nombres, idioma]

## Validación obligatoria
- Ejecutar <comando de tests> tras cada cambio
- No reducir la cobertura por debajo de X%

## Reglas
- [prohibiciones y restricciones]
```

### El AGENTS.md como contrato de calidad

Un aspecto clave es que AGENTS.md **no es decorativo**: los agentes lo leen antes de actuar. Esto convierte las buenas prácticas del proyecto en un *contrato* que se cumple de forma consistente:

| Sin AGENTS.md | Con AGENTS.md |
| :--- | :--- |
| El agente ignora la arquitectura | Respeta la estructura de capas |
| No ejecuta tests | Valida antes de finalizar |
| Convenciones inconsistentes | Estilo homogéneo en cada cambio |
| Riesgo de pasos prohibidos | Reglas explícitas de bloqueo |

### Preguntas de diseño

Antes de crear un AGENTS.md, respondé:

1. ¿Qué debe saber cualquier agente antes de tocar este repo?
2. ¿Qué errores repetidos quiero prevenir?
3. ¿Qué comandos de validación son obligatorios?

### Resumen

- AGENTS.md aporta contexto de proyecto al agente de IA.
- Describe arquitectura, convenciones, validaciones y reglas.
- Convierte las buenas prácticas en un contrato de calidad consistente.
- Un buen AGENTS.md reduce errores y acelera las tareas asistidas.
