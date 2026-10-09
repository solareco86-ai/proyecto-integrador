"""Genera archivos descargables para analizar la asignación de aulas.

Uso:
    python scripts/generate_classroom_graphs.py
    python scripts/generate_classroom_graphs.py --output-dir tmp/grafos-aulas
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.adapters.classroom_assignment.csv_reader import read_csv_rows
from src.adapters.classroom_assignment.graph_exporter import (
    export_compatibility_dot,
    export_compatibility_graphml,
    export_overlap_dot,
    export_overlap_graphml,
)
from src.adapters.classroom_assignment.pattern_report import write_pattern_report
from src.application.use_cases.classroom_assignment.detect_conflicts import DetectConflictsUseCase
from src.application.use_cases.classroom_assignment.validate_input_data import ValidateInputDataUseCase
from src.domain.classroom_assignment.graph import build_compatibility_graph


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tmp/grafos-asignacion-aulas"),
        help="Directorio donde se guardarán GraphML, DOT, SVG y el informe Markdown.",
    )
    args = parser.parse_args()

    data_dir = Path("data/asignacion_aulas")
    validation = ValidateInputDataUseCase().execute(
        read_csv_rows(data_dir / "aulas.csv"),
        read_csv_rows(data_dir / "comisiones.csv"),
    )
    if not validation.is_valid:
        for issue in validation.issues:
            print(f"Fila {issue.row_number}, {issue.field}: {issue.message}")
        return 1

    report, overlap_graph = DetectConflictsUseCase().execute(validation.comisiones, validation.aulas)
    compatibility_graph = build_compatibility_graph(validation.comisiones, validation.aulas)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    overlap_graphml = args.output_dir / "grafo-superposicion.graphml"
    compatibility_graphml = args.output_dir / "grafo-comision-aula.graphml"
    overlap_dot = args.output_dir / "grafo-superposicion.dot"
    compatibility_dot = args.output_dir / "grafo-comision-aula.dot"
    export_overlap_graphml(overlap_graph, overlap_graphml)
    export_compatibility_graphml(compatibility_graph, compatibility_graphml)
    export_overlap_dot(overlap_graph, overlap_dot)
    export_compatibility_dot(compatibility_graph, compatibility_dot)
    write_pattern_report(report, overlap_graph, compatibility_graph, args.output_dir / "patrones.md")

    dot = shutil.which("dot")
    if dot:
        for dot_file in (overlap_dot, compatibility_dot):
            subprocess.run(
                [dot, "-Tsvg", str(dot_file), "-o", str(dot_file.with_suffix(".svg"))],
                check=True,
            )
    print(f"Archivos generados en: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
