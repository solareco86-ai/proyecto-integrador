# Proyecto Integrador: asignación de aulas

Documento inicial para definir el alcance, los datos y el primer entregable del proyecto integrador. El objetivo es construir un prototipo que procese información académica y proponga asignaciones de aulas sin conflictos.

## Resultado de esta etapa

- Se define un MVP limitado a la asignación de aulas.
- Los horarios de las comisiones ya están definidos como datos de entrada.
- Se priorizan archivos CSV y Excel.
- Se utilizan datos sintéticos hasta obtener autorización y archivos reales del instituto.
- El procesamiento de PDF queda fuera de esta primera etapa.

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
| `equipamiento` | texto | No | Equipamiento separado por comas. |

### `comisiones.csv`

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `id_comision` | texto | Sí | Identificador único de la comisión. |
| `materia` | texto | Sí | Nombre de la materia. |
| `carrera` | texto | Sí | Carrera a la que pertenece. |
| `cantidad_estudiantes` | entero | Sí | Cantidad estimada de estudiantes. |
| `dia` | texto | Sí | Día de cursada. |
| `hora_inicio` | `HH:MM` | Sí | Inicio de la clase. |
| `hora_fin` | `HH:MM` | Sí | Fin de la clase. |

## Restricciones obligatorias

1. Una comisión no puede superar la capacidad del aula.
2. Un aula no puede tener dos comisiones en horarios superpuestos.
3. La hora de inicio debe ser anterior a la hora de fin.
4. Los identificadores deben ser únicos.
5. Los registros inválidos deben informarse y no utilizarse silenciosamente.

## Datos sintéticos

Los archivos ubicados en `data/asignacion_aulas/` son únicamente de prueba. No representan datos reales del instituto y no deben utilizarse para tomar decisiones institucionales.

El conjunto actual contiene aulas de una sede ficticia y comisiones con horarios superpuestos para poder probar tanto asignaciones válidas como conflictos de capacidad y disponibilidad.

## Flujo previsto

```text
CSV/XLSX → carga → validación → normalización → conflictos → asignación → resultados
```

La lógica de procesamiento se implementará separada de los endpoints FastAPI. FastAPI podrá encargarse de recibir archivos y devolver resultados, pero no contendrá las reglas principales del dominio.

## Criterios de aceptación de esta etapa

- [ ] Los dos CSV tienen encabezados documentados.
- [ ] Los identificadores no se repiten.
- [ ] Las capacidades y cantidades de estudiantes son positivas.
- [ ] Los horarios respetan el formato `HH:MM`.
- [ ] Existe al menos un caso con aula suficiente.
- [ ] Existe al menos un caso que requiera detectar un conflicto.
- [ ] Los archivos se pueden leer con Python y pandas.

## Próximo work unit

Implementar la carga y validación de estos dos archivos, comenzando por pruebas unitarias con los datos sintéticos.

Commit sugerido:

```text
docs(aulas): definir contrato inicial de datos
```
