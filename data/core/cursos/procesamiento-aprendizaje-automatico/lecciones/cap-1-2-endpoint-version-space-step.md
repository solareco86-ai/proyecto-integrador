# Lección 1.2: Endpoint POST /version-space/step para Refinamiento Interactivo en energy-ml

En la lección anterior analizamos formalmente la dinámica del algoritmo Candidate-Elimination. Ahora integraremos este motor de aprendizaje simbólico en la arquitectura de microservicios de ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md), implementando el endpoint `POST /api/v1/version-space/step` en FastAPI.

Este servicio permite a los ingenieros de despacho y a los agentes de software enviar eventos de telemetría de forma incremental y recibir en tiempo real el estado actualizado de las fronteras $S$ y $G$.

---

## 1. Contratos de Datos y Esquemas Pydantic v2

Comenzamos definiendo los esquemas de validación estricta en la capa de aplicación (`src/application/dtos/version_space_dto.py`). Cada atributo de telemetría debe respetar el dominio finito acordado:

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class TelemetriaEvento(BaseModel):
    """Atributos discretos de telemetría eléctrica en subestación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tension_red: Literal["baja", "nominal", "alta"] = Field(
        ..., description="Nivel de tensión medido en barras primarias"
    )
    carga_trafo: Literal["ligera", "nominal", "critica"] = Field(
        ..., description="Estado de carga del transformador de potencia"
    )
    temperatura_aceite: Literal["normal", "elevada", "extrema"] = Field(
        ..., description="Temperatura interna del refrigerante dieléctrico"
    )
    armonicos_thd: Literal["admisible", "alto"] = Field(
        ..., description="Tasa de distorsión armónica total (THD)"
    )


class MuestraEntrenamientoRequest(BaseModel):
    """Instancia etiquetada para actualizar el espacio de versiones."""

    model_config = ConfigDict(extra="forbid")

    telemetria: TelemetriaEvento
    disparo_termico: bool = Field(
        ...,
        description="Etiqueta real del evento: True si ocurrió disparo térmico",
    )


class HipotesisDTO(BaseModel):
    """Hipótesis conjuntiva expresada como diccionario de restricciones."""

    model_config = ConfigDict(frozen=True)

    tension_red: str
    carga_trafo: str
    temperatura_aceite: str
    armonicos_thd: str


class EstadoEspacioVersionesResponse(BaseModel):
    """Respuesta con el estado actual de las fronteras S y G."""

    frontera_especifica: list[HipotesisDTO] = Field(
        ..., description="Hipótesis más específicas (S)"
    )
    frontera_general: list[HipotesisDTO] = Field(
        ..., description="Hipótesis más generales (G)"
    )
    convergio: bool = Field(
        ..., description="True si S y G son idénticas y de tamaño 1"
    )
    colapso: bool = Field(
        ..., description="True si alguna de las fronteras quedó vacía por ruido"
    )
    total_muestras_procesadas: int
```

---

## 2. Lógica de Dominio: El Motor `VersionSpaceLearner`

En `src/domain/version_space.py`, encapsulamos la lógica pura sin dependencias de frameworks web, respetando los principios de Arquitectura Limpia:

```python
from dataclasses import dataclass, field
from typing import Mapping, Sequence

ATRIBUTOS = [
    "tension_red",
    "carga_trafo",
    "temperatura_aceite",
    "armonicos_thd",
]
DOMINIO_VALORES: dict[str, list[str]] = {
    "tension_red": ["baja", "nominal", "alta"],
    "carga_trafo": ["ligera", "nominal", "critica"],
    "temperatura_aceite": ["normal", "elevada", "extrema"],
    "armonicos_thd": ["admisible", "alto"],
}


def cubre_instancia(
    hipotesis: Mapping[str, str], instancia: Mapping[str, str]
) -> bool:
    """Verifica si una hipótesis cubre (satisface) una instancia de telemetría."""
    for attr in ATRIBUTOS:
        val_h = hipotesis[attr]
        if val_h == "0":
            return False
        if val_h != "?" and val_h != instancia[attr]:
            return False
    return True


def es_mas_general_o_igual(
    h1: Mapping[str, str], h2: Mapping[str, str]
) -> bool:
    """Determina si h1 es más general o igual que h2."""
    for attr in ATRIBUTOS:
        v1, v2 = h1[attr], h2[attr]
        if v1 != "?" and v1 != v2 and v2 != "0":
            return False
    return True


@dataclass
class VersionSpaceLearner:
    """Administrador en memoria de las fronteras S y G."""

    s: list[dict[str, str]] = field(
        default_factory=lambda: [{a: "0" for a in ATRIBUTOS}]
    )
    g: list[dict[str, str]] = field(
        default_factory=lambda: [{a: "?" for a in ATRIBUTOS}]
    )
    muestras_procesadas: int = 0

    def step(
        self, instancia: Mapping[str, str], es_positivo: bool
    ) -> "VersionSpaceLearner":
        self.muestras_procesadas += 1

        if es_positivo:
            # Eliminar de G las hipótesis inconsistentes con el positivo
            self.g = [h for h in self.g if cubre_instancia(h, instancia)]

            nuevos_s: list[dict[str, str]] = []
            for h_s in self.s:
                if cubre_instancia(h_s, instancia):
                    nuevos_s.append(h_s)
                else:
                    # Generalizar mínimamente
                    gen = dict(h_s)
                    for attr in ATRIBUTOS:
                        if gen[attr] == "0":
                            gen[attr] = instancia[attr]
                        elif gen[attr] != instancia[attr]:
                            gen[attr] = "?"
                    # Conservar solo si alguna hipótesis en G es más general
                    if any(
                        es_mas_general_o_igual(h_g, gen) for h_g in self.g
                    ):
                        nuevos_s.append(gen)
            self.s = nuevos_s

        else:  # Caso Ejemplo Negativo
            # Eliminar de S las hipótesis que cubren al negativo
            self.s = [h for h in self.s if not cubre_instancia(h, instancia)]

            nuevos_g: list[dict[str, str]] = []
            for h_g in self.g:
                if not cubre_instancia(h_g, instancia):
                    nuevos_g.append(h_g)
                else:
                    # Especializar mínimamente
                    for attr in ATRIBUTOS:
                        if h_g[attr] == "?":
                            for val in DOMINIO_VALORES[attr]:
                                if val != instancia[attr]:
                                    esp = dict(h_g)
                                    esp[attr] = val
                                    if any(
                                        es_mas_general_o_igual(esp, h_s)
                                        for h_s in self.s
                                    ):
                                        nuevos_g.append(esp)
            self.g = nuevos_g

        return self
```

---

## 3. Implementación de la Ruta en FastAPI

En `src/infrastructure/fastapi/routes/version_space.py`:

```python
from fastapi import APIRouter, HTTPException, status
from src.application.dtos.version_space_dto import (
    EstadoEspacioVersionesResponse,
    HipotesisDTO,
    MuestraEntrenamientoRequest,
)
from src.domain.version_space import VersionSpaceLearner

router = APIRouter(prefix="/api/v1/version-space", tags=["Espacio de Versiones"])

# Instancia singleton para demostración interactiva
learner_global = VersionSpaceLearner()


@router.post(
    "/step",
    response_model=EstadoEspacioVersionesResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar fronteras S y G con un nuevo evento de telemetría",
)
def registrar_paso_entrenamiento(
    request: MuestraEntrenamientoRequest,
) -> EstadoEspacioVersionesResponse:
    instancia_dict = request.telemetria.model_dump()
    learner_global.step(instancia_dict, request.disparo_termico)

    colapso = len(learner_global.s) == 0 or len(learner_global.g) == 0
    convergio = (
        not colapso
        and len(learner_global.s) == 1
        and len(learner_global.g) == 1
        and learner_global.s[0] == learner_global.g[0]
    )

    return EstadoEspacioVersionesResponse(
        frontera_especifica=[
            HipotesisDTO(**h) for h in learner_global.s
        ],
        frontera_general=[
            HipotesisDTO(**h) for h in learner_global.g
        ],
        convergio=convergio,
        colapso=colapso,
        total_muestras_procesadas=learner_global.muestras_procesadas,
    )
```

---

## 4. Validación Automatizada con Pytest

Para garantizar la estabilidad del servicio, creamos la suite de pruebas unitarias en `tests/test_version_space.py`:

```python
from fastapi.testclient import TestClient
from src.infrastructure.fastapi.main import app

client = TestClient(app)


def test_version_space_step_flujo_incremental():
    # 1. Enviar primer ejemplo positivo
    payload_pos = {
        "telemetria": {
            "tension_red": "alta",
            "carga_trafo": "critica",
            "temperatura_aceite": "elevada",
            "armonicos_thd": "alto",
        },
        "disparo_termico": True,
    }
    resp1 = client.post("/api/v1/version-space/step", json=payload_pos)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["colapso"] is False
    assert len(data1["frontera_especifica"]) == 1
    assert data1["frontera_especifica"][0]["tension_red"] == "alta"

    # 2. Enviar ejemplo negativo
    payload_neg = {
        "telemetria": {
            "tension_red": "nominal",
            "carga_trafo": "critica",
            "temperatura_aceite": "elevada",
            "armonicos_thd": "alto",
        },
        "disparo_termico": False,
    }
    resp2 = client.post("/api/v1/version-space/step", json=payload_neg)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["colapso"] is False
    # La frontera general debe haberse especializado excluyendo 'nominal'
    assert any(h["tension_red"] == "alta" for h in data2["frontera_general"])
```

Con este endpoint operativo, cualquier agente de software o panel de ingeniería puede enviar trazas de fallas y auditar cómo se delimita matemáticamente la causa raíz del evento crítico.
