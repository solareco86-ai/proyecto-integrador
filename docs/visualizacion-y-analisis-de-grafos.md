# Visualización y análisis de grafos de asignación de aulas

El proyecto genera dos grafos para explicar los problemas de asignación sin ocultar las decisiones del algoritmo.

## Generar los archivos

Desde la raíz del repositorio:

```bash
python scripts/generate_classroom_graphs.py
```

Los resultados se guardan en `tmp/grafos-asignacion-aulas/`:

| Archivo | Uso |
|---|---|
| `grafo-superposicion.graphml` | Abrir en Gephi, yEd o Cytoscape. |
| `grafo-comision-aula.graphml` | Analizar compatibilidad entre comisiones y aulas. |
| `grafo-superposicion.svg` | Visualización directa en el navegador. |
| `grafo-comision-aula.svg` | Visualización directa en el navegador. |
| `*.dot` | Fuente editable para Graphviz. |
| `patrones.md` | Informe de indicadores y decisiones del dataset procesado. |
| `asignaciones.csv` | Propuesta de aula para cada comisión asignada. |
| `comisiones-sin-asignar.csv` | Comisiones que no recibieron aula y motivo. |

También se puede elegir otro directorio de salida:

```bash
python scripts/generate_classroom_graphs.py --output-dir /tmp/grafos-aulas
```

## Grafo de superposición

- Cada nodo representa una comisión.
- Cada arista conecta dos comisiones cuyos horarios se superponen.
- Un nodo con muchos vecinos representa una comisión que compite temporalmente con muchas otras.
- Un grupo muy conectado indica una franja horaria con alta demanda de aulas.

Este grafo muestra competencia temporal, pero una arista no significa necesariamente que exista un conflicto bloqueante: puede haber aulas diferentes para las comisiones.

## Grafo bipartito comisión-aula

- Los nodos de comisión representan clases que deben ubicarse.
- Los nodos de aula representan espacios disponibles.
- Una arista conecta una comisión con un aula si la capacidad del aula es suficiente.

Patrones relevantes:

- Comisión sin aristas: no tiene aula compatible por capacidad.
- Aula con grado alto: es un recurso flexible y potencialmente crítico.
- Comisión con una sola arista: tiene pocas alternativas y debe priorizarse.
- Muchas comisiones conectadas con pocas aulas: posible cuello de botella.

## Decisiones tomadas

1. Los horarios son datos de entrada en el MVP; todavía no se generan automáticamente.
2. La capacidad es una restricción obligatoria.
3. La superposición horaria se informa como advertencia hasta comprobar si existe un matching suficiente de aulas.
4. La falta de un aula compatible o de aulas suficientes es un conflicto bloqueante.
5. GraphML se utiliza como formato portable para análisis externo; SVG se utiliza para una visualización rápida.
6. Los resultados generados no se versionan automáticamente porque dependen del dataset procesado y se guardan en `tmp/`.

## Propuesta automática

Dentro de cada franja horaria exacta, el sistema construye un matching bipartito entre comisiones y aulas compatibles. Una comisión se conecta con un aula cuando la capacidad del aula alcanza la cantidad de estudiantes.

El matching intenta asignar la mayor cantidad posible de comisiones sin reutilizar un aula dentro de la misma franja. Las aulas pueden volver a utilizarse en otra franja horaria.

Esta primera versión no resuelve todavía superposiciones parciales como una clase de 18:00 a 20:00 junto con otra de 19:00 a 21:00. Ese caso queda documentado como ampliación del modelo.

## Cómo usar el informe

El archivo `patrones.md` no reemplaza la evaluación del proyecto. Sirve como primera evidencia para documentar:

- Qué comisiones concentran más superposiciones.
- Qué aulas aparecen como recursos críticos.
- Qué comisiones no tienen alternativas.
- Qué decisiones de modelado se tomaron.

Cuando se obtengan datos reales anonimizados, se debe conservar el mismo formato y guardar una copia del informe con la fecha y la versión del dataset utilizado.
