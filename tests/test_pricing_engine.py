"""Pruebas unitarias para el motor de pricing WBS, calculadora y switch booleano."""

import pytest

from src.application.pricing_service import PricingService


@pytest.fixture
def pricing_service() -> PricingService:
    return PricingService(data_dir="data")


def test_pricing_service_loads_config(pricing_service: PricingService):
    config = pricing_service.get_config()
    assert "wbs_subitems" in config
    assert "viaticos_zonas" in config
    assert "descuentos" in config or "descuentos" in config.get("config", {})
    assert pricing_service.is_public_pricing_enabled() is False


def test_resolver_viaticos_by_postal_code(pricing_service: PricingService):
    # Garín
    tarifa, zona = pricing_service.resolver_viaticos("1619")
    assert tarifa == 50000
    assert "Garín" in zona

    # Pilar
    tarifa, zona = pricing_service.resolver_viaticos("1629")
    assert tarifa == 50000
    assert "Pilar" in zona

    # Campana
    tarifa, zona = pricing_service.resolver_viaticos("2804")
    assert tarifa == 60000
    assert "Campana" in zona

    # CP desconocido (fallback base GBA Norte)
    tarifa, zona = pricing_service.resolver_viaticos("9999")
    assert tarifa == 50000
    assert "9999" in zona


def test_calcular_presupuesto_obra_punto_estandar(pricing_service: PricingService):
    # Punto estándar 2026 (b: $260.000 + e: $140.000 + viáticos Garín: $50.000 = $450.000)
    presupuesto = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        tiene_convenio_bapro=False,
        adhiere_vitrina_publica=False,
    )

    assert presupuesto.subtotal_mano_obra_ars == 400000
    assert presupuesto.viaticos_ars == 50000
    assert presupuesto.subtotal_bruto_ars == 450000
    assert presupuesto.total_descuentos_ars == 0
    assert presupuesto.total_neto_ars == 450000
    assert len(presupuesto.subitems) == 2


def test_calcular_presupuesto_obra_integral_con_acondicionamiento_y_termica(pricing_service: PricingService):
    # Obra compleja 2026: Instalación (b: 260k) + Térmica (c: 80k) + Acondicionamiento (d: 120k) + Cloud (e: 140k) + Viáticos (50k) = $650.000
    presupuesto = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "c", "d", "e"],
        cp="1629",
    )

    assert presupuesto.subtotal_mano_obra_ars == 600000
    assert presupuesto.viaticos_ars == 50000
    assert presupuesto.subtotal_bruto_ars == 650000
    assert presupuesto.total_neto_ars == 650000
    assert len(presupuesto.subitems) == 4


def test_descuentos_individuales_bapro_y_vitrina(pricing_service: PricingService):
    # Subtotal bruto $450.000
    # BAPRO 10% OFF = $45.000 desc -> Total $405.000
    p_bapro = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        tiene_convenio_bapro=True,
        adhiere_vitrina_publica=False,
    )
    assert p_bapro.total_descuentos_ars == 45000
    assert p_bapro.total_neto_ars == 405000

    # Vitrina 15% OFF = $67.500 desc -> Total $382.500
    p_vitrina = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        tiene_convenio_bapro=False,
        adhiere_vitrina_publica=True,
    )
    assert p_vitrina.total_descuentos_ars == 67500
    assert p_vitrina.total_neto_ars == 382500


def test_descuento_stacking_25_pct(pricing_service: PricingService):
    # Stacking total: 10% + 15% = 25% OFF sobre $450.000 = $112.500 desc -> Total $337.500
    p_stacking = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        tiene_convenio_bapro=True,
        adhiere_vitrina_publica=True,
    )
    assert p_stacking.total_descuentos_ars == 112500
    assert p_stacking.total_neto_ars == 337500
    assert p_stacking.ahorro_total_ars == 112500


def test_diagnostico_inicial_deducible(pricing_service: PricingService):
    # $450.000 con $55.000 deducibles de la visita de peritaje preliminar = $395.000
    p_diag = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        aplico_diagnostico_previo=True,
    )
    assert p_diag.diagnostico_previo_bonificado_ars == 55000
    assert p_diag.total_neto_ars == 395000
    assert p_diag.ahorro_total_ars == 55000


def test_resumen_whatsapp_formato(pricing_service: PricingService):
    presupuesto = pricing_service.calcular_presupuesto_obra(
        codigos_subitems=["b", "e"],
        cp="1619",
        tiene_convenio_bapro=True,
        adhiere_vitrina_publica=True,
        aplico_diagnostico_previo=True,
    )

    wa_text = presupuesto.resumen_whatsapp
    assert "DATAMAQ" in wa_text
    assert "Garín" in wa_text
    assert "TOTAL NETO ESTIMADO" in wa_text
    assert "Stacking Total" in wa_text
    assert "Peritaje Inicial Deducible" in wa_text
    assert "Pactar Digital" in wa_text


def test_switch_show_public_prices(pricing_service: PricingService):
    # Cuando show_public_prices es False (por defecto)
    assert pricing_service.get_plan_display_price("plataforma-cloud") == "$0"
    assert pricing_service.get_plan_display_price("instalacion-hardware") == "A cotizar"
    assert pricing_service.get_plan_display_price("consultoria-energia") == "A cotizar"
    assert pricing_service.get_plan_display_price("predios-submetering") == "A cotizar"


def test_obtener_tarifas_consultoria_escalonada(pricing_service: PricingService):
    tarifas = pricing_service.obtener_tarifas_consultoria()
    assert len(tarifas) >= 3
    cats = {t.categoria: t.tarifa_base_ars for t in tarifas}
    assert cats["T2"] == 350000
    assert cats["T3 BT"] == 650000
    assert cats["T3 MT"] == 850000


def test_obtener_lineas_remotas(pricing_service: PricingService):
    remotos = pricing_service.obtener_lineas_remotas()
    assert remotos.tele_peritaje_ars == 150000
    assert remotos.capacitacion_in_company_ars == 450000
    assert remotos.datamaq_insights_min_ars == 85000
    assert remotos.datamaq_insights_max_ars == 150000


def test_calcular_payback_t2_metalurgica(pricing_service: PricingService):
    # Caso 1: PyME Metalúrgica Tigre (T2)
    # Pérdida mensual: $395.400 / Inversión: $1.195.000 -> Payback ~91 días (~3 meses)
    payback = pricing_service.calcular_payback(
        categoria_tarifa="T2",
        perdida_mensual_ars=395400,
        inversion_total_ars=1195000,
    )
    assert payback.dias_payback in (90, 91)
    assert payback.meses_payback == 3.0
    assert payback.ahorro_anual_proyectado_ars == (395400 * 12) - 1195000
    assert "T2" in payback.resumen_ejecutivo_cfo
    assert "Pactar Digital" in payback.resumen_ejecutivo_cfo


def test_calcular_payback_t3_inyectora_plastico(pricing_service: PricingService):
    # Caso 2: Inyectora de Plásticos Pilar (T3 BT)
    # Pérdida mensual: $3.931.900 / Inversión: $4.245.000 -> Payback 32 días (~1.1 meses)
    payback = pricing_service.calcular_payback(
        categoria_tarifa="T3 BT",
        perdida_mensual_ars=3931900,
        inversion_total_ars=4245000,
    )
    assert payback.dias_payback == 32
    assert payback.meses_payback == 1.1
    assert payback.ahorro_anual_proyectado_ars == (3931900 * 12) - 4245000
    assert "T3 BT" in payback.resumen_ejecutivo_cfo


def test_calcular_payback_validaciones(pricing_service: PricingService):
    with pytest.raises(ValueError, match="mayor a 0"):
        pricing_service.calcular_payback("T2", 0, 100000)
    with pytest.raises(ValueError, match="mayor a 0"):
        pricing_service.calcular_payback("T2", 100000, -500)
