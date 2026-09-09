### ¿Qué es OpenCode?

OpenCode es una herramienta de línea de comandos que integra un agente de inteligencia artificial directamente en tu flujo de desarrollo. En lugar de alternar entre un editor y un chat externo, el agente opera sobre tu repositorio real: lee archivos, ejecuta comandos, propone cambios y te permite revisarlos antes de aplicarlos.

### El agente como asistente de ingeniería

Un agente de IA no es un simple autocompletado: es un asistente con acceso a herramientas. En un flujo típico, el agente puede:

1. **Explorar** la estructura del proyecto y leer los archivos relevantes.
2. **Ejecutar** comandos (tests, linters, scripts) para verificar hipótesis.
3. **Proponer** cambios de código que podés aceptar o descartar.
4. **Iterar** sobre los errores hasta lograr el resultado esperado.

Esto convierte a la IA en un colaborador que razona sobre *tu* contexto, y no solo sobre texto suelto.

### ¿Por qué es relevante para Ciencia de Datos e IA?

En proyectos de datos, gran parte del tiempo se consume en tareas repetitivas y propensas a error:

| Tarea | Sin agente | Con agente asistido |
| :--- | :--- | :--- |
| Limpiar y preparar datos | Escribir pipelines a mano | Generar pipelines con validación |
| Prototipar modelos | Copiar código de ejemplos | Adaptar el ejemplo al dataset real |
| Documentar | Postergar la documentación | Generar docstrings y READMEs |
| Corregir bugs | Buscar en Stack Overflow | Depurar con ejecución dirigida |

### Cómo funciona a grandes rasgos

El agente recibe una *consigna* (tu prompt), cuenta con el contexto del repositorio y decide qué herramientas invocar para cumplirla. El resultado es una serie de acciones que vos podés supervisar.

### Ideas para la práctica

> Proponé al agente que **explique** el código de un script Python existente antes de pedirle que lo modifique. Entender el contexto mejora enormemente la calidad de las respuestas.

### Resumen

- OpenCode es una CLI con un agente de IA integrado al repositorio.
- El agente explora, ejecuta y propone cambios de forma iterativa.
- En ciencia de datos acelera las tareas repetitivas de preparación, prototipado y documentación.
- La calidad del resultado depende del contexto y de la claridad de la consigna.
