# Datos de asignación de aulas

Esta carpeta contiene el dataset sintético inicial del Proyecto Integrador. Se utiliza para desarrollar y probar la carga, validación, detección de conflictos y asignación de aulas.

## Archivos

| Archivo | Contenido |
|---|---|
| `aulas.csv` | Aulas disponibles, capacidad, tipo, sede y equipamiento. |
| `comisiones.csv` | Sesiones de comisiones con cantidad de estudiantes, horario y requerimientos. |

## Importante

- Los datos son ficticios.
- No contienen información personal.
- No representan la planificación real del instituto.
- No deben reemplazarse por datos reales sin autorización institucional.

## Reglas del formato

- Codificación: UTF-8.
- Separador: coma (`,`).
- Primera fila: encabezados obligatorios.
- Horarios: formato de 24 horas `HH:MM`.
- Horario institucional de prueba: lunes a viernes, aproximadamente de 18:30 a 21:30/21:40.
- Capacidades y cantidades: números enteros positivos.
- `id_aula` e `id_sesion`: únicos dentro de cada archivo.
- `id_comision`: puede repetirse cuando una materia tiene más de una sesión semanal.
- `requerimientos`: capacidades separadas por comas, por ejemplo `laboratorio_computacion` o `biblioteca`.

## Casos incluidos

El conjunto permite probar:

- Comisiones con cantidad de estudiantes menor que la capacidad de varias aulas.
- Comisiones que requieren aulas grandes.
- Comisiones que requieren laboratorio de computación o biblioteca.
- Una comisión con dos sesiones semanales identificadas por el mismo `id_comision`.
- Competencia por el único laboratorio de computación.
- Horarios superpuestos el mismo día.
- Horarios diferentes que permiten reutilizar un aula.
- Aulas ubicadas en dos sedes ficticias.

## Próxima evolución

Cuando el instituto facilite información, se deberá crear un archivo anonimizado con esta misma estructura o documentar explícitamente las transformaciones necesarias. Los archivos originales no deben subirse al repositorio si contienen datos personales o información institucional sensible.
