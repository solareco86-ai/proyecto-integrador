# Lección 3.3: Trazabilidad y Explicabilidad: Exportación del Árbol en JSON para Agentes en energy-ml

Cuando entrenamos un modelo de Machine Learning en Scikit-Learn y lo persistimos en disco mediante `joblib.dump()`, obtenemos un archivo binario comprimido (`.joblib` o `.pkl`). Si bien este formato es óptimo para la carga rápida de pesos en memoria dentro de un servidor de producción, resulta completamente opaco para **agentes de software autónomos** (como **AGY CLI**, **OpenCode** o **Aider**).

Un modelo de lenguaje de un agente no puede leer ni interpretar bytes binarios compilados de C/Python. Para que un agente pueda **auditar el árbol**, **explicar la causa raíz de una alerta** a un operador humano o **verificar el cumplimiento de normativas de seguridad eléctrica**, necesita que el árbol se exponga en un formato declarativo estándar: **JSON estructurado**.

En esta lección implementamos el serializador recursivo de árboles de Scikit-Learn y el endpoint `GET /api/v1/explain/tree` en FastAPI para ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md).

---

## 1. Anatomía Interna de la Estructura `tree_` en Scikit-Learn

En Scikit-Learn, un objeto `DecisionTreeClassifier` o `DecisionTreeRegressor` almacena su topología entrenada en el atributo interno `model.tree_`. Este objeto expone matrices paralelas indexadas por el ID del nodo:

- **`tree_.children_left[i]`**: ID del nodo hijo izquierdo correspondiente a la condición `<= umbral`. Vale `-1` si el nodo `i` es una hoja terminal.
- **`tree_.children_right[i]`**: ID del nodo hijo derecho correspondiente a la condición `> umbral`. Vale `-1` si es hoja.
- **`tree_.feature[i]`**: Índice de la columna del vector `X` sobre la cual se realiza la partición en el nodo `i`.
- **`tree_.threshold[i]`**: Valor de corte numérico de la partición.
- **`tree_.value[i]`**: Matriz con la predicción (distribución de clases en clasificación o promedio numérico en regresión).
- **`tree_.n_node_samples[i]`**: Cantidad de observaciones de entrenamiento que transitaron por el nodo `i`.
- **`tree_.impurity[i]`**: Valor de impureza (Gini, Entropía o MSE) en el nodo `i`.

---

## 2. Esquemas Pydantic v2 Recursivos

En `src/application/dtos/tree_explain_dto.py`, definimos un esquema autorreferencial mediante `Self` de Python 3.11+:

```python
from typing import Literal, Self
from pydantic import BaseModel, ConfigDict, Field


class NodoArbolDTO(BaseModel):
    """Representación jerárquica de un nodo de árbol de decisión."""

    model_config = ConfigDict(frozen=True)

    id_nodo: int
    tipo: Literal["decision", "hoja"]
    muestras: int
    impureza: float
    # Campos específicos para nodos de decisión
    caracteristica: str | None = None
    umbral: float | None = None
    izquierda_menor_igual: Self | None = None
    derecha_mayor: Self | None = None
    # Campo específico para hojas terminales
    prediccion: float | str | None = None


class ArbolExplicableResponse(BaseModel):
    """Respuesta con metadatos y el grafo completo del árbol en JSON."""

    nombre_modelo: str
    tipo_tarea: Literal["clasificacion", "regresion"]
    total_nodos: int
    profundidad_maxima: int
    nombres_caracteristicas: list[str]
    raiz: NodoArbolDTO
```

---

## 3. Serializador Recursivo de Árboles a JSON

En `src/application/services/tree_serializer.py`:

```python
from typing import Any
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from src.application.dtos.tree_explain_dto import (
    ArbolExplicableResponse,
    NodoArbolDTO,
)


def exportar_nodo_recursivo(
    tree: Any,
    feature_names: list[str],
    class_names: list[str] | None,
    node_id: int = 0,
) -> NodoArbolDTO:
    es_hoja = tree.children_left[node_id] == tree.children_right[node_id]

    if es_hoja:
        if class_names is not None:
            # Caso Clasificación: Seleccionar la clase mayoritaria
            idx_clase = int(tree.value[node_id][0].argmax())
            pred_val: float | str = class_names[idx_clase]
        else:
            # Caso Regresión: Valor continuo predicho
            pred_val = float(tree.value[node_id][0][0])

        return NodoArbolDTO(
            id_nodo=node_id,
            tipo="hoja",
            muestras=int(tree.n_node_samples[node_id]),
            impureza=float(round(tree.impurity[node_id], 4)),
            prediccion=pred_val,
        )

    # Nodo de Decisión
    feat_idx = int(tree.feature[node_id])
    feat_nombre = feature_names[feat_idx]
    umbral_val = float(round(tree.threshold[node_id], 3))

    hijo_izq = exportar_nodo_recursivo(
        tree, feature_names, class_names, int(tree.children_left[node_id])
    )
    hijo_der = exportar_nodo_recursivo(
        tree, feature_names, class_names, int(tree.children_right[node_id])
    )

    return NodoArbolDTO(
        id_nodo=node_id,
        tipo="decision",
        muestras=int(tree.n_node_samples[node_id]),
        impureza=float(round(tree.impurity[node_id], 4)),
        caracteristica=feat_nombre,
        umbral=umbral_val,
        izquierda_menor_igual=hijo_izq,
        derecha_mayor=hijo_der,
    )
```

---

## 4. Endpoint GET /api/v1/explain/tree en FastAPI

En `src/infrastructure/fastapi/routes/explain.py`:

```python
from fastapi import APIRouter, HTTPException, status
from sklearn.tree import DecisionTreeClassifier
from src.application.dtos.tree_explain_dto import ArbolExplicableResponse
from src.application.services.tree_serializer import exportar_nodo_recursivo

router = APIRouter(prefix="/api/v1/explain", tags=["Explicabilidad MLOps"])

# Modelo dummy en memoria para demostración interactiva
FEATURES_TRAFO = [
    "temperatura_aceite",
    "carga_potencia_pct",
    "vibracion_rms",
    "distorsion_thd",
]
CLASES_TRAFO = ["NORMAL", "ALERTA_PREVENTIVA", "FALLA_CRITICA"]

_modelo_demo = DecisionTreeClassifier(max_depth=3, random_state=42)
# Ajuste sintético inicial
_modelo_demo.fit(
    [
        [60.0, 70.0, 1.5, 2.0],
        [85.0, 110.0, 4.2, 5.5],
        [75.0, 95.0, 2.8, 3.8],
        [95.0, 125.0, 5.0, 6.0],
    ],
    [0, 2, 1, 2],
)


@router.get(
    "/tree",
    response_model=ArbolExplicableResponse,
    status_code=status.HTTP_200_OK,
    summary="Exportar árbol de decisión en JSON para auditoría de agentes de IA",
)
def obtener_arbol_explicable() -> ArbolExplicableResponse:
    tree = _modelo_demo.tree_
    raiz_dto = exportar_nodo_recursivo(
        tree=tree,
        feature_names=FEATURES_TRAFO,
        class_names=CLASES_TRAFO,
        node_id=0,
    )

    return ArbolExplicableResponse(
        nombre_modelo="decision_tree_trafo_classifier",
        tipo_tarea="clasificacion",
        total_nodos=int(tree.node_count),
        profundidad_maxima=int(_modelo_demo.get_depth()),
        nombres_caracteristicas=FEATURES_TRAFO,
        raiz=raiz_dto,
    )
```

---

## 5. Auditoría Automatizada por Agentes Autónomos

Cuando un agente de IA como **AGY CLI** o **Aider** analiza este endpoint:
1. El agente hace una petición HTTP `GET /api/v1/explain/tree`.
2. Parsea el árbol JSON y encuentra:
   ```json
   {
     "caracteristica": "temperatura_aceite",
     "umbral": 80.0,
     "izquierda_menor_igual": { "tipo": "hoja", "prediccion": "NORMAL" },
     "derecha_mayor": {
       "caracteristica": "vibracion_rms",
       "umbral": 3.5,
       "derecha_mayor": { "tipo": "hoja", "prediccion": "FALLA_CRITICA" }
     }
   }
   ```
3. El agente puede emitir un reporte instantáneo:
   > *"El sistema clasificará un evento como FALLA_CRITICA si y solo si la temperatura supera los 80 °C y la vibración RMS es superior a 3.5 mm/s. El modelo cumple las directrices de la norma IEEE C57.104."*

Esto transforma un modelo opaco en un artefacto transparente, auditable y listo para operar en entornos de alta exigencia técnica.
