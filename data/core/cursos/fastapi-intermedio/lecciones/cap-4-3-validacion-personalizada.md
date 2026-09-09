### 4.3 Validación de Datos Personalizada con Pydantic (Custom Data Validation)

Aunque Pydantic incluye validaciones nativas de tipos y rangos, las reglas de negocio complejas (como verificar la consistencia entre dos campos o limpiar cadenas) requieren **validadores personalizados**.

En Pydantic V2 utilizamos los decoradores **`@field_validator`** (para campos individuales) y **`@model_validator`** (para validar el modelo completo).

---

### 1. Validadores de Campo con `@field_validator`

El decorador `@field_validator` permite interceptar el valor de un campo específico antes o después de la conversión de tipos nativa.

```python
from pydantic import BaseModel, Field, field_validator

class RegistroEquipo(BaseModel):
    codigo_serial: str
    temperatura_operacion: float

    # 1. Validador para limpiar y formatear el código serial
    @field_validator("codigo_serial", mode="after")
    @classmethod
    def validar_y_limpiar_serial(cls, v: str) -> str:
        v_clean = v.strip().upper()
        if not v_clean.startswith("EQ-"):
            raise ValueError("El código serial debe comenzar obligatoriamente con el prefijo 'EQ-'")
        return v_clean

    # 2. Validador para rango de temperatura de negocio
    @field_validator("temperatura_operacion", mode="after")
    @classmethod
    def verificar_temperatura_razonable(cls, v: float) -> float:
        if v < -273.15:
            raise ValueError("La temperatura no puede ser inferior al cero absoluto (-273.15 °C)")
        return round(v, 2)
```

#### Parámetros de `@field_validator`:
- `mode="after"` (Predeterminado): El validador se ejecuta **después** de que Pydantic convirtió el tipo básico (ej. cadena a float).
- `mode="before"`: El validador se ejecuta **antes** de la conversión de tipos (recibe el valor crudo enviado por el cliente).

---

### 2. Validadores a Nivel de Modelo con `@model_validator`

Cuando la regla de validación depende de la relación entre **múltiples campos simultáneamente** (por ejemplo, verificar que `temperatura_maxima` sea estrictamente mayor que `temperatura_minima`), se utiliza `@model_validator`:

```python
from pydantic import BaseModel, Field, model_validator

class RangoOperacionSensor(BaseModel):
    sensor_id: str
    temp_min: float = Field(..., description="Temperatura mínima de operación")
    temp_max: float = Field(..., description="Temperatura máxima de operación")
    alerta_activa: bool = False

    @model_validator(mode="after")
    def validar_coherencia_rangos(self) -> "RangoOperacionSensor":
        """
        Se ejecuta una vez que todos los campos individuales ya fueron parseados.
        'self' representa la instancia del modelo Pydantic.
        """
        if self.temp_max <= self.temp_min:
            raise ValueError(
                f"La temperatura máxima ({self.temp_max} °C) debe ser mayor que la mínima ({self.temp_min} °C)."
            )
            
        # Modificar estado en caliente basado en reglas cruzadas
        if self.temp_max > 120.0:
            self.alerta_activa = True

        return self
```

---

### 3. Manejo de Excepciones y Formato de Respuestas en FastAPI

Cuando un validador personalizado eleva un `ValueError` o `AssertionError`, Pydantic captura la excepción y FastAPI la convierte automáticamente en una respuesta con código **422 Unprocessable Entity**:

#### Ejemplo de Petición Inválida enviada a la API:
```json
{
  "sensor_id": "S-101",
  "temp_min": 100.0,
  "temp_max": 50.0
}
```

#### Respuesta JSON recibida en el cliente:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Value error, La temperatura máxima (50.0 °C) debe ser mayor que la mínima (100.0 °C).",
      "input": {
        "sensor_id": "S-101",
        "temp_min": 100.0,
        "temp_max": 50.0
      }
    }
  ]
}
```

---

### Resumen de la Lección
Usar `@field_validator` para campos individuales y `@model_validator` para reglas inter-campo traslada la responsabilidad de la validación a la capa de esquemas de Pydantic, manteniendo los controladores de FastAPI limpios y legibles.
