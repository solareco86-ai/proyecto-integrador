### ¿Qué es Jupyter Notebook?

**Jupyter Notebook** es un entorno interactivo que combina código, texto, visualizaciones y resultados en un único documento llamado *notebook*. Es la herramienta estándar para exploración y análisis de datos porque permite iterar de forma visual y documentar el proceso.

### Instalación y arranque

```bash
# Instalar con pip (dentro del entorno virtual)
pip install jupyter

# Iniciar el servidor local
jupyter notebook
```

Esto abre una interfaz en el navegador desde la cual se crean y administran los notebooks.

### Celdas y modos

Un notebook se compone de **celdas** de dos tipos principales:

| Tipo de celda | Contenido | Uso |
| :--- | :--- | :--- |
| Código | Python | Ejecutar lógica y ver resultados |
| Markdown | Texto con formato | Documentar y explicar |

Atajos esenciales:

| Atajo | Acción |
| :--- | :--- |
| `Shift+Enter` | Ejecutar la celda y avanzar |
| `M` | Convertir la celda a Markdown |
| `Y` | Convertir la celda a código |
| `Esc` | Salir del modo edición |

### Flujo de trabajo típico

```text
1. Crear un notebook para el análisis.
2. Documentar con celdas Markdown el objetivo y las hipótesis.
3. Cargar los datos con celdas de código.
4. Explorar, transformar y visualizar de forma iterativa.
5. Exportar el notebook como HTML o PDF para compartir.
```

### Ejemplo de análisis en celdas

**Celda 1 (código):** cargar datos

```python
import pandas as pd

df = pd.read_csv("data/consumo.csv")
df.head()
```

**Celda 2 (markdown):**

```markdown
### Exploración inicial
Las primeras filas muestran las columnas disponibles y sus tipos.
```

**Celda 3 (código):** resumen estadístico

```python
df.describe()
```

### Buenas prácticas en notebooks

1. **Ejecutar en orden**: las celdas dependen unas de otras; ejecutá todo el notebook de arriba hacia abajo.
2. **Documentar**: usá Markdown para explicar decisiones y hallazgos.
3. **Separar carga y análisis**: mantener los datos crudos separados del procesamiento.
4. **Versionar los notebooks**: Git guarda los cambios, aunque los resultados generados pueden ensuciar el historial.

### Micro-desafío práctico

> Creá un notebook que cargue un pequeño dataset en CSV, muestre las primeras 5 filas con `head()` y agregue una celda Markdown que resuma qué columnas contiene.

### Resumen

- Jupyter combina código, texto y resultados en un solo documento.
- Las celdas de código y Markdown estructuran el análisis.
- El flujo típico es: documentar → cargar → explorar → visualizar.
- Documentar y ejecutar en orden son buenas prácticas clave.
