### El poder de la tecla Tab

La tecla **Tab** es uno de los aceleradores más importantes de OpenCode. Activa el **autocompletado**: a medida que escribís una consigna, el sistema te sugiere comandos, nombres de archivos y opciones, que podés aceptar sin tipearlos completos.

### ¿Qué autocompleta la tecla Tab?

| Categoría | Ejemplo |
| :--- | :--- |
| Comandos de la TUI | `/help`, `/clear`, `/compact` |
| Archivos y rutas del proyecto | `data/`, `src/domain/models.py` |
| Opciones y banderas | `--model`, `--agent` |
| Snippets de consigna frecuentes | plantillas que definiste |

### Cómo usar el autocompletado

El flujo es iterativo:

```text
1. Escribís el inicio de la consigna, por ejemplo "expl".
2. Presionás Tab y se muestra una sugerencia ("explorar el proyecto").
3. Si es correcta, la aceptás; si no, seguís escribiendo o Tab de nuevo.
4. Continuás armando la consigna y la envías con Enter.
```

### Ventajas en la práctica

- **Menos errores de tipeo**: evita escribir comandos largos o rutas anidadas a mano.
- **Mayor velocidad**: las consignas se componen en segundos.
- **Descubrimiento**: Tab revela funcionalidades que quizás no conocías.

### Trucos para aprovecharla

- **Combiná Tab con las flechas**: después de activar el autocompletado, usá `↑`/`↓` para recorrer las alternativas.
- **Creá plantillas**: si repetís consignas (por ejemplo "revisá el estilo del código"), guardalas como snippets para invocarlas con Tab.
- **Usala para navegar**: escribí una parte de una ruta de archivo y dejá que Tab la complete.

### Resumen

- Tab activa el autocompletado de comandos, archivos y opciones.
- Acelera la escritura y reduce errores de tipeo.
- Se combina con las flechas para elegir entre alternativas.
- Las plantillas personalizadas potencian el flujo de trabajo repetitivo.
