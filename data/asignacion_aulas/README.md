# Datos de asignación de aulas

Esta carpeta contiene el dataset sintético inicial del Proyecto Integrador. Se utiliza para desarrollar y probar la carga, validación, detección de conflictos y asignación de aulas.

## Archivos

| Archivo | Contenido |
|---|---|
| `aulas.csv` | Aulas disponibles, capacidad, sede y equipamiento. |
| `comisiones.csv` | Comisiones con cantidad de estudiantes y horario definido. |

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
- Capacidades y cantidades: números enteros positivos.
- Identificadores: únicos dentro de cada archivo.

## Casos incluidos

El conjunto permite probar:

- Comisiones con cantidad de estudiantes menor que la capacidad de varias aulas.
- Comisiones que requieren aulas grandes.
- Horarios superpuestos el mismo día.
- Horarios diferentes que permiten reutilizar un aula.
- Aulas ubicadas en dos sedes ficticias.

## Próxima evolución

Cuando el instituto facilite información, se deberá crear un archivo anonimizado con esta misma estructura o documentar explícitamente las transformaciones necesarias. Los archivos originales no deben subirse al repositorio si contienen datos personales o información institucional sensible.
