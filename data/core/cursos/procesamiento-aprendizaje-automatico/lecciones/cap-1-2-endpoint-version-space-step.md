### Endpoint POST /version-space/step para refinamiento interactivo de hipótesis

Para experimentar con la convergencia de hipótesis de forma interactiva, expondremos un servicio en FastAPI que actualiza las fronteras $S$ y $G$ con cada nueva muestra enviada por el cliente.

#### Implementación del Endpoint en FastAPI
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/version-space", tags=["Espacio de Versiones"])

class InstanciaEntrenamiento(BaseModel):
    caracteristicas: dict[str, str]
    etiqueta_positiva: bool

class EstadoEspacioVersiones(BaseModel):
    frontera_especifica: list[dict[str, str]]
    frontera_general: list[dict[str, str]]
    convergio: bool

@router.post("/step", response_model=EstadoEspacioVersiones)
def refinar_hipotesis(muestra: InstanciaEntrenamiento) -> EstadoEspacioVersiones:
    # Lógica de actualización de límites S y G
    # Retorna las hipótesis vigentes tras procesar la muestra
    return EstadoEspacioVersiones(
        frontera_especifica=[{"clima": "soleado", "humedad": "?"}],
        frontera_general=[{"clima": "soleado"}],
        convergio=False
    )
```
