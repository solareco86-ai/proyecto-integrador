### Modelado de features con Pydantic: validación, rangos y tipado

En una API de Machine Learning en producción, la calidad de la predicción depende estrictamente de la integridad de los datos de entrada (*Garbage In, Garbage Out*). Pydantic nos permite definir contratos de datos tipados y verificados en tiempo de ejecución.

#### Definición de Esquemas con Restricciones
```python
from pydantic import BaseModel, Field

class SensoresEntrada(BaseModel):
    temperatura_rotor: float = Field(
        ...,
        ge=-20.0,
        le=150.0,
        description="Temperatura del rotor en grados Celsius"
    )
    vibracion_rms: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="Valor RMS de vibración en mm/s"
    )
    presion_bar: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Presión de lubricación hidráulica en bar"
    )

class PrediccionFalla(BaseModel):
    falla_inminente: bool
    probabilidad_falla: float = Field(..., ge=0.0, le=1.0)
    clase_predicha: str
```

#### Rechazo Automático de Datos Inválidos
FastAPI utiliza los esquemas de Pydantic para generar documentación OpenAPI y rechazar solicitudes anómalas (por ejemplo, una vibración negativa) respondiendo inmediatamente con código HTTP 422 antes de invocar la lógica matemática del modelo.
