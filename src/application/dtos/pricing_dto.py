"""DTOs de Pydantic para el motor de cálculo de pricing y presupuestos WBS."""

from pydantic import BaseModel, Field


class SubitemPresupuestoDTO(BaseModel):
    codigo: str
    nombre: str
    descripcion: str = ""
    tarifa_ars: float
    seleccionado: bool = True


class ItemDescuentoDTO(BaseModel):
    concepto: str
    porcentaje: float
    monto_ars: float


class TarifaConsultoriaDTO(BaseModel):
    categoria: str
    rango: str
    tarifa_base_ars: float = Field(gt=0)
    descripcion: str


class CalculoPaybackDTO(BaseModel):
    categoria_tarifa: str
    perdida_mensual_estimada_ars: float = Field(gt=0)
    inversion_total_ars: float = Field(gt=0)
    dias_payback: int = Field(ge=1)
    meses_payback: float = Field(ge=0.0)
    ahorro_anual_proyectado_ars: float
    resumen_ejecutivo_cfo: str


class LineasRemotasDTO(BaseModel):
    tele_peritaje_ars: float = Field(gt=0)
    capacitacion_in_company_ars: float = Field(gt=0)
    datamaq_insights_min_ars: float = Field(gt=0)
    datamaq_insights_max_ars: float = Field(gt=0)


class PresupuestoCalculadoDTO(BaseModel):
    zona_nombre: str
    cp_destino: str | None = None
    subitems: list[SubitemPresupuestoDTO] = Field(default_factory=lambda: list[SubitemPresupuestoDTO]())
    subtotal_mano_obra_ars: float
    viaticos_ars: float
    subtotal_bruto_ars: float
    descuentos_aplicados: list[ItemDescuentoDTO] = Field(default_factory=lambda: list[ItemDescuentoDTO]())
    total_descuentos_ars: float
    diagnostico_previo_bonificado_ars: float = 0.0
    total_neto_ars: float
    ahorro_total_ars: float
    resumen_whatsapp: str
    resumen_texto_formal: str
