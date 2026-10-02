### Trazabilidad y explicabilidad: exportación del árbol en JSON para agentes

Para que herramientas como Aider, OpenCode o AGY puedan analizar y auditar el árbol de decisión de forma programática, exportamos la estructura jerárquica en formato JSON nativo.

#### Generación de Traza Jerárquica
```python
def exportar_nodo(arbol, feature_names, node_id=0) -> dict:
    if arbol.tree_.children_left[node_id] == arbol.tree_.children_right[node_id]:
        # Nodo Hoja
        return {
            "tipo": "hoja",
            "valor_predicho": float(arbol.tree_.value[node_id][0][0]),
            "muestras": int(arbol.tree_.n_node_samples[node_id])
        }
    
    # Nodo de Decisión
    feature_idx = arbol.tree_.feature[node_id]
    umbral = arbol.tree_.threshold[node_id]
    
    return {
        "tipo": "decision",
        "caracteristica": feature_names[feature_idx],
        "umbral": float(umbral),
        "izquierda_menor_igual": exportar_nodo(arbol, feature_names, arbol.tree_.children_left[node_id]),
        "derecha_mayor": exportar_nodo(arbol, feature_names, arbol.tree_.children_right[node_id])
    }
```
