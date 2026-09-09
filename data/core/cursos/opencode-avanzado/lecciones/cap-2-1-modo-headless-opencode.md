### ¿Qué es el modo headless?

El **modo headless** permite ejecutar OpenCode **sin la interfaz TUI**, de forma no interactiva, desde la línea de comandos o dentro de scripts. Es la vía para integrar al agente en automatizaciones, hooks y tuberías de CI/CD.

### Invocación no interactiva

En lugar de abrir la interfaz, se pasa la consigna directamente como argumento:

```bash
opencode "Generá una función que valide emails con Pydantic"
```

El proceso ejecuta la consigna, aplica (o reporta) los cambios y termina, devolviendo el control al shell. Esto habilita el encadenamiento con otras herramientas.

### Salida controlada

En contextos automatizados conviene controlar el formato de la salida. Opciones habituales:

| Opción | Uso |
| :--- | :--- |
| Salida JSON | Facilita el procesamiento programático de la respuesta |
| Modo silencioso | Suprime logs innecesarios en ejecuciones masivas |
| Umbral de cambios | Define si el agente aplica cambios o solo los propone |

> Verificá las banderas soportadas por tu versión: el conjunto exacto cambia entre releases.

### Casos de uso típicos

1. **Revisión rápida**: ejecutar una consigna puntual sin abrir la TUI.
2. **Generación de contenido**: crear documentación o scaffolding de forma reproducible.
3. **Integración en scripts**: encadenar el agente con otras herramientas del shell.
4. **CI/CD**: invocar al agente dentro de una tubería de integración continua.

### Ejemplo de uso en script

```bash
#!/bin/bash
# Ejemplo: usar OpenCode headless para documentar un módulo
opencode "Agregá docstrings a src/domain/models.py" --json
```

### Buenas prácticas

- **Consignas deterministas**: describí el resultado esperado con precisión para reducir variabilidad.
- **Entornos limpios**: ejecutá sobre repositorios con estado conocido.
- **Límite de recursos**: definí timeouts y límites para evitar ejecuciones infinitas.
- **Revisión posterior**: incluso automatizado, todo cambio del agente debe ser revisable.

### Resumen

- El modo headless ejecuta OpenCode sin TUI, de forma no interactiva.
- Se invoca pasando la consigna como argumento y controla la salida.
- Habilita la automatización con scripts, hooks y CI/CD.
- Usá consignas precisas y entornos limpios para resultados reproducibles.
