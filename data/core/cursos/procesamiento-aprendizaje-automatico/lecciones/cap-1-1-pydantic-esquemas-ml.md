# Guía de Laboratorio — Lección 1.1: Modelado de Features con Pydantic: Validación de Telemetría Eléctrica, Rangos y Tipado Estricto en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 1:** Arquitectura de Inferencia y Esquemas Pydantic  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Unidad 1 (Fundamentos de Git, Asistentes de IA y FastAPI en `energy-ml`).

---

## 1. El Principio de Calidad de Datos en Inferencia de Producción

En los sistemas de monitoreo y diagnóstico industrial como **`energy-ml`**, los modelos de Machine Learning toman decisiones críticas: detectar si un transformador de distribución de media tensión está en riesgo de falla catastrófica, o si una línea eléctrica presenta una sobrecarga térmica inminente.

En este nivel operativo rige una ley inexorable de la ingeniería de datos: **"Garbage In, Garbage Out" (Si ingresa basura, sale basura)**. Si un sensor transmite una lectura corrupta, con valores físicamente imposibles o con datos fuera de formato, el modelo no debe recibirla bajo ninguna circunstancia.

Para lograr una barrera de defensa impenetrable, **Pydantic** se utiliza como la capa de contrato y validación estricta de entrada, verificando no solo tipos primitivos, sino **leyes físicas y rangos operativos válidos**.

---

## 2. El Espacio de Características (*Features*) en `energy-ml`

Un transformador industrial de distribución eléctrica transmite periódicamente las siguientes variables analíticas:

```text
┌────────────────────────────────────────────────────────────────────────┐
│               TELEMETRÍA DE MONITOREO DE TRANSFORMADOR                 │
├──────────────────────────┬──────────────┬──────────────────────────────┤
│ Feature                  │ Unidad       │ Rango Físico Válido          │
├──────────────────────────┼──────────────┼──────────────────────────────┤
│ Voltaje de Fase (RMS)    │ Voltios (V)  │ 180.0 V a 260.0 V            │
│ Corriente de Línea (RMS) │ Amperios (A) │ 0.0 A a 150.0 A              │
│ Potencia Activa          │ Kilovatios   │ 0.0 kW a 60.0 kW             │
│ Temperatura de Aceite    │ Celsius (°C) │ -10.0 °C a 120.0 °C          │
│ Frecuencia de Red        │ Hertz (Hz)   │ 48.0 Hz a 52.0 Hz            │
│ Nivel de Vibración RMS   │ mm/s         │ 0.0 mm/s a 50.0 mm/s         │
└──────────────────────────┴──────────────┴──────────────────────────────┘
```

Si la frecuencia medida fuera de `35 Hz` o la temperatura de `-40 °C`, estaríamos ante una falla del sensor de telemetría y no ante una condición operativa real.

---

## 3. Implementación del Esquema con Pydantic y Validadores de Coherencia

En `src/schemas/diagnostico.py` dentro de `energy-ml`, definimos el modelo de entrada incorporando validación de campos con `Field` y validaciones cruzadas mediante `@model_validator`:

```python
"""Esquemas de validación estricta para diagnóstico de transformadores."""

from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class TelemetriaTransformadorRequest(BaseModel):
    """Contrato de entrada para inferencia de estado térmico y electromecánico."""
    transformador_id: str = Field(
        ...,
        min_length=4,
        max_length=30,
        description="Identificador único del activo industrial (ej: TRF-TALAR-01)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Estampa de tiempo UTC de la medición"
    )
    voltaje_v: float = Field(
        ...,
        ge=180.0,
        le=260.0,
        description="Voltaje eficaz de fase en Voltios"
    )
    corriente_a: float = Field(
        ...,
        ge=0.0,
        le=150.0,
        description="Corriente eficaz de línea en Amperios"
    )
    potencia_activa_kw: float = Field(
        ...,
        ge=0.0,
        le=60.0,
        description="Potencia activa entregada en kilovatios"
    )
    temperatura_aceite_c: float = Field(
        ...,
        ge=-10.0,
        le=120.0,
        description="Temperatura del dieléctrico en grados Celsius"
    )
    frecuencia_hz: float = Field(
        ...,
        ge=48.0,
        le=52.0,
        description="Frecuencia del sistema eléctrico en Hertz"
    )

    @model_validator(mode="after")
    def verificar_coherencia_electrica(self) -> "TelemetriaTransformadorRequest":
        """Valida que la potencia activa no supere la potencia aparente teórica (P <= V * I)."""
        potencia_aparente_kw = (self.voltaje_v * self.corriente_a) / 1000.0
        # Permitimos una pequeña tolerancia del 5% por transitorios de medición
        if self.potencia_activa_kw > (potencia_aparente_kw * 1.05) and self.corriente_a > 1.0:
            raise ValueError(
                f"Incoherencia física: Potencia activa ({self.potencia_activa_kw} kW) "
                f"supera la potencia aparente calculada ({potencia_aparente_kw:.2f} kVA)."
            )
        return self


class DiagnosticoTransformadorResponse(BaseModel):
    """Contrato de salida con resultado de la inferencia."""
    transformador_id: str
    estado_operativo: str = Field(..., description="Condición: normal, advertencia o falla_critica")
    probabilidad_sobrecalentamiento: float = Field(..., ge=0.0, le=1.0)
    accion_recomendada: str
    tiempo_inferencia_ms: float
```

---

## 4. Taller Práctico: Verificación en Consola de Python

Nos posicionamos en `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Abrimos una terminal interactiva de Python para probar la robustez del validador:

```python
from src.schemas.diagnostico import TelemetriaTransformadorRequest
from pydantic import ValidationError

# Caso 1: Lectura normal válida
datos_ok = {
    "transformador_id": "TRF-TALAR-01",
    "voltaje_v": 222.0,
    "corriente_a": 45.0,
    "potencia_activa_kw": 9.5,
    "temperatura_aceite_c": 65.4,
    "frecuencia_hz": 50.02
}
req = TelemetriaTransformadorRequest(**datos_ok)
print(f"Validación exitosa para {req.transformador_id}")

# Caso 2: Violación de rango físico (temperatura imposible)
try:
    TelemetriaTransformadorRequest(
        transformador_id="TRF-TALAR-01",
        voltaje_v=220.0,
        corriente_a=10.0,
        potencia_activa_kw=2.0,
        temperatura_aceite_c=180.0,  # Límite superior es 120.0
        frecuencia_hz=50.0
    )
except ValidationError as e:
    print("\nError detectado y bloqueado por Pydantic:")
    print(e.errors()[0]["msg"])
```

---

## 5. Integración con FastAPI y Respuesta Automática 422

Cuando conectamos este modelo a un endpoint en FastAPI:

```python
@router.post("/diagnostico/transformador", response_model=DiagnosticoTransformadorResponse)
def diagnosticar_transformador(lectura: TelemetriaTransformadorRequest):
    ...
```

Cualquier sensor averiado o atacante malicioso que envíe un dato fuera de los rangos establecidos recibirá un código **`422 Unprocessable Entity`** con un JSON detallado que indica el campo exacto que violó las restricciones, sin que tu modelo de Machine Learning gaste un solo ciclo de CPU intentando predecir sobre datos absurdos.

---

## 6. Conclusión

El modelado riguroso de características con **Pydantic** convierte a la API en el primer filtro de calidad del pipeline analítico.

En la siguiente lección, resolveremos el desafío de la gestión de memoria en el servidor web: cómo cargar nuestro modelo de Machine Learning una sola vez durante el inicio mediante el protocolo **`lifespan`** de FastAPI.
