# Lección 2.3: Exposición y Auditoría del Conjunto de Reglas en GET /rules en energy-ml

En las lecciones anteriores exploramos cómo inducir reglas lógicas transparentes mediante cobertura secuencial (AQ) y relaciones de primer orden (FOIL). En esta lección llevamos estas reglas al plano operativo construyendo un servicio de auditoría en FastAPI para ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md).

El endpoint `GET /api/v1/rules` expone la base de conocimiento inducida en formato JSON estructurado, permitiendo que ingenieros de despacho, auditores del ente regulador y agentes de IA autónomos inspeccionen el fundamento exacto detrás de las decisiones del sistema.

---

## 1. Esquemas Pydantic v2 para Reglas Simbólicas

En la capa de aplicación (`src/application/dtos/rules_dto.py`), modelamos cada selector lógico y regla formal:

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class CondicionSelector(BaseModel):
    """Selector atómico que conforma el antecedente de una regla."""

    model_config = ConfigDict(frozen=True)

    atributo: str = Field(..., example="temperatura_aceite")
    operador: Literal[">", "<", ">=", "<=", "==", "!="] = Field(
        ..., example=">"
    )
    valor_umbral: float | str = Field(..., example=85.0)
    unidad_medida: str | None = Field(None, example="°C")


class ReglaOperativaDTO(BaseModel):
    """Regla lógica inducida para monitoreo de contingencias eléctricas."""

    model_config = ConfigDict(frozen=True)

    id_regla: str = Field(..., example="R-IND-01")
    nombre: str = Field(..., example="Sobrecalentamiento en Transformador")
    antecedente: list[CondicionSelector] = Field(
        ..., description="Lista conjuntiva de condiciones"
    )
    consecuente: str = Field(
        ..., example="ESTADO_DISPARO_CRITICO", description="Acción o clase"
    )
    soporte_muestras: int = Field(
        ..., ge=1, description="Número de eventos históricos que la respaldan"
    )
    confianza_pct: float = Field(
        ..., ge=0.0, le=100.0, description="Precisión empírica de la regla"
    )
    nivel_criticidad: Literal["BAJA", "MEDIA", "CRITICA"] = Field(...)
    fecha_induccion: datetime


class CatalogoReglasResponse(BaseModel):
    """Respuesta consolidada para auditoría de reglas activas."""

    total_reglas: int
    reglas_criticas: int
    reglas: list[ReglaOperativaDTO]
```

---

## 2. Implementación del Router en FastAPI

En `src/infrastructure/fastapi/routes/rules.py`:

```python
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, HTTPException, Query, status
from src.application.dtos.rules_dto import (
    CatalogoReglasResponse,
    CondicionSelector,
    ReglaOperativaDTO,
)

router = APIRouter(prefix="/api/v1/rules", tags=["Auditoría de Reglas"])

# Repositorio en memoria de reglas inducidas por AQ/FOIL
REGLAS_MEMORIA: list[ReglaOperativaDTO] = [
    ReglaOperativaDTO(
        id_regla="R-IND-01",
        nombre="Falla Térmica Inminente por Sobrecarga Prolongada",
        antecedente=[
            CondicionSelector(
                atributo="temperatura_aceite",
                operador=">",
                valor_umbral=85.0,
                unidad_medida="°C",
            ),
            CondicionSelector(
                atributo="carga_potencia_pct",
                operador=">=",
                valor_umbral=110.0,
                unidad_medida="%",
            ),
        ],
        consecuente="ESTADO_DISPARO_CRITICO",
        soporte_muestras=412,
        confianza_pct=98.8,
        nivel_criticidad="CRITICA",
        fecha_induccion=datetime(2026, 10, 1, 10, 0, tzinfo=timezone.utc),
    ),
    ReglaOperativaDTO(
        id_regla="R-IND-02",
        nombre="Anomalía Dieléctrica por Descargas Parciales",
        antecedente=[
            CondicionSelector(
                atributo="gases_dga_ppm",
                operador=">",
                valor_umbral=150.0,
                unidad_medida="ppm",
            ),
            CondicionSelector(
                atributo="distorsion_thd_pct",
                operador=">",
                valor_umbral=5.0,
                unidad_medida="%",
            ),
        ],
        consecuente="ALERTA_MANTENIMIENTO_PREVENTIVO",
        soporte_muestras=180,
        confianza_pct=94.5,
        nivel_criticidad="MEDIA",
        fecha_induccion=datetime(2026, 10, 2, 14, 30, tzinfo=timezone.utc),
    ),
]


@router.get(
    "",
    response_model=CatalogoReglasResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar reglas lógicas aprendidas por inducción formal",
)
def listar_reglas(
    criticidad: Literal["BAJA", "MEDIA", "CRITICA"] | None = Query(
        None, description="Filtrar por severidad de la contingencia"
    ),
) -> CatalogoReglasResponse:
    filtradas = REGLAS_MEMORIA
    if criticidad:
        filtradas = [r for r in filtradas if r.nivel_criticidad == criticidad]

    criticas = sum(1 for r in filtradas if r.nivel_criticidad == "CRITICA")

    return CatalogoReglasResponse(
        total_reglas=len(filtradas),
        reglas_criticas=criticas,
        reglas=filtradas,
    )


@router.get(
    "/{id_regla}",
    response_model=ReglaOperativaDTO,
    summary="Consultar detalle de una regla lógica por su identificador",
)
def obtener_regla(id_regla: str) -> ReglaOperativaDTO:
    for regla in REGLAS_MEMORIA:
        if regla.id_regla == id_regla:
            return regla
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"La regla con identificador '{id_regla}' no existe en el catálogo",
    )
```

---

## 3. Pruebas Unitarias con Pytest y TestClient

En `tests/test_rules_endpoint.py`:

```python
from fastapi.testclient import TestClient
from src.infrastructure.fastapi.main import app

client = TestClient(app)


def test_get_rules_retorna_catalogo_valido():
    response = client.get("/api/v1/rules")
    assert response.status_code == 200
    data = response.json()
    assert "total_reglas" in data
    assert data["total_reglas"] >= 2
    assert "reglas" in data
    primera_regla = data["reglas"][0]
    assert "antecedente" in primera_regla
    assert len(primera_regla["antecedente"]) > 0


def test_get_rules_filtro_por_criticidad():
    response = client.get("/api/v1/rules?criticidad=CRITICA")
    assert response.status_code == 200
    data = response.json()
    for regla in data["reglas"]:
        assert regla["nivel_criticidad"] == "CRITICA"


def test_get_regla_no_encontrada():
    response = client.get("/api/v1/rules/R-INEXISTENTE-99")
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]
```

---

## 4. Consumo por Agentes de IA y Explicabilidad Operativa

Cuando un agente de IA en la sala de control (por ejemplo, **AGY CLI** ejecutando una tarea de diagnóstico de telemetría) detecta que una subestación se acerca a un umbral de peligro:
1. El agente ejecuta una llamada HTTP `GET /api/v1/rules?criticidad=CRITICA`.
2. Lee el antecedente: `temperatura_aceite > 85.0 AND carga_potencia_pct >= 110.0`.
3. Compara con la telemetría actual (`temperatura: 87.2 °C, carga: 112%`).
4. Genera una recomendación fundamentada:
   > *"Activando protocolo de alivio de carga en Tigre Centro: Se cumple la regla R-IND-01 (soporte: 412 casos históricos, confianza: 98.8%)."*

Esta capacidad de auditoría elimina el problema de las predicciones inexplicables y sienta las bases para arquitecturas agénticas confiables en infraestructura crítica.
