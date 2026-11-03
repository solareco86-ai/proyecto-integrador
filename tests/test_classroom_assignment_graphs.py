"""Pruebas de grafos y exportación de resultados."""

import csv
from pathlib import Path

from src.adapters.classroom_assignment.graph_exporter import export_compatibility_graphml
from src.application.use_cases.classroom_assignment.validate_input_data import ValidateInputDataUseCase
from src.domain.classroom_assignment.graph import build_compatibility_graph, build_overlap_graph

DATA_DIR = Path(__file__).parents[1] / "data" / "asignacion_aulas"


def _read(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_grafo_bipartito_conecta_comisiones_y_aulas_compatibles() -> None:
    result = ValidateInputDataUseCase().execute(_read("aulas.csv"), _read("comisiones.csv"))

    graph = build_compatibility_graph(result.comisiones, result.aulas)

    assert "S001" in graph.commission_nodes
    assert "A001" in graph.room_nodes
    assert ("S001", "A004") in graph.edges
    assert ("S003", "A003") not in graph.edges


def test_grafo_de_superposicion_crea_aristas_por_horario() -> None:
    result = ValidateInputDataUseCase().execute(_read("aulas.csv"), _read("comisiones.csv"))

    graph = build_overlap_graph(result.comisiones)

    assert ("S001", "S003") in graph.edges
    assert ("S001", "S005") not in graph.edges


def test_exporta_grafo_bipartito_en_graphml(tmp_path: Path) -> None:
    result = ValidateInputDataUseCase().execute(_read("aulas.csv"), _read("comisiones.csv"))
    graph = build_compatibility_graph(result.comisiones, result.aulas)
    destination = tmp_path / "compatibilidad.graphml"

    export_compatibility_graphml(graph, destination)

    content = destination.read_text(encoding="utf-8")
    assert "<graphml" in content
    assert 'id="S001"' in content
    assert 'id="A001"' in content
