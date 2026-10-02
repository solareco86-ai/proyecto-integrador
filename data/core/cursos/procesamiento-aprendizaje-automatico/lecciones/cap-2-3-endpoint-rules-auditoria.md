### Exposición y auditoría del conjunto de reglas en GET /rules

En este laboratorio construiremos un endpoint que permite a ingenieros y agentes autónomos inspeccionar las reglas lógicas activas en el servicio, verificando su cobertura y soporte empírico.

#### Endpoint de Auditoría de Reglas
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Reglas Simbólicas"])

class ReglaLogica(BaseModel):
    id_regla: str
    antecedente: str
    consecuente: str
    soporte_ejemplos: int
    confianza: float

@router.get("/rules", response_model=list[ReglaLogica])
def listar_reglas_aprendidas() -> list[ReglaLogica]:
    return [
        ReglaLogica(
            id_regla="R-01",
            antecedente="temperatura > 85.0 AND vibracion_rms > 4.5",
            consecuente="estado = ALERTA_CRITICA",
            soporte_ejemplos=420,
            confianza=0.985
        ),
        ReglaLogica(
            id_regla="R-02",
            antecedente="presion_bar < 1.2",
            consecuente="estado = FALLA_LUBRICACION",
            soporte_ejemplos=115,
            confianza=0.991
        )
    ]
```
