### Implementación del endpoint POST /classify/knn en FastAPI

Implementaremos el endpoint de inferencia de vecinos más cercanos, analizando cómo el hiperparámetro $k$ condiciona la frontera de decisión.

#### Código del Endpoint
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/classify", tags=["k-NN"])

class VectorEntrada(BaseModel):
    caracteristicas: list[float]
    k_vecinos: int = 5

class RespuestaKNN(BaseModel):
    clase_asignada: str
    distancias_vecinos: list[float]

@router.post("/knn", response_model=RespuestaKNN)
def clasificar_knn(entrada: VectorEntrada) -> RespuestaKNN:
    modelo_knn = ml_models["knn"]
    
    # Inferencia basada en instancias
    distancias, indices = modelo_knn.kneighbors(
        [entrada.caracteristicas],
        n_neighbors=entrada.k_vecinos
    )
    clase = modelo_knn.predict([entrada.caracteristicas])[0]
    
    return RespuestaKNN(
        clase_asignada=str(clase),
        distancias_vecinos=[float(d) for d in distancias[0]]
    )
```
