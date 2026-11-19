# Proyecto Integrador: asignación de aulas

Documento de alcance y seguimiento del Proyecto Integrador. El MVP ya cuenta con un núcleo ejecutable que procesa datos académicos sintéticos, detecta conflictos y propone asignaciones de aulas. Este documento distingue lo cumplido de las mejoras pendientes.

## Estado actual

- ✅ Se definió un MVP limitado a la asignación de aulas.
- ✅ Los horarios de las comisiones se reciben como datos de entrada.
- ✅ Se implementó el flujo CSV: lectura, validación, conflictos, matching y exportación.
- ✅ Se utilizan datos sintéticos hasta obtener autorización y archivos reales del instituto.
- ⏳ El soporte Excel/XLSX queda para una etapa posterior.
- ✅ El procesamiento de PDF queda fuera del alcance actual.

## Problema

La asignación manual de aulas puede generar superposiciones, aulas con capacidad insuficiente y espacios desaprovechados. El sistema no reemplazará inicialmente toda la planificación académica: primero verificará datos y propondrá un aula válida para cada comisión.

## Objetivo del MVP

Procesar archivos de aulas y comisiones para:

1. Validar la estructura y los valores recibidos.
2. Detectar datos faltantes, duplicados y registros inválidos.
3. Detectar conflictos de capacidad y superposición horaria.
4. Generar una propuesta de asignación respetando las restricciones obligatorias.
5. Exportar resultados e indicadores para su revisión.

## Fuera de alcance

- Generar automáticamente los horarios de cursada.
- Asignar docentes.
- Procesar cualquier formato de PDF.
- Integrarse con el sistema administrativo del instituto.
- Garantizar una solución óptima para todos los casos.

## Contrato de datos inicial

### `aulas.csv`

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `id_aula` | texto | Sí | Identificador único del aula. |
| `nombre` | texto | Sí | Nombre visible del aula. |
| `capacidad` | entero | Sí | Cantidad máxima de estudiantes. |
| `edificio` | texto | Sí | Edificio o sede. |
| `tipo_aula` | texto | Sí | Tipo de espacio: aula común, laboratorio o biblioteca. |
| `equipamiento` | texto | No | Equipamiento separado por comas. |

### `comisiones.csv`

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `id_comision` | texto | Sí | Identificador de la comisión o materia. Puede repetirse. |
| `id_sesion` | texto | Sí | Identificador único de cada encuentro semanal. |
| `materia` | texto | Sí | Nombre de la materia. |
| `carrera` | texto | Sí | Carrera a la que pertenece. |
| `cantidad_estudiantes` | entero | Sí | Cantidad estimada de estudiantes. |
| `dia` | texto | Sí | Día de cursada. |
| `hora_inicio` | `HH:MM` | Sí | Inicio de la clase. |
| `hora_fin` | `HH:MM` | Sí | Fin de la clase. |
| `requerimientos` | texto | No | Tipo o capacidades requeridas, separadas por comas. |

Una materia que cursa dos veces por semana se representa con dos filas distintas y el mismo `id_comision`, pero con distinto `id_sesion` y posiblemente distinto día.

## Restricciones obligatorias

1. Una sesión no puede superar la capacidad del aula.
2. Un aula no puede tener dos comisiones en horarios superpuestos.
3. La hora de inicio debe ser anterior a la hora de fin.
4. `id_aula` e `id_sesion` deben ser únicos.
5. Los registros inválidos deben informarse y no utilizarse silenciosamente.
6. El aula debe satisfacer los requerimientos de la sesión.

## Datos sintéticos

Los archivos ubicados en `data/asignacion_aulas/` son únicamente de prueba. No representan datos reales del instituto y no deben utilizarse para tomar decisiones institucionales.

El conjunto actual representa dos carreras de una sede ficticia, cursadas de lunes a viernes en el turno vespertino. Incluye un único laboratorio de computación, una biblioteca, materias con requerimientos especiales y una comisión con dos sesiones semanales.

## Flujo previsto

```text
CSV → carga → validación → normalización → conflictos → asignación → resultados

> XLSX se incorporará en una etapa posterior mediante el mismo puerto de entrada tabular.
```

La lógica de procesamiento se mantiene separada de los endpoints FastAPI. Si más adelante se incorpora una interfaz web, FastAPI podrá recibir archivos y devolver resultados, pero no contendrá las reglas principales del dominio.

## Criterios de aceptación y estado

- [x] Los dos CSV tienen encabezados documentados.
- [x] Los identificadores `id_aula` e `id_sesion` no se repiten en el dataset y se validan al cargarlo.
- [x] Las capacidades y cantidades de estudiantes son positivas.
- [x] Los horarios respetan el formato `HH:MM` y la hora inicial es anterior a la final.
- [x] Existe al menos un caso con aula suficiente.
- [x] Existe al menos un caso que requiere detectar un conflicto.
- [x] Los archivos se pueden leer con Python mediante el adaptador CSV de la librería estándar.
- [x] Se valida que las sesiones estén dentro del rango institucional `18:30–21:40`.
- [x] Se validan días permitidos y se prueban superposiciones parciales, por ejemplo `18:30–20:00` y `19:00–21:00`.
- [x] Existe una prueba end-to-end que recorre el flujo completo y verifica los artefactos exportados.

> **Decisión sobre Excel:** CSV es el formato oficial del MVP. La lectura de Excel/XLSX se implementará en una etapa posterior mediante un adaptador, sin introducir dependencias de archivos tabulares en el dominio.

## Evidencia disponible

El núcleo actual cuenta con pruebas específicas para:

- Validación de aulas, comisiones, identificadores, capacidades y horarios.
- Conflictos de capacidad, aulas especiales, superposición y laboratorio único.
- Matching, asignaciones y sesiones sin aula.
- Grafos de superposición, compatibilidad y exportaciones.

También se verificó que el módulo respeta las reglas de Clean Architecture, Hexagonal y DDD. La suite específica del módulo queda cubierta por 24 pruebas. La suite general del portal sigue como tarea separada porque el entorno de ejecución se bloquea en `tests/test_additional_routes.py::test_sitemap_rendered`, incluso con `-n 0` y con un timeout de `faulthandler`.

## Cómo agregar la prueba end-to-end

Se recomienda crear `tests/test_classroom_assignment_e2e.py` con este flujo:

1. Leer `data/asignacion_aulas/aulas.csv` y `comisiones.csv` con `read_csv_rows`.
2. Ejecutar `ValidateInputDataUseCase` y verificar que el resultado sea válido.
3. Ejecutar `DetectConflictsUseCase` y comprobar el conflicto del laboratorio único.
4. Ejecutar `AssignRoomsUseCase`.
5. Construir los grafos de superposición y compatibilidad.
6. Exportar los resultados a `tmp_path` y verificar que existan los CSV, GraphML, DOT y Markdown esperados.
7. Comprobar que las asignaciones no reutilicen un aula en la misma franja y que las sesiones sin asignar incluyan un motivo.

La prueba debe usar `tmp_path` para no modificar `tmp/grafos-asignacion-aulas` ni depender de archivos generados previamente.

## Próximos work units

1. ✅ **Validar rango horario y días:** se impone `18:30 <= hora_inicio`, `hora_fin <= 21:40` y se validan lunes a viernes.
2. ✅ **Agregar prueba end-to-end:** se verifica el flujo completo y sus archivos de salida usando `tmp_path`.
3. **Corregir la suite completa:** investigar el bloqueo de `test_sitemap_rendered` sin mezclarlo con la lógica de asignación de aulas.
4. ✅ **Resolver superposiciones parciales:** el matching ya evita reutilizar un aula en intervalos como `18:30–20:00` y `19:00–21:00`.
5. **Etapa posterior:** incorporar lectura XLSX mediante un adaptador y evaluar una interfaz de usuario. La interfaz no es necesaria para la evaluación actual, porque el foco está en el proceso, las decisiones técnicas y la evidencia de pruebas.

Los dos primeros work units son los prioritarios para cerrar el MVP académico.

Commits sugeridos:

```text
feat(aulas): validar rango horario institucional
test(aulas): cubrir flujo end-to-end
```
