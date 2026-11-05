"""Validación de datos de entrada para asignación de aulas.

Este módulo no conoce CSV, FastAPI, pandas ni la base de datos. Recibe filas
tabulares ya leídas y devuelve entidades de dominio junto con los problemas
encontrados.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, time

from src.domain.classroom_assignment.entities import Aula, Comision

VALID_DAYS: frozenset[str] = frozenset(("Lunes", "Martes", "Miércoles", "Jueves", "Viernes"))
SCHEDULE_START = time(18, 30)
SCHEDULE_END = time(21, 40)

REQUIRED_AULA_FIELDS: tuple[str, ...] = (
    "id_aula",
    "nombre",
    "capacidad",
    "edificio",
    "tipo_aula",
)
REQUIRED_COMISION_FIELDS: tuple[str, ...] = (
    "id_comision",
    "id_sesion",
    "materia",
    "carrera",
    "cantidad_estudiantes",
    "dia",
    "hora_inicio",
    "hora_fin",
)


@dataclass(frozen=True)
class ValidationIssue:
    """Problema localizado en una fila o en el encabezado."""

    row_number: int
    field: str
    code: str
    message: str


@dataclass(frozen=True)
class AulasValidationResult:
    """Resultado de validar las filas de aulas."""

    aulas: tuple[Aula, ...]
    issues: tuple[ValidationIssue, ...]


@dataclass(frozen=True)
class ComisionesValidationResult:
    """Resultado de validar las filas de comisiones."""

    comisiones: tuple[Comision, ...]
    issues: tuple[ValidationIssue, ...]


def validate_aulas(rows: Iterable[Mapping[str, str | None]]) -> AulasValidationResult:
    """Valida filas de aulas y construye las entidades válidas."""
    rows_list: list[Mapping[str, str | None]] = list(rows)
    issues: list[ValidationIssue] = _validate_headers(rows_list, REQUIRED_AULA_FIELDS)
    if issues:
        return AulasValidationResult(aulas=(), issues=tuple(issues))

    aulas: list[Aula] = []
    seen_ids: set[str] = set()
    for row_number, row in enumerate(rows_list, start=2):
        row_issues: list[ValidationIssue] = []
        aula_id = _value(row, "id_aula")
        nombre = _value(row, "nombre")
        edificio = _value(row, "edificio")
        tipo_aula = _value(row, "tipo_aula")
        equipamiento = _value(row, "equipamiento")
        capacidad = _positive_integer(row, "capacidad", row_number, row_issues)

        _check_required_text(row, "id_aula", row_number, row_issues)
        _check_required_text(row, "nombre", row_number, row_issues)
        _check_required_text(row, "edificio", row_number, row_issues)
        _check_required_text(row, "tipo_aula", row_number, row_issues)
        if aula_id and aula_id in seen_ids:
            row_issues.append(
                ValidationIssue(row_number, "id_aula", "duplicate", "El identificador del aula está repetido.")
            )

        if row_issues:
            issues.extend(row_issues)
            continue

        seen_ids.add(aula_id)
        aulas.append(
            Aula(
                id_aula=aula_id,
                nombre=nombre,
                capacidad=capacidad,
                edificio=edificio,
                tipo_aula=tipo_aula,
                equipamiento=_split_equipment(equipamiento),
            )
        )

    return AulasValidationResult(aulas=tuple(aulas), issues=tuple(issues))


def validate_comisiones(rows: Iterable[Mapping[str, str | None]]) -> ComisionesValidationResult:
    """Valida filas de comisiones y construye las entidades válidas."""
    rows_list: list[Mapping[str, str | None]] = list(rows)
    issues: list[ValidationIssue] = _validate_headers(rows_list, REQUIRED_COMISION_FIELDS)
    if issues:
        return ComisionesValidationResult(comisiones=(), issues=tuple(issues))

    comisiones: list[Comision] = []
    seen_session_ids: set[str] = set()
    for row_number, row in enumerate(rows_list, start=2):
        comision, row_issues = _validate_comision_row(row, row_number, seen_session_ids)
        if comision is None:
            issues.extend(row_issues)
            continue
        seen_session_ids.add(comision.id_sesion)
        comisiones.append(comision)

    return ComisionesValidationResult(comisiones=tuple(comisiones), issues=tuple(issues))


def _validate_comision_row(
    row: Mapping[str, str | None], row_number: int, seen_session_ids: set[str]
) -> tuple[Comision | None, list[ValidationIssue]]:
    row_issues: list[ValidationIssue] = []
    values = {field: _value(row, field) for field in ("id_comision", "id_sesion", "materia", "carrera", "dia")}
    cantidad = _positive_integer(row, "cantidad_estudiantes", row_number, row_issues)
    hora_inicio = _parse_time(row, "hora_inicio", row_number, row_issues)
    hora_fin = _parse_time(row, "hora_fin", row_number, row_issues)

    for field in values:
        _check_required_text(row, field, row_number, row_issues)
    _check_allowed_day(values["dia"], row_number, row_issues)
    if hora_inicio is not None and hora_fin is not None and hora_inicio >= hora_fin:
        row_issues.append(
            ValidationIssue(row_number, "hora_fin", "invalid_interval", "La hora de fin debe ser posterior a la hora de inicio.")
        )
    if hora_inicio is not None and hora_inicio < SCHEDULE_START:
        row_issues.append(
            ValidationIssue(
                row_number,
                "hora_inicio",
                "outside_schedule",
                "La hora de inicio debe ser igual o posterior a las 18:30.",
            )
        )
    if hora_fin is not None and hora_fin > SCHEDULE_END:
        row_issues.append(
            ValidationIssue(
                row_number,
                "hora_fin",
                "outside_schedule",
                "La hora de fin debe ser igual o anterior a las 21:40.",
            )
        )
    if values["id_sesion"] and values["id_sesion"] in seen_session_ids:
        row_issues.append(
            ValidationIssue(row_number, "id_sesion", "duplicate", "El identificador de la sesión está repetido.")
        )
    if row_issues or hora_inicio is None or hora_fin is None:
        return None, row_issues

    return (
        Comision(
            id_comision=values["id_comision"],
            id_sesion=values["id_sesion"],
            materia=values["materia"],
            carrera=values["carrera"],
            cantidad_estudiantes=cantidad,
            dia=values["dia"],
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            requerimientos=_split_equipment(_value(row, "requerimientos")),
        ),
        [],
    )


def _validate_headers(
    rows: list[Mapping[str, str | None]], required_fields: tuple[str, ...]
) -> list[ValidationIssue]:
    if not rows:
        return [ValidationIssue(1, "__header__", "empty_file", "El archivo no contiene filas.")]
    headers = set(rows[0].keys())
    missing = [field for field in required_fields if field not in headers]
    return [
        ValidationIssue(1, "__header__", "missing_column", f"Falta la columna obligatoria '{field}'.")
        for field in missing
    ]


def _value(row: Mapping[str, str | None], field: str) -> str:
    value = row.get(field)
    return value.strip() if value is not None else ""


def _check_required_text(
    row: Mapping[str, str | None], field: str, row_number: int, issues: list[ValidationIssue]
) -> None:
    if not _value(row, field):
        issues.append(ValidationIssue(row_number, field, "required", "El campo es obligatorio."))


def _check_allowed_day(day: str, row_number: int, issues: list[ValidationIssue]) -> None:
    if day and day not in VALID_DAYS:
        issues.append(
            ValidationIssue(
                row_number,
                "dia",
                "invalid_day",
                "El día debe ser de lunes a viernes.",
            )
        )


def _positive_integer(
    row: Mapping[str, str | None], field: str, row_number: int, issues: list[ValidationIssue]
) -> int:
    raw_value = _value(row, field)
    if not raw_value:
        issues.append(ValidationIssue(row_number, field, "required", "El campo es obligatorio."))
        return 0
    try:
        value = int(raw_value)
    except ValueError:
        issues.append(ValidationIssue(row_number, field, "not_integer", "El valor debe ser un número entero."))
        return 0
    if value <= 0:
        issues.append(ValidationIssue(row_number, field, "not_positive", "El valor debe ser mayor que cero."))
    return value


def _parse_time(
    row: Mapping[str, str | None], field: str, row_number: int, issues: list[ValidationIssue]
) -> time | None:
    raw_value = _value(row, field)
    if not raw_value:
        issues.append(ValidationIssue(row_number, field, "required", "El campo es obligatorio."))
        return None
    try:
        return datetime.strptime(raw_value, "%H:%M").time()
    except ValueError:
        issues.append(
            ValidationIssue(row_number, field, "invalid_time", "La hora debe usar el formato HH:MM de 24 horas.")
        )
        return None


def _split_equipment(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())

