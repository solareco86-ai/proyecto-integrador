### Construcción del endpoint POST /classify/bayes con OpenCode

En este laboratorio utilizaremos **OpenCode** para generar el código de un endpoint de inferencia probabilística en FastAPI, exponiendo las probabilidades de pertenencia a cada clase.

#### Definición del Contrato en FastAPI
```python
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/classify", tags=["Clasificación"])

class MuestraSensores(BaseModel):
    temperatura: float = Field(..., description="Temperatura en °C")
    vibracion: float = Field(..., description="Vibración en mm/s")

class RespuestaBayes(BaseModel):
    clase_predicha: str
    probabilidades: dict[str, float]
    confianza: float

@router.post("/bayes", response_model=RespuestaBayes)
def clasificar_bayes(datos: MuestraSensores) -> RespuestaBayes:
    # Obtener modelo desde memoria
    modelo = ml_models["naive_bayes"]
    vector = [[datos.temperatura, datos.vibracion]]
    
    prediccion = modelo.predict(vector)[0]
    probs = modelo.predict_proba(vector)[0]
    
    prob_dict = {
        clase: float(prob)
        for clase, prob in zip(modelo.classes_, probs)
    }
    
    return RespuestaBayes(
        clase_predicha=prediccion,
        probabilidades=prob_dict,
        confianza=float(max(probs))
    )
```

#### Verificación Asistida
Utilizá OpenCode para generar casos de prueba con valores atípicos y verificar el comportamiento del endpoint ante saturación de sensores.
