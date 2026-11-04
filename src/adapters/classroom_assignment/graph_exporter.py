"""Exportación de grafos a formatos abiertos para visualización."""

from collections.abc import Iterable
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, indent, tostring

from src.domain.classroom_assignment.graph import CompatibilityGraph, OverlapGraph

GRAPHML_NAMESPACE = "http://graphml.graphdrawing.org/xmlns"


def export_overlap_graphml(graph: OverlapGraph, path: Path) -> None:
    """Guarda el grafo de superposición en formato GraphML."""
    nodes = ((node, "commission") for node in graph.nodes)
    _write_graphml(nodes, graph.edges, path, directed=False)


def export_compatibility_graphml(graph: CompatibilityGraph, path: Path) -> None:
    """Guarda el grafo bipartito comisión-aula en formato GraphML."""
    nodes = (
        [(node, "commission") for node in graph.commission_nodes]
        + [(node, "room") for node in graph.room_nodes]
    )
    _write_graphml(nodes, graph.edges, path, directed=False)


def export_overlap_dot(graph: OverlapGraph, path: Path) -> None:
    """Guarda el grafo de superposición en formato DOT."""
    lines = ["graph superposicion {", '  graph [overlap="false", splines=true];']
    lines.extend(f'  "{node}" [shape=circle];' for node in graph.nodes)
    lines.extend(f'  "{first}" -- "{second}";' for first, second in graph.edges)
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_compatibility_dot(graph: CompatibilityGraph, path: Path) -> None:
    """Guarda el grafo bipartito en formato DOT."""
    lines = ["graph compatibilidad {", '  graph [overlap="false", splines=true];']
    lines.extend(f'  "{node}" [shape=circle, color="#2563eb"];' for node in graph.commission_nodes)
    lines.extend(f'  "{node}" [shape=box, color="#16a34a"];' for node in graph.room_nodes)
    lines.extend(f'  "{commission}" -- "{room}";' for commission, room in graph.edges)
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_graphml(
    nodes: Iterable[tuple[str, str]],
    edges: Iterable[tuple[str, str]],
    path: Path,
    directed: bool,
) -> None:
    root = Element("graphml", xmlns=GRAPHML_NAMESPACE)
    key = SubElement(
        root,
        "key",
        attrib={
            "id": "node_type",
            "for": "node",
            "attr.name": "tipo",
            "attr.type": "string",
        },
    )
    del key
    graph = SubElement(root, "graph", id="G", edgedefault="directed" if directed else "undirected")
    for node_id, node_type in nodes:
        node = SubElement(graph, "node", id=node_id)
        data = SubElement(node, "data", key="node_type")
        data.text = node_type
    for index, (source, target) in enumerate(edges):
        SubElement(graph, "edge", id=f"e{index}", source=source, target=target)
    indent(root, space="  ")
    path.write_bytes(tostring(root, encoding="utf-8", xml_declaration=True))
