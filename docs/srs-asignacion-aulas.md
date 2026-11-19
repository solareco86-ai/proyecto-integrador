# SRS: Sistema de asignación de aulas

**Versión:** 1.0.0  
**Estado:** especificación del MVP académico  
**Repositorio:** `proyecto-integrador`  
**Fecha:** 2026-11-17

## 1. Propósito y alcance

El sistema recibe archivos tabulares con aulas y sesiones semanales de comisiones. Valida los datos, detecta conflictos y genera una propuesta reproducible de asignación de aulas. La salida debe ser revisada por una persona responsable de la institución.

El MVP utiliza CSV y datos sintéticos. No genera horarios, no asigna docentes, no reemplaza la decisión institucional y no garantiza una solución óptima para todos los escenarios.

## 2. Modelo de prestación e ingreso

La experiencia puede generar un ingreso por dos caminos:

- **Relación laboral:** ocupar un puesto de desarrolladora backend, analista de datos o analista de sistemas académicos en una institución educativa o empresa EdTech.
- **Prestación comercial — camino elegido:** ofrecer implementación y configuración del sistema a institutos, colegios y universidades que necesiten analizar sus espacios educativos.

Se elige inicialmente la prestación comercial de implementación porque cada institución puede tener reglas, horarios, equipamiento y formatos de archivos diferentes. El servicio incluiría adaptación del contrato de datos, configuración, ejecución, informe de conflictos y soporte, sin afirmar todavía que existe un SaaS terminado ni una asignación óptima garantizada.

## 3. Actores

| Actor | Responsabilidad |
|---|---|
| Responsable académico | Provee los archivos, revisa errores y aprueba o corrige la propuesta. |
| Operador del sistema | Ejecuta el flujo y analiza conflictos, asignaciones y reportes. |
| Sistema | Valida, analiza, asigna y exporta resultados sin tomar decisiones fuera de las reglas declaradas. |

## 4. Datos de entrada

### `aulas.csv`

Campos obligatorios: `id_aula`, `nombre`, `capacidad`, `edificio`, `tipo_aula`.  
Campo opcional: `equipamiento`.

### `comisiones.csv`

Campos obligatorios: `id_comision`, `id_sesion`, `materia`, `carrera`, `cantidad_estudiantes`, `dia`, `hora_inicio`, `hora_fin`.  
Campo opcional: `requerimientos`.

Una comisión puede tener varias filas. Cada sesión semanal debe tener un `id_sesion` distinto.

## 5. Requisitos funcionales

| ID | Requisito verificable |
|---|---|
| RF-01 | El sistema debe leer los dos archivos CSV mediante un adaptador de entrada tabular. |
| RF-02 | Debe informar archivo, fila y campo cuando falte una columna, haya un valor nulo o exista un formato inválido. |
| RF-03 | Debe rechazar `id_aula` e `id_sesion` duplicados. Debe permitir repetir `id_comision` cuando las sesiones sean distintas. |
| RF-04 | Debe validar capacidades y cantidades de estudiantes positivas. |
| RF-05 | Debe aceptar únicamente días de lunes a viernes y horarios entre 18:30 y 21:40, con inicio anterior al fin. |
| RF-06 | Debe verificar que el aula tenga capacidad, tipo y equipamiento compatibles con cada sesión. |
| RF-07 | Debe informar falta de aulas compatibles como conflicto bloqueante y las superposiciones resolubles como advertencias. |
| RF-08 | Debe generar un matching por día e intervalo, sin reutilizar un aula durante intervalos superpuestos y permitiendo reutilizarla en horarios diferentes. |
| RF-09 | Debe priorizar sesiones con menos alternativas y producir una salida determinista para los mismos datos. |
| RF-10 | Debe informar cada sesión sin asignar junto con un motivo explicable. |
| RF-11 | Debe generar CSV de asignaciones y de sesiones sin asignar. |
| RF-12 | Debe generar grafos de superposición y compatibilidad en GraphML y DOT, además de un informe Markdown de patrones. |

## 6. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | El dominio debe usar únicamente la biblioteca estándar de Python y mantenerse independiente de frameworks y archivos. |
| RNF-02 | La lógica de negocio debe permanecer separada de adaptadores, exportadores e infraestructura. |
| RNF-03 | Las entradas inválidas deben fallar de forma explicable, sin descartarse silenciosamente. |
| RNF-04 | El resultado debe ser reproducible con el mismo conjunto de entradas y reglas. |
| RNF-05 | El código nuevo debe tener tipado explícito, pasar Ruff y respetar la verificación de arquitectura. |
| RNF-06 | Las pruebas unitarias y funcionales deben cubrir los casos normales, los errores y los conflictos principales; objetivo de cobertura: 85% o superior. |
| RNF-07 | Los datos reales no deben incorporarse sin autorización; el dataset versionado actual es sintético. |

## 7. Casos de uso principales

### CU-01 — Validar entradas

1. El operador entrega `aulas.csv` y `comisiones.csv`.
2. El sistema comprueba encabezados, campos, identificadores, capacidades, días y horarios.
3. Si hay errores, informa fila y campo y no continúa con datos inválidos.
4. Si todo es válido, devuelve las entidades listas para el análisis.

### CU-02 — Detectar conflictos

1. El sistema calcula aulas compatibles.
2. Detecta falta de capacidad, requerimientos no satisfechos y superposiciones.
3. Clasifica los resultados como error bloqueante o advertencia.
4. Incluye sesiones, aulas, día e intervalo involucrados cuando corresponde.

### CU-03 — Proponer asignaciones

1. El sistema agrupa sesiones por día.
2. Busca el matching máximo respetando intervalos y compatibilidad.
3. Genera asignaciones y sesiones sin asignar con sus motivos.
4. Exporta los resultados para revisión humana.

### CU-04 — Analizar patrones

1. El sistema construye los grafos de superposición y compatibilidad.
2. Exporta GraphML y DOT.
3. Genera un informe Markdown con aulas de alta conectividad, sesiones superpuestas y sesiones sin aula.

## 8. Criterios de aceptación y trazabilidad

| Requisito | Evidencia esperada |
|---|---|
| RF-01 a RF-05 | `tests/test_classroom_assignment_validation.py` |
| RF-06 a RF-07 | `tests/test_classroom_assignment_conflicts.py` |
| RF-08 a RF-10 | `tests/test_classroom_assignment_assignment.py` |
| RF-11 a RF-12 | Tests de exportadores y `tests/test_classroom_assignment_e2e.py` |
| RNF-01 y RNF-02 | `scripts/verify_architecture.py` |
| RNF-05 a RNF-06 | Ruff, Pyright y `pytest --cov` |

## 9. Limitaciones y evolución

- El matching maximiza la cantidad de sesiones asignadas, pero no es un optimizador institucional completo.
- No se consideran preferencias docentes, distancias entre edificios ni cambios de aula durante una misma comisión.
- XLSX, PDF, una API y una interfaz web se evaluarán en etapas posteriores.
- La configuración de horarios, días, tipos de aula y requerimientos deberá externalizarse antes de generalizar el sistema a múltiples instituciones.

