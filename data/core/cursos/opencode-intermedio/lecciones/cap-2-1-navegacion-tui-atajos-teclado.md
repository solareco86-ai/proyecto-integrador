### La interfaz TUI de OpenCode

OpenCode ofrece una **TUI** (interfaz de usuario de terminal) que organiza la interacción con el agente en una sola pantalla. A diferencia de una interfaz gráfica, la TUI es liviana, funciona en cualquier entorno y permite un uso fluido con el teclado.

### Áreas principales

La interfaz se divide en zonas con responsabilidades claras:

1. **Área de conversación**: muestra el historial de consignas y respuestas del agente.
2. **Línea de entrada**: donde escribís tus consignas al agente.
3. **Panel de contexto/archivos**: los archivos y herramientas que el agente considera relevantes.
4. **Estado**: indica si el agente está trabajando, esperando o finalizó.

### Atajos de teclado esenciales

Dominar los atajos evita alternar constantemente entre el mouse y el teclado:

| Atajo | Acción |
| :--- | :--- |
| `Esc` | Cancelar la operación actual o cerrar paneles |
| `Ctrl+C` | Interrumpir la generación en curso |
| `Tab` | Activar el autocompletado de comandos y sugerencias |
| `↑` / `↓` | Navegar el historial de consignas |
| `Enter` | Enviar la consigna actual |
| `q` | Salir de la TUI (en la mayoría de las vistas) |

> Los atajos exactos pueden variar entre versiones. Consultá la ayuda integrada de tu instalación con `/help` o el equivalente.

### Buenas prácticas de navegación

- **Revisá el contexto antes de escribir**: verificá qué archivos tiene en cuenta el agente para evitar sorpresas.
- **Cancelá en vez de esperar**: si el agente tomó una dirección equivocada, cancelá con `Esc` y reformulá.
- **Trabajá en lotes pequeños**: consignas cortas y verificables son más fáciles de supervisar que una sola instrucción gigante.

### Flujo típico de sesión

```text
1. Abrís la TUI con `opencode`.
2. Explorás el estado del proyecto con una consigna informativa.
3. Enviás una consigna de trabajo concreta.
4. Revisás la respuesta y aceptás o corregís.
5. Verificás con los comandos del proyecto (tests, lint).
```

### Resumen

- La TUI concentra conversación, contexto y estado en una sola pantalla.
- Los atajos de teclado (`Esc`, `Tab`, flechas) aceleran la interacción.
- Revisar el contexto y trabajar en lotes pequeños mejora la supervisión.
- Conocé la ayuda integrada para adaptarte a la versión instalada.
