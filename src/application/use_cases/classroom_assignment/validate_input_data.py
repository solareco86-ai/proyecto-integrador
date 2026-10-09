"""Caso de uso para validar los archivos de entrada de aulas y comisiones."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from src.domain.classroom_assignment.entities import Aula, Comision
from src.domain.classroom_assignment.validation import (
    ValidationIssue,
    validate_aulas,
    validate_comisiones,
)


@dataclass(frozen=True)
class ValidateInputDataResult:
    """Resultado combinado de validar ambos conjuntos de datos."""

    aulas: tuple[Aula, ...]
    comisiones: tuple[Comision, ...]
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        """Indica si no se encontraron problemas de validación."""
        return not self.issues


class ValidateInputDataUseCase:
    """Coordina la validación de aulas y comisiones."""

    def execute(
        self,
        aulas_rows: Iterable[Mapping[str, str | None]],
        comisiones_rows: Iterable[Mapping[str, str | None]],
    ) -> ValidateInputDataResult:
        """Valida filas previamente leídas desde archivos tabulares."""
        aulas_result = validate_aulas(aulas_rows)
        comisiones_result = validate_comisiones(comisiones_rows)
        return ValidateInputDataResult(
            aulas=aulas_result.aulas,
            comisiones=comisiones_result.comisiones,
            issues=aulas_result.issues + comisiones_result.issues,
        )

